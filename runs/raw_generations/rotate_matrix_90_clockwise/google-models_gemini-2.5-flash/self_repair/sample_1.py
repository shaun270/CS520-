```python
def rotate_matrix_90_clockwise(m: list[list[int]]) -> list[list[int]]:
    """
    Rotates a square matrix 90 degrees clockwise, returning a new matrix.

    Args:
        m: A list of lists of integers representing a square matrix.

    Returns:
        A new list of lists of integers representing the 90-degree clockwise
        rotation of the input matrix.
    """
    n = len(m)

    # Handle the case of an empty matrix.
    if n == 0:
        return []

    # Initialize a new matrix of the same dimensions with default values (e.g., 0).
    # This is necessary because the problem asks for a *new* matrix, not an in-place rotation.
    rotated_m = [[0] * n for _ in range(n)]