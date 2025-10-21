def is_anagram(a: str, b: str) -> bool:
    """
    Checks if two strings are anagrams, ignoring case, spaces, and punctuation.

    Args:
        a: The first string.
        b: The second string.

    Returns:
        True if the strings are anagrams, False otherwise.
    """
    
    # Normalize string a: convert to lowercase and keep only alphabetic characters
    normalized_a_chars = [char.lower() for char in a if char.isalpha()]
    
    # Normalize string b: convert to lowercase and keep only alphabetic characters
    normalized_b_chars = [char.lower() for char in b if char.isalpha()]

    # Sort the lists of characters. If they are anagrams, their sorted character lists
    # should be identical.
    normalized_a_chars.sort()
    normalized_b_chars.sort()

    # Compare the sorted lists
    return normalized_a_chars == normalized_b_chars
