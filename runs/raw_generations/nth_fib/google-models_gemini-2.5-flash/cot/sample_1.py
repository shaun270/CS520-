def nth_fib(n: int) -> int:
    """
    Calculates the 0-indexed Fibonacci number for a given non-negative integer n.

    The Fibonacci sequence is defined as:
    F(0) = 0
    F(1) = 1
    F(n) = F(n-1) + F(n-2) for n > 1

    Args:
        n: The 0-indexed position in the Fibonacci sequence (n >= 0).

    Returns:
        The Fibonacci number at position n.
    """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        # Initialize the first two Fibonacci numbers
        a, b = 0, 1
        # Iterate n-1 times to reach the nth Fibonacci number
        # After the loop, b will hold F(n)
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

