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
