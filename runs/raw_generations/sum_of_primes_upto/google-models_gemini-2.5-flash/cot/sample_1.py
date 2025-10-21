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

    # Sieve of Eratosthenes to find all primes up to n
    # Create a boolean array "is_prime[0..n]" and initialize
    # all entries it as true. A value in is_prime[i] will
    # finally be false if i is Not a prime, else true.
    is_prime = [True] * (n + 1)
    is_prime[0] = False  # 0 is not a prime number
    is_prime