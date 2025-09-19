def replace_rows(c, r1, r2):
    c[r1] = c[r2]
    c[r2] = c[r1]

def scale_row(c, r):
    c[r] = [val * (1 / c[r][r]) for val in c[r]]

def add_rows(c, r1, r2):
    c[r1] = [val1 + val2 * (-c[r1][r2]/c[r2][r2]) for val1, val2 in zip(c[r1], c[r2])]

def hasInconsistentRow(c):
    for row in c:
        if all(value == 0 for value in row[:n]) and row[n] != 0:
            return True
    return False

def uniqueAnswer(c):
    pivots = set()
    for row in c:
        for j, value in enumerate(row[:n]):
            if value != 0:
                pivots.add(j)
                break
    return len(pivots) == n

def row_reduced_echelon_form(c):
    for i in range(n):
        if c[i][i] == 0:
            next_row = next((k for k in range(i + 1, n) if c[k][i] != 0), None)
            if next_row is not None:
                replace_rows(c, i, next_row)

        if c[i][i] == 0:
            continue

        scale_row(c, i)
        
        for j in (j for j in range(n) if j != i):
            add_rows(c, j, i)

#_______________________________main function:_____________________________________
n = int(input())

# c = Coefficients
c = [list(map(int, input().split())) for _ in range(n)]

s = [int(x) for x in input().split()]

[c[i].append(s[i]) for i in range(n)]

row_reduced_echelon_form(c)
if hasInconsistentRow(c):
    print("javab nadarad!")
elif not uniqueAnswer(c):
    print("javab yekta nadarad!")    
else:
    print(*["{:.2f}".format(row[n]) for row in c], sep="\n")
   
#_______________________________________________________________________
