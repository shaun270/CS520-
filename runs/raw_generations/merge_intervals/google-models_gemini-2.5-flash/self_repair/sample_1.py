```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    # Handle edge case: if the list of intervals is empty, return an empty list.
    if not intervals:
        return []

    # Sort the intervals based on their start times.
    # This is crucial for the merging logic to work correctly, as it ensures
    #