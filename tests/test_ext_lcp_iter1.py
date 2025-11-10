from problems.longest_common_prefix import longest_common_prefix

# Early mismatch empties prefix
def test_early_mismatch():
    assert longest_common_prefix(["dog","racecar","car"]) == ""

# Classic positive (shared prefix) - shrink loop executes
def test_shared_prefix_shrink():
    assert longest_common_prefix(["flower","flow","flight"]) == "fl"

# Full word as prefix
def test_full_word_as_prefix():
    assert longest_common_prefix(["car","carpet"]) == "car"

# Single element (no loop)
def test_single_element_no_loop():
    assert longest_common_prefix(["solo"]) == "solo"

# Shrink-to-empty inside while
def test_shrink_to_empty_inside_while():
    assert longest_common_prefix(["abc","x"]) == ""

# Equality boundary (no shrink)
def test_equality_boundary_no_shrink():
    assert longest_common_prefix(["car","car"]) == "car"

# Progressive shrink (correct expectation)
def test_progressive_shrink_correct_expectation():
    assert longest_common_prefix(["interview","internet","internal"]) == "inter"
