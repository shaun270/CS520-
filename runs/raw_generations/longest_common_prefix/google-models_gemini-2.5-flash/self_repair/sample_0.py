def longest_common_prefix(strs: list[str]) -> str:
    if not strs:
        return ""

    # If there's only one string, it's the longest common prefix
    if len(strs) == 1:
        return strs[0]

    # Take the first string as a reference for comparison
    first_str = strs[0]

    # Iterate through the characters of the first string
    for i in range(len(first_str)):
        char_to_match = first_str[i]

        # Compare this character with the character at the same position in all other strings
        for j in range(1, len(strs)):
            current_str = strs[j]

            # If the current string is shorter than the current index 'i',
            # or if the character at index 'i' in the current string does not match
            # the character from the first string, then we've found the end of the common prefix.
            if i >= len(current_str) or current_str[i] != char_to_match:
                # Return the prefix found so far (up to, but not including, index 'i')
                return first_str[:i]

    # If the loop completes, it means the entire first_str is a common prefix
    # (i.e., all other strings start with first_str and are at least as long).
    return first_str
