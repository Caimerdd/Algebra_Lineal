import re

# Tolerancia para comparar con cero (evita problemas de punto flotante)
EPS = 1e-12

# -------------------------
# Utilidades y parseo
# -------------------------

def normalizar_guiones(s):
    """Reemplaza guiones raros por '-' y deja la cadena lista para parsear."""
    return s.replace('−', '-').replace('–', '-').replace('—', '-')

def parsear_lado(expr):
    """
    Convierte un lado de la ecuación en:
      - vars_dict: {variable: coeficiente}
      - const: suma de términos constantes del lado
    Ejemplos de términos aceptados: 'x', '-2y', '3.5', '+z2'
    """
    s = normalizar_guiones(expr).replace(' ', '')
    if s == '':
        raise ValueError("Lado vacío")
    # Asegurar que cada término tenga signo al inicio
    if s[0] not in '+-':
        s = '+' + s
    # Convertir '-' en '+-' para luego split por '+'
    s = s.replace('-', '+-')
    partes = [t for t in s.split('+') if t != '']

    vars_dict = {}
    const = 0.0

    for p in partes:
        # idx se posiciona justo donde termina la parte numérica (coef) y empieza la variable
        idx = 0
        while idx < len(p) and (p[idx].isdigit() or p[idx] == '.' or p[idx] == '-'):
            idx += 1

        # Casos:
        # 1) idx == 0 y p[0].isalpha() -> variable sola, coef implícito 1
        # 2) idx == len(p) -> es una constante (sin variable)
        # 3) en otro caso -> coef_str = p[:idx], var = p[idx:]
        if idx == 0 and p[0].isalpha():
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

def parsear_ecuacion(eq):
    """Parsea ecuación 'lhs = rhs' retornando (vars_dict, constante_final)."""
    s = eq.replace(' ', '')
    s = normalizar_guiones(s)
    if s.count('=') != 1:
        raise ValueError("La ecuación debe tener un '='.")
    lhs, rhs = s.split('=')
    vars_lhs, const_lhs = parsear_lado(lhs)
    vars_rhs, const_rhs = parsear_lado(rhs)

    # Mover todas las variables al LHS: coef_final = coef_lhs - coef_rhs
    vars_final = {}
    for v, c in vars_lhs.items():
        vars_final[v] = vars_final.get(v, 0.0) + c
    for v, c in vars_rhs.items():
        vars_final[v] = vars_final.get(v, 0.0) - c

    # Constante final = rhs_const - lhs_const  (porque movimos constantes al RHS)
    constante_final = const_rhs - const_lhs
    return vars_final, constante_final

# -------------------------
# Entrada del sistema
# -------------------------

def leer_sistema():
    """
    Lee ecuaciones línea por línea desde la consola hasta una línea vacía.
    Devuelve:
      - ecuaciones: lista de (vars_dict, constante)
      - var_orden: lista ordenada de todas las variables encontradas
    """
    ecuaciones = []
    todas_vars = set()
    print("Escribe tus ecuaciones (una por línea). Línea vacía para terminar:")
    while True:
        linea = input("> ").strip()
        if linea == "":
            break
        vars_dict, constante = parsear_ecuacion(linea)
        ecuaciones.append((vars_dict, constante))
        # Detectar variables en la línea (para construir columnas)
        variables_en_ec = re.findall(r"[a-zA-Z]\w*", linea)
        todas_vars.update(variables_en_ec)

    if not ecuaciones:
        raise ValueError("No se ingresaron ecuaciones.")

    var_orden = sorted(list(todas_vars))
    return ecuaciones, var_orden

# -------------------------
# Construcción e impresión de la matriz
# -------------------------

def construir_matriz(ecuaciones, var_orden):
    """
    Construye la matriz aumentada como lista de filas (listas de floats).
    Cada fila tiene len(var_orden) coeficientes + 1 constante al final.
    """
    n = len(ecuaciones)
    m = len(var_orden)
    matriz = [[0.0 for _ in range(m + 1)] for _ in range(n)]
    for i, (vars_dict, const) in enumerate(ecuaciones):
        for j, v in enumerate(var_orden):
            matriz[i][j] = vars_dict.get(v, 0.0)
        matriz[i][m] = const
    return matriz

def fmt_number(x):
    """Formatea número para imprimir: elimina ceros innecesarios."""
    if abs(x) < EPS:
        return "0"
    # Si es casi entero, mostrar entero
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    s = f"{x:.6f}".rstrip('0').rstrip('.')
    return s

def imprimir_matriz(matriz, var_orden):
    """
    Imprime la matriz alineada por columnas.
    Devuelve la cadena para poder mostrarla también en logs si se desea.
    """
    m = len(var_orden)
    # calcular anchos por columna
    anchos = [len(v) for v in var_orden] + [1]  # última para 'b'
    filas_fmt = []
    for fila in matriz:
        for i, val in enumerate(fila):
            anchos[i] = max(anchos[i], len(fmt_number(val)))
    # crear encabezado
    header_parts = []
    for i, v in enumerate(var_orden):
        header_parts.append(v.rjust(anchos[i]))
    header_parts.append("b".rjust(anchos[-1]))
    header = "  ".join(header_parts)
    filas_fmt.append(header)
    # filas
    for fila in matriz:
        partes = []
        for i in range(len(fila)):
            partes.append(fmt_number(fila[i]).rjust(anchos[i]))
        filas_fmt.append("  ".join(partes))
    salida = "\n".join(filas_fmt)
    print(salida)
    return salida

# -------------------------
# Gauss-Jordan con pasos
# -------------------------

