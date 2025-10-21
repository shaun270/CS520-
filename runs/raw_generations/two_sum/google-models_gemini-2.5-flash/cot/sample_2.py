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
    # The format is {number: index}.
    seen_numbers = {} 

    # Iterate through the list with both index (i) and value (num).
    for i, num in enumerate(nums):
        # Calculate the complement needed to reach the target.
        # If num + complement == target, then complement = target - num.
        complement = target - num
        
        # Check if the complement has been seen before.
        if complement in seen_numbers:
            # If the complement is found in seen_numbers, it means we have
            # found two numbers that sum up to the target.
            # The index 'j' of the complement will always be less than the
            # current index 'i'