# from typing import List, Tuple, Optional

# def two_sum(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
#     """Return indices (i, j) with i<j and nums[i]+nums[j]==target, else None."""
#     raise NotImplementedError

# def is_anagram(a: str, b: str) -> bool:
#     """Case-insensitive; ignore spaces/punctuation. Return True if anagrams."""
#     raise NotImplementedError

# def roman_to_int(s: str) -> int:
#     """Convert Roman numerals (<=3999) to integer."""
#     raise NotImplementedError

# def longest_common_prefix(strs: List[str]) -> str:
#     """Return the longest common prefix among strs."""
#     raise NotImplementedError

# def valid_parentheses(s: str) -> bool:
#     """Return True if (), [], {} are balanced and properly nested."""
#     raise NotImplementedError

# def rotate_matrix_90_clockwise(m: List[List[int]]) -> List[List[int]]:
#     """Return a new matrix that is the 90° clockwise rotation of square matrix m."""
#     raise NotImplementedError

# def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
#     """Merge overlapping [start,end] intervals. Return sorted result."""
#     raise NotImplementedError

# def nth_fib(n: int) -> int:
#     """0-indexed Fibonacci: fib(0)=0, fib(1)=1; n>=0."""
#     raise NotImplementedError

# def sum_of_primes_upto(n: int) -> int:
#     """Sum all primes <= n (n>=0)."""
#     raise NotImplementedError

# def word_wrap(text: str, width: int) -> List[str]:
#     """Greedy wrap on spaces; words longer than width get their own line."""
#     raise NotImplementedError

from typing import List, Optional, Tuple

def two_sum(nums: list[int], target: int) -> tuple[int,int] | None:
    """
    Finds two distinct indices i and j in the list nums such that i < j and nums[i] + nums[j] == target.

    Args:
        nums: A list of integers.
        target: The target sum.

    Returns:
        A tuple (i, j) with i < j if such a pair is found, otherwise None.
    """
    # A dictionary to store numbers encountered so far and their indices.
    # Key: number, Value: index
    seen_numbers = {}

    # Iterate through the list with both index and value
    for i, num in enumerate(nums):
        # Calculate the complement needed to reach the target
        complement = target - num

        # Check if the complement has been seen before
        if complement in seen_numbers:
            # If it has, we found a pair.
            # The index of the complement (j) will always be less than the current index (i)
            # because we add numbers to seen_numbers only after checking for their complements.
            j = seen_numbers[complement]
            return (j, i)
        
        # If the complement is not found, add the current number and its index to the dictionary
        # for future lookups.
        seen_numbers[num] = i
    
    # If no pair is found after iterating through the entire list, return None
    return None



def is_anagram(a: str, b: str) -> bool:
    """
    Checks if two strings are anagrams, ignoring case, spaces, and punctuation.

    Args:
        a: The first string.
        b: The second string.

    Returns:
        True if the strings are anagrams, False otherwise.
    """
    
    # Normalize string a: convert to lowercase and keep only alphabetic characters
    normalized_a_chars = [char.lower() for char in a if char.isalpha()]
    
    # Normalize string b: convert to lowercase and keep only alphabetic characters
    normalized_b_chars = [char.lower() for char in b if char.isalpha()]

    # Sort the lists of characters. If they are anagrams, their sorted character lists
    # should be identical.
    normalized_a_chars.sort()
    normalized_b_chars.sort()

    # Compare the sorted lists
    return normalized_a_chars == normalized_b_chars



def roman_to_int(s: str) -> int:
    roman_numerals = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    
    result = 0
    for i in range(len(s)):
        if i > 0 and roman_numerals[s[i]] > roman_numerals[s[i - 1]]:
            result += roman_numerals[s[i]] - 2 * roman_numerals[s[i - 1]]
        else:
            result += roman_numerals[s[i]]
    
    return result


def longest_common_prefix(strs: list[str]) -> str:
    if not strs:
        return ""

    # If there's only one string, it's the longest common prefix
    if len(strs) == 1:
        return strs[0]

    # Take the first string as a reference for comparison
    first_str = strs[0]

    # Iterate through the characters of the first string
    for i in range(len(first_str)):
        char_to_match = first_str[i]

        # Compare this character with the character at the same position in all other strings
        for j in range(1, len(strs)):
            current_str = strs[j]

            # If the current string is shorter than the current index 'i',
            # or if the character at index 'i' in the current string does not match
            # the character from the first string, then we've found the end of the common prefix.
            if i >= len(current_str) or current_str[i] != char_to_match:
                # Return the prefix found so far (up to, but not including, index 'i')
                return first_str[:i]

    # If the loop completes, it means the entire first_str is a common prefix
    # (i.e., all other strings start with first_str and are at least as long).
    return first_str



