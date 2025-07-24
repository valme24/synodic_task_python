import threading
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')


class MatrixError(Exception):
    """Custom exception class for matrix-related errors."""
    pass


def matrix_multiply(A, B):
    """Multiply two matrices A and B. Returns the product matrix."""
    if not A or not B:
        raise MatrixError("One or both matrices are empty.")

    if not all(len(row) == len(A[0]) for row in A):
        raise MatrixError("Matrix A is not rectangular.")

    if not all(len(row) == len(B[0]) for row in B):
        raise MatrixError("Matrix B is not rectangular.")

    if len(A[0]) != len(B):
        raise MatrixError("Cannot multiply: Incompatible dimensions.")

    result = []
    for i in range(len(A)):
        result_row = []
        for j in range(len(B[0])):
            sum_value = 0
            for k in range(len(B)):
                sum_value += A[i][k] * B[k][j]
            result_row.append(sum_value)
        result.append(result_row)

    logging.info("Matrix multiplication completed successfully.")
    return result


def matrix_transpose(A):
    """Returns the transpose of matrix A."""
    if not A:
        raise MatrixError("Matrix is empty.")

    if not all(len(row) == len(A[0]) for row in A):
        raise MatrixError("Matrix is not rectangular.")

    result = []
    for i in range(len(A[0])):
        row = []
        for j in range(len(A)):
            row.append(A[j][i])
        result.append(row)

    logging.info("Matrix transpose completed successfully.")
    return result


def read_matrix_from_file(filename):
    """Reads a matrix from a file with numbers separated by spaces. Skips empty lines.
       Raises MatrixError on malformed lines."""
    matrix = []

    try:
        with open(filename, 'r') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    parts = line.strip().split()
                    try:
                        row = [int(x) for x in parts]
                    except ValueError:
                        raise MatrixError(f"Invalid number on line {line_num}: {line.strip()}")
                    matrix.append(row)
    except FileNotFoundError:
        raise MatrixError(f"File not found: {filename}")

    if not matrix:
        raise MatrixError("Matrix file is empty.")

    row_lengths = [len(row) for row in matrix]
    if len(set(row_lengths)) > 1:
        raise MatrixError("Rows have inconsistent lengths.")

    logging.info(f"Matrix read successfully from {filename}")
    return matrix


class ConcurrentMultiplier:
    """Performs matrix multiplication using multiple threads (safely)."""

    def __init__(self, A, B):
        if not A or not B:
            raise MatrixError("One or both matrices are empty.")

        if not all(len(row) == len(A[0]) for row in A):
            raise MatrixError("Matrix A is not rectangular.")
        if not all(len(row) == len(B[0]) for row in B):
            raise MatrixError("Matrix B is not rectangular.")
        if len(A[0]) != len(B):
            raise MatrixError("Cannot multiply: Incompatible dimensions.")

        self.A = A
        self.B = B
        self.result = [[0] * len(B[0]) for _ in range(len(A))]
        self.lock = threading.Lock()

    def worker(self, i, j):
        sum_val = 0
        for k in range(len(self.B)):
            sum_val += self.A[i][k] * self.B[k][j]
        with self.lock:
            self.result[i][j] = sum_val

    def multiply(self):
        threads = []
        for i in range(len(self.A)):
            for j in range(len(self.B[0])):
                t = threading.Thread(target=self.worker, args=(i, j))
                threads.append(t)
                t.start()

        for t in threads:
            t.join()

        logging.info("Concurrent matrix multiplication completed.")
        return self.result
