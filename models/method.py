import contextlib
from dataclasses import dataclass
from functools import lru_cache
import json
from typing import List, Optional
from controllers.command_runner import CommandRunner
from models.project import Project
import os
import pandas as pd
from controllers.d4j_controller import D4JController

@dataclass
class Method:
    project: Project
    file_path: str
    method_name: str
    javadoc_start_line: int
    annotations_start_line: int
    method_start_line: int
    end_line: int

    @property
    def filename(self):
        return os.path.basename(self.file_path)

    @property
    def package_path(self):
        return os.path.dirname(self.file_path)
    
    @property
    def full_name(self):
        return f"{self.package}::{self.method_name}"

    @property
    def package(self):
        components = [p for p in self.package_path.split("/") if p not in self.project.src_path]
        return ".".join(components)

    @property
    def content_lines(self):
        if not hasattr(self, "file_lines"):
            self.file_lines = CommandRunner.read_from_file(f"{self.project.PATH}/{self.file_path}").split("\n")
        return self.file_lines[self.javadoc_start_line-1:self.end_line]
    
    @property
    def content(self):
        return "\n".join(self.content_lines)

    @classmethod
    def _from_duplicates(cls, project: Project, path: str, duplicates: list[dict]) -> 'Method':
        method = Method(project, path, **json.loads(duplicates[0]))
        for duplicate in duplicates[1:]:
            djson = json.loads(duplicate)
            method.javadoc_start_line = min(method.javadoc_start_line, djson['javadoc_start_line'])
            method.annotations_start_line = min(method.annotations_start_line, djson['annotations_start_line'])
            method.method_start_line = min(method.method_start_line, djson['method_start_line'])
            method.end_line = max(method.end_line, djson['end_line'])
        return method
    
    @classmethod
    def from_df(cls, df: pd.DataFrame, project: Project) -> List['Method']:
        methods = []
        for method_details_lines, path in zip(df[3], df[4]):
            duplicates = method_details_lines.split("\n")
            methods.append(Method._from_duplicates(project, path, duplicates))
        return methods
    
    def to_dict(self):
        return {
            "file_path": self.file_path,
            "method_name": self.method_name,
            "content": self.content,
            "javadoc_start_line": self.javadoc_start_line,
            "annotations_start_line": self.annotations_start_line,
            "method_start_line": self.method_start_line,
            "end_line": self.end_line,
        }
    
    @classmethod
    def from_json(cls, project, json):
        with contextlib.suppress(KeyError):
            json.pop("content")
        return cls(project, **json)

    
@dataclass
class OrderedMethod(Method):
    call_order: int

    @classmethod
    def from_df(cls, df: pd.DataFrame, project: Project) -> List['OrderedMethod']:
        methods = []
        for method_details_lines, path in zip(df[3], df[4]):
            method_details_lines_splitted = method_details_lines.split("\n")
            for method_details_line in method_details_lines_splitted:
                call_order, method = method_details_line.split("|")
                methods.append(OrderedMethod(project, path, **json.loads(method), call_order=int(call_order)))
        return list(sorted(methods, key=lambda m: m.call_order))
    
    
    