def rotate_matrix_90_clockwise(m: list[list[int]]) -> list[list[int]]:
    """
    Rotates a square matrix 90 degrees clockwise, returning a new matrix.

    Args:
        m: A list of lists of integers representing the square matrix.

    Returns:
        A new list of lists of integers representing the rotated matrix.
    """
    # Handle the case of an empty matrix or a matrix with no rows.
    if not m:
        return []

    n = len(m)  # Get the size of the square matrix (N x N)

    # Create a new N x N matrix initialized with zeros.
    # This ensures we are returning a new matrix and not modifying the original.
    rotated_m = [[0] * n for _ in range(n)]

    # Iterate through each element of the original matrix
    for r in range(n):
        for c in range(n):
            # The element at original_matrix[row][col] moves to
            # new_matrix[col][N - 1 - row] after a 90-degree clockwise rotation.
            rotated_m[c][n - 1 - r] = m[r][c]

    return rotated_m
