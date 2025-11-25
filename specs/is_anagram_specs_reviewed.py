# Assume:
#   a: str
#   b: str
#   res: bool   # expected result of is_anagram(a, b)

na = [c.lower() for c in a if c.isalpha()]
nb = [c.lower() for c in b if c.isalpha()]

# S1: main characterization – res is True iff normalized multisets match
assert res == (sorted(na) == sorted(nb))

# S2: length mismatch after normalization implies not anagrams
if len(na) != len(nb):
    assert res is False

# S3: both normalize to empty → trivially anagrams
if not na and not nb:
    assert res is True

# S4: exactly one side empty → cannot be anagrams
if (not na and nb) or (na and not nb):
    assert res is False

# S5: if normalized multisets match, result must be True
if sorted(na) == sorted(nb):
    assert res is True
