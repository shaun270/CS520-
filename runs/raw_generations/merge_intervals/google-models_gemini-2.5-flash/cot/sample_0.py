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
