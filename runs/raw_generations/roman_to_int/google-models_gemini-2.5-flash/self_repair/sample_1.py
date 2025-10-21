```python
def roman_to_int(s: str) -> int:
    """
    Converts a Roman numeral string (up to 3999) to its integer equivalent.

    The function iterates through the Roman numeral string from left to right.
    It applies the rule that if a smaller value precedes a larger value, it's
    subtracted (e.g., IV = 4, IX = 9). Otherwise, it's added. The last character
    is always added.

    Args:
        s: A string representing a Roman numeral (e.g., "MCMXCIV").
           Assumed to be a valid Roman numeral string within the range [1, 3999].