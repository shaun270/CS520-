# Assume:
#   text: str
#   width: int
#   lines: list[str]   # expected result of word_wrap(text, width)

words = text.split()
flat = [w for line in lines for w in line.split()]

# S1: empty text or non-positive width → no lines
if not text or width < 1:
    assert lines == []

# S2: words are preserved in order and never split across lines
assert flat == words

# S3: line length constraint with long-word exception
for line in lines:
    if len(line) > width:
        parts = line.split()
        # if a line exceeds width, it must be a single long word
        assert len(parts) == 1 and len(parts[0]) > width
    else:
        assert len(line) <= width

# S4: if no word exceeds width, then no line exceeds width
if words and width >= max(len(w) for w in words):
    assert all(len(line) <= width for line in lines)

# S5: no empty strings as lines
assert all(line != "" for line in lines)
