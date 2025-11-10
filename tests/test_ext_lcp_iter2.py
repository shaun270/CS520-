from problems.longest_common_prefix import longest_common_prefix

def test_early_mismatch():
    # Test early mismatch
    assert longest_common_prefix(["dog", "racecar", "car"]) == ""

def test_full_word_as_prefix():
    # Test full word as prefix
    assert longest_common_prefix(["flower", "flow", "flight"]) == "fl"

def test_empty_list():
    # Test empty input
    assert longest_common_prefix([]) == ""

def test_single_element():
    # Test single element
    assert longest_common_prefix(["solo"]) == "solo"

def test_boundary_at_first_character():
    # Test boundary at first character (no 1-char outlier)
    assert longest_common_prefix(["xray", "xenon", "xa"]) == "x"

def test_min_length_cap_greater_than_1():
    # Test min-length cap > 1
    assert longest_common_prefix(["ab", "abc", "abz"]) == "ab"
