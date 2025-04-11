from dataclasses import dataclass
from typing import List, Optional

from difflib_parser.diff_code import DiffCode


@dataclass
class Diff:
    code: DiffCode
    line: str
    left_changes: Optional[List[int]] = None
    right_changes: Optional[List[int]] = None
    newline: Optional[str] = None
