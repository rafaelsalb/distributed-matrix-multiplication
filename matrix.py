import random


class Matrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.data = [[0 for _ in range(cols)] for _ in range(rows)]

    @staticmethod
    def random(rows, cols, a=0, b=100):
        matrix = Matrix(rows, cols)
        for i in range(rows):
            for j in range(cols):
                matrix[i][j] = random.randint(a, b)
        return matrix

    @staticmethod
    def from_list(lst):
        rows = len(lst)
        cols = len(lst[0]) if lst else 0
        matrix = Matrix(rows, cols)
        for i in range(rows):
            for j in range(cols):
                matrix[i][j] = lst[i][j]
        return matrix

    def __getitem__(self, idx):
        return self.data[idx]

    def __setitem__(self, idx, value):
        self.data[idx] = value

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.data])

    def __mul__(self, other):
        if self.cols != other.rows:
            raise ValueError(f"Dimensões incompatíveis para multiplicação. {self.cols} != {other.rows}")

        result = Matrix(self.rows, other.cols)
        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    result[i][j] += self[i][k] * other[k][j]
        return result

    def __eq__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            return False
        for i in range(self.rows):
            for j in range(self.cols):
                if self[i][j] != other[i][j]:
                    return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __list__(self):
        _A = []
        for i in range(self.rows):
            _A.append(self[i])
        return _A
