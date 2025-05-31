import difflib
from typing import Iterator, List

from difflib_parser.diff import Diff
from difflib_parser.diff_change import DiffChange
from difflib_parser.diff_code import DiffCode
from difflib_parser.diff_line import DiffLine
from difflib_parser.diff_line_code import DiffLineCode


# Parser inspired by https://github.com/yebrahim/difflibparser/blob/master/difflibparser.py
class DifflibParser:
    def __init__(self, left_text: List[str], right_text: List[str]):
        self.__left_text = left_text
        self.__right_text = right_text
        self.__diff = list(difflib.ndiff(self.__left_text, self.__right_text))

    def iter_diffs(self) -> Iterator[Diff]:
        line_no = 0
        while line_no < len(self.__diff):
            current_line = self.__diff[line_no]
            diff_line = DiffLine.parse(current_line)
            if diff_line.line is None:
                line_no += 1
                continue
            code = diff_line.code
            diff = Diff(code=DiffCode.SAME, line=diff_line.line)

            if code == DiffLineCode.ADDED:
                diff.code = DiffCode.RIGHT_ONLY
            elif code == DiffLineCode.REMOVED:
                change = self.__get_incremental_change(line_no)
                if change is None:
                    diff.code = DiffCode.LEFT_ONLY
                else:
                    diff.code = DiffCode.CHANGED
                    diff.left_changes = change.left
                    diff.right_changes = change.right
                    diff.newline = change.newline
                    line_no += change.skip_lines

            line_no += 1
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
        # We can ignore all of these lines because we know that a None line would have
        # been skipped
        if self.__match_pattern(lines, pattern_a):
            return DiffChange(
                left=[i for (i, c) in enumerate(b.line) if c in ["-", "^"]],  # type: ignore
                right=[i for (i, c) in enumerate(d.line) if c in ["+", "^"]],  # type: ignore
                newline=c.line,  # type: ignore
                skip_lines=3,
            )

        # This represents the case where only additions are present in the edit
        pattern_b = [DiffLineCode.REMOVED, DiffLineCode.ADDED, DiffLineCode.MISSING]
        if self.__match_pattern(lines, pattern_b):
            return DiffChange(
                left=[],
                right=[i for (i, c) in enumerate(c.line) if c in ["+", "^"]],  # type: ignore
                newline=b.line,  # type: ignore
                skip_lines=2,
            )

        # This represents the case where only removals are present in the edit
        pattern_c = [DiffLineCode.REMOVED, DiffLineCode.MISSING, DiffLineCode.ADDED]
        if self.__match_pattern(lines, pattern_c):
            return DiffChange(
                left=[i for (i, c) in enumerate(b.line) if c in ["-", "^"]],  # type: ignore
                right=[],
                newline=c.line,  # type: ignore
                skip_lines=2,
            )

        return None

    def __match_pattern(
        self, diff_lines: List[DiffLine], codes: List[DiffLineCode]
    ) -> bool:
        return all([line.code == code for line, code in zip(diff_lines, codes)])
