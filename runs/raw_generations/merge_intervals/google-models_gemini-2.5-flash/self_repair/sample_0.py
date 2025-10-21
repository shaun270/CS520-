def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """
    Merges overlapping [start, end] intervals and returns a sorted list of non-overlapping intervals.

    Args:
        intervals: A list of intervals, where each interval is a list [start, end].

    Returns:
        A list of merged, non-overlapping intervals, sorted by their start times.
    """
    if not intervals:
        return []

    # Sort the intervals by their start times.
    # This is crucial for the merging logic to work correctly.
    intervals.sort(key=lambda x: x[0])

    merged = []
    for interval in intervals:
        # If the merged list is empty or if the current interval does not overlap
        # with the last merged interval, simply add it to the merged list.
        # An overlap exists if current_start > last_merged_end.
        if not merged or interval[0] > merged[-1][1]:
            merged.append(interval)
        else:
            # There is an overlap, so merge the current interval with the last
            # merged interval by updating the end time of the last merged interval
            # to be the maximum of its current end and the current interval's end.
            merged[-1][1] = max(merged[-1][1], interval[1])

    return merged
