def valid_parentheses(s: str) -> bool:
    """
    Validates if parentheses (), [], {} are properly nested and balanced in a string.

    Args:
        s: The input string containing parentheses and potentially other characters.

    Returns:
        True if the parentheses are valid, False otherwise.
    """
    stack = []
    
    # Define the mapping for closing to opening parentheses
    # This allows quick lookup for matching pairs
    parentheses_map = {
        ")": "(",
        "]": "[",
        "}": "{",
    }
    
    # A set of opening parentheses for efficient checking
    opening_brackets = set(parentheses_map.values())

    for char in s:
        if char in opening_brackets:
            # If it's an opening bracket, push it onto the stack
            stack.append(char)
        elif char in parentheses_map:
            # If it's a closing bracket
            if not stack:
                # If the stack is empty, there's no opening bracket to match
                return False
            
            # Pop the top element from the stack
            top_element = stack.pop()
            
            # Check if the popped element is the corresponding opening bracket
            if parentheses_map[char] != top_element:
                return False
        # If the character is not a parenthesis, simply ignore it.

    # After iterating through the entire string, if the stack is empty,
    # all opening brackets have been matched. Otherwise, there are unmatched
    # opening brackets.
    return not stack

