```python
def roman_to_int(s: str) -> int:
    """
    Converts a Roman numeral string (up to 3999) to its integer equivalent.

    The function handles the standard Roman numeral system, including the
    subtractive notation (e.g., IV=4, IX=9, XL=40, XC=90, CD=400, CM=900).

    Args:
        s: A string representing a Roman numeral. It is guaranteed to be a
           valid Roman numeral within the range [1, 3999].

    Returns:
        An integer representing the decimal value of the Roman