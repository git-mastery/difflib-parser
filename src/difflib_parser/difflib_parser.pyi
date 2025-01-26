from dataclasses import dataclass
from difflib_parser.diff_line import DiffLine as DiffLine, DiffLineCode as DiffLineCode
from enum import Enum
from typing import Iterator

class DiffCode(Enum):
    SAME = 0
    RIGHT_ONLY = 1
    LEFT_ONLY = 2
    CHANGED = 3

@dataclass
class DiffChange:
    left: list[int]
    right: list[int]
    newline: str
    skip_lines: int
    def __init__(self, left, right, newline, skip_lines) -> None: ...

@dataclass
class Diff:
    code: DiffCode
    line: str
    left_changes: list[int] | None = ...
    right_changes: list[int] | None = ...
    newline: str | None = ...
    def __init__(self, code, line, left_changes=..., right_changes=..., newline=...) -> None: ...

class DiffParser:
    def __init__(self, left_text: list[str], right_text: list[str]) -> None: ...
    def iter_diffs(self) -> Iterator[Diff]: ...