def gauss_jordan_con_pasos(matriz, var_orden):
    """
    Aplica Gauss-Jordan y va imprimiendo cada operación:
      - intercambio de filas
      - división de fila (normalizar pivote)
      - suma/resta de filas (eliminación)
    Además detecta: pivotes, variables libres, inconsistencia, solución única o infinitas.
    """
    n = len(matriz)
    m = len(var_orden)
    fila = 0
    pivot_map = {}  # col -> fila donde quedó el pivote

    print("\n--- Inicio Gauss-Jordan (paso a paso) ---\n")
    print("Matriz inicial:")
    imprimir_matriz(matriz, var_orden)
    print()

    for col in range(m):
        # 1) buscar pivote en la columna col a partir de la fila 'fila'
        sel = None
        for r in range(fila, n):
            if abs(matriz[r][col]) > EPS:
                sel = r
                break
        if sel is None:
            # No hay pivote en esta columna -> variable libre
            print(f"No hay pivote en columna {col} (variable '{var_orden[col]}') -> variable libre.\n")
            continue

        # 2) si sel != fila, intercambiar filas
        if sel != fila:
            print(f"Operación: F{fila+1} <-> F{sel+1}  (intercambio para traer pivote)")
            matriz[fila], matriz[sel] = matriz[sel], matriz[fila]
            imprimir_matriz(matriz, var_orden)
            print()

        # 3) normalizar pivote (hacer que el pivote valga 1)
        piv_val = matriz[fila][col]
        print(f"Pivote encontrado en ({fila+1},{col+1}) = {fmt_number(piv_val)}")
        if abs(piv_val - 1.0) > EPS:
            print(f"Operación: F{fila+1} -> F{fila+1} / ({fmt_number(piv_val)})  (normalizar pivote)")
            for c in range(m + 1):
                matriz[fila][c] /= piv_val
            imprimir_matriz(matriz, var_orden)
            print()
        else:
            print(f"El pivote ya es 1, no se divide.\n")

        # 4) eliminar la columna del pivote en todas las otras filas
        for r in range(n):
            if r == fila:
                continue
            factor = matriz[r][col]
            if abs(factor) > EPS:
                # Notación: F_r -> F_r - factor * F_fila
                if factor > 0:
                    print(f"Operación: F{r+1} -> F{r+1} - ({fmt_number(factor)})*F{fila+1}")
                else:
                    print(f"Operación: F{r+1} -> F{r+1} + ({fmt_number(abs(factor))})*F{fila+1}")
                for c in range(m + 1):
                    matriz[r][c] -= factor * matriz[fila][c]
                imprimir_matriz(matriz, var_orden)
                print()

        # 5) registrar pivote y avanzar fila
        pivot_map[col] = fila
        fila += 1
        if fila == n:
            print("Se alcanzó el número máximo de filas procesadas. Fin del paso por columnas.\n")
            break

    # -------------------------
    # Determinar tipo de solución
    # -------------------------
    # 1) verificar inconsistencia: fila con todos coef cero y constante != 0
    sistema_inconsistente = False
    for r in range(n):
        all_zero_vars = all(abs(matriz[r][c]) < EPS for c in range(m))
        const_nonzero = abs(matriz[r][m]) > EPS
        if all_zero_vars and const_nonzero:
            sistema_inconsistente = True
            break

    if sistema_inconsistente:
        print("Resultado: El sistema es INCONSISTENTE (no tiene solución).")
        return

    # 2) verificar si hay pivote por cada variable -> solución única
    if len(pivot_map) == m:
        # construir solución: cada variable corresponde a la constante en la fila del pivote
        sol = [0.0] * m
        for col, r in pivot_map.items():
            sol[col] = matriz[r][m]
        print("Resultado: Solución única encontrada:")
        for i, v in enumerate(var_orden):
            print(f"  {v} = {fmt_number(sol[i])}")
        return

    # 3) si no es inconsistente y faltan pivotes -> infinitas soluciones
    libres = [col for col in range(m) if col not in pivot_map]
    print("Resultado: El sistema tiene INFINITAS soluciones.")
    print("Variables libres:", ", ".join(var_orden[c] for c in libres))

    # Mostrar solución en forma paramétrica (opcionalmente)
    # Parametrizamos cada variable libre con t1, t2, ...
    param_map = {col: f"t{idx+1}" for idx, col in enumerate(libres)}
    print("\nForma paramétrica (variables dependientes en función de parámetros):")
    # Para cada variable (por columna) damos expresión
    for col in range(m):
        varname = var_orden[col]
        if col in param_map:
            print(f"  {varname} = {param_map[col]}  (variable libre)")
        else:
            # variable dependiente: usar fila del pivote para expresarla
            r = pivot_map[col]
            const_term = matriz[r][m]
            expr = fmt_number(const_term)
            # restar términos correspondientes a variables libres
            for fc in libres:
                coef = matriz[r][fc]  # coeficiente multiplicando la variable libre
                if abs(coef) > EPS:
                    sign = "-" if coef > 0 else "+"
                    coef_str = fmt_number(abs(coef))
                    # si coef == 1 omitimos 1*
                    if coef_str == "1":
                        term = f"{sign} {param_map[fc]}"
                    else:
                        term = f"{sign} {coef_str}*{param_map[fc]}"
                    expr += " " + term
            print(f"  {varname} = {expr}")

# -------------------------
# Programa principal
# -------------------------

def main():
    try:
        ecuaciones, var_orden = leer_sistema()
    except Exception as e:
        print("Error al leer el sistema:", e)
        return

    matriz = construir_matriz(ecuaciones, var_orden)
    print("\nMatriz aumentada inicial:")
    imprimir_matriz(matriz, var_orden)
    gauss_jordan_con_pasos(matriz, var_orden)

if __name__ == "__main__":
    main()
