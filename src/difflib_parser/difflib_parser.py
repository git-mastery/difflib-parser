from typing import List, Generator, Any
import difflib
from enum import Enum
from dataclasses import dataclass

from difflib_parser.diff_line import DiffLine, DiffLineCode


class DiffCode(Enum):
    SAME = 0
    RIGHT_ONLY = 1
    LEFT_ONLY = 2
    CHANGED = 3


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
    def __init__(self, left_text: List[str], right_text: List[str]):
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

        [_, b, c, d] = lines

        # This represents the case where both additions and removals are present in the edit
        pattern_a = [
            DiffLineCode.REMOVED,
            DiffLineCode.MISSING,
            DiffLineCode.ADDED,
            DiffLineCode.MISSING,
        ]
        if self.__match_pattern(lines, pattern_a):
            return DiffChange(
                left=[i for (i, c) in enumerate(b.line) if c in ["-", "^"]],
                right=[i for (i, c) in enumerate(d.line) if c in ["+", "^"]],
                newline=c.line,
                skip_lines=3,
            )

        # This represents the case where only additions are present in the edit
        pattern_b = [DiffLineCode.REMOVED, DiffLineCode.ADDED, DiffLineCode.MISSING]
        if self.__match_pattern(lines, pattern_b):
            return DiffChange(
                left=[],
                right=[i for (i, c) in enumerate(c.line) if c in ["+", "^"]],
                newline=b.line,
                skip_lines=2,
            )

        # This represents the case where only removals are present in the edit
        pattern_c = [DiffLineCode.REMOVED, DiffLineCode.MISSING, DiffLineCode.ADDED]
        if self.__match_pattern(lines, pattern_c):
            return DiffChange(
                left=[i for (i, c) in enumerate(b.line) if c in ["-", "^"]],
                right=[],
                newline=c.line,
                skip_lines=2,
            )

        return None

    def __match_pattern(
        self, diff_lines: List[DiffLine], codes: List[DiffLineCode]
    ) -> bool:
        return all([line.code == code for line, code in zip(diff_lines, codes)])
