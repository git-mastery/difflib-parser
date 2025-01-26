from enum import Enum

class DiffLineCode(Enum):
    ADDED = 0
    REMOVED = 1
    COMMON = 2
    MISSING = 3

class DiffLine:
    def __init__(self, line: str | None) -> None: ...
    @staticmethod
    def parse(line: str | None) -> DiffLine: ...
    @property
    def code(self) -> DiffLineCode | None: ...
    @property
    def line(self) -> str | None: ...
