
import logging
import os
import shutil
from constants.paths import DEFECTS4J_HOME
from controllers.command_runner import CommandRunner
from decorators.ensure_in_path import ensure_in_path
from models.failing_test import FailingTest
import models.project as pj


class D4JController:
    @classmethod
    @ensure_in_path(DEFECTS4J_HOME)
    def checkout(cls, project: 'pj.Project', force: bool = True):
        if not force and os.path.exists(project.PATH):
            logging.info(f"Skipping checkout of {project.name} {project.version}")
            return
        if os.path.exists(project.PATH):
            logging.info(f"Deleting {project.PATH}")
            shutil.rmtree(project.PATH)
        CommandRunner.run(
            "defects4j", "checkout",
            "-p", project.name,
            "-v", f"{project.version}b" if project.is_buggy else f"{project.version}f",
            "-w", project.PATH
        )
    
    @classmethod
    @ensure_in_path(DEFECTS4J_HOME)
    def run_tests(cls, project: 'pj.Project'):
        return CommandRunner.run("defects4j", "test", "-w", project.PATH)
    
    @classmethod
    @ensure_in_path(DEFECTS4J_HOME)
    def run_test(cls, project: 'pj.Project', test: FailingTest):
        return CommandRunner.run("defects4j", "test", "-w", project.PATH, "-t", test.full_name)
    
    @classmethod
    @ensure_in_path(DEFECTS4J_HOME)
    def export(cls, project: 'pj.Project', property: str):
        with CommandRunner.chdir(project.PATH):
            return CommandRunner.run("defects4j", "export", "-p", property)