from itertools import cycle
from time import monotonic
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
    submatrix_count = n_hosts if n_hosts < m else m

    print("Criando submatrizes")
    submatrix_size = A.rows // submatrix_count
    submatrices = [Matrix(submatrix_size, A.cols) for _ in range(submatrix_count)]
    print(len(submatrices), submatrices[0].rows, submatrices[0].cols)
    for m in range(submatrix_count):
        for i in range(submatrix_size):
            for j in range(A.cols):
                # Calcula o índice da linha em A correspondente à linha i da submatriz m.
                # Multiplica-se m pelo tamanho de cada submatriz para pular as linhas já distribuídas
                # e soma-se i para acessar a linha específica dentro do bloco atual.
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
    a = monotonic()
    responses = grequests.map(responses)
    b = monotonic()
    print(f"Multiplicação distribuída levou {b - a:.4f} segundos")
    if any(response is None for response in responses):
        raise RuntimeError("Alguma requisição falhou. Verifique os servidores.")
    print("Submatrizes multiplicadas")
    print(responses)
    result = Matrix(A.rows, B.cols)

    assert result.rows == A.rows
    assert result.cols == B.cols

    print("Construindo matriz resultado")

    for m in range(submatrix_count):
        for i in range(submatrix_size):
            for j in range(B.cols):
                result[m * submatrix_size + i][j] = responses[m].json()['result'][i][j]

    print("Multiplicando localmente")
    a = monotonic()
    C = A * B
    b = monotonic()
    print(f"Multiplicação local levou {b - a:.4f} segundos")
    assert C == result, "Os resultados da multiplicação não são iguais!"

    # print(result)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cliente para multiplicação distribuída de matrizes.")
    parser.add_argument("m", type=int, default=100, help="Número de linhas da matriz A.")
    parser.add_argument("p", type=int, default=100, help="Número de colunas da matriz A e linhas da matriz B.")
    parser.add_argument("n", type=int, default=100, help="Número de colunas da matriz B.")
    parser.add_argument("--hosts", type=int, default=2, help="Número de hosts para distribuir a multiplicação.")
    parser.add_argument("--base-url", type=str, default="http://localhost", help="URL base dos servidores.")
    parser.add_argument("--port-start", type=int, default=5000, help="Porta base para os servidores.")

    args = parser.parse_args()

    m = args.m
    p = args.p
    n = args.n
    n_hosts = args.hosts
    base_url = args.base_url
    if n_hosts < 1:
        raise ValueError("O número de hosts deve ser pelo menos 1.")
    if m < 1 or p < 1 or n < 1:
        raise ValueError("As dimensões das matrizes devem ser pelo menos 1.")

    main(n_hosts=n_hosts, base_url=base_url, m=m, p=p, n=n)
