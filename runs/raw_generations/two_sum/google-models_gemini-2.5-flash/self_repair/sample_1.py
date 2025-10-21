```python
def two_sum(nums: list[int], target: int) -> tuple[int,int] | None:
    """
    Finds two distinct indices i and j (where i < j) in the list nums
    such that nums[i] + nums[j] == target.

    Args:
        nums: A list of integers.
        target: The target sum.

    Returns:
        A tuple (i, j) containing the indices if a pair is found,
        otherwise None.
    """
    # A dictionary to store numbers and their indices encountered so far.
    # Key: number, Value: index
    num_map = {}

    for i, num in enumerate(nums):
        complement = target - num
        
        # Check if the complement exists in our map.
        # If it does, we've found the two numbers.
        # The index stored in num_map[complement] will always be less than
        # the current index 'i' because we add numbers to the map *after*
        # checking for their