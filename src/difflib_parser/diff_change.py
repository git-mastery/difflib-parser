from dataclasses import dataclass
from typing import List


@dataclass
class DiffChange:
    left: List[int]
    right: List[int]
    newline: str
    skip_lines: int
