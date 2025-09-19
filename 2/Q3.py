import re
import numpy as np

def dot(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def parse_poly(expr):
    terms = re.findall(r'([+-]\d+\.?\d*)\*x\^(\d+)', expr)
    return [(float(c), int(e)) for c, e in terms]

def elim(n, aug):
    tol = 1e-9
    for i in range(n):
        max_r = i
        max_v = abs(aug[i, i])
        for k in range(i+1, n):
            cur_v = abs(aug[k, i])
            if cur_v > max_v:
                max_v = cur_v
                max_r = k
        aug[[i, max_r]] = aug[[max_r, i]].copy()
        pivot = aug[i, i]
        if abs(pivot) < tol:
            if np.all(np.abs(aug[i, :-1]) < tol):
                if np.abs(aug[i, -1]) >= tol:
                    raise ValueError("inconsistent")
                else:
                    continue

        for k in range(i+1, n):
            f = aug[k, i] / pivot
            aug[k, i:] -= f * aug[i, i:]

def back_sub(n, aug):
    x = np.zeros(n, dtype=np.float128)
    for i in range(n-1, -1, -1):
        if np.all(np.abs(aug[i, :-1]) < 1e-9):
            if np.abs(aug[i, -1]) >= 1e-9:
                raise ValueError("inconsistent")
            else:
                x[i] = 0
        else:
            x[i] = (aug[i, -1] - dot(aug[i, i+1:n], x[i+1:n])) / aug[i, i]
    return x

def solve(A, B):
    n = A.shape[0]
    aug = np.hstack([A, B.reshape(n, 1)]).astype(np.float128)
    elim(n, aug)
    return back_sub(n, aug)

def make_A(n, polys):
    A = np.zeros((n, n), dtype=np.float128)
    for i in range(n):
        p1 = polys[i]
        for j in range(n):
            p2 = polys[j]
            s = 0
            for c1, e1 in p1:
                for c2, e2 in p2:
                    s += c1 * c2 / (e1 + e2 + 1)
            A[i, j] = s
            if i == j:
                A[i, j] += 1e-9
    return A

def make_B(n, polys):
    B = np.zeros(n, dtype=np.float128)
    for i in range(n):
        p = polys[i]
        s = 0
        for c, e in p:
            s += -c / ((e + 1) ** 2)
        B[i] = s
    return B

def main():
    n = int(input())

    polys = []
    for _ in range(n):
        line = input().strip()
        poly = parse_poly(line)
        polys.append(poly)

    A = make_A(n, polys)
    B = make_B(n, polys)

    try:
        alpha = solve(A, B)
        min_val = 2.0 - dot(B, alpha)
        print("{0:.3f}".format(min_val))
    except ValueError:
        print("2.000")

if __name__ == "__main__":
    main()
