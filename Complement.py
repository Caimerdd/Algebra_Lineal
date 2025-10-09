# complement.py
# Utilidades de Álgebra Lineal usadas por la interfaz:
# - gauss_steps: Eliminación Gaussiana (solo adelante) con pasos.
# - gauss_jordan_steps: Gauss-Jordan (RREF) con pasos.
# - independenciaVectores: rank por eliminación y prueba de independencia (columnas).

from copy import deepcopy
from typing import List, Dict, Optional

EPS: float = 1e-9  # tolerancia numérica para ceros


def _matrix_snapshot(M: List[List[float]]) -> List[List[float]]:
    """Devuelve una copia float de la matriz para registrar un 'paso'."""
    return [[float(x) for x in fila] for fila in M]


def _fmt(x: float) -> str:
    return f"{x:.4g}"


def gauss_steps(matriz: List[List[float]]) -> Dict:
    """
    Ejecuta Eliminación Gaussiana (solo 'forward elimination') sobre una copia de `matriz`
    (matriz aumentada: última columna es el término independiente).

    Devuelve:
      {
        'steps': [matriz_en_cada_paso],
        'status': 'unique' | 'inconsistent' | 'incomplete' | 'empty',
        'solution': [x1, x2, ...] | None
      }
    - 'unique' si hay solución única y se pudo hacer sustitución regresiva.
    - 'inconsistent' si hay fila 0...0 | b!=0.
    - 'incomplete' si no hay pivotes suficientes para única solución (faltan columnas pivote).
    - 'empty' si la matriz está vacía.
    """
    A = deepcopy(matriz)
    n = len(A)
    if n == 0:
        return {'steps': [], 'status': 'empty', 'solution': None}
    m = len(A[0]) - 1  # número de variables (última col = RHS)

    steps = [_matrix_snapshot(A)]
    ops: list[str] = ['Inicial']

    row = 0
    pivot_cols: List[int] = []
    # Fase hacia adelante (triangular superior)
    for col in range(m):
        sel = None
        for r in range(row, n):
            if abs(A[r][col]) > EPS:
                sel = r
                break
        if sel is None:
            continue

        if sel != row:
            A[row], A[sel] = A[sel], A[row]
            steps.append(_matrix_snapshot(A))
            ops.append(f'Intercambiar F{row+1} <-> F{sel+1}')

        # eliminar por debajo
        for r in range(row + 1, n):
            if abs(A[r][col]) > EPS:
                factor = A[r][col] / A[row][col]
                for c in range(col, m + 1):
                    A[r][c] -= factor * A[row][c]
                steps.append(_matrix_snapshot(A))
                ops.append(f'F{r+1} = F{r+1} - ({_fmt(factor)})·F{row+1}')

        pivot_cols.append(col)
        row += 1
        if row == n:
            break

    # inconsistencia: 0...0 | b!=0
    for r in range(n):
        if all(abs(A[r][c]) < EPS for c in range(m)) and abs(A[r][m]) > EPS:
            return {'steps': steps, 'ops': ops, 'status': 'inconsistent', 'solution': None}

    # sustitución regresiva si hay tantos pivotes como variables
    if len(pivot_cols) == m:
        x = [0.0] * m
        for i in range(len(pivot_cols) - 1, -1, -1):
            col = pivot_cols[i]
            r = i
            s = A[r][m]
            for c in range(col + 1, m):
                s -= A[r][c] * x[c]
            # el pivote A[r][col] no debería ser ~0
            x[col] = s / A[r][col]
    return {'steps': steps, 'ops': ops, 'status': 'unique', 'solution': x}

    return {'steps': steps, 'ops': ops, 'status': 'incomplete', 'solution': None}


def gauss_jordan_steps(matriz: List[List[float]]) -> Dict:
    """
    Ejecuta Gauss-Jordan (RREF) sobre una copia de `matriz`
    (matriz aumentada: última columna es RHS).

    Devuelve:
      {
        'steps': [matriz_en_cada_paso],
        'status': 'unique' | 'inconsistent' | 'infinite' | 'empty',
        'solution': [x1, x2, ...] | None,
        'free_vars': [idx_col, ...] (solo si 'infinite')
      }
    """
    A = deepcopy(matriz)
    n = len(A)
    if n == 0:
        return {'steps': [], 'status': 'empty', 'solution': None}
    m = len(A[0]) - 1

    steps = [_matrix_snapshot(A)]
    ops: List[str] = ["Inicial"]

    fila = 0
    pivot_map: Dict[int, int] = {}  # col -> fila

    for col in range(m):
        # buscar pivote en (fila..n-1, col)
        sel = None
        for r in range(fila, n):
            if abs(A[r][col]) > EPS:
                sel = r
                break
        if sel is None:
            continue
        # swap si hace falta
        if sel != fila:
            A[fila], A[sel] = A[sel], A[fila]
            steps.append(_matrix_snapshot(A))
            ops.append(f'Intercambiar F{fila+1} <-> F{sel+1}')

        # normalizar fila del pivote
        pivote = A[fila][col]
        for c in range(m + 1):
            A[fila][c] /= pivote
        steps.append(_matrix_snapshot(A))
        ops.append(f'F{fila+1} = F{fila+1} / {_fmt(pivote) if isinstance(pivote, float) else pivote}')

        # eliminar en el resto de filas (arriba y abajo)
        for r in range(n):
            if r != fila and abs(A[r][col]) > EPS:
                factor = A[r][col]
                for c in range(m + 1):
                    A[r][c] -= factor * A[fila][c]
                steps.append(_matrix_snapshot(A))
                ops.append(f'F{r+1} = F{r+1} - ({_fmt(factor)})·F{fila+1}')

        pivot_map[col] = fila
        fila += 1
        if fila == n:
            break

    # inconsistencia: 0...0 | b!=0
    for r in range(n):
        if all(abs(A[r][c]) < EPS for c in range(m)) and abs(A[r][m]) > EPS:
            return {'steps': steps, 'ops': ops, 'status': 'inconsistent', 'solution': None}

    # única si hay pivote en todas las columnas de variable
    if len(pivot_map) == m:
        sol = [0.0] * m
        for col, r in pivot_map.items():
            sol[col] = A[r][m]
        return {'steps': steps, 'ops': ops, 'status': 'unique', 'solution': sol}

    # si no, infinitas: columnas sin pivote = variables libres
    libres = [c for c in range(m) if c not in pivot_map]
    return {'steps': steps, 'ops': ops, 'status': 'infinite', 'solution': None, 'free_vars': libres}


def independenciaVectores(matriz: List[List[float]]) -> Dict:
    """
    Determina si las **columnas** de `matriz` son linealmente independientes.

    Retorna:
      {
        'independent': bool,
        'rank': int,
        'num_vectors': int
      }
    - 'rank' se calcula por eliminación (sin necesidad de RREF completa).
    - 'num_vectors' = número de columnas (vectores).
    - independientes <=> rank == num_vectors.
    """
    A = deepcopy(matriz)
    if not A:
        return {'independent': True, 'rank': 0, 'num_vectors': 0}

    filas = len(A)
    cols = len(A[0])

    # asegurar float
    for i in range(filas):
        for j in range(cols):
            A[i][j] = float(A[i][j])

    rank = 0
    for col in range(cols):
        # buscar pivote en columna 'col' empezando en fila 'rank'
        sel = None
        for r in range(rank, filas):
            if abs(A[r][col]) > EPS:
                sel = r
                break
        if sel is None:
            continue

        # swap pivote a 'rank'
        if sel != rank:
            A[rank], A[sel] = A[sel], A[rank]

        pivote = A[rank][col]
        # eliminar por debajo
        for r in range(rank + 1, filas):
            if abs(A[r][col]) > EPS:
                factor = A[r][col] / pivote
                for c in range(col, cols):
                    A[r][c] -= factor * A[rank][c]

        rank += 1
        if rank == filas:
            break

    independiente = (rank == cols)
    return {'independent': independiente, 'rank': rank, 'num_vectors': cols}
