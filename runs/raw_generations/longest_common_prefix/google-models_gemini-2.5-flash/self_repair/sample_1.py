def longest_common_prefix(strs: list[str]) -> str:
    if not strs:
        return ""

    # If there's only one string, it is the longest common prefix.
    if len(strs) == 1:
        return strs[0]

    # Take the first string as a reference for comparison.
    first_str = strs[0]
    
    # Iterate through each character of the first string.
    # This loop determines the potential length of the common prefix.
    for i in range(len(first_str)):
        char_to_match = first_str[i]
        
        # Compare this character with the character at the same position
        # in all other strings in the list.
        for j in range(1, len(strs)):
            # Two conditions indicate the end of the common prefix:
            # 1