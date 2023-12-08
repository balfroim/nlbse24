import os
from dataclasses import dataclass
import controllers.d4j_controller as d4j


@dataclass
class Project:
    name: str
    version: int
    is_buggy: bool = True
    
    @property
    def PATH(self):
        return f"./projects/{self.name}/{self.version}"
    
    @property
    def DB_PATH(self):
        return os.path.join(self.PATH, "codeql-db")
    
    @property
    def CODEQL_PATH(self):
        return os.path.join(self.PATH, "codeql")
    
    @property
    def RESULTS_PATH(self):
        return os.path.join(self.PATH, "results")
    
    @property
    def STACKTRACE_PATH(self):
        return f"./stacktraces/{self.name}-{self.version}.json"
    
    def results_path(self, file_name: str):
        return os.path.join(self.RESULTS_PATH, file_name)
    
    def rel_results_path(self, file_name: str):
        return os.path.join("results", file_name)
    

    @property
    def TOURS_PATH(self):
        return f"./tours/{self.name}/{self.version}"
    
    def tour_path(self, test_name: str, method_name: str):
        return f"{self.TOURS_PATH}/codetour-{test_name}-{method_name}.tour"
    
    @property
    def REF(self):
        return f"D4J_{self.name}_{self.version}_BUGGY_VERSION"
    
    @classmethod
    def from_json(cls, json):
        return cls(**json)

    @property
    def src_path(self):
        if not hasattr(self, "_src_path"):
            self._src_path = d4j.D4JController.export(self, "dir.src.classes")
        return self._src_path
    
    @property
    def tests_path(self):
        if not hasattr(self, "_tests_path"):
            self._tests_path = d4j.D4JController.export(self, "dir.src.tests")
        return self._tests_path