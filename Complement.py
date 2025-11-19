from copy import deepcopy
from typing import List, Dict

EPS = 1e-9

# umbral para cambiar de metodo de determinante
UMBRAL_TAMANO_DETERMINANTE = 4

def _snap(M: List[List[float]]) -> List[List[float]]:
    return [[float(x) for x in r] for r in M]

def _fmt(x: float) -> str:
    return f"{x:.4g}"

def gauss_steps(M: List[List[float]]) -> Dict:
    """calcula la forma escalonada usando eliminacion gaussiana"""
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
                if abs(A[row][col]) > EPS:
                    f = A[r][col] / A[row][col]
                    for c in range(col, m+1): A[r][c] -= f * A[row][c]
                    steps.append(_snap(A)); ops.append(f'F{r+1} ← F{r+1} − ({_fmt(f)})·F{row+1}')
                else:
                    pass # pivote practicamente cero no operar
        pivcols.append(col)
        row += 1
        if row == n: break
    for r in range(n):
        if all(abs(A[r][c]) < EPS for c in range(m)) and abs(A[r][m]) > EPS:
            return {'steps': steps, 'ops': ops, 'status': 'inconsistent', 'solution': None}
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
             return {'steps': steps, 'ops': ops, 'status': 'error', 'mensaje': 'Error de indice durante retro-sustitucion.', 'solution': None}
        return {'steps': steps, 'ops': ops, 'status': 'unique', 'solution': x}
    return {'steps': steps, 'ops': ops, 'status': 'incomplete', 'solution': None}

def gauss_jordan_steps(M: List[List[float]]) -> Dict:
    """calcula la forma escalonada reducida usando gauss-jordan"""
    A = deepcopy(M)
    n = len(A)
    if n == 0: return {'steps': [], 'ops': [], 'status': 'empty', 'solution': None}
    m = len(A[0]) - 1
    if m < 0: return {'steps':[], 'ops':[], 'status':'error', 'mensaje':'Matriz sin columna de resultados.', 'solution':None}
    steps = [_snap(A)]
    ops = ['Inicial']
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
            steps.append(_snap(A)); ops.append(f'F{fila_pivote+1} ↔ F{indice_max+1}')
        piv_val = A[fila_pivote][columna_pivote]
        if abs(piv_val - 1.0) > EPS:
            try:
                for j in range(columna_pivote, m + 1):
                    A[fila_pivote][j] /= piv_val
                steps.append(_snap(A)); ops.append(f'F{fila_pivote+1} ← F{fila_pivote+1} / {_fmt(piv_val)}')
            except ZeroDivisionError:
                 return {'steps': steps, 'ops': ops, 'status': 'error', 'mensaje':'Division por cero inesperada.', 'solution': None}
        for i in range(n):
            if i != fila_pivote:
                factor = A[i][columna_pivote]
                if abs(factor) > EPS:
                    for j in range(columna_pivote, m + 1):
                        A[i][j] -= factor * A[fila_pivote][j]
                    steps.append(_snap(A)); ops.append(f'F{i+1} ← F{i+1} − ({_fmt(factor)})·F{fila_pivote+1}')
        pivot_map[columna_pivote] = fila_pivote
        fila_pivote += 1
        columna_pivote += 1
    for i in range(fila_pivote, n):
        if abs(A[i][m]) > EPS:
             if all(abs(A[i][j]) < EPS for j in range(m)):
                  return {'steps': steps, 'ops': ops, 'status': 'inconsistent', 'solution': None}
    if len(pivot_map) == m:
        sol = [0.0]*m
        for col, r in pivot_map.items():
             if r < n:
                 sol[col] = A[r][m]
             else:
                 return {'steps': steps, 'ops': ops, 'status': 'error', 'mensaje': f'Error logico: fila de pivote {r} fuera de rango.', 'solution': None}
        return {'steps': steps, 'ops': ops, 'status': 'unique', 'solution': sol}
    else:
        libres = [c for c in range(m) if c not in pivot_map]
        basic_solution = {}
        for col_pivote, fila_pivote_idx in pivot_map.items():
             if fila_pivote_idx < n:
                 basic_solution[col_pivote] = A[fila_pivote_idx][m]
             else:
                  return {'steps': steps, 'ops': ops, 'status': 'error', 'mensaje': f'Error logico: fila de pivote {fila_pivote_idx} fuera de rango.', 'solution': None}
        return {'steps': steps, 'ops': ops, 'status': 'infinite', 'solution': None,
                'free_vars': libres, 'basic_solution': basic_solution}

def independenciaVectores(M: List[List[float]]) -> Dict:
    """determina si un conjunto de vectores es linealmente independiente"""
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
                 # Solo calcular factor si el elemento no es ya cero
                 if abs(A[i][col]) > EPS:
                     factor = A[i][col] / piv_val
                     for j in range(col, num_vectores):
                         A[i][j] -= factor * A[fila_pivote][j]
         fila_pivote += 1
         rank = fila_pivote
    return {'independent': rank == num_vectores, 'rank': rank, 'num_vectors': num_vectores}

def inverse_steps(A: List[List[float]]) -> Dict:
    """calcula la inversa de una matriz cuadrada"""
    n = len(A)
    if n == 0: return {'steps': [], 'ops': [], 'status': 'singular', 'inverse': None}
    if any(len(f) != n for f in A):
        return {'steps': [], 'ops': [], 'status': 'error', 'mensaje': 'la matriz debe ser cuadrada para calcular la inversa'}

    matriz_aumentada = [fila + [1.0 if i == j else 0.0 for j in range(n)] for i, fila in enumerate(A)]
    resultado_gj = gauss_jordan_steps(matriz_aumentada)
    steps = resultado_gj.get('steps', [])
    ops = resultado_gj.get('ops', [])

    if resultado_gj['status'] not in ('unique', 'infinite'):
         return {'steps': steps, 'ops': ops, 'status': 'singular', 'inverse': None}

    matriz_final = resultado_gj['steps'][-1] if resultado_gj['steps'] else matriz_aumentada
    for i in range(n):
        for j in range(n):
            if abs(matriz_final[i][j] - (1.0 if i == j else 0.0)) > EPS * n:
                return {'steps': steps, 'ops': ops, 'status': 'singular', 'inverse': None}

    inv = [fila[n:] for fila in matriz_final]
    return {'steps': steps, 'ops': ops, 'status': 'invertible', 'inverse': inv}

def _determinante_expansion_recursivo(sub_matriz: List[List[float]], pasos: List[str], sangria: str = "") -> float:
    """funcion interna recursiva para determinante por expansion"""
    tamano = len(sub_matriz)
    if not sub_matriz or any(len(fila) != tamano for fila in sub_matriz):
        raise ValueError("la submatriz debe ser cuadrada y no vacia")

    # Mostrar matriz actual solo si es relevante
    if sangria == "" or tamano <= 3:
        pasos.append(f"{sangria}calculando det de matriz {tamano}x{tamano}:")
        for fila in sub_matriz:
            pasos.append(f"{sangria}  {[ _fmt(elem) for elem in fila ]}")
    else:
        pasos.append(f"{sangria}calculando det de submatriz {tamano}x{tamano}...")

    if tamano == 1:
        determinante = sub_matriz[0][0]
        pasos.append(f"{sangria}└─> resultado (caso base 1x1): {_fmt(determinante)}\n")
        return determinante
    if tamano == 2:
        a, b = sub_matriz[0][0], sub_matriz[0][1]
        c, d = sub_matriz[1][0], sub_matriz[1][1]
        determinante = a * d - b * c
        pasos.append(f"{sangria}└─> ({_fmt(a)}*{_fmt(d)}) - ({_fmt(b)}*{_fmt(c)}) = {_fmt(determinante)}\n")
        return determinante

    determinante_total = 0.0
    pasos.append(f"{sangria}expandiendo por la primera fila:")
    for j in range(tamano):
        elemento = sub_matriz[0][j]
        # Saltar calculo si el elemento es cero (termino sera cero)
        if abs(elemento) < EPS:
            pasos.append(f"{sangria}  termino {j+1}: elemento es {_fmt(elemento)}, el termino es 0")
            continue

        signo = (-1)**j
        matriz_menor = [fila[:j] + fila[j+1:] for fila in sub_matriz[1:]]
        texto_signo = "+" if signo > 0 else "-"
        pasos.append(f"{sangria}  termino {j+1}: signo(-1)^(0+{j}) * (elemento) * det(submatriz)")
        pasos.append(f"{sangria}  = ({texto_signo} {_fmt(elemento)}) * det(submatriz)")
        try:
            determinante_submatriz = _determinante_expansion_recursivo(matriz_menor, pasos, sangria + "    ")
            termino = signo * elemento * determinante_submatriz
            determinante_total += termino
            pasos.append(f"{sangria}  └─> valor del termino: {texto_signo} {_fmt(elemento)} * {_fmt(determinante_submatriz)} = {_fmt(termino)}")
        except Exception as e:
             pasos.append(f"{sangria}  └─> error al calcular det(submatriz): {e}")
             raise e # Propagar el error hacia arriba

    pasos.append(f"{sangria}└─> suma total de terminos = {_fmt(determinante_total)}\n")
    return determinante_total

