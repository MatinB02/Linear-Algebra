import numpy as np

def rank(A):
    A = A.copy().astype(float)
    m, n = A.shape
    tol = 0.0005
    rank = 0
    for col in range(n):
        pivot_row = None
        max_val = tol
        for row in range(rank, m):
            if abs(A[row, col]) > max_val:
                max_val = abs(A[row, col])
                pivot_row = row
        if pivot_row is not None:
            A[[rank, pivot_row]] = A[[pivot_row, rank]]
            A[rank] /= A[rank, col]
            for row in range(m):
                if row != rank and abs(A[row, col]) > tol:
                    A[row] -= A[row, col] * A[rank]
            rank += 1
    return rank

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def norm(v):
    return sum(x * x for x in v) ** 0.5

def qr(A):
    A = A.copy().astype(float)
    m, n = A.shape
    Q = np.zeros((m, n))
    R = np.zeros((n, n))

    for j in range(n):
        v = A[:, j]
        for i in range(j):
            R[i, j] = dot(Q[:, i], A[:, j])
            v = v - R[i, j] * Q[:, i]
        R[j, j] = norm(v)
        if R[j, j] > 0.0005:
            Q[:, j] = v / R[j, j]
        else:
            Q[:, j] = 0

    return Q, R


def main():
    m, n = map(int, input().split())
    M = np.array([list(map(float, input().split())) for _ in range(m)])

    #Column Space
    OCM, _ = qr(M)
    rank_M = rank(M)
    OCM = OCM[:, :rank_M]
    print(rank_M)
    print_matrix(OCM @ OCM.T, shape=(m, m))

    #Null Space
    NM = null_space(M)
    nullity_M = NM.shape[1]
    print(nullity_M)
    if nullity_M == 0:
        print_matrix(np.zeros((n, n)))
    else:
        print_matrix(NM @ NM.T, shape=(n, n))

    #Column Space of M^T
    OCMT, _ = qr(M.T)
    rank_Mt = rank(M.T)
    OCMT = OCMT[:, :rank_Mt]
    print(rank_Mt)
    print_matrix(OCMT @ OCMT.T, shape=(n, n))

    #Null Space of M^T
    NMT = null_space(M.T)
    nullity_Mt = NMT.shape[1]
    print(nullity_Mt)
    if nullity_Mt == 0:
        print_matrix(np.zeros((m, m)))
    else:
        print_matrix(NMT @ NMT.T, shape=(m, m))

def null_space(A):
    U, S, Vt = np.linalg.svd(A)
    rank = (S > 0.0005).sum()
    null_space = Vt[rank:].T
    return null_space



def print_matrix(matrix, shape=None):
    if shape:
        full_matrix = np.zeros(shape)
        rows, cols = matrix.shape
        full_matrix[:rows, :cols] = matrix
        matrix = full_matrix

    for row in matrix:
        line = []
        for x in row:
            if abs(x) < 0.0005:
                x = 0.0
            line.append(f"{x:.{3}f}")
        print(' '.join(line))

if __name__ == "__main__":
    main()




