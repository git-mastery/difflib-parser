from enum import Enum


class DiffLineCode(Enum):
    ADDED = 0
    REMOVED = 1
    COMMON = 2
    MISSING = 3


class DiffLine:
    def __init__(self, line: str | None):
        self.__line = line
        print(self.__line)

    @staticmethod
    def parse(line: str | None) -> "DiffLine":
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
