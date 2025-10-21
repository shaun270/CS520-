```python
def sum_of_primes_upto(n: int) -> int:
    """
    Calculates the sum of all prime numbers less than or equal to n.

    Args:
        n: An integer (n >= 0).

    Returns:
        The sum of all primes up to n.
    """
    if n < 2:
        return 0

    # Initialize a boolean array `is_prime` for the Sieve of Eratosthenes.
    # is_prime[i] will be True if i is prime, False otherwise.
    # We need n + 1 elements to cover numbers from 0 to n.
    is_prime = [True] * (n + 1)
    is_prime[0] = False  # 0 is not a prime number
    is_prime[1] = False  # 1 is not a prime number

    # Start checking from p = 2.
    # We only need to iterate up to sqrt(n) because any composite number
    # n will have at least one prime factor less than or equal to sqrt(n).
    p = 2
    while p * p <= n:
        # If is_prime[p] is still True, then p is a prime number.