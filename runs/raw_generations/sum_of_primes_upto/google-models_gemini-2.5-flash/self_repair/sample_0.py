```python
def sum_of_primes_upto(n: int) -> int:
    if n < 2:
        return 0

    # Sieve of Eratosthenes
    # is_prime[i] will be True if i is prime, False otherwise.
    # Initialize a boolean list for numbers up to n.
    is_prime = [True] * (n + 1)
    is_prime[0] = False  # 0 is not prime
    is_prime[1] = False  # 1 is not prime

    # Iterate from 2 up to sqrt(n)
    # We only need to check for prime factors up to sqrt(n)
    # because any composite number n must have at least one prime factor
    # less than or equal to sqrt(n).
    p = 2
    while p * p <= n:
        # If is_prime[p] is still True, then p is a prime number
        if is_prime[p]:
            # Mark all multiples of p as not prime.
            # We can start marking from p*p because smaller multiples (p*2, p*3, etc.)
            # would have already been marked by smaller prime factors (2, 3, etc.).
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
        p += 1

    # Sum all prime numbers found
    total_sum