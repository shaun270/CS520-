```python
def two_sum(nums: list[int], target: int) -> tuple[int,int] | None:
    """
    Finds two distinct indices i and j in the list nums such that i < j and nums[i] + nums[j] == target.

    Args:
        nums: A list of integers.
        target: The target sum.

    Returns:
        A tuple (i, j) where i < j and nums[i] + nums[j] == target,
        or None if no such pair is found.
    """
    # A dictionary to store numbers encountered so far and their indices.
    # Key: number, Value: index
    seen_numbers = {}

    for i, num in enumerate(nums):
        complement = target - num
        
        # If the complement exists in our seen_numbers dictionary,
        # it means we have found two numbers that sum up to the target.
        # Since we iterate from left to right (increasing 'i'),
        # the index 'j' of the complement will always be less than 'i'.
        if complement in seen_numbers:
            j = seen_numbers[complement]
            return (j, i)
        
        # If the complement is not found, add the current number and its index
        # to the dictionary for future checks.
        seen_numbers[num] = i
            
    # If the loop completes without