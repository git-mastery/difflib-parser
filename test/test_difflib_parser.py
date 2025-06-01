from difflib_parser import difflib_parser, DiffCode


def test_diff_parser_same_lines():
    parser = difflib_parser.DifflibParser(["Hello world"], ["Hello world"])
    for diff in parser.iter_diffs():
        assert diff.code == DiffCode.SAME


def test_diff_parser_added_line():
    parser = difflib_parser.DifflibParser([], ["Hello world"])
    for diff in parser.iter_diffs():
        assert diff.code == DiffCode.RIGHT_ONLY


def test_diff_parser_removed_line():
    parser = difflib_parser.DifflibParser(["Hello world"], [])
    for diff in parser.iter_diffs():
        assert diff.code == DiffCode.LEFT_ONLY


def test_diff_parser_edited_multi_line():
    parser = difflib_parser.DifflibParser(
        ["- Milk", "- Eggs", "Bread", "- Apples", "- Ham"],
        ["- Milk", "- Eggs", "Bread", "- Apples", "- Ham1"],
    )
    expected_codes = [
        DiffCode.SAME,
        DiffCode.SAME,
        DiffCode.SAME,
        DiffCode.SAME,
        DiffCode.CHANGED,
    ]
    i = 0
    for diff in parser.iter_diffs():
        assert diff.code == expected_codes[i]
        if diff.code == DiffCode.CHANGED:
            assert diff.line == "- Ham"
            assert diff.newline == "- Ham1"
            assert diff.left_changes == []
            assert diff.right_changes == [5]
        i += 1


def test_diff_parser_changed_line_pattern_a():
    # Pattern a essentially looks at the case where existing characters were added/removed
    parser = difflib_parser.DifflibParser(["Hello world"], ["Hola world"])
    for diff in parser.iter_diffs():
        assert diff.code == DiffCode.CHANGED
        assert diff.line == "Hello world"
        assert diff.newline == "Hola world"
        assert diff.left_changes == [1, 3, 4]
        assert diff.right_changes == [1, 3]


def test_diff_parser_changed_line_pattern_b():
    # Pattern b essentially looks at the case where only additions were included
    parser = difflib_parser.DifflibParser(["Hello world"], ["Hello world!"])
    for diff in parser.iter_diffs():
        assert diff.code == DiffCode.CHANGED
        assert diff.line == "Hello world"
        assert diff.newline == "Hello world!"
        assert diff.left_changes == []
        assert diff.right_changes == [11]


def test_diff_parser_changed_line_pattern_c():
    # Pattern c essentially looks at the case where only removals were included
    parser = difflib_parser.DifflibParser(["Hello world"], ["Hello worl"])
    for diff in parser.iter_diffs():
        assert diff.code == DiffCode.CHANGED
        assert diff.line == "Hello world"
        assert diff.newline == "Hello worl"
        assert diff.left_changes == [10]
        assert diff.right_changes == []
