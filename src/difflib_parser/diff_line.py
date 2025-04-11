from difflib_parser.diff_line_code import DiffLineCode


class DiffLine:
    def __init__(self, line: str | None):
        self.__line = line

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

        return None

    @property
    def line(self) -> str | None:
        if self.__line is None:
            return None

        return self.__line[2:]
