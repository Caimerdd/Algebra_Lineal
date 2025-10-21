from copy import deepcopy
from typing import List, Dict

EPS = 1e-9

def _snap(M: List[List[float]]) -> List[List[float]]:
    return [[float(x) for x in r] for r in M]

def _fmt(x: float) -> str:
    return f"{x:.4g}"

def gauss_steps(M: List[List[float]]) -> Dict:
    """Calcula la forma escalonada de una matriz usando Eliminación Gaussiana."""
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
    """Calcula la forma escalonada reducida de una matriz usando Gauss-Jordan."""
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
    """Determina si un conjunto de vectores es linealmente independiente."""
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
    """Calcula la inversa de una matriz cuadrada."""
    n = len(A)
    if n == 0: return {'steps': [], 'ops': [], 'status': 'singular', 'inverse': None}
    if any(len(f) != n for f in A): raise ValueError('La inversa requiere matriz cuadrada.')
    Aug = [list(map(float, fila)) + [1.0 if i == j else 0.0 for j in range(n)] for i, fila in enumerate(deepcopy(A))]
    total_cols = 2 * n
    steps = [_snap(Aug)]
    ops = ['Inicial [A | I]']
    fila = 0
    for col in range(n):
        sel = None
        for r in range(fila, n):
            if abs(Aug[r][col]) > EPS: sel = r; break
        if sel is None: return {'steps': steps, 'ops': ops, 'status': 'singular', 'inverse': None}
        if sel != fila:
            Aug[fila], Aug[sel] = Aug[sel], Aug[fila]
            steps.append(_snap(Aug)); ops.append(f'F{fila+1} ↔ F{sel+1}')
        piv = Aug[fila][col]
        if abs(piv - 1.0) > EPS:
            for c in range(total_cols): Aug[fila][c] /= piv
            steps.append(_snap(Aug)); ops.append(f'F{fila+1} ← F{fila+1} / {_fmt(piv)}')
        for r in range(n):
            if r != fila and abs(Aug[r][col]) > EPS:
                f = Aug[r][col]
                for c in range(total_cols): Aug[r][c] -= f * Aug[fila][c]
                steps.append(_snap(Aug)); ops.append(f'F{r+1} ← F{r+1} − ({_fmt(f)})·F{fila+1}')
        fila += 1
        if fila == n: break
    for i in range(n):
        for j in range(n):
            if abs(Aug[i][j] - (1.0 if i == j else 0.0)) > 1e-6:
                return {'steps': steps, 'ops': ops, 'status': 'singular', 'inverse': None}
    inv = [Aug[i][n:2*n] for i in range(n)]
    return {'steps': steps, 'ops': ops, 'status': 'invertible', 'inverse': inv}

def pasos_determinante(matriz: List[List[float]]) -> Dict:
    """Calcula el determinante mostrando los pasos por expansión."""
    pasos = []
    def _determinante_recursivo(sub_matriz: List[List[float]], sangria: str = "") -> float:
        nonlocal pasos
        tamano = len(sub_matriz)
        if not sub_matriz or any(len(fila) != tamano for fila in sub_matriz):
            raise ValueError("La submatriz debe ser cuadrada y no vacía.")
        pasos.append(f"{sangria}Calculando det de matriz {tamano}x{tamano}:")
        for fila in sub_matriz:
            pasos.append(f"{sangria}  {[ _fmt(elem) for elem in fila ]}")
        if tamano == 1:
            determinante = sub_matriz[0][0]
            pasos.append(f"{sangria}└─> Resultado (caso base 1x1): {_fmt(determinante)}\n")
            return determinante
        if tamano == 2:
            a, b = sub_matriz[0][0], sub_matriz[0][1]
            c, d = sub_matriz[1][0], sub_matriz[1][1]
            determinante = a * d - b * c
            pasos.append(f"{sangria}└─> ({_fmt(a)}*{_fmt(d)}) - ({_fmt(b)}*{_fmt(c)}) = {_fmt(determinante)}\n")
            return determinante
        determinante_total = 0
        pasos.append(f"{sangria}Expandiendo por la primera fila:")
        for j in range(tamano):
            elemento = sub_matriz[0][j]
            signo = (-1)**j
            matriz_menor = [fila[:j] + fila[j+1:] for fila in sub_matriz[1:]]
            texto_signo = "+" if signo > 0 else "-"
            pasos.append(f"{sangria}  Término {j+1}: signo(-1)^(0+{j}) * (elemento) * det(submatriz)")
            pasos.append(f"{sangria}  = ({texto_signo} {_fmt(elemento)}) * det(submatriz)")
            determinante_submatriz = _determinante_recursivo(matriz_menor, sangria + "    ")
            termino = signo * elemento * determinante_submatriz
            determinante_total += termino
            pasos.append(f"{sangria}  └─> Valor del término: {texto_signo} {_fmt(elemento)} * {_fmt(determinante_submatriz)} = {_fmt(termino)}")
        pasos.append(f"{sangria}└─> Suma total de términos = {_fmt(determinante_total)}\n")
        return determinante_total
    try:
        if not matriz:
            return {'estado': 'error', 'mensaje': 'La matriz está vacía.'}
        tamano = len(matriz)
        if any(len(fila) != tamano for fila in matriz):
            return {'estado': 'error', 'mensaje': 'La matriz debe ser cuadrada.'}
        determinante_final = _determinante_recursivo(deepcopy(matriz))
        return {'estado': 'exito', 'determinante': determinante_final, 'pasos': pasos}
    except Exception as error:
        return {'estado': 'error', 'mensaje': str(error)}