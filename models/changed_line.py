from dataclasses import dataclass


@dataclass
class ChangedLine:
    path: str
    line: int

    @property
    def filename(self):
        return self.path.split("/")[-1]
