from problems.problems import word_wrap


def test_empty_input_returns_empty_list():
    lines = word_wrap("", 5)
    assert lines == []


def test_single_line_within_width():
    text = "short text"
    width = 20
    lines = word_wrap(text, width)

    # All lines within width
    assert all(len(line) <= width for line in lines)
    # Words preserved and not split
    flat = [w for line in lines for w in line.split()]
    assert flat == text.split()


def test_wraps_to_multiple_lines():
    text = "one two three four five"
    width = 9  # narrow enough to force wrapping somewhere
    lines = word_wrap(text, width)

    # All lines within width
    assert all(len(line) <= width for line in lines)
    # Words preserved and not split
    flat = [w for line in lines for w in line.split()]
    assert flat == text.split()
    # Should wrap into at least 2 lines
    assert len(lines) >= 2


def test_no_empty_lines_in_output():
    text = "a bb ccc dddd"
    width = 5
    lines = word_wrap(text, width)

    # No empty strings as lines
    assert all(line != "" for line in lines)
    # Still within width
    assert all(len(line) <= width for line in lines)
