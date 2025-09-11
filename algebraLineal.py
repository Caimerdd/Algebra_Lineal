# Función para pedir la matriz aumentada
def leer_matriz():
    while True:
        try:
            filas = int(input("Ingrese el número de ecuaciones (filas): "))
            columnas = int(input("Ingrese el número de incógnitas (columnas): ")) + 1  # +1 por la columna de términos independientes
                
            if filas <= 0 or columnas <= 1:
                print("Error: el número de filas o columnas no puede ser negativo o cero.")
                continue
            break
        except ValueError:
            print("Error: ingrese números enteros válidos.")

    matriz = []
    print(f"Ingrese la matriz aumentada ({filas}x{columnas}), separando los valores con espacios:")

    for i in range(filas):
        while True:
            entrada = input(f"Fila {i+1}: ").strip().split()
            if len(entrada) != columnas:
                print(f"Error: debe ingresar exactamente {columnas} valores.")
                continue
            try:
                fila = [float(x) for x in entrada]  # convierte a números
                matriz.append(fila)
                break
            except ValueError:
                print("Error: ingrese solo números válidos.")
            

    return matriz


# Mostrar la matriz de forma bonita
def mostrar_matriz(matriz):
    for fila in matriz:
        print(["{0:8.3f}".format(x) for x in fila])
    print()

# Método de Gauss-Jordan paso a paso
def gauss_jordan(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    pivote_col = []  # guardará qué columnas fueron pivote

    print("\n--- Resolviendo con Gauss-Jordan ---\n")
    mostrar_matriz(matriz)

    fila_actual = 0
    for col in range(columnas - 1):  # no incluimos la última columna (términos independientes)
        # Buscar un pivote en esta columna
        pivote = None
        for f in range(fila_actual, filas):
            if matriz[f][col] != 0:
                pivote = f
                break

        if pivote is None:
            continue  # no hay pivote en esta columna → variable libre
        pivote_col.append(col)

        # Intercambiar filas si el pivote no está en la fila actual
        if pivote != fila_actual:
            matriz[fila_actual], matriz[pivote] = matriz[pivote], matriz[fila_actual]
            print(f"Operacion: F{fila_actual+1} <-> F{pivote+1}")
            mostrar_matriz(matriz)

        # Normalizar la fila pivote (hacer que el pivote sea 1)
        divisor = matriz[fila_actual][col]
        if divisor != 1:  # solo si de verdad divide
            matriz[fila_actual] = [x/divisor for x in matriz[fila_actual]]
            print(f"Operacion: F{fila_actual+1} -> (1/{divisor:.3f}) * F{fila_actual+1}")
            mostrar_matriz(matriz)


        # Hacer ceros en la columna pivote
        for f in range(filas):
            if f != fila_actual and matriz[f][col] != 0:
                factor = matriz[f][col]
                matriz[f] = [a - factor*b for a, b in zip(matriz[f], matriz[fila_actual])]
                print(f"Eliminando columna {col+1} en fila {f+1}")
                mostrar_matriz(matriz)

        fila_actual += 1
        if fila_actual == filas:
            break

    # -------------------------------
    # Analizar el tipo de solución
    # -------------------------------
    # Verificar inconsistencia (ejemplo: 0 0 0 | b con b ≠ 0)
    for fila in matriz:
        if all(abs(x) < 1e-9 for x in fila[:-1]) and abs(fila[-1]) > 1e-9:
            print("El sistema es INCONSISTENTE (no tiene solución).")
            return

    # Variables libres = columnas sin pivote
    libres = [c for c in range(columnas-1) if c not in pivote_col]

    if len(pivote_col) == columnas-1:
        print("El sistema tiene solución ÚNICA:")
        solucion = [fila[-1] for fila in matriz]
        for i, val in enumerate(solucion):
            print(f"x{i+1} = {val:.3f}")
    else:
        print("El sistema tiene INFINITAS soluciones.")
        if libres:
            print("Variables libres:", [f"x{c+1}" for c in libres])


# -------------------------------
# Programa principal
# -------------------------------
if __name__ == "__main__":
    matriz = leer_matriz()
    gauss_jordan(matriz)
