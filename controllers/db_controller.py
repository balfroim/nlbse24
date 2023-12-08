import contextlib
from typing import Set, Type
from controllers.command_runner import CommandRunner
from models.bug import Bug
from models.project import Project
import os
from decorators.ensure_in_path import ensure_in_path
from constants.paths import CODEQL_HOME
from constants.code import FIXED_BUILD_CHART
from models.query import ExtractMethodsQuery

class DBController:
    @classmethod
    def _install_codeql(cls, project: Project):
        CommandRunner.run("cp", "-r", "codeql", project.CODEQL_PATH)

    @classmethod
    def rmv_passing_tests(cls, kept_files_names: Set[str], dir_path: str):
        # Reduce database creation time by removing passing tests
        for root, _, files in os.walk(dir_path):
            for file in files:
                if not file.endswith(".java") or file not in kept_files_names:
                    os.remove(os.path.join(root, file))
    
    @classmethod
    @ensure_in_path(CODEQL_HOME)
    def create_db(cls, bug: Bug):
        cls._install_codeql(bug.project)
        DBController.rmv_passing_tests(bug.failing_tests, bug.project.tests_path)
        with CommandRunner.chdir(bug.project.PATH), contextlib.suppress(FileNotFoundError):
            if bug.project.name == "Lang":
                # This file is not compilable so we remove it
                os.remove("./src/test/java/org/apache/commons/lang3/reflect/TypeUtilsTest.java")
            if bug.project.name == "Chart":
                with open('./ant/build.xml', 'w') as file:
                    file.write(FIXED_BUILD_CHART)
        return CommandRunner.run(
            "codeql",
            "database",
            "create",
            bug.project.DB_PATH,
            "--language=java",
            "--overwrite",
            "--source-root",
            bug.project.PATH,
        )

    @classmethod
    @ensure_in_path(CODEQL_HOME)
    def analyse(cls, query: Type[ExtractMethodsQuery]):
        os.makedirs(query.project.RESULTS_PATH, exist_ok=True)
        CommandRunner.run(
            "codeql",
            "database",
            "analyze",
            query.project.DB_PATH,
            query.PATH,
            "--format=csv",
            "--output",
            query.OUTPUT_PATH,
            "--search-path",
            query.project.CODEQL_PATH,
        )