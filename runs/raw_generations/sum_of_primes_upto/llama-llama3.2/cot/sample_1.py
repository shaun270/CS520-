def sum_of_primes_upto(n: int) -> int:
    """
    This function calculates the sum of all prime numbers up to n.

    Args:
        n (int): The upper limit for the prime numbers.

    Returns:
        int: The sum of all prime numbers up to n.
    """

    # Initialize a boolean array, prime, of size n+1
    prime = [True] * (n + 1)
    prime[0] = prime[1] = False

    # Iterate from 2 to sqrt(n)
    for p in range(2, int(n ** 0.5) + 1):
        # If p is a prime, mark as composite all the multiples of p
        if prime[p]:
            for i in range(p * p, n + 1, p):
                prime[i] = False

    # Sum all prime numbers up to n
    return sum(p for p in range(2, n + 1) if prime[p])