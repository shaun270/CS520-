def nth_fib(n: int) -> int:
    """
    Returns the 0-indexed Fibonacci number for a given non-negative integer n.

    The Fibonacci sequence is defined as:
    F(0) = 0
    F(1) = 1
    F(n) = F(n-1) + F(n-2) for n > 1

    Args:
        n: A non-negative integer (n >= 0).

    Returns:
        The n-th Fibonacci number.
    """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        # Initialize the first two Fibonacci numbers
        a, b = 0, 1
        # Iterate from the 2nd number up to the n-th number
        for _ in range(2, n + 1):
            # Calculate the next Fibonacci number
            next_fib = a + b
            # Update a and b for the next iteration
            a = b
            b = next_fib
        return b

