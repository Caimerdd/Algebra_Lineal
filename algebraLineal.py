import re

EPS = 1e-9  # tolerancia numérica

# --- Utilidad para limpiar guiones ---
def normalizarGuiones(s):
    """Reemplaza distintos tipos de guiones por '-' (normalización)."""
    return s.replace('−', '-').replace('–', '-').replace('—', '-')
# alias por compatibilidad
normalizar_guiones = normalizarGuiones

# --- Parsear un lado de la ecuación ---
def parsearLado(expr):
    """Parsea un lado de una ecuación en coeficientes y término independiente."""
    s = normalizarGuiones(expr)
    if s == '':
        raise ValueError("Lado vacío")
    if s[0] not in '+-':
        s = '+' + s
    s = s.replace('-', '+-')
    partes = [t for t in s.split('+') if t != '']

    vars_dict = {}
    const = 0.0

    for p in partes:
        idx = 0
        while idx < len(p) and (p[idx].isdigit() or p[idx] == '.' or p[idx] == '-'):
            idx += 1

        if idx == 0 and (p[0].isalpha()):
            coef_str = ''
            var = p
        elif idx == len(p):
            const += float(p)
            continue
        else:
            coef_str = p[:idx]
            var = p[idx:]

        if coef_str in ('', '+'):
            coef = 1.0
        elif coef_str == '-':
            coef = -1.0
        else:
            coef = float(coef_str)

        vars_dict[var] = vars_dict.get(var, 0.0) + coef

    return vars_dict, const
# alias
parsear_lado = parsearLado

# --- Parsear toda la ecuación ---
def parsearEcuacion(eq):
    """Parsea una ecuación completa y devuelve (vars_dict, constante)."""
    s = eq.replace(' ', '')
    s = s.replace('−', '-').replace('–', '-').replace('—', '-')
    if s.count('=') != 1:
        raise ValueError("La ecuación debe tener un '='.")
    lhs, rhs = s.split('=')
    vars_lhs, const_lhs = parsearLado(lhs)
    vars_rhs, const_rhs = parsearLado(rhs)

    vars_final = {}
    for v, c in vars_lhs.items():
        vars_final[v] = vars_final.get(v, 0.0) + c
    for v, c in vars_rhs.items():
        vars_final[v] = vars_final.get(v, 0.0) - c

    constante_final = const_rhs - const_lhs
    return vars_final, constante_final
# alias
parsear_ecuacion = parsearEcuacion

# --- Leer sistema de ecuaciones ---
def leerSistema():
    """Lee desde stdin un sistema de ecuaciones, retorna (ecuaciones, orden_variables)."""
    ecuaciones = []
    todas_vars = set()
    print("Escribe tus ecuaciones (una por línea). Línea vacía para terminar:")
    while True:
        linea = input("> ").strip()
        if linea == "":
            break
        vars_dict, constante = parsearEcuacion(linea)
        ecuaciones.append((vars_dict, constante))
        variables_en_ec = re.findall(r"[a-zA-Z]\w*", linea)
        todas_vars.update(variables_en_ec)

    if not ecuaciones:
        raise ValueError("No se ingresaron ecuaciones.")

    var_orden = sorted(list(todas_vars))
    return ecuaciones, var_orden
# alias
leer_sistema = leerSistema

# --- Construir matriz aumentada ---
def construirMatriz(ecuaciones, var_orden):
    """Construye la matriz aumentada a partir de las ecuaciones y el orden de variables."""
    n = len(ecuaciones)
    m = len(var_orden)
    matriz = [[0.0 for _ in range(m+1)] for _ in range(n)]
    for i, (vars_dict, const) in enumerate(ecuaciones):
        for j, v in enumerate(var_orden):
            matriz[i][j] = vars_dict.get(v, 0.0)
        matriz[i][m] = const
    return matriz
# alias
construir_matriz = construirMatriz

# --- Imprimir matriz ---
def imprimirMatriz(matriz, var_orden):
    """Imprime la matriz aumentada en formato legible."""
    header = " | ".join(var_orden + ["b"])
    print(header)
    for fila in matriz:
        print(" | ".join(f"{x:7.2f}" for x in fila))
# alias
imprimir_matriz = imprimirMatriz

# --- Método Gauss–Jordan ---
def gaussJordan(matriz, var_orden):
    n = len(matriz)
    m = len(var_orden)
    fila = 0
    pivot_map = {}

    for col in range(m):
        # buscar pivote
        sel = None
        for r in range(fila, n):
            if abs(matriz[r][col]) > EPS:
                sel = r
                break
        if sel is None:
            continue

        # intercambiar filas
        if sel != fila:
            matriz[fila], matriz[sel] = matriz[sel], matriz[fila]

        # normalizar pivote
        pivote = matriz[fila][col]
        for c in range(m+1):
            matriz[fila][c] /= pivote

        # eliminar en otras filas
        for r in range(n):
            if r != fila and abs(matriz[r][col]) > EPS:
                factor = matriz[r][col]
                for c in range(m+1):
                    matriz[r][c] -= factor * matriz[fila][c]

        pivot_map[col] = fila
        fila += 1
        if fila == n:
            break

    # detectar inconsistencia
    sistema_inconsistente = False
    for r in range(n):
        if all(abs(matriz[r][c]) < EPS for c in range(m)) and abs(matriz[r][m]) > EPS:
            sistema_inconsistente = True
            break

    if sistema_inconsistente:
        print("El sistema es INCONSISTENTE (sin solución).")
    elif len(pivot_map) == m:
        sol = [0.0] * m
        for col, r in pivot_map.items():
            sol[col] = matriz[r][m]
        print("Solución única:")
        for i, v in enumerate(var_orden):
            print(f"{v} = {sol[i]:.2f}")
    else:
        libres = [var_orden[c] for c in range(m) if c not in pivot_map]
        print("El sistema tiene INFINITAS soluciones.")
        print("Variables libres:", ", ".join(libres))
