```python
def two_sum(nums: list[int], target: int) -> tuple[int,int] | None:
    """
    Finds two distinct indices i and j in the list nums such that nums[i] + nums[j] == target.
    The function guarantees that i < j in the returned tuple.

    Args:
        nums: A list of integers.
        target: The target sum.

    Returns:
        A tuple (i, j) where i < j and nums[i] + nums[j] == target,
        or None if no such pair of indices is found.
    """
    # A dictionary to store numbers and their indices encountered so far.
    # Key: number, Value: index
    num_map = {}

    # Iterate through the list with both index and value
    for i, num in enumerate(