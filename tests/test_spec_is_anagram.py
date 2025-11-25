from problems.problems import is_anagram


def test_both_empty_strings_trivially_anagrams():
    # Both normalize to empty -> res must be True
    assert is_anagram("", "") is True


def test_both_punctuation_only_normalize_to_empty():
    # No letters in either string -> both normalize to empty -> res must be True
    assert is_anagram("!!!", "...") is True


def test_one_empty_one_nonempty_not_anagrams():
    # Exactly one side normalizes to empty -> cannot be anagrams
    assert is_anagram("", "abc") is False
    assert is_anagram("abc", "") is False


def test_simple_positive_anagrams_letters_only():
    # Same multiset of letters -> True
    assert is_anagram("abcde", "edcba") is True
    assert is_anagram("abcdE", "dcbae") is True  # case-insensitive


def test_length_mismatch_after_normalization_false():
    # Normalized lengths differ -> must be False
    assert is_anagram("aabbc", "abbc") is False


def test_case_and_punctuation_ignored():
    # Case and non-letters ignored
    assert is_anagram("!a@b,c", "!c,b,a@!") is True
    assert is_anagram("AbCdE", "eDcBa") is True


def test_clearly_non_anagrams_same_length():
    # Same length after normalization but different multisets -> False
    assert is_anagram("abc", "abd") is False


def test_digits_ignored_in_normalization():
    # Digits are ignored, letters compared
    # "Dormitory123" vs "Dirty room 321" -> anagrams under normalization
    assert is_anagram("Dormitory123", "Dirty room 321") is True
