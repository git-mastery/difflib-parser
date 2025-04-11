from enum import Enum


class DiffLineCode(Enum):
    ADDED = 0
    REMOVED = 1
    COMMON = 2
    MISSING = 3