# alias
gauss_jordan = gaussJordan


def _matrixSnapshot(m):
    return [[float(x) for x in row] for row in m]
# alias
_matrix_snapshot = _matrixSnapshot


def gaussJordanPasos(matriz):
    """Perform Gauss-Jordan elimination on a copy of `matriz` and
    return a dict with 'steps' (list of matrix snapshots), 'status', and 'solution' if unique.
    `matriz` is a list of rows; last column is the RHS (augmented matrix).
    """
    from copy import deepcopy

    A = deepcopy(matriz)
    n = len(A)
    if n == 0:
        return {'steps': [], 'status': 'empty', 'solution': None}
    m = len(A[0]) - 1

    steps = [ _matrixSnapshot(A) ]

    fila = 0
    pivot_map = {}

    for col in range(m):
        # buscar pivote
        sel = None
        for r in range(fila, n):
            if abs(A[r][col]) > EPS:
                sel = r
                break
        if sel is None:
            continue

        # intercambiar filas
        if sel != fila:
            A[fila], A[sel] = A[sel], A[fila]
            steps.append(_matrixSnapshot(A))

        # normalizar pivote
        pivote = A[fila][col]
        for c in range(m+1):
            A[fila][c] /= pivote
        steps.append(_matrixSnapshot(A))

        # eliminar en otras filas
        for r in range(n):
            if r != fila and abs(A[r][col]) > EPS:
                factor = A[r][col]
                for c in range(m+1):
                    A[r][c] -= factor * A[fila][c]
                steps.append(_matrixSnapshot(A))

        pivot_map[col] = fila
        fila += 1
        if fila == n:
            break

    # detectar inconsistencia
    sistemaInconsistente = False
    for r in range(n):
        if all(abs(A[r][c]) < EPS for c in range(m)) and abs(A[r][m]) > EPS:
            sistemaInconsistente = True
            break

    if sistemaInconsistente:
        return {'steps': steps, 'status': 'inconsistent', 'solution': None}
    elif len(pivot_map) == m:
        sol = [0.0] * m
        for col, r in pivot_map.items():
            sol[col] = A[r][m]
        return {'steps': steps, 'status': 'unique', 'solution': sol}
    else:
        libres = [c for c in range(m) if c not in pivot_map]
        return {'steps': steps, 'status': 'infinite', 'free_vars': libres}
# alias
gauss_jordan_steps = gaussJordanPasos
gaussJordanSteps = gaussJordanPasos


def gaussSteps(matriz):
    """Perform Gaussian elimination (forward elimination) returning steps and then back-substitution result if possible.
    Returns dict with 'steps', 'status', and 'solution' or None.
    """
    from copy import deepcopy

    A = deepcopy(matriz)
    n = len(A)
    if n == 0:
        return {'steps': [], 'status': 'empty', 'solution': None}
    m = len(A[0]) - 1

    steps = [ _matrixSnapshot(A) ]

    # Forward elimination to make upper triangular (Gaussian elimination)
    row = 0
    pivot_cols = []
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
            steps.append(_matrixSnapshot(A))

        # eliminate below
        for r in range(row+1, n):
            if abs(A[r][col]) > EPS:
                factor = A[r][col] / A[row][col]
                for c in range(col, m+1):
                    A[r][c] -= factor * A[row][c]
                steps.append(_matrixSnapshot(A))

        pivot_cols.append(col)
        row += 1
        if row == n:
            break

    # check inconsistency
    for r in range(n):
        if all(abs(A[r][c]) < EPS for c in range(m)) and abs(A[r][m]) > EPS:
            return {'steps': steps, 'status': 'inconsistent', 'solution': None}

    # back substitution if possible (unique solution)
    # simple check: number of pivots == m
    if len(pivot_cols) == m:
        # back substitution
        x = [0.0]*m
        for i in range(len(pivot_cols)-1, -1, -1):
            col = pivot_cols[i]
            r = i
            s = A[r][m]
            for c in range(col+1, m):
                s -= A[r][c]*x[c]
            x[col] = s / A[r][col]
        return {'steps': steps, 'status': 'unique', 'solution': x}
    else:
        return {'steps': steps, 'status': 'incomplete', 'solution': None}
# alias
gauss_steps = gaussSteps


def independenciaVectores(matriz):
    """Determina si las columnas de `matriz` (lista de filas) son linealmente independientes.
    Retorna un dict con {'independent': bool, 'rank': int, 'num_vectors': int}.
    """
    from copy import deepcopy

    A = deepcopy(matriz)
    if not A:
        return {'independent': True, 'rank': 0, 'num_vectors': 0}
    rows = len(A)
    cols = len(A[0])

    # convertir a float
    for i in range(rows):
        for j in range(cols):
            A[i][j] = float(A[i][j])

    rank = 0
    for col in range(cols):
        # buscar pivote en columna col empezando en fila 'rank'
        sel = None
        for r in range(rank, rows):
            if abs(A[r][col]) > EPS:
                sel = r
                break
        if sel is None:
            continue
        # swap
        if sel != rank:
            A[rank], A[sel] = A[sel], A[rank]
        pivote = A[rank][col]
        # eliminar filas por debajo
        for r in range(rank+1, rows):
            if abs(A[r][col]) > EPS:
                factor = A[r][col] / pivote
                for c in range(col, cols):
                    A[r][c] -= factor * A[rank][c]
        rank += 1
        if rank == rows:
            break

    independent = (rank == cols)
    return {'independent': independent, 'rank': rank, 'num_vectors': cols}

# alias por compatibilidad
independencia_vectores = independenciaVectores