from itertools import cycle
import grequests
from matrix import Matrix


def main(n_hosts, base_url="http://localhost", m=100, p=100, n=100):
    host_pool = [
        f"{base_url}:{5000 + i}" for i in range(n_hosts)
    ]
    pool = cycle(host_pool)

    print("Criando matrizes")
    A = Matrix.random(m, p)
    print("Matriz A criada")
    B = Matrix.random(p, n)
    print("Matriz B criada")
    submatrix_count = 4

    print("Criando submatrizes")
    submatrix_size = A.rows // submatrix_count
    submatrices = [Matrix(submatrix_size, A.cols) for _ in range(submatrix_count)]
    print(len(submatrices), submatrices[0].rows, submatrices[0].cols)
    for m in range(submatrix_count):
        for i in range(submatrix_size):
            for j in range(A.cols):
                submatrices[m][i][j] = A[m * submatrix_size + i][j]
    print("Submatrizes criadas")

    responses = [
        grequests.post(
            f"{next(pool)}/multiply",
            json={
                'A': list(submatrices[i]),
                'B': list(B),
                'key': i,
            }
        ) for i in range(submatrix_count)
    ]
    print("Multiplicando submatrizes")
    responses = grequests.map(responses)
    print("Submatrizes multiplicadas")
    print(responses)
    result = Matrix(A.rows, B.cols)

    assert result.rows == A.rows
    assert result.cols == B.cols

    for m in range(submatrix_count):
        for i in range(submatrix_size):
            for j in range(B.cols):
                result[m * submatrix_size + i][j] = responses[m].json()['result'][i][j]

    C = A * B
    assert C == result, "Os resultados da multiplicação não são iguais!"

    print(result)


if __name__ == "__main__":
    import sys

    m = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    p = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 100

    main(2, m=m, p=p, n=n)
