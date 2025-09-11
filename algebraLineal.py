import re
import time

EPS = 1e-12
DELAY = 0.7  # tiempo entre pasos

def normalizar_guiones(s):
    return s.replace('−', '-').replace('–', '-').replace('—', '-').replace(' ', '')

def parsear_lado(expr):
    s = normalizar_guiones(expr)
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

def parsear_ecuacion(eq):
    s = eq.replace(' ', '')
    s = s.replace('−', '-').replace('–', '-').replace('—', '-')
    if s.count('=') != 1:
        raise ValueError("La ecuación debe tener un '='.")
    lhs, rhs = s.split('=')
    vars_lhs, const_lhs = parsear_lado(lhs)
    vars_rhs, const_rhs = parsear_lado(rhs)

    vars_final = {}
    for v, c in vars_lhs.items():
        vars_final[v] = vars_final.get(v, 0.0) + c
    for v, c in vars_rhs.items():
        vars_final[v] = vars_final.get(v, 0.0) - c

    constante_final = const_rhs - const_lhs
    return vars_final, constante_final

def leer_sistema():
    """
    Lee ecuaciones línea por línea y mantiene el orden
    en que aparecen las variables.
    """
    ecuaciones = []
    var_orden = []
    seen = set()

    print("Escribe tus ecuaciones (una por línea). Línea vacía para terminar:")
    while True:
        linea = input("> ").strip()
        if linea == "":
            break
        vars_dict, constante = parsear_ecuacion(linea)
        ecuaciones.append((vars_dict, constante))

        for m in re.finditer(r"[a-zA-Z]\w*", linea):
            v = m.group(0)
            if v not in seen:
                seen.add(v)
                var_orden.append(v)

    if not ecuaciones:
        raise ValueError("No se ingresaron ecuaciones.")

    return ecuaciones, var_orden

def construir_matriz(ecuaciones, var_orden):
    matriz = []
    for vars_dict, constante in ecuaciones:
        fila = []
        for v in var_orden:
            fila.append(float(vars_dict.get(v, 0.0)))
        fila.append(float(constante))
        matriz.append(fila)
    return matriz

def fmt_number(x):
    if abs(x) < EPS:
        return "0"
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    s = f"{x:.6f}".rstrip('0').rstrip('.')
    return s

def imprimir_matriz(matriz, var_orden):
    m = len(var_orden)
    anchos = [len(v) for v in var_orden] + [1]
    for fila in matriz:
        for i, val in enumerate(fila):
            anchos[i] = max(anchos[i], len(fmt_number(val)))
    header = "  ".join(var_orden[i].rjust(anchos[i]) for i in range(m)) + "   | " + "b".rjust(anchos[-1])
    print(header, flush=True)
    for fila in matriz:
        fila_str = "  ".join(fmt_number(fila[i]).rjust(anchos[i]) for i in range(m))
        fila_str += "   | " + fmt_number(fila[-1]).rjust(anchos[-1])
        print(fila_str, flush=True)
    print("", flush=True)
    time.sleep(DELAY)

def gauss_jordan(matriz, var_orden):
    n = len(matriz)
    m = len(var_orden)
    fila = 0
    pivot_map = {}

    for col in range(m):
        sel = None
        for r in range(fila, n):
            if abs(matriz[r][col]) > EPS:
                sel = r
                break
        if sel is None:
            print(f"No hay pivote en columna {col+1} ({var_orden[col]}). Variable libre.", flush=True)
            time.sleep(DELAY)
            continue

        if sel != fila:
            print(f"Operación: F{fila+1} <-> F{sel+1}", flush=True)
            matriz[fila], matriz[sel] = matriz[sel], matriz[fila]
            imprimir_matriz(matriz, var_orden)

        piv_val = matriz[fila][col]
        print(f"Pivote en ({fila+1},{col+1}) = {fmt_number(piv_val)}", flush=True)
        time.sleep(DELAY)

        if abs(piv_val - 1.0) > EPS:
            print(f"Operación: F{fila+1} -> F{fila+1} / {fmt_number(piv_val)}", flush=True)
            matriz[fila] = [x / piv_val for x in matriz[fila]]
            imprimir_matriz(matriz, var_orden)

        for r in range(n):
            if r != fila and abs(matriz[r][col]) > EPS:
                factor = matriz[r][col]
                if factor > 0:
                    print(f"Operación: F{r+1} -> F{r+1} - ({fmt_number(factor)})*F{fila+1}", flush=True)
                else:
                    print(f"Operación: F{r+1} -> F{r+1} + ({fmt_number(abs(factor))})*F{fila+1}", flush=True)
                matriz[r] = [a - factor * b for a, b in zip(matriz[r], matriz[fila])]
                imprimir_matriz(matriz, var_orden)

        pivot_map[col] = fila
        fila += 1
        if fila == n:
            break

    # Verificación de tipo de solución
    sistema_inconsistente = False
    for r in range(n):
        if all(abs(matriz[r][c]) < EPS for c in range(m)) and abs(matriz[r][m]) > EPS:
            sistema_inconsistente = True
            break

    if sistema_inconsistente:
        print("El sistema es INCONSISTENTE (sin solución).", flush=True)
        return

    if len(pivot_map) == m:
        sol = [0.0] * m
        for col, r in pivot_map.items():
            sol[col] = matriz[r][m]
        print("Solución única:", flush=True)
        for i, v in enumerate(var_orden):
            print(f"{v} = {fmt_number(sol[i])}", flush=True)
    else:
        libres = [var_orden[c] for c in range(m) if c not in pivot_map]
        print("El sistema tiene INFINITAS soluciones.", flush=True)
        print("Variables libres:", ", ".join(libres), flush=True)

def main():
    try:
        ecuaciones, var_orden = leer_sistema()
    except Exception as e:
        print("Error al leer el sistema:", e)
        return
    matriz = construir_matriz(ecuaciones, var_orden)
    print("\nMatriz aumentada inicial:")
    imprimir_matriz(matriz, var_orden)
    gauss_jordan(matriz, var_orden)

if __name__ == "__main__":
    main()
