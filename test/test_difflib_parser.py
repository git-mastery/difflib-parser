from difflib_parser import difflib_parser


def test_diff_parser_same_lines():
    parser = difflib_parser.DiffParser(["Hello world"], ["Hello world"])
    for diff in parser.iter_diffs():
        assert diff.code == difflib_parser.DiffCode.SAME


def test_diff_parser_added_line():
    parser = difflib_parser.DiffParser([], ["Hello world"])
    for diff in parser.iter_diffs():
        assert diff.code == difflib_parser.DiffCode.RIGHT_ONLY


def test_diff_parser_removed_line():
    parser = difflib_parser.DiffParser(["Hello world"], [])
    for diff in parser.iter_diffs():
        assert diff.code == difflib_parser.DiffCode.LEFT_ONLY


def test_diff_parser_changed_line_pattern_a():
    # Pattern a essentially looks at the case where existing characters were added/removed
    parser = difflib_parser.DiffParser(["Hello world"], ["Hola world"])
    for diff in parser.iter_diffs():
        assert diff.code == difflib_parser.DiffCode.CHANGED
        assert diff.line == "Hello world"
        assert diff.newline == "Hola world"
        assert diff.left_changes == [1, 3, 4]
        assert diff.right_changes == [1, 3]


def test_diff_parser_changed_line_pattern_b():
    # Pattern b essentially looks at the case where only additions were included
    parser = difflib_parser.DiffParser(["Hello world"], ["Hello world!"])
    for diff in parser.iter_diffs():
        assert diff.code == difflib_parser.DiffCode.CHANGED
        assert diff.line == "Hello world"
        assert diff.newline == "Hello world!"
        assert diff.left_changes == []
        assert diff.right_changes == [11]


def test_diff_parser_changed_line_pattern_c():
    # Pattern c essentially looks at the case where only removals were included
    parser = difflib_parser.DiffParser(["Hello world"], ["Hello worl"])
    for diff in parser.iter_diffs():
        assert diff.code == difflib_parser.DiffCode.CHANGED
        assert diff.line == "Hello world"
        assert diff.newline == "Hello worl"
        assert diff.left_changes == [10]
        assert diff.right_changes == []
