def rotate_matrix_90_clockwise(m: list[list[int]]) -> list[list[int]]:
    """
    Rotates a square matrix 90 degrees clockwise, returning a new matrix.

    Args:
        m: A list of lists of integers representing a square matrix.

    Returns:
        A new list of lists of integers representing the rotated matrix.
    """
    # Handle the case of an empty matrix (0x0)
    if not m:
        return []

    N = len(m)

    # Create a new matrix of the same size, initialized with placeholders (e.g., 0s)
    # This ensures we are returning a new matrix, not modifying the original in-place.
    rotated_m = [[0 for _ in range(N)] for _ in range(N)]

    # Iterate through the original matrix and place elements into their new positions
    # For a 90-degree clockwise rotation, an element at m[row][col] moves to
    # rotated_m[col][N - 1 - row].
    for r in range(N):
        for c in range(N):
            rotated_m[c][N - 1 - r] = m[r][c]

    return rotated_m