def determinante_por_gauss(matriz: List[List[float]]) -> Dict:
    """calcula el determinante usando eliminacion gaussiana y mostrando pasos"""
    pasos = []
    try:
        if not matriz:
            return {'estado': 'error', 'mensaje': 'la matriz esta vacia', 'pasos': pasos}
        n = len(matriz)
        if any(len(fila) != n for fila in matriz):
            return {'estado': 'error', 'mensaje': 'la matriz debe ser cuadrada', 'pasos': pasos}

        A = deepcopy(matriz)
        pasos.append("metodo: eliminacion gaussiana")
        pasos.append("matriz original:")
        for fila in A: pasos.append("  " + str([_fmt(val) for val in fila]))
        pasos.append("")

        num_intercambios = 0
        determinante_final = 1.0 # Empezar con 1 para el producto

        for i in range(n):
            # buscar pivote (el mayor en valor absoluto en la columna actual)
            pivote_idx = i
            for k in range(i + 1, n):
                if abs(A[k][i]) > abs(A[pivote_idx][i]):
                    pivote_idx = k

            # intercambiar filas si es necesario
            if pivote_idx != i:
                A[i], A[pivote_idx] = A[pivote_idx], A[i]
                num_intercambios += 1
                pasos.append(f"intercambio: f{i+1} <-> f{pivote_idx+1} (cambia signo det)")
                for fila in A: pasos.append("  " + str([_fmt(val) for val in fila]))
                pasos.append("")

            # si el pivote es (casi) cero, determinante es (casi) cero
            pivote_val = A[i][i]
            if abs(pivote_val) < EPS:
                pasos.append(f"pivote en ({i+1},{i+1}) es {_fmt(pivote_val)} (cero) -> determinante = 0")
                return {'estado': 'exito', 'determinante': 0.0, 'pasos': pasos}

            # eliminar elementos debajo del pivote
            for k in range(i + 1, n):
                # Solo operar si el elemento no es ya (casi) cero
                if abs(A[k][i]) > EPS:
                    factor = A[k][i] / pivote_val
                    # Optimización: No mostrar la operación si el factor es casi cero
                    # (puede pasar por errores de precision)
                    if abs(factor) > EPS:
                        for j in range(i, n): # Empezar desde la columna i
                            A[k][j] -= factor * A[i][j]
                        pasos.append(f"operacion: f{k+1} <- f{k+1} - ({_fmt(factor)})*f{i+1}")
                        for fila in A: pasos.append("  " + str([_fmt(val) for val in fila]))
                        pasos.append("")

        # La matriz A ahora es triangular superior
        pasos.append("matriz triangular superior obtenida:")
        for fila in A: pasos.append("  " + str([_fmt(val) for val in fila]))
        pasos.append("")

        # Calcular determinante como producto de la diagonal
        diag_str = []
        for i in range(n):
            determinante_final *= A[i][i]
            diag_str.append(_fmt(A[i][i]))

        pasos.append("producto de la diagonal = " + " * ".join(diag_str) + f" = {_fmt(determinante_final)}")

        # Ajustar signo por intercambios
        if num_intercambios > 0:
            pasos.append(f"numero de intercambios de filas = {num_intercambios}")
            if num_intercambios % 2 != 0:
                determinante_final *= -1
                pasos.append(f"como es impar, el signo del determinante cambia -> {_fmt(determinante_final)}")
            else:
                 pasos.append(f"como es par, el signo del determinante no cambia -> {_fmt(determinante_final)}")
        else:
             pasos.append("no hubo intercambios de filas")

        return {'estado': 'exito', 'determinante': determinante_final, 'pasos': pasos}

    except Exception as error:
        return {'estado': 'error', 'mensaje': str(error), 'pasos': pasos}


def pasos_determinante(matriz: List[List[float]]) -> Dict:
    """calcula el determinante eligiendo el metodo segun el tamaño"""
    try:
        if not matriz:
            return {'estado': 'error', 'mensaje': 'la matriz esta vacia'}
        tamano = len(matriz)
        if any(len(fila) != tamano for fila in matriz):
            return {'estado': 'error', 'mensaje': 'la matriz debe ser cuadrada'}

        # elegir metodo segun tamaño
        if tamano >= UMBRAL_TAMANO_DETERMINANTE:
            # Usar Gauss para matrices grandes
            resultado = determinante_por_gauss(matriz)
        else:
            # Usar Expansion para matrices pequeñas
            pasos_expansion = ["metodo: expansion por cofactores"]
            determinante_final = _determinante_expansion_recursivo(deepcopy(matriz), pasos_expansion)
            resultado = {'estado': 'exito', 'determinante': determinante_final, 'pasos': pasos_expansion}

        return resultado

    except Exception as error:
        # Captura errores de validacion inicial o propagados de las funciones internas
        return {'estado': 'error', 'mensaje': str(error), 'pasos': []}


