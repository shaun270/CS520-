def rotate_matrix_90_clockwise(m: list[list[int]]) -> list[list[int]]:
    return [list(reversed(i)) for i in zip(*m)]