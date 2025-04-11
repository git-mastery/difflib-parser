from enum import Enum


class DiffCode(Enum):
    SAME = 0
    RIGHT_ONLY = 1
    LEFT_ONLY = 2
    CHANGED = 3