def resolver_por_cramer(matriz_aumentada: List[List[float]]) -> Dict:
    """resuelve un sistema ax=b usando la regla de cramer"""
    pasos_generales = []
    # Funcion interna para formatear y añadir matriz a los pasos
    def _anadir_matriz_pasos(mat, titulo):
        pasos_generales.append(titulo)
        for fila in mat:
            pasos_generales.append("  " + "  ".join(_fmt(val) for val in fila))
        pasos_generales.append("") # Linea en blanco

    try:
        if not matriz_aumentada or not matriz_aumentada[0]:
            return {'estado': 'error', 'mensaje': 'la matriz aumentada esta vacia', 'pasos': pasos_generales}

        num_filas = len(matriz_aumentada)
        num_cols_total = len(matriz_aumentada[0])
        num_vars = num_cols_total - 1

        if num_filas != num_vars:
            return {'estado': 'error', 'mensaje': 'la matriz de coeficientes a debe ser cuadrada', 'pasos': pasos_generales}
        if num_vars <= 0:
            return {'estado': 'error', 'mensaje': 'el sistema no tiene variables', 'pasos': pasos_generales}

        matriz_a = [fila[:num_vars] for fila in matriz_aumentada]
        vector_b = [fila[num_vars] for fila in matriz_aumentada]

        _anadir_matriz_pasos(matriz_a, "matriz de coeficientes (a):")
        pasos_generales.append("vector de resultados (b):")
        pasos_generales.append("  " + str([_fmt(val) for val in vector_b]) + "\n")

        pasos_generales.append("calculando el determinante del sistema (d = det(a)):")
        # Usar la funcion principal que elige el metodo
        resultado_det_a = pasos_determinante(matriz_a)
        if resultado_det_a.get('pasos'):
            # Añadir los pasos del determinante principal
            for paso in resultado_det_a['pasos']:
                if isinstance(paso, str):
                    pasos_generales.append(paso)
                else:
                    pasos_generales.append(str(paso))

        if resultado_det_a['estado'] == 'error':
            error_msg = resultado_det_a.get('mensaje', 'error desconocido al calcular d')
            pasos_generales.append(f"error al calcular d: {error_msg}")
            return {'estado': 'error', 'mensaje': f"error al calcular d: {error_msg}", 'pasos': pasos_generales}

        determinante_d = resultado_det_a['determinante']
        pasos_generales.append(f"determinante del sistema d = {_fmt(determinante_d)}\n")

        if abs(determinante_d) < EPS:
            return {'estado': 'sin_solucion_unica', 'mensaje': 'el determinante del sistema es 0 la regla de cramer no aplica', 'pasos': pasos_generales}

        solucion = []
        for j in range(num_vars):
            matriz_aj = deepcopy(matriz_a)
            for i in range(num_filas):
                matriz_aj[i][j] = vector_b[i]

            _anadir_matriz_pasos(matriz_aj, f"matriz para d{j+1} (reemplazando columna {j+1} con b):")
            pasos_generales.append(f"calculando determinante d{j+1} = det(a{j+1}):")
            # Usar la funcion principal que elige el metodo
            resultado_det_aj = pasos_determinante(matriz_aj)
            if resultado_det_aj.get('pasos'):
                # Añadir los pasos del determinante de cada matriz
                for paso in resultado_det_aj['pasos']:
                    if isinstance(paso, str):
                        pasos_generales.append(paso)
                    else:
                        pasos_generales.append(str(paso))

            if resultado_det_aj['estado'] == 'error':
                error_msg_j = resultado_det_aj.get('mensaje', f'error desconocido al calcular d{j+1}')
                pasos_generales.append(f"error al calcular d{j+1}: {error_msg_j}")
                return {'estado': 'error', 'mensaje': f"error al calcular d{j+1}: {error_msg_j}", 'pasos': pasos_generales}

            determinante_dj = resultado_det_aj['determinante']
            pasos_generales.append(f"determinante d{j+1} = {_fmt(determinante_dj)}\n")

            valor_xj = determinante_dj / determinante_d
            solucion.append(valor_xj)
            pasos_generales.append(f"calculando x{j+1} = d{j+1} / d = {_fmt(determinante_dj)} / {_fmt(determinante_d)} = {_fmt(valor_xj)}\n")

        return {'estado': 'exito', 'solucion': solucion, 'pasos': pasos_generales}

    except Exception as error:
        return {'estado': 'error', 'mensaje': str(error), 'pasos': pasos_generales}