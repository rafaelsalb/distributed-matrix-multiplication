from examples import Examples


def example(A, B, C, D, serial_time_ms, distributed_time_ms):
    print("Matriz A:")
    print(A.rows, A.cols)
    print("Matriz B:")
    print(B.rows, B.cols)
    print("Matriz C (Resultado Serial):")
    print(C.rows, C.cols)
    print("Matriz D (Resultado Distribuído):")
    print(D.rows, D.cols)
    print(f"Tempo de execução serial: {serial_time_ms:.2f} ms")
    print(f"Tempo de execução distribuído: {distributed_time_ms:.2f} ms")


def main():
    print("Exemplo 1:")
    example(*Examples.example_1())
    print()
    print("Exemplo 2:")
    example(*Examples.example_2(n=4))
    print()
    for i in range(2, 10):
        if 100 % i == 0:
            print(f"Exemplo 3, com n = {i}:")
            example(*Examples.example_3(n=i))

if __name__ == "__main__":
    main()
