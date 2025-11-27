from copy import deepcopy
from typing import List, Dict, Any

EPS = 1e-9
# Umbral para cambiar de método de determinante (Expansion < 4, Gauss >= 4)
UMBRAL_TAMANO_DETERMINANTE = 4

def _snap(M: List[List[float]]) -> List[List[float]]:
    """Limpia la matriz de 'ruido' numérico (convierte 1e-15 a 0.0)"""
    res = []
    for r in M:
        fila = []
        for x in r:
            if abs(x) < EPS:
                fila.append(0.0)
            else:
                fila.append(float(x))
        res.append(fila)
    return res

def _fmt(x: float) -> str:
    """Formatea números para mostrar en los pasos (UI)"""
    if abs(x) < EPS:
        return "0"
    # Si es entero (ej. 5.0), mostrar sin decimales
    if abs(x - round(x)) < EPS:
        return f"{int(round(x))}"
    return f"{x:.4g}"

def gauss_steps(M: List[List[float]]) -> Dict[str, Any]:
    """Calcula la forma escalonada usando eliminación gaussiana"""
    A = deepcopy(M)
    n = len(A)
    if n == 0: return {'steps': [], 'ops': [], 'status': 'empty', 'solution': None}
    m = len(A[0]) - 1
    steps = [_snap(A)]
    ops = ['Matriz Inicial']
    row = 0
    pivcols: List[int] = []
    
    for col in range(m):
        if row >= n: break
        
        # Pivoteo parcial
        sel = None
        for r in range(row, n):
            if abs(A[r][col]) > EPS:
                sel = r; break
        if sel is None: continue
        
        if sel != row:
            A[row], A[sel] = A[sel], A[row]
            steps.append(_snap(A))
            ops.append(f'F{row+1} ↔ F{sel+1}')
            
        for r in range(row+1, n):
            if abs(A[r][col]) > EPS:
                factor = A[r][col] / A[row][col]
                for c in range(col, m+1): A[r][c] -= factor * A[row][c]
                steps.append(_snap(A))
                ops.append(f'F{r+1} ← F{r+1} − ({_fmt(factor)})·F{row+1}')
        
        pivcols.append(col)
        row += 1

    # Verificar consistencia
    for r in range(n):
        if all(abs(A[r][c]) < EPS for c in range(m)) and abs(A[r][m]) > EPS:
            return {'steps': steps, 'ops': ops, 'status': 'inconsistent', 'solution': None}
            
    # Sustitución hacia atrás (Back-substitution)
    if len(pivcols) == m:
        x = [0.0]*m
        try:
             for i in range(len(pivcols)-1, -1, -1):
                 col = pivcols[i]; r = i; s = A[r][m]
                 for c in range(col+1, m): s -= A[r][c] * x[c]
                 if abs(A[r][col]) > EPS:
                      x[col] = s / A[r][col]
                 else:
                      return {'steps': steps, 'ops': ops, 'status': 'incomplete', 'solution': None}
        except IndexError:
             return {'steps': steps, 'ops': ops, 'status': 'error', 'mensaje': 'Error de índice durante retro-sustitución.', 'solution': None}
        return {'steps': steps, 'ops': ops, 'status': 'unique', 'solution': x}
        
    return {'steps': steps, 'ops': ops, 'status': 'incomplete', 'solution': None}

