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
    # The key is the number, and the value is its index.
    num_map =