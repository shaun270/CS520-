def sum_of_primes_upto(n: int) -> int:
    """
    Calculates the sum of all prime numbers less than or equal to n.

    Args:
        n: An integer (n >= 0).

    Returns:
        The sum of primes up to n. Returns 0 if n < 2.
    """
    if n < 2:
        return 0

    # Initialize a boolean list `is_prime` for the Sieve of Eratosthenes.
    # is_prime[i] will be True if i is prime, False otherwise.
    # We need n + 1 elements to cover numbers from 0 to n.
    is_prime = [True] * (n + 1)

    # 0 and 1 are not prime numbers.
    is_prime[0] = False
    is_prime[1] = False

    # Start the sieve from p = 2.
    # We only need to check up to sqrt(n) because if a number m has a factor
    # greater than sqrt(m), it must also have a factor smaller than sqrt(m).
    # So, p * p <= n is sufficient.
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
