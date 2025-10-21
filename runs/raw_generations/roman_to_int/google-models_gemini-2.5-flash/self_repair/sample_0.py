```python
def roman_to_int(s: str) -> int:
    """
    Converts a Roman numeral string (up to 3999) to its integer equivalent.

    The function handles the standard Roman numeral notation, including
    subtractive cases (e.g., IV=4, IX=9).

    Args:
        s: A string representing a Roman numeral. It is guaranteed to be
           a valid Roman numeral within the range [1, 3999].

    Returns:
        The integer representation of the given Roman numeral.
    """
    roman_map = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }

    total = 0
    n = len(s)

    # Iterate through the Roman numeral string from left to right
    # up to the second-to-last character.
    for i in range(n - 1):
        current_value = roman_map[s[i]]
        next_value = roman_map[s[i+1]]

        # If the current symbol's value is less than the next symbol's value,
        # it means we have a subtractive case (e.g., IV, IX, XL, etc.).
        # In this case, subtract the current value from the total.
        if current_value < next_value:
            total -= current_value
        # Otherwise, add the current value to the total.
        else:
            total += current_value

    # After the loop, add the value of the last character.