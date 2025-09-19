def scale_row(matrix, row, col, rank_count, cols):
    scale = matrix[row][col]
    matrix[row] = [matrix[row][i] - scale * matrix[rank_count][i] for i in range(cols)]

def compute_rank(mat):
    from copy import deepcopy
    
    matrix = deepcopy(mat)
    rows, cols = len(matrix), len(matrix[0])
    rank_count = 0
    
    for current_column in range(cols):
        pivot_idx, max_value = -1, 0.01
        for row in range(rank_count, rows):
            if abs(matrix[row][current_column]) > max_value:
                max_value, pivot_idx = abs(matrix[row][current_column]), row
        
        if pivot_idx != -1:
            matrix[rank_count], matrix[pivot_idx] = matrix[pivot_idx], matrix[rank_count]
            pivot_value = matrix[rank_count][current_column]
            matrix[rank_count] = [element / pivot_value for element in matrix[rank_count]]
            
            for row in range(rows):
                if row != rank_count and abs(matrix[row][current_column]) > 0.001:
                    scale_row(matrix, row, current_column, rank_count, cols)

            rank_count += 1
    
    return rank_count


def main():
    dimensions = int(input())
    num_vectors = list(map(int, input().split()))
    vectors_A = [list(map(float, input().split())) for _ in range(dimensions)]
    vectors_B = [list(map(float, input().split())) for _ in range(dimensions)]
    
    combined_vectors = [vectors_A[i] + vectors_B[i] for i in range(dimensions)]
    
    rank_A, rank_B = compute_rank(vectors_A), compute_rank(vectors_B)
    print(rank_A) 
    print(rank_B)
    
    if rank_A == rank_B and compute_rank(combined_vectors) == rank_B:
        print("The two sets of vectors have the same span.")
    else:
        print("The two sets of vectors do NOT have the same span.")


main()