def gauss_jordan_steps(M: List[List[float]]) -> Dict[str, Any]:
    """Calcula la forma escalonada reducida usando Gauss-Jordan"""
    A = deepcopy(M)
    n = len(A)
    if n == 0: return {'steps': [], 'ops': [], 'status': 'empty', 'solution': None}
    m = len(A[0]) - 1
    if m < 0: return {'steps':[], 'ops':[], 'status':'error', 'mensaje':'Matriz sin columna de resultados.', 'solution':None}
    
    steps = [_snap(A)]
    ops = ['Matriz Inicial']
    fila_pivote = 0
    columna_pivote = 0
    pivot_map: Dict[int, int] = {}
    
    while fila_pivote < n and columna_pivote < m:
        indice_max = fila_pivote
        for k in range(fila_pivote + 1, n):
            if abs(A[k][columna_pivote]) > abs(A[indice_max][columna_pivote]):
                indice_max = k
                
        if abs(A[indice_max][columna_pivote]) < EPS:
            columna_pivote += 1
            continue
            
        if indice_max != fila_pivote:
            A[fila_pivote], A[indice_max] = A[indice_max], A[fila_pivote]
            steps.append(_snap(A))
            ops.append(f'F{fila_pivote+1} ↔ F{indice_max+1}')
            
        piv_val = A[fila_pivote][columna_pivote]
        if abs(piv_val - 1.0) > EPS:
            try:
                for j in range(columna_pivote, m + 1):
                    A[fila_pivote][j] /= piv_val
                steps.append(_snap(A))
                ops.append(f'F{fila_pivote+1} ← F{fila_pivote+1} / {_fmt(piv_val)}')
            except ZeroDivisionError:
                 return {'steps': steps, 'ops': ops, 'status': 'error', 'mensaje':'División por cero inesperada.', 'solution': None}
                 
        for i in range(n):
            if i != fila_pivote:
                factor = A[i][columna_pivote]
                if abs(factor) > EPS:
                    for j in range(columna_pivote, m + 1):
                        A[i][j] -= factor * A[fila_pivote][j]
                    steps.append(_snap(A))
                    ops.append(f'F{i+1} ← F{i+1} − ({_fmt(factor)})·F{fila_pivote+1}')
                    
        pivot_map[columna_pivote] = fila_pivote
        fila_pivote += 1
        columna_pivote += 1
        
    # Análisis de solución
    for i in range(fila_pivote, n):
        if abs(A[i][m]) > EPS:
             if all(abs(A[i][j]) < EPS for j in range(m)):
                  return {'steps': steps, 'ops': ops, 'status': 'inconsistent', 'solution': None}
                  
    if len(pivot_map) == m:
        sol = [0.0]*m
        for col, r in pivot_map.items():
             sol[col] = A[r][m]
        return {'steps': steps, 'ops': ops, 'status': 'unique', 'solution': sol}
    else:
        libres = [c for c in range(m) if c not in pivot_map]
        basic_solution = {}
        for col_pivote, fila_pivote_idx in pivot_map.items():
             basic_solution[col_pivote] = A[fila_pivote_idx][m]
        return {'steps': steps, 'ops': ops, 'status': 'infinite', 'solution': None,
                'free_vars': libres, 'basic_solution': basic_solution}

def independenciaVectores(M: List[List[float]]) -> Dict[str, Any]:
    """Determina si un conjunto de vectores es linealmente independiente (usando Rango)"""
    A = deepcopy(M)
    if not A: return {'independent': True, 'rank': 0, 'num_vectors': 0}
    num_filas, num_vectores = len(A), len(A[0])
    rank = 0
    fila_pivote = 0
    
    for col in range(num_vectores):
         if fila_pivote >= num_filas: break
         indice_max = fila_pivote
         for k in range(fila_pivote + 1, num_filas):
             if abs(A[k][col]) > abs(A[indice_max][col]):
                 indice_max = k
         if abs(A[indice_max][col]) < EPS:
             continue
         if indice_max != fila_pivote:
             A[fila_pivote], A[indice_max] = A[indice_max], A[fila_pivote]
             
         piv_val = A[fila_pivote][col]
         if abs(piv_val) > EPS:
             for i in range(fila_pivote + 1, num_filas):
                 if abs(A[i][col]) > EPS:
                     factor = A[i][col] / piv_val
                     for j in range(col, num_vectores):
                         A[i][j] -= factor * A[fila_pivote][j]
         fila_pivote += 1
         rank = fila_pivote
         
    return {'independent': rank == num_vectores, 'rank': rank, 'num_vectors': num_vectores}

def inverse_steps(A: List[List[float]]) -> Dict[str, Any]:
    """Calcula la inversa de una matriz cuadrada mediante Gauss-Jordan"""
    n = len(A)
    if n == 0: return {'steps': [], 'ops': [], 'status': 'singular', 'inverse': None}
    if any(len(f) != n for f in A):
        return {'steps': [], 'ops': [], 'status': 'error', 'mensaje': 'La matriz debe ser cuadrada.'}

    # Crear matriz aumentada [A | I]
    matriz_aumentada = [fila + [1.0 if i == j else 0.0 for j in range(n)] for i, fila in enumerate(A)]
    
    resultado_gj = gauss_jordan_steps(matriz_aumentada)
    steps = resultado_gj.get('steps', [])
    ops = resultado_gj.get('ops', [])

    if resultado_gj['status'] not in ('unique', 'infinite'):
         return {'steps': steps, 'ops': ops, 'status': 'singular', 'inverse': None}

    matriz_final = resultado_gj['steps'][-1] if resultado_gj['steps'] else matriz_aumentada
    
    # Verificar si la parte izquierda es la Identidad
    for i in range(n):
        for j in range(n):
            if abs(matriz_final[i][j] - (1.0 if i == j else 0.0)) > EPS * n: # Tolerancia ajustada al tamaño
                return {'steps': steps, 'ops': ops, 'status': 'singular', 'inverse': None}

    inv = [fila[n:] for fila in matriz_final]
    return {'steps': steps, 'ops': ops, 'status': 'invertible', 'inverse': inv}

def _determinante_expansion_recursivo(sub_matriz: List[List[float]], pasos: List[str], sangria: str = "") -> float:
    """Función interna recursiva para determinante por cofactores"""
    tamano = len(sub_matriz)
    
    if sangria == "" or tamano <= 3:
        pasos.append(f"{sangria}Analizando matriz {tamano}x{tamano}:")
        for fila in sub_matriz:
            pasos.append(f"{sangria}  {[ _fmt(elem) for elem in fila ]}")
    else:
        pasos.append(f"{sangria}Submatriz {tamano}x{tamano}...")

    if tamano == 1:
        det = sub_matriz[0][0]
        pasos.append(f"{sangria}└─> Resultado: {_fmt(det)}\n")
        return det
        
    if tamano == 2:
        a, b = sub_matriz[0][0], sub_matriz[0][1]
        c, d = sub_matriz[1][0], sub_matriz[1][1]
        det = a * d - b * c
        pasos.append(f"{sangria}└─> ({_fmt(a)}·{_fmt(d)}) - ({_fmt(b)}·{_fmt(c)}) = {_fmt(det)}\n")
        return det

    det_total = 0.0
    pasos.append(f"{sangria}Expandiendo por fila 1:")
    
    for j in range(tamano):
        elem = sub_matriz[0][j]
        if abs(elem) < EPS:
            continue

        signo = (-1)**j
        matriz_menor = [fila[:j] + fila[j+1:] for fila in sub_matriz[1:]]
        texto_signo = "+" if signo > 0 else "-"
        
        pasos.append(f"{sangria}  Termino {j+1}: ({texto_signo} {_fmt(elem)}) · det(menor)")
        try:
            det_sub = _determinante_expansion_recursivo(matriz_menor, pasos, sangria + "    ")
            termino = signo * elem * det_sub
            det_total += termino
        except Exception as e:
             raise e

    pasos.append(f"{sangria}└─> Suma total = {_fmt(det_total)}\n")
    return det_total

def determinante_por_gauss(matriz: List[List[float]]) -> Dict[str, Any]:
    """Calcula el determinante triangulando la matriz (Gauss)"""
    pasos = []
    try:
        if not matriz: return {'estado': 'error', 'mensaje': 'Matriz vacía', 'pasos': []}
        n = len(matriz)
        A = deepcopy(matriz)
        
        pasos.append("Método: Eliminación Gaussiana (Triangulación)")
        pasos.append("Matriz original:")
        for fila in A: pasos.append("  " + str([_fmt(val) for val in fila]))
        pasos.append("")

        intercambios = 0
        det_acumulado = 1.0

        for i in range(n):
            # Pivoteo
            pivote_idx = i
            for k in range(i + 1, n):
                if abs(A[k][i]) > abs(A[pivote_idx][i]):
                    pivote_idx = k

            if pivote_idx != i:
                A[i], A[pivote_idx] = A[pivote_idx], A[i]
                intercambios += 1
                pasos.append(f"Intercambio: F{i+1} ↔ F{pivote_idx+1} (cambia signo)")
                
            pivote_val = A[i][i]
            if abs(pivote_val) < EPS:
                pasos.append(f"Pivote cero en ({i+1},{i+1}) -> Determinante es 0")
                return {'estado': 'exito', 'determinante': 0.0, 'pasos': pasos}

            for k in range(i + 1, n):
                if abs(A[k][i]) > EPS:
                    factor = A[k][i] / pivote_val
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
                    pasos.append(f"F{k+1} ← F{k+1} - ({_fmt(factor)})·F{i+1}")

        pasos.append("Matriz triangular obtenida. Multiplicando diagonal...")
        prod = 1.0
        diag_str = []
        for i in range(n):
            prod *= A[i][i]
            diag_str.append(_fmt(A[i][i]))

        pasos.append(f"Producto diagonal = {' * '.join(diag_str)} = {_fmt(prod)}")
        
        if intercambios % 2 != 0:
            prod *= -1
            pasos.append(f"Ajuste por {intercambios} intercambios (impar) -> Resultado: {_fmt(prod)}")
        else:
            pasos.append(f"Intercambios pares ({intercambios}) -> Signo se mantiene.")

        return {'estado': 'exito', 'determinante': prod, 'pasos': pasos}

    except Exception as error:
        return {'estado': 'error', 'mensaje': str(error), 'pasos': pasos}

