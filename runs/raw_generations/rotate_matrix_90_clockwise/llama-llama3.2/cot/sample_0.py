def rotate_matrix_90_clockwise(m: list[list[int]]) -> list[list[int]]:
    """
    This function takes a square matrix as input and returns its 90-degree clockwise rotation.

    Args:
        m (list[list[int]]): A square matrix represented as a list of lists.

    Returns:
        list[list[int]]: The 90-degree clockwise rotation of the input matrix.
    """

    # Check if the input matrix is empty
    if not m:
        return []

    # Get the size of the matrix
    n = len(m)

    # Create a new matrix filled with zeros, with the same size as the input matrix
    rotated_matrix = [[0] * n for _ in range(n)]

    # Iterate over each element in the input matrix
    for i in range(n):
        for j in range(n):
            # Calculate the new position of the element after rotation
            rotated_matrix[j][n - i - 1] = m[i][j]

    # Return the rotated matrix
    return rotated_matrix