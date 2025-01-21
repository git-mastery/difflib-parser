from difflib_parser import diff_line


def test_diff_line_parse_None():
    line = diff_line.DiffLine.parse(None)
    assert line is not None
    assert line.code is None
    assert line.line is None


def test_diff_line_code_added():
    line = diff_line.DiffLine.parse("+ ")
    assert line is not None
    assert line.code == diff_line.DiffLineCode.ADDED


def test_diff_line_code_removed():
    line = diff_line.DiffLine.parse("- ")
    assert line is not None
    assert line.code == diff_line.DiffLineCode.REMOVED


def test_diff_line_code_common():
    line = diff_line.DiffLine.parse("  ")
    assert line is not None
    assert line.code == diff_line.DiffLineCode.COMMON


def test_diff_line_code_missing():
    line = diff_line.DiffLine.parse("?  ")
    assert line is not None
    assert line.code == diff_line.DiffLineCode.MISSING


def test_diff_line_line():
    line = diff_line.DiffLine.parse("? Hello world!")
    assert line is not None
    assert line.code == diff_line.DiffLineCode.MISSING
    assert line.line == "Hello world!"
