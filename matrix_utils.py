import threading
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MatrixError(Exception):
    pass


def matrix_multiply(A, B):
    """
    Multiply two matrices A and B.
    A and B are lists of lists (2D matrices).
    Returns the product matrix.
    """
    if not A or not B or not A[0] or not B[0]:
        raise MatrixError("Empty matrix provided.")

    if len(A[0]) != len(B):
        raise MatrixError("Cannot multiply: Incompatible dimensions.")

    result = []
    for i in range(len(A)):
        result_row = []
        for j in range(len(B[0])):
            sum_value = sum(A[i][k] * B[k][j] for k in range(len(A[0])))
            result_row.append(sum_value)
        result.append(result_row)
    return result


def matrix_transpose(A):
    """
    Returns the transpose of matrix A.
    """
    if not A or not A[0]:
        raise MatrixError("Empty matrix cannot be transposed.")

    result = []
    for i in range(len(A[0])):
        row = [A[j][i] for j in range(len(A))]
        result.append(row)
    return result


def read_matrix_from_file(filename):
    """
    Reads a matrix from a file with numbers separated by spaces. Skips empty lines.
    Raises MatrixError on malformed lines.
    """
    matrix = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split()
                    try:
                        row = [int(x) for x in parts]
                        matrix.append(row)
                    except ValueError:
                        raise MatrixError(f"Invalid number in file: {line.strip()}")
        if len(set(len(r) for r in matrix)) > 1:
            raise MatrixError("Rows have inconsistent lengths")
        return matrix
    except FileNotFoundError:
        raise MatrixError(f"File not found: {filename}")


