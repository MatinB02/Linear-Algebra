def main():
    d = int(input())
    p, q = map(int, input().split())
    vecs = []
    for _ in range(p + q):
        vecs.append(list(map(float, input().split())))
    
    U = vecs[:p]
    V = vecs[p:]
    
    augmented = []
    for i in range(d):
        row = []
        for u in U:
            row.append(u[i])
        for v in V:
            row.append(-v[i])
        augmented.append(row)
    
    null_basis = nullspace_basis(augmented)
    
    if not null_basis:
        print(0)
        return
    
    intersection = []
    for sol in null_basis:
        coeffs = sol[:p]
        comb = [0] * d
        for j in range(p):
            comb = add(comb, scale(coeffs[j], U[j]))
        intersection.append(comb)
    
    intersection = [v for v in intersection if norm(v) > 0.0005]
    
    
    orthobasis = orthogonalize(intersection)
    
    if not orthobasis:
        print(0)
        return
    
    orthobasis = [normalize_vec(v) for v in orthobasis]
    
    if not intersection:
        print(0)
        return
        
    for i in range(d):
        line = []
        for v in orthobasis:
            line.append(v[i])
        print(*line)




def orthogonalize(vectors):
    orthobasis = []
    for v in vectors:
        w = v[:]
        for u in orthobasis:
            proj = scale(dot(w, u)/dot(u, u), u)
            w = sub(w, proj)
        if norm(w) > 0.0005:
            orthobasis.append(w)
    return orthobasis

def row_reduce(mat):
    mat = [row[:] for row in mat]
    rows, cols = len(mat), len(mat[0])
    r = 0
    for c in range(cols):
        if r >= rows:
            break
        pivot_idx = None
        for i in range(r, rows):
            if abs(mat[i][c]) > 0.0005:
                pivot_idx = i
                break
        if pivot_idx is None:
            continue
        mat[r], mat[pivot_idx] = mat[pivot_idx], mat[r]
        pivot_val = mat[r][c]
        mat[r] = [x / pivot_val for x in mat[r]]
        for i in range(rows):
            if i != r and abs(mat[i][c]) > 0.0005:
                factor = mat[i][c]
                mat[i] = [xi - factor * ri for xi, ri in zip(mat[i], mat[r])]
        r += 1
    return mat

def nullspace_basis(mat):
    mat = row_reduce(mat)
    rows, cols = len(mat), len(mat[0])
    pivots = set()
    for i in range(rows):
        for j in range(cols):
            if abs(mat[i][j]) > 0.0005:
                pivots.add(j)
                break
    free_vars = [j for j in range(cols) if j not in pivots]
    basis = []
    for free_col in free_vars:
        vec = [0] * cols
        vec[free_col] = 1
        for i in range(rows):
            pivot_col = None
            for j in range(cols):
                if abs(mat[i][j]) > 0.0005:
                    pivot_col = j
                    break
            if pivot_col is not None and pivot_col < free_col:
                vec[pivot_col] = -mat[i][free_col]
        basis.append(vec)
    return basis

def normalize_vec(u):
    length = norm(u)
    if length < 0.0005:
        return u
    return [a / length for a in u]


def sub(x, y):
    return [a - b for a, b in zip(x, y)]

def add(x, y):
    return [a + b for a, b in zip(x, y)]

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def norm(v):
    return sum(x * x for x in v) ** 0.5

def scale(c, v):
    return [c * x for x in v]


if __name__ == "__main__":
    main()