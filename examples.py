import random
import time
from distributed import distributed_matrix_multiplication
from matrix import Matrix


class Examples:
    @staticmethod
    def example_1():
        A = Matrix(2, 3)
        B = Matrix(3, 2)
        A[0][0] = 1
        A[0][1] = 2
        A[0][2] = 3
        A[1][0] = 4
        A[1][1] = 5
        A[1][2] = 6

        B[0][0] = 7
        B[0][1] = 8
        B[1][0] = 9
        B[1][1] = 10
        B[2][0] = 11
        B[2][1] = 12

        a = time.monotonic()
        C = A * B
        b = time.monotonic()
        serial_time_ms = b - a

        n = 2  # Número de submatrizes
        a = time.monotonic()
        D = distributed_matrix_multiplication(A, B, n)
        b = time.monotonic()
        distributed_time_ms = b - a

        return A, B, C, D, serial_time_ms, distributed_time_ms

    @staticmethod
    def example_2(n=4):
        A = Matrix(100, 100)
        B = Matrix(100, 100)

        for i in range(100):
            for j in range(100):
                A[i][j] = i + j
                B[i][j] = i - j

        a = time.monotonic()
        C = A * B
        b = time.monotonic()
        serial_time_ms = b - a

        a = time.monotonic()
        D = distributed_matrix_multiplication(A, B, n)
        b = time.monotonic()
        distributed_time_ms = b - a

        if C != D:
            raise ValueError("Os resultados da multiplicação não são iguais!")

        return A, B, C, D, serial_time_ms, distributed_time_ms

    @staticmethod
    def example_3(n=4):
        A = Matrix.random(100, 500)
        B = Matrix.random(500, 1000)

        a = time.monotonic()
        C = A * B
        b = time.monotonic()
        serial_time_ms = b - a

        a = time.monotonic()
        D = distributed_matrix_multiplication(A, B, n)
        b = time.monotonic()
        distributed_time_ms = b - a

        if C != D:
            raise ValueError("Os resultados da multiplicação não são iguais!")

        return A, B, C, D, serial_time_ms, distributed_time_ms

