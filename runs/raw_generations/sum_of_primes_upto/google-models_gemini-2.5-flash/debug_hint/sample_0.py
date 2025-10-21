```python
def sum_of_primes_upto(n: int) -> int:
    """
    Calculates the sum of all prime numbers less than or equal to n.

    Uses the Sieve of Eratosthenes to find primes efficiently.

    Args:
        n: An integer representing the upper limit (inclusive). Must be >= 0.

    Returns:
        The sum of all primes <= n. Returns 0 if n < 2.
    """
    if n < 2:
        return 0

    # Initialize a boolean list `is_prime` where is_prime[i] is True if i is potentially prime.
    # The list size is n + 1 to include n itself.
    is_prime = [True] * (n + 1)

    # 0 and 1 are not prime numbers.
    is_prime[0] = False
    is_prime[1] = False

    # Start the Sieve process from p = 2.
    # We only need to check up to sqrt(n) because if a number m has a prime factor
    # greater than sqrt(m), it must also have a prime factor smaller than sqrt(m).
    # The loop condition p * p <= n is equivalent to p <= sqrt(n).
    p = 2
    while (p * p) <= n:
        # If is_prime[p] is still True, then p is a prime number.
        if is_prime[p]:
            # Mark all multiples of p (starting from p*p)