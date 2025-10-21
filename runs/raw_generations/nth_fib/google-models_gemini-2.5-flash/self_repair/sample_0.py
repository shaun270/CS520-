def nth_fib(n: int) -> int:
    """
    Calculates the n-th Fibonacci number (0-indexed).

    The Fibonacci sequence is defined as:
    F(0) = 0
    F(1) = 1
    F(n) = F(n-1) + F(n-2) for n > 1

    Args:
        n: The 0-indexed position of the desired Fibonacci number. Must be n >= 0.

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
        # Iterate n-1 times to calculate the n-th Fibonacci number
        # After the loop, 'b' will hold F(n)
        for _ in range(n - 1):
            a, b = b, a + b
        return b

