from dataclasses import dataclass
import os
from typing import List
from models.changed_line import ChangedLine
from constants.queries import EXTRACT_METHODS_QUERY, EXTRACT_METHODS_ORDERED_QUERY
from constants.paths import QUERIES_MIDDLE_PATH
from models.project import Project


@dataclass
class ExtractMethodExpression:
    filename: str
    line: int

    def __str__(self):
        return f'getMethodOrConstructor(moc, "{self.filename}", {self.line})'
    
@dataclass
class ExtractMethodOrderedExpression(ExtractMethodExpression):
    call_order: int

    def __str__(self) -> str:
        parent_expression  = super().__str__()
        return f"({parent_expression} and call_order = {self.call_order})"

@dataclass
class ExtractMethodsQuery:
    name: str
    project: Project
    changed_files: List[ChangedLine]

    @property
    def PATH(self):
        return os.path.join(self.project.PATH, *QUERIES_MIDDLE_PATH, f"{self.name}.ql")
    
    @property
    def OUTPUT_PATH(self):
        return os.path.join(self.project.RESULTS_PATH, f"{self.name}.csv")

    def __str__(self) -> str:
        joined_expressions = " or\n\t".join(
            str(ExtractMethodExpression(file.filename, file.line)) for file in self.changed_files
        )
        return EXTRACT_METHODS_QUERY.format(
            joined_expressions=joined_expressions
        )

@dataclass
class ExtractMethodsOrderedQuery(ExtractMethodsQuery):


    def __str__(self) -> str:
        joined_expressions = " or\n\t".join(
            str(ExtractMethodOrderedExpression(file.filename, file.line, call_order)) for call_order, file in enumerate(self.changed_files)
        )
        return EXTRACT_METHODS_ORDERED_QUERY.format(
            joined_expressions=joined_expressions
        )
    