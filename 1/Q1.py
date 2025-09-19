import numpy as np

def compute_fundamental_subspaces(M):
    # Compute the four fundamental subspaces
    m, n = M.shape
    
    # Column space C(M)
    U, s, Vh = np.linalg.svd(M, full_matrices=False)
    rank = np.sum(s > 1e-10)
    
    # C(M)
    C_M = U[:, :rank]
    C_M_QT = C_M @ C_M.T
    
    # N(M^T) = left null space
    N_MT = U[:, rank:]
    if N_MT.size == 0:
        N_MT_QT = np.zeros((m, m))
    else:
        N_MT_QT = N_MT @ N_MT.T
    
    # For M^T we need to do another SVD on M.T
    U_MT, s_MT, Vh_MT = np.linalg.svd(M.T, full_matrices=False)
    rank_MT = np.sum(s_MT > 1e-10)
    
    # C(M^T) = row space
    C_MT = U_MT[:, :rank_MT]
    C_MT_QT = C_MT @ C_MT.T
    
    # N(M) = null space
    N_M = U_MT[:, rank_MT:]
    if N_M.size == 0:
        N_M_QT = np.zeros((n, n))
    else:
        N_M_QT = N_M @ N_M.T
    
    return (C_M_QT, N_M_QT, C_MT_QT, N_MT_QT), (rank, n-rank_MT, rank_MT, m-rank)

def print_result(QT, dim):
    print(dim)
    if dim == 0:
        # Print zero matrix of appropriate size
        rows, cols = QT.shape
        for _ in range(rows):
            print(' '.join(['0.000']*cols))
    else:
        for row in QT:
            print(' '.join([f'{x:.3f}' for x in row]))

def main():
    # Read input
    m, n = map(int, input().split())
    M = []
    for _ in range(m):
        row = list(map(float, input().split()))
        M.append(row)
    M = np.array(M)
    
    # Compute subspaces
    QTs, dims = compute_fundamental_subspaces(M)
    C_M_QT, N_M_QT, C_MT_QT, N_MT_QT = QTs
    dim_C_M, dim_N_M, dim_C_MT, dim_N_MT = dims
    
    # Print results in order: C(M), N(M), C(M^T), N(M^T)
    print_result(C_M_QT, dim_C_M)
    print_result(N_M_QT, dim_N_M)
    print_result(C_MT_QT, dim_C_MT)
    print_result(N_MT_QT, dim_N_MT)

if __name__ == "__main__":
    main()