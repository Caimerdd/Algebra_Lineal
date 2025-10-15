from copy import deepcopy
from typing import List, Dict

EPS = 1e-9

def _snap(M: List[List[float]]) -> List[List[float]]:
    return [[float(x) for x in r] for r in M]

def _fmt(x: float) -> str:
    return f"{x:.4g}"

def gauss_steps(M: List[List[float]]) -> Dict:
    A = deepcopy(M)
    n = len(A)
    if n == 0: return {'steps': [], 'ops': [], 'status': 'empty', 'solution': None}
    m = len(A[0]) - 1

    steps = [_snap(A)]
    ops = ['Inicial']

    row = 0
    pivcols: List[int] = []
    for col in range(m):
        sel = None
        for r in range(row, n):
            if abs(A[r][col]) > EPS:
                sel = r; break
        if sel is None: continue

        if sel != row:
            A[row], A[sel] = A[sel], A[row]
            steps.append(_snap(A)); ops.append(f'F{row+1} ↔ F{sel+1}')

        for r in range(row+1, n):
            if abs(A[r][col]) > EPS:
                f = A[r][col] / A[row][col]
                for c in range(col, m+1): A[r][c] -= f * A[row][c]
                steps.append(_snap(A)); ops.append(f'F{r+1} ← F{r+1} − ({_fmt(f)})·F{row+1}')

        pivcols.append(col)
        row += 1
        if row == n: break

    for r in range(n):
        if all(abs(A[r][c]) < EPS for c in range(m)) and abs(A[r][m]) > EPS:
            return {'steps': steps, 'ops': ops, 'status': 'inconsistent', 'solution': None}

    if len(pivcols) == m:
        x = [0.0]*m
        for i in range(len(pivcols)-1, -1, -1):
            col = pivcols[i]; r = i; s = A[r][m]
            for c in range(col+1, m): s -= A[r][c] * x[c]
            x[col] = s / A[r][col] if abs(A[r][col])>EPS else 0.0
        return {'steps': steps, 'ops': ops, 'status': 'unique', 'solution': x}

    return {'steps': steps, 'ops': ops, 'status': 'incomplete', 'solution': None}

def gauss_jordan_steps(M: List[List[float]]) -> Dict:
    A = deepcopy(M)
    n = len(A)
    if n == 0: return {'steps': [], 'ops': [], 'status': 'empty', 'solution': None}
    m = len(A[0]) - 1

    steps = [_snap(A)]
    ops = ['Inicial']

    fila = 0
    pivot_map: Dict[int, int] = {}
    for col in range(m):
        sel = None
        for r in range(fila, n):
            if abs(A[r][col]) > EPS: sel = r; break
        if sel is None: continue

        if sel != fila:
            A[fila], A[sel] = A[sel], A[fila]
            steps.append(_snap(A)); ops.append(f'F{fila+1} ↔ F{sel+1}')

        piv = A[fila][col]
        if abs(piv) > EPS and abs(piv-1) > EPS:
            for c in range(m+1): A[fila][c] /= piv
            steps.append(_snap(A)); ops.append(f'F{fila+1} ← F{fila+1} / {_fmt(piv)}')

        for r in range(n):
            if r != fila and abs(A[r][col]) > EPS:
                f = A[r][col]
                for c in range(m+1): A[r][c] -= f * A[fila][c]
                steps.append(_snap(A)); ops.append(f'F{r+1} ← F{r+1} − ({_fmt(f)})·F{fila+1}')

        pivot_map[col] = fila
        fila += 1
        if fila == n: break

    for r in range(n):
        if all(abs(A[r][c]) < EPS for c in range(m)) and abs(A[r][m]) > EPS:
            return {'steps': steps, 'ops': ops, 'status': 'inconsistent', 'solution': None}

    if len(pivot_map) == m:
        sol = [0.0]*m
        for col, r in pivot_map.items(): sol[col] = A[r][m]
        return {'steps': steps, 'ops': ops, 'status': 'unique', 'solution': sol}

    libres = [c for c in range(m) if c not in pivot_map]
    basic_solution = {col: A[r][m] for col, r in pivot_map.items()}
    return {'steps': steps, 'ops': ops, 'status': 'infinite', 'solution': None,
            'free_vars': libres, 'basic_solution': basic_solution}

def independenciaVectores(M: List[List[float]]) -> Dict:
    A = deepcopy(M)
    if not A: return {'independent': True, 'rank': 0, 'num_vectors': 0}
    f, c = len(A), len(A[0])
    for i in range(f):
        for j in range(c): A[i][j] = float(A[i][j])
    rank = 0
    for col in range(c):
        sel = None
        for r in range(rank, f):
            if abs(A[r][col]) > EPS: sel = r; break
        if sel is None: continue
        if sel != rank: A[rank], A[sel] = A[sel], A[rank]
        piv = A[rank][col]
        for r in range(rank+1, f):
            if abs(A[r][col]) > EPS:
                factor = A[r][col] / piv
                for cc in range(col, c): A[r][cc] -= factor * A[rank][cc]
        rank += 1
        if rank == f: break
    return {'independent': rank == c, 'rank': rank, 'num_vectors': c}

def inverse_steps(A):
    # A: matriz cuadrada n×n
    from copy import deepcopy
    n = len(A)
    if n == 0: 
        return {'steps': [], 'ops': [], 'status': 'singular', 'inverse': None}
    if any(len(f) != n for f in A):
        raise ValueError('La inversa requiere matriz cuadrada.')

    # Construir [A | I]
    Aug = [list(map(float, fila)) + [1.0 if i == j else 0.0 for j in range(n)]
           for i, fila in enumerate(deepcopy(A))]
    m = n                # columnas de variables (solo el bloque izquierdo)
    total_cols = 2 * n   # columnas totales (izq + der)

    def _snap(M): return [[float(x) for x in r] for r in M]
    def _fmt(x):  return f"{x:.4g}"
    EPS = 1e-9

    steps = [_snap(Aug)]
    ops = ['Inicial [A | I]']

    fila = 0
    for col in range(m):
        # buscar pivote
        sel = None
        for r in range(fila, n):
            if abs(Aug[r][col]) > EPS:
                sel = r; break
        if sel is None:
            # no hay pivote en esta columna -> singular
            return {'steps': steps, 'ops': ops, 'status': 'singular', 'inverse': None}

        # swap si hace falta
        if sel != fila:
            Aug[fila], Aug[sel] = Aug[sel], Aug[fila]
            steps.append(_snap(Aug)); ops.append(f'F{fila+1} ↔ F{sel+1}')

        # normalizar fila del pivote
        piv = Aug[fila][col]
        if abs(piv - 1.0) > EPS:
            for c in range(total_cols):
                Aug[fila][c] /= piv
            steps.append(_snap(Aug)); ops.append(f'F{fila+1} ← F{fila+1} / {_fmt(piv)}')

        # eliminar en el resto de filas
        for r in range(n):
            if r != fila and abs(Aug[r][col]) > EPS:
                f = Aug[r][col]
                for c in range(total_cols):
                    Aug[r][c] -= f * Aug[fila][c]
                steps.append(_snap(Aug)); ops.append(f'F{r+1} ← F{r+1} − ({_fmt(f)})·F{fila+1}')

        fila += 1
        if fila == n: break

    # verificar que el bloque izquierdo es (aprox) I
    for i in range(n):
        for j in range(n):
            if abs(Aug[i][j] - (1.0 if i == j else 0.0)) > 1e-6:
                return {'steps': steps, 'ops': ops, 'status': 'singular', 'inverse': None}

    # extraer A^{-1} (bloque derecho)
    inv = [Aug[i][n:2*n] for i in range(n)]
    return {'steps': steps, 'ops': ops, 'status': 'invertible', 'inverse': inv}

