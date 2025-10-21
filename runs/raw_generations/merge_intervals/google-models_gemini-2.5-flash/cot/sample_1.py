def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """
    Merges overlapping [start, end] intervals and returns the result sorted by start time.

    Args:
        intervals: A list of intervals, where each interval is a list [start, end].

    Returns:
        A new list of merged, non-overlapping intervals, sorted by their start times.
    """
    if not intervals:
        return []

    # Sort intervals by their start times.
    # If start times are equal, the order doesn't strictly matter for correctness
    # but sorting by end time as a secondary key can provide a deterministic order.
    intervals.sort(key=lambda x: x[0])

    merged = []
    for interval in intervals:
        # If the merged list is empty or if the current interval does not overlap
        # with the last merged interval, simply append it.
        if not merged or interval[0] > merged[-1][1]:
            merged.append(interval)
        else:
            # There is an overlap, so merge the current interval with the last one
            # in the merged list by updating the end time of the last merged interval.
            merged[-1][1] = max(merged[-1][1], interval[1])

    return merged
