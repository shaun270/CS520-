assert not res if not a or not b
assert res == (sorted(a) == sorted(b))
assert res == len(set(a) & set(b)) == 0
assert not res if len(a) != len(b)
assert res == (a.count(b) > 0 and b.count(a) > 0)