def pasos_determinante(matriz: List[List[float]]) -> Dict[str, Any]:
    """Fachada que elige el mejor método de determinante según tamaño"""
    try:
        if not matriz: return {'estado': 'error', 'mensaje': 'Matriz vacía'}
        tamano = len(matriz)
        if any(len(fila) != tamano for fila in matriz):
            return {'estado': 'error', 'mensaje': 'La matriz debe ser cuadrada'}

        if tamano >= UMBRAL_TAMANO_DETERMINANTE:
            return determinante_por_gauss(matriz)
        else:
            pasos = ["Método: Expansión por Cofactores"]
            det = _determinante_expansion_recursivo(deepcopy(matriz), pasos)
            return {'estado': 'exito', 'determinante': det, 'pasos': pasos}
    except Exception as e:
        return {'estado': 'error', 'mensaje': str(e), 'pasos': []}

def resolver_por_cramer(matriz_aumentada: List[List[float]]) -> Dict[str, Any]:
    """Resuelve sistema Ax=b por Regla de Cramer"""
    pasos = []
    def _log_mat(m, titulo):
        pasos.append(titulo)
        for f in m: pasos.append("  " + "  ".join(_fmt(x) for x in f))
        pasos.append("")

    try:
        if not matriz_aumentada or not matriz_aumentada[0]:
            return {'estado': 'error', 'mensaje': 'Matriz vacía', 'pasos': pasos}

        n = len(matriz_aumentada)
        cols = len(matriz_aumentada[0])
        num_vars = cols - 1

        if n != num_vars:
            return {'estado': 'error', 'mensaje': 'La matriz de coeficientes debe ser cuadrada.', 'pasos': pasos}

        matriz_A = [f[:num_vars] for f in matriz_aumentada]
        vector_B = [f[num_vars] for f in matriz_aumentada]

        _log_mat(matriz_A, "Matriz Coeficientes (A):")
        
        # 1. Determinante del Sistema
        pasos.append("Calculando det(A)...")
        res_A = pasos_determinante(matriz_A)
        pasos.extend(res_A.get('pasos', []))
        
        det_A = res_A.get('determinante', 0.0)
        pasos.append(f"-> det(A) = {_fmt(det_A)}\n")

        if abs(det_A) < EPS:
            return {'estado': 'sin_solucion_unica', 'mensaje': 'El determinante es 0. Cramer no aplica (infinitas soluciones o sin solución).', 'pasos': pasos}

        solucion = []
        for j in range(num_vars):
            # Reemplazar columna j con vector B
            matriz_Aj = deepcopy(matriz_A)
            for i in range(n):
                matriz_Aj[i][j] = vector_B[i]

            pasos.append(f"--- Calculando det(A{j+1}) ---")
            # Optimización: Solo mostrar pasos de determinantes si es pequeña, para no saturar
            res_Aj = pasos_determinante(matriz_Aj)
            if n <= 3: 
                pasos.extend(res_Aj.get('pasos', []))
            
            det_Aj = res_Aj.get('determinante', 0.0)
            val_x = det_Aj / det_A
            solucion.append(val_x)
            
            pasos.append(f"det(A{j+1}) = {_fmt(det_Aj)}")
            pasos.append(f"x{j+1} = {_fmt(det_Aj)} / {_fmt(det_A)} = {_fmt(val_x)}\n")

        return {'estado': 'exito', 'solucion': solucion, 'pasos': pasos}

    except Exception as error:
        return {'estado': 'error', 'mensaje': str(error), 'pasos': pasos}