```python
def two_sum(nums: list[int], target: int) -> tuple[int,int] | None:
    # A dictionary to store numbers encountered so far and their indices.
    # The key will be the number, and the value will be its index.
    num_map = {}

    # Iterate through the list of numbers with their indices.
    for i, num in enumerate(nums):
        # Calculate the 'complement' needed to reach the target.
        # If num + complement == target, then complement = target - num.
        complement = target - num

        # Check if the complement already exists in our map.
        # If it does, we have found two numbers that sum up to the target.
        if complement in num_map:
            # The index of the complement is stored in num_map[complement].
            # Let's call this index 'j'.
            # The current number's index is 'i'.
            # Since we iterate from left to right, if complement was found in num_map,
            # its index (num_map[complement]) must be less than the current index 'i'.
            # Thus, we satisfy the i < j condition by returning (num_map[complement], i).
            return (num_map[complement], i)
        
        # If the complement is not found