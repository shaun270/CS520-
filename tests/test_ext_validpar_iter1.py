from problems.valid_parentheses import valid_parentheses

# Success branches
def test_valid_success():
    """
    Target success cases where the parentheses are balanced.
    """
    assert valid_parentheses("{[]}") == True
    assert valid_parentheses("()[]{}") == True

# Closing on empty stack branch
def test_closing_on_empty_stack():
    """
    Test that a closing parenthesis returns False when the stack is empty.
    """
    assert valid_parentheses(")") == False

# Mismatched type branch
def test_mismatched_type():
    """
    Check that mismatched types (e.g., "(" vs "]" or "(" vs ")", etc.) return False.
    """
    assert valid_parentheses("(]") == False

# Leftover stack at end branch
def test_leftover_stack_at_end():
    """
    Verify that if an opening parenthesis is not closed, the function returns False.
    """
    assert valid_parentheses("(") == False