def valid_parentheses(s: str) -> bool:
    """
    Validates if parentheses (), [], {} are properly nested and balanced in a string.

    Args:
        s: The input string containing parentheses and potentially other characters.

    Returns:
        True if the parentheses are valid, False otherwise.
    """
    stack = []
    
    # Define the mapping for closing to opening parentheses
    # This allows quick lookup for matching pairs
    parentheses_map = {
        ")": "(",
        "]": "[",
        "}": "{",
    }
    
    # A set of opening parentheses for efficient checking
    opening_brackets = set(parentheses_map.values())

    for char in s:
        if char in opening_brackets:
            # If it's an opening bracket, push it onto the stack
            stack.append(char)
        elif char in parentheses_map:
            # If it's a closing bracket
            if not stack:
                # If the stack is empty, there's no opening bracket to match
                return False
            
            # Pop the top element from the stack
            top_element = stack.pop()
            
            # Check if the popped element is the corresponding opening bracket
            if parentheses_map[char] != top_element:
                return False
        # If the character is not a parenthesis, simply ignore it.

    # After iterating through the entire string, if the stack is empty,
    # all opening brackets have been matched. Otherwise, there are unmatched
    # opening brackets.
    return not stack




def rotate_matrix_90_clockwise(m: list[list[int]]) -> list[list[int]]:
    """
    Rotates a square matrix 90 degrees clockwise, returning a new matrix.

    Args:
        m: A list of lists of integers representing a square matrix.

    Returns:
        A new list of lists of integers representing the rotated matrix.
    """
    # Handle the case of an empty matrix (0x0)
    if not m:
        return []

    N = len(m)

    # Create a new matrix of the same size, initialized with placeholders (e.g., 0s)
    # This ensures we are returning a new matrix, not modifying the original in-place.
    rotated_m = [[0 for _ in range(N)] for _ in range(N)]

    # Iterate through the original matrix and place elements into their new positions
    # For a 90-degree clockwise rotation, an element at m[row][col] moves to
    # rotated_m[col][N - 1 - row].
    for r in range(N):
        for c in range(N):
            rotated_m[c][N - 1 - r] = m[r][c]

    return rotated_m


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """
    Merges overlapping [start, end] intervals and returns the result sorted by start time.

    Args:
        intervals: A list of intervals, where each interval is a list [start, end].

    Returns:
        A new list of non-overlapping intervals, sorted by their start times.
    """
    if not intervals:
        return []

    # Sort the intervals by their start times.
    # If start times are equal, the order of end times doesn't strictly matter for correctness
    # but a consistent sort helps. Python's default tuple comparison handles this fine.
    sorted_intervals = sorted(intervals)

    merged = []
    for interval in sorted_intervals:
        # If the merged list is empty or if the current interval does not overlap
        # with the last merged interval, simply add it.
        if not merged or interval[0] > merged[-1][1]:
            merged.append(interval)
        else:
            # Otherwise, there is an overlap, so merge the current and last intervals
            # by updating the end time of the last merged interval.
            merged[-1][1] = max(merged[-1][1], interval[1])

    return merged



def nth_fib(n: int) -> int:
    """
    Returns the 0-indexed Fibonacci number for a given non-negative integer n.

    The Fibonacci sequence is defined as:
    F(0) = 0
    F(1) = 1
    F(n) = F(n-1) + F(n-2) for n > 1

    Args:
        n: A non-negative integer (n >= 0).

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
        # Iterate from the 2nd number up to the n-th number
        for _ in range(2, n + 1):
            # Calculate the next Fibonacci number
            next_fib = a + b
            # Update a and b for the next iteration
            a = b
            b = next_fib
        return b




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


def word_wrap(text: str, width: int) -> list[str]:
    if not text or width < 1:
        return []
    
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(word) > width:
            if current_line:
                lines.append(current_line)
            current_line = word
        elif len(current_line) + (1 if current_line else 0) + len(word) <= width:
            if current_line:
                current_line += " "
            current_line += word
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return lines
