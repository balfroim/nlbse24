

from itertools import chain
from typing import Dict, List
import json

from models.changed_line import ChangedLine
from models.failing_test import FailingTest
from models.project import Project

from dataclasses import dataclass


@dataclass
class Bug:
    project: Project
    changed_lines: List[ChangedLine]
    failing_tests: List[FailingTest]

    @classmethod
    def from_json(cls, json_instance: Dict):
        project = Project(json_instance["project"], json_instance["bugId"])
        changed_lines = cls._get_changed_lines(json_instance["changedFiles"])
        failing_tests = [FailingTest(**test) for test in json_instance["failingTests"]]
        return cls(project=project, changed_lines=changed_lines, failing_tests=failing_tests)

    @classmethod
    def _get_changed_lines(cls, changed_files: Dict) -> List[ChangedLine]:
        changed_lines = []
        for path, actions in changed_files.items():
            for _, lines in actions.items():
                changed_lines.extend(ChangedLine(path=path, line=line) for line in chain.from_iterable(lines))
        return changed_lines

    @classmethod
    def from_json_file(cls, file_path: str) -> List['Bug']:
        with open(file_path, "r") as f:
            json_list = json.load(f)
        return [cls.from_json(json_instance) for json_instance in json_list]