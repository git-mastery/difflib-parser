from typing import List, Generator, Any
import difflib
from enum import Enum
from dataclasses import dataclass


class DiffCode(Enum):
    SAME = 0
    RIGHT_ONLY = 1
    LEFT_ONLY = 2
    CHANGED = 3


class DiffLineCode(Enum):
    ADDED = 0
    REMOVED = 1
    COMMON = 2
    MISSING = 3


class DiffLine:
    def __init__(self, line: str | None):
        self.__line = line

    @staticmethod
    def parse(line: str) -> "DiffLine":
        return DiffLine(line)

    @property
    def code(self) -> DiffLineCode | None:
        if self.__line is None:
            return None

        match self.__line[:2]:
            case "+ ":
                return DiffLineCode.ADDED
            case "- ":
                return DiffLineCode.REMOVED
            case "  ":
                return DiffLineCode.COMMON
            case "? ":
                return DiffLineCode.MISSING

    @property
    def line(self) -> str | None:
        if self.__line is None:
            return None

        return self.__line[2:]


@dataclass
class DiffChange:
    left: List[int]
    right: List[int]
    newline: str
    skip_lines: int


@dataclass
class Diff:
    code: DiffCode
    line: str
    left_changes: List[int] | None = None
    right_changes: List[int] | None = None
    newline: str | None = None


# Parser inspired by https://github.com/yebrahim/difflibparser/blob/master/difflibparser.py
class DiffParser:
    def __init__(self, left_text, right_text):
        self.__left_text = left_text
        self.__right_text = right_text
        self.__diff = list(difflib.ndiff(self.__left_text, self.__right_text))
        self.__line_no = 0

    def iter_diffs(self) -> Generator[Diff, Any, Any]:
        while self.__line_no < len(self.__diff):
            current_line = self.__diff[self.__line_no]
            diff_line = DiffLine.parse(current_line)
            code = diff_line.code
            diff = Diff(code=DiffCode.SAME, line=diff_line.line)
            if code == DiffLineCode.ADDED:
                diff.code = DiffCode.RIGHT_ONLY
            elif code == DiffLineCode.REMOVED:
                change = self.__get_incremental_change(self.__line_no)
                if change is None:
                    diff.code = DiffCode.LEFT_ONLY
                else:
                    diff.code = DiffCode.CHANGED
                    diff.left_changes = change.left
                    diff.right_changes = change.right
                    diff.newline = change.newline
                    self.__line_no = change.skip_lines
            self.__line_no += 1
            yield diff

    def __get_incremental_change(self, line_no: int) -> DiffChange | None:
        lines = [
            DiffLine.parse(
                self.__diff[line_no + i] if line_no + i < len(self.__diff) else None
            )
            for i in range(4)
        ]

        pattern_a = [
            DiffLineCode.REMOVED,
            DiffLineCode.MISSING,
            DiffLineCode.ADDED,
            DiffLineCode.MISSING,
        ]
        if self.__match_pattern(lines, pattern_a):
            return DiffChange(
                left=[i for (i, c) in enumerate(lines[1].line) if c in ["-", "^"]],
                right=[i for (i, c) in enumerate(lines[3].line) if c in ["+", "^"]],
                newline=lines[2].line,
                skip_lines=3,
            )

        pattern_b = [DiffLineCode.REMOVED, DiffLineCode.ADDED, DiffLineCode.MISSING]
        if self.__match_pattern(lines, pattern_b):
            return DiffChange(
                left=[],
                right=[i for (i, c) in enumerate(lines[2].line) if c in ["+", "^"]],
                newline=lines[1].line,
                skip_lines=2,
            )

        pattern_c = [DiffLineCode.REMOVED, DiffLineCode.MISSING, DiffLineCode.ADDED]
        if self.__match_pattern(lines, pattern_c):
            return DiffChange(
                left=[i for (i, c) in enumerate(lines[1].line) for c in ["-", "^"]],
                right=[],
                newline=lines[1].line,
                skip_lines=2,
            )

        return None

    def __match_pattern(
        self, diff_lines: List[DiffLine], codes: List[DiffLineCode]
    ) -> bool:
        return all([line.code == code for line, code in zip(diff_lines, codes)])
