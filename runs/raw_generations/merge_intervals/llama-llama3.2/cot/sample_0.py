def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    # If the input list is empty, return an empty list
    if not intervals:
        return []

    # Sort the intervals based on the start value of each interval
    intervals.sort(key=lambda x: x[0])

    merged = [intervals[0]]

    # Iterate over the intervals starting from the second one
    for current in intervals[1:]:
        # Get the last merged interval
        last_merged = merged[-1]

        # If the current interval overlaps with the last merged interval, merge them
        if current[0] <= last_merged[1]:
            merged[-1] = [last_merged[0], max(last_merged[1], current[1])]
        else:
            # Add the current interval to the list of merged intervals
            merged.append(current)

    return merged