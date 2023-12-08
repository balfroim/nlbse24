from dataclasses import dataclass
import json
import os
from typing import List
from models.failing_test import FailingTest
from models.method import Method

from models.project import Project


@dataclass
class CodeTourStep:
    file: str
    description: str
    line: int

    def to_json(self):
        return {
            "file": self.file,
            "description": self.description,
            "line": self.line
        }


@dataclass
class CodeTour:
    steps: List[CodeTourStep]
    project: Project
    test: FailingTest
    method: Method

    @property
    def title(self):
        return f"Stacktrace of between {self.test.methodName} and {self.method.method_name}"

    def to_json(self):
        return {
            "$schema": "https://aka.ms/codetour-schema",
            "title": self.title,
            "steps": [step.to_json() for step in self.steps],
            "ref": self.project.REF
        }

    def dump(self):
        os.makedirs(f"{self.project.PATH}/.tour", exist_ok=True)
        with open(f"{self.project.PATH}/.tour/codetour-{self.title}.tour", "w") as f:
            json.dump(self.to_json(), f, indent=2)