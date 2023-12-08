from dataclasses import dataclass


@dataclass
class FailingTest:
    className: str
    methodName: str
    error: str
    message: str

    @property
    def filename(self):
        name = self.className.split(".")[-1]
        return f"{name}.java"
    
    @property
    def full_name(self):
        class_name = self.className.split(".")[-1]
        return f"{class_name}::{self.methodName}"
    
    def to_dict(self):
        return {
            "className": self.className,
            "methodName": self.methodName,
            "error": self.error,
            "message": self.message,
        }
    
    @classmethod
    def from_json(cls, json):
        return cls(**json)
