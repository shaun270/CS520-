def nth_fib(n: int) -> int:
    """
    This function calculates the nth number in the Fibonacci sequence.
    
    Args:
        n (int): The position of the Fibonacci number to be calculated.
        
    Returns:
        int: The nth Fibonacci number.
    """
    
    # Base cases
    if n == 0:
        return 0
    elif n == 1:
        return 1
    
    # Initialize variables for the previous two numbers in the sequence
    a, b = 0, 1
    
    # Calculate the nth Fibonacci number
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    # Return the nth Fibonacci number
    return b