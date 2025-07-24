import time

import random
from matrix_utils import matrix_multiply, ConcurrentMultiplier, MatrixError

def generate_matrix(rows, cols):
    return [[random.randint(1, 10) for _ in range(cols)] for _ in range(rows)]

def matrices_are_equal(A, B, tolerance=1e-6):
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return False
    for i in range(len(A)):
        for j in range(len(A[0])):
            if abs(A[i][j] - B[i][j]) > tolerance:
                return False
    return True

def test_matrix_multiplication(size):
    print(f"\nTesting matrix multiplication with size {size}x{size}")
    A = generate_matrix(size, size)
    B = generate_matrix(size, size)

    # Sequential
    start = time.time()
    result_seq = matrix_multiply(A, B)
    end = time.time()
    print(f"Sequential time: {end - start:.2f} seconds")

    # Concurrent
    start = time.time()
    result_conc = ConcurrentMultiplier(A, B).multiply()
    end = time.time()
    print(f"Concurrent time: {end - start:.2f} seconds")

    print("Results match:", matrices_are_equal(result_seq, result_conc))


def test_edge_cases():
    print("\n\n🔎 Testing small edge cases...")

    cases = [
        {
            "A": [[2]],
            "B": [[3]],
            "desc": "1x1 × 1x1",
            "should_pass": True
        },
        {
            "A": [[1, 2]],
            "B": [[3], [4]],
            "desc": "1x2 × 2x1",
            "should_pass": True
        },
        {
            "A": [[1, 2], [3, 4]],
            "B": [[5, 6], [7, 8]],
            "desc": "2x2 × 2x2",
            "should_pass": True
        },
        {
            "A": [],
            "B": [],
            "desc": "Empty matrices",
            "should_pass": False
        },
        {
            "A": [[1, 2, 3], [4, 5, 6]],
            "B": [[7, 8], [9, 10]],
            "desc": "Incompatible dimensions",
            "should_pass": False
        },
        {
            "A": [[1, 2], [3]],  # ragged matrix
            "B": [[4, 5], [6, 7]],
            "desc": "Non-rectangular A",
            "should_pass": False
        }
    ]

    for case in cases:
        print(f"\nCase: {case['desc']}")
        try:
            result_seq = matrix_multiply(case["A"], case["B"])
            result_conc = ConcurrentMultiplier(case["A"], case["B"]).multiply()
            match = matrices_are_equal(result_seq, result_conc)
            print("✅ Passed" if match and case["should_pass"] else "❌ Unexpected result")
        except MatrixError as e:
            if not case["should_pass"]:
                print(f"✅ Correctly raised error: {e}")
            else:
                print(f"❌ Unexpected error: {e}")
        except Exception as e:
            print(f"❌ Unhandled exception: {e}")

if __name__ == "__main__":
    test_edge_cases()
    test_matrix_multiplication(100)
    test_matrix_multiplication(1000)
