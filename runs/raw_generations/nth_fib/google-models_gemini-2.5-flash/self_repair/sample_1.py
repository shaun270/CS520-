def nth_fib(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        # Initialize a and b to the first two Fibonacci numbers, F(0) and F(1)
        # 'a' will represent F(k-2) and 'b' will represent F(k-1)
        a = 0
        b = 1
        
        # Iterate from the 2nd Fibonacci number up to the nth Fibonacci number
        # The loop runs n-1 times to calculate F(2) through F(n)
        for _ in range(2, n + 1):
            next_fib = a + b
            a = b
            b = next_fib
            
        # After the loop, 'b' holds the nth Fibonacci number
        return b
