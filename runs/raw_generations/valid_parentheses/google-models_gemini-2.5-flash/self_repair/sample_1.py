```python
def valid_parentheses(s: str) -> bool:
    """
    Validates if the parentheses (), [], {} in a string are properly nested and balanced.

    Args:
        s: The input string containing parentheses and potentially other characters.

    Returns:
        True if the parentheses are valid, False otherwise.
    """
    stack = []  # Use a list as a stack
    
    # Define sets for opening brackets and a map for closing to opening brackets
    opening_brackets = {'(', '[', '{'}
    bracket_map = {')': '(', ']': '[', '}': '{'}
    
    for char in s:
        if char in opening_brackets:
            # If it's an opening bracket, push it onto the stack
            stack.append(char)
        elif char in bracket_map:
            # If it's a closing bracket
            # 1. Check if the stack is empty. If so, a closing bracket appeared
            #    without a corresponding opening one.
            if not stack:
                return False
            
            # 2