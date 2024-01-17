import json
import os
from typing import List
from models.query import ExtractMethodsQuery, ExtractMethodsOrderedQuery
import pandas as pd
from models.method import Method, OrderedMethod
from models.changed_line import ChangedLine

from constants.paths import DATASET_PATH, QUERIES_MIDDLE_PATH
from constants.code import EXTRACT_METHODS_QLL
from models.bug import Bug
import logging
import contextlib
import shutil
from controllers.d4j_controller import D4JController
from controllers.db_controller import DBController
from controllers.command_runner import CommandRunner

import contextlib
from models.method import Method
from models.failing_test import FailingTest
from constants.code import STACK_TRACE_RECORDER_CODE, STACK_TRACE_RECORDER_LINE
from constants.values import DELETE, VERBOSE_SKIP
from controllers.command_runner import CommandRunner
from install_codeql import install_codeql
from decorators.ensure_in_path import ensure_in_path

bugs = Bug.from_json_file(DATASET_PATH)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
                        logging.StreamHandler(),
                              logging.FileHandler('stacktraces.log')
                              ]
                              )

class CodeInjectionContext:
    def __init__(self, method: Method, test: FailingTest):
        self.method = method
        self.test = test
        self.original_file = CommandRunner.read_from_file(f"{self.method.project.PATH}/{self.method.file_path}").split("\n")

    @property
    def result_path(self):
        return f"results/stacktrace-{self.test.methodName}-{self.method.method_name}.csv"

    def __enter__(self):
        logging.info(f"Injecting code in {self.method.full_name}")
        injected_file = self.original_file.copy()
        self._inject_lines(injected_file)
        CommandRunner.write_to_file(f"{self.method.project.PATH}/{self.method.file_path}", "\n".join(injected_file))
        st_code = STACK_TRACE_RECORDER_CODE.format(package=self.method.package)
        CommandRunner.write_to_file(f"{self.method.project.PATH}/{self.method.package_path}/StackTraceRecorder.java", st_code)
        return self

    def _inject_lines(self, injected_file):
        insert_line = self.method.method_start_line
        if "super()" in injected_file[self.method.method_start_line]:
            insert_line += 1
        stacktrace_recorder_line = STACK_TRACE_RECORDER_LINE.format(test_name=self.test.methodName, method_name=self.method.method_name, stacktrace_csv=self.result_path)
        injected_file.insert(insert_line, stacktrace_recorder_line)

    def __exit__(self, exc_type, exc_value, traceback):
        logging.info(f"Reverting back to original {self.method.full_name}")
        CommandRunner.write_to_file(f"{self.method.project.PATH}/{self.method.file_path}", "\n".join(self.original_file))


def extract_patched_methods(bug):
    query = ExtractMethodsQuery("patched-methods", bug.project, bug.changed_lines)
    CommandRunner.write_to_file(query.PATH, str(query))
    DBController.analyse(query)
    df = pd.read_csv(query.OUTPUT_PATH, sep=",", header=None)
    return Method.from_df(df, query.project)


def extract_changed_lines(src_path, data) -> List[ChangedLine]:
    changed_lines = []
    for _, row in data.iterrows():
        package_path = row["package"].replace(".", "/")          
        file_path = f"/{src_path}/{package_path}/{row['class']}.java"
        changed_line = ChangedLine(file_path, row["line number"])
        changed_lines.append(changed_line)
    return changed_lines

def delete_project(path):
    if DELETE:
        with contextlib.suppress(Exception):
            shutil.rmtree(path)
        logging.info(f"Deleted {bug.project.name} {bug.project.version}")

def fail(bug, error, reason):
    logging.info(f"Skipping {bug.project.name} {bug.project.version} because it {reason}")
    logging.error(error)
    delete_project(bug.project.PATH)
    CommandRunner.write_to_file(bug.project.STACKTRACE_PATH, json.dumps({
                    "tours": [],
                    "project": {
                        "name": bug.project.name,
                        "version": bug.project.version
                    },
                    "generation_failure": {
                        "error": reason,
                        "error_message": str(error)
                    }
                }))
    
def fail_tour(error, reason):
    logging.error(error)
    return {
            "error": reason,
            "error_message": str(error)
        }

if not os.path.exists("./codeql"):
    logging.info("CodeQL not found. Installing CodeQL...")
    install_codeql()

os.makedirs(os.path.join(*QUERIES_MIDDLE_PATH), exist_ok=True)
os.makedirs("./stacktraces", exist_ok=True)

for bug in bugs:
    if os.path.exists(bug.project.STACKTRACE_PATH) or bug.project.name == "Mockito":
        if VERBOSE_SKIP:
            logging.info(f"Skipping {bug.project.name} {bug.project.version}")
        continue

    logging.info(f"Initializing {bug.project.name} {bug.project.version}")
    try:
        D4JController.checkout(bug.project)
        DBController.create_db(bug)
    except TypeError as e:
        fail(bug, e, ".env might not be set")
        continue
    except Exception as e:
        fail(bug, e, "failed to initialize")
        continue

    logging.info(f"Extracting start and end points for {bug.project.name} {bug.project.version}")
    failing_tests = bug.failing_tests
    try:
        patched_methods = extract_patched_methods(bug)
    except Exception as e:
        fail(bug, e, "failed to extract patched methods")
        continue


    tours = []
    for test in failing_tests:
        for method in patched_methods:
            tour = {
                "failing_test": test.to_dict(),
                "patched_method": method.to_dict(),
            }
            try:
                with CodeInjectionContext(method, test) as context:
                    D4JController.run_tests(bug.project)
                    result_path = context.result_path
                    data = pd.read_csv(f"{bug.project.PATH}/{result_path}", sep=",")
                changed_lines = extract_changed_lines(bug.project.src_path, data)
                query = ExtractMethodsOrderedQuery(f"stacktrace-methods-{test.methodName}-{method.method_name}", bug.project, changed_lines)
                CommandRunner.write_to_file(query.PATH, str(query))
                DBController.analyse(query)
                df = pd.read_csv(query.OUTPUT_PATH, sep=",", header=None)
                st_methods = OrderedMethod.from_df(df, query.project)
                steps = []
                for m in st_methods:
                    step = m.to_dict()
                    step["line"] = m.end_line
                tour["steps"] = [m.to_dict() for m in st_methods]
            except Exception as e:
                logging.info(f"Skipping {test.methodName} to {method.method_name} in {bug.project.name} {bug.project.version} because it failed to generate stacktrace")
                logging.error(e)
                tour["steps"] = []
                tour["generation_failure"] = {
                    "error": "Failed to generate stacktrace",
                    "error_message": str(e)
                }
            tours.append(tour)
    json_data = json.dumps({
        "tours": tours,
        "project": {
            "name": bug.project.name,
            "version": bug.project.version
        }
    })
    CommandRunner.write_to_file(bug.project.STACKTRACE_PATH, json_data)

    delete_project(bug.project.PATH)
