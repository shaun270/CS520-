def sum_of_primes_upto(n: int) -> int:
    """
    Calculates the sum of all prime numbers less than or equal to n.

    Uses the Sieve of Eratosthenes for efficient prime number generation.

    Args:
        n: An integer representing the upper limit (inclusive).

    Returns:
        The sum of all prime numbers up to n. Returns 0 if n < 2.
    """
    if n < 2:
        return 0

    # Initialize a boolean list `is_prime` where is_prime[i] is True if i is potentially prime.
    # The list size needs to be n + 1 to include n itself.
    is_prime = [True] * (n + 1)

    # 0 and 1 are not prime numbers.
    is_prime[0] = False
    is_prime[1] = False

    # Apply the Sieve of Eratosthenes
    # We only need to check for prime factors up to sqrt(n).
    # The loop condition `p * p <= n` is equivalent to `p <= sqrt(n)`
    # and avoids floating-point calculations and the need for the `math` module.
    p = 2
    while p * p <= n:
        # If is_prime[p] is still True, then p is a prime number.
        if is_prime[p]:
            # Mark all multiples of p (starting from p*p) as not prime.
            # Multiples less than p*p would have already been marked by smaller primes.
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
        p += 1

    # Sum all numbers that are marked as prime.
    total_sum = 0
    for i in range(2, n + 1):
        if is_prime[i]:
            total_sum += i

    return total_sum
