import math
import string
import pytest
from problems.problems import (
    two_sum, is_anagram, roman_to_int, longest_common_prefix,
    valid_parentheses, rotate_matrix_90_clockwise, merge_intervals,
    nth_fib, sum_of_primes_upto, word_wrap
)

def test_two_sum_basic():
    assert two_sum([2,7,11,15], 9) in {(0,1)}
    assert two_sum([3,2,4], 6) in {(1,2)}
    assert two_sum([3,3], 6) in {(0,1)}
    assert two_sum([1,2,3], 7) is None

def test_is_anagram():
    assert is_anagram("Listen", "Silent") is True
    assert is_anagram("A decimal point", "I'm a dot in place") is True
    assert is_anagram("Hello", "Ole lh!") is True
    assert is_anagram("Hello", "World") is False

def test_roman_to_int():
    assert roman_to_int("III") == 3
    assert roman_to_int("IV") == 4
    assert roman_to_int("IX") == 9
    assert roman_to_int("LVIII") == 58
    assert roman_to_int("MCMXCIV") == 1994
    assert roman_to_int("MMMCMXCIX") == 3999

def test_longest_common_prefix():
    assert longest_common_prefix(["flower","flow","flight"]) == "fl"
    assert longest_common_prefix(["dog","racecar","car"]) == ""
    assert longest_common_prefix([]) == ""
    assert longest_common_prefix(["interspecies","interstellar","interstate"]) == "inters"

def test_valid_parentheses():
    assert valid_parentheses("()") is True
    assert valid_parentheses("()[]{}") is True
    assert valid_parentheses("(]") is False
    assert valid_parentheses("([)]") is False
    assert valid_parentheses("{[]}") is True

def test_rotate_matrix_90_clockwise():
    m = [[1,2,3],[4,5,6],[7,8,9]]
    assert rotate_matrix_90_clockwise(m) == [[7,4,1],[8,5,2],[9,6,3]]

def test_merge_intervals():
    iv = [[1,3],[2,6],[8,10],[15,18]]
    assert merge_intervals(iv) == [[1,6],[8,10],[15,18]]
    iv2 = [[1,4],[4,5]]
    assert merge_intervals(iv2) == [[1,5]]
    iv3 = []
    assert merge_intervals(iv3) == []

def test_nth_fib():
    expected = [0,1,1,2,3,5,8,13,21,34,55]
    for i, v in enumerate(expected):
        assert nth_fib(i) == v
    assert nth_fib(30) == 832040

def test_sum_of_primes_upto():
    assert sum_of_primes_upto(0) == 0
    assert sum_of_primes_upto(1) == 0
    assert sum_of_primes_upto(2) == 2
    assert sum_of_primes_upto(10) == 17
    assert sum_of_primes_upto(30) == 129

def test_word_wrap():
    text = "This is a small piece of text to wrap."
    out = word_wrap(text, 10)
    assert all(len(line) <= 10 for line in out)
    assert " ".join(out) == text
    text2 = "supercalifragilisticexpialidocious test"
    out2 = word_wrap(text2, 10)
    assert out2[0] == "supercalifragilisticexpialidocious"
    assert out2[1] == "test"
