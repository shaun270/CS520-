from problems.valid_parentheses import valid_parentheses

# Success branch
def test_success():
    assert valid_parentheses("{[]}") == True
    assert valid_parentheses("()[]{}") == True

# Closing on empty stack branch
def test_closing_on_empty_stack():
    assert valid_parentheses(")") == False

# Mismatched type branch
def test_mismatched_type_branch():
    assert valid_parentheses("(]") == False

# Leftover stack at end (opens not closed) branch
def test_leftover_stack_at_end():
    assert valid_parentheses("(") == False
