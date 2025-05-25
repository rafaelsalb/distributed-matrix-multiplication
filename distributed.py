from matrix import Matrix
from multiprocessing import Pool, cpu_count


def _multiply_submatrices(A: Matrix, B: Matrix) -> Matrix:
    return A * B


def distributed_matrix_multiplication(A: Matrix, B: Matrix, n: int) -> Matrix:
    submatrix_size = A.rows // n
    submatrices = [Matrix(submatrix_size, A.cols) for _ in range(n)]
    for m in range(n):
        for i in range(submatrix_size):
            for j in range(A.cols):
                submatrices[m][i][j] = A[m * submatrix_size + i][j]

    with Pool(processes=cpu_count()) as pool:
        results = pool.starmap(_multiply_submatrices, [(submatrices[m], B) for m in range(n)])

    result = Matrix(A.rows, B.cols)
    for m in range(n):
        for i in range(submatrix_size):
            for j in range(B.cols):
                result[m * submatrix_size + i][j] = results[m][i][j]

    return result
