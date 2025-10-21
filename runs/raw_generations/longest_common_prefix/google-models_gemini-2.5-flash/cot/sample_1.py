```python
def longest_common_prefix(strs: list[str]) -> str:
    if not strs:
        return ""

    # If there's only one string, it's the longest common prefix
    if len(strs) == 1:
        return strs[0]

    # Take the first string as the reference for comparison
    # The longest common prefix cannot be longer than the shortest string.
    # We iterate through the characters of the first string.
    first