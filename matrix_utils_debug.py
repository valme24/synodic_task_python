import logging
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MatrixError(Exception):
    """Custom exception for matrix-related errors."""
    pass

def is_rectangular(matrix):
    """Check if a matrix is rectangular (all rows have the same length)."""
    return all(len(row) == len(matrix[0]) for row in matrix)

def validate_matrix(matrix, name="Matrix"):
    if not matrix:
        raise MatrixError(f"{name} is empty.")
    if not is_rectangular(matrix):
        raise MatrixError(f"{name} is not rectangular.")

def validate_dimensions(A, B):
    if len(A[0]) != len(B):
        raise MatrixError(
            f"Incompatible matrices for multiplication: A has {len(A[0])} columns, "
            f"B has {len(B)} rows."
        )

def matrix_multiply(A, B):
    """Multiply two matrices using a standard nested loop algorithm."""
    validate_matrix(A, "Matrix A")
    validate_matrix(B, "Matrix B")
    validate_dimensions(A, B)

    result = [[0] * len(B[0]) for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            result[i][j] = sum(A[i][k] * B[k][j] for k in range(len(B)))
    return result

class ConcurrentMultiplier:
    """Performs matrix multiplication using threads for each row."""
    def __init__(self, A, B, max_workers=8):
        validate_matrix(A, "Matrix A")
        validate_matrix(B, "Matrix B")
        validate_dimensions(A, B)

        self.A = A
        self.B = B
        self.max_workers = max_workers
        self.result = [[0] * len(B[0]) for _ in range(len(A))]

    def _compute_row(self, i):
        for j in range(len(self.B[0])):
            self.result[i][j] = sum(self.A[i][k] * self.B[k][j] for k in range(len(self.B)))

    def multiply(self):
        logger.info("Starting concurrent multiplication")
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self._compute_row, i) for i in range(len(self.A))]
            for future in futures:
                future.result()  # wait for all threads to finish
        logger.info("Finished concurrent multiplication")
        return self.result

def transpose_matrix(matrix):
    """Transpose a 2D matrix (swap rows and columns)."""
    validate_matrix(matrix, "Matrix")
    return [list(row) for row in zip(*matrix)]

def read_matrix_from_file(filename):
    """Read a matrix from a text file with space-separated values."""
    try:
        with open(filename, 'r') as file:
            matrix = [list(map(float, line.strip().split())) for line in file if line.strip()]
    except Exception as e:
        raise MatrixError(f"Error reading matrix from file: {e}")

    validate_matrix(matrix, "Matrix from file")
    return matrix
