def imprimir_matriz(matriz, mensaje=""):
    """Imprime la matriz de forma legible."""
    if mensaje:
        print("\n" + mensaje)
    for fila in matriz:
        print(["{0:8.3f}".format(x) for x in fila])
    print()

def eliminacion_gaussiana(matriz):
    """Aplica el método de eliminación Gaussiana paso a paso."""
    n = len(matriz)         # Número de filas (ecuaciones)
    m = len(matriz[0])      # Número de columnas (incógnitas + 1)

    imprimir_matriz(matriz, "Matriz inicial (aumentada):")

    # Eliminación hacia adelante
    for i in range(n):
        # 1. Asegurar que el pivote no sea cero (si es, cambiar filas)
        if matriz[i][i] == 0:
            for k in range(i+1, n):
                if matriz[k][i] != 0:
                    matriz[i], matriz[k] = matriz[k], matriz[i]
                    imprimir_matriz(matriz, f"Intercambio de fila {i+1} con fila {k+1}:")
                    break

        # 2. Normalizar la fila i (pivote = 1)
        pivote = matriz[i][i]
        if pivote != 0:
            matriz[i] = [x / pivote for x in matriz[i]]
            imprimir_matriz(matriz, f"Normalizando fila {i+1} (pivote = 1):")

        # 3. Eliminar los elementos debajo del pivote
        for j in range(i+1, n):
            factor = matriz[j][i]
            matriz[j] = [a - factor*b for a, b in zip(matriz[j], matriz[i])]
            imprimir_matriz(matriz, f"Eliminando elemento en fila {j+1}, columna {i+1}:")

    # Sustitución hacia atrás
    soluciones = [0 for _ in range(n)]
    for i in range(n-1, -1, -1):
        suma = sum(matriz[i][j] * soluciones[j] for j in range(i+1, n))
        soluciones[i] = matriz[i][-1] - suma

    print("\n Solución final del sistema:")
    for i, valor in enumerate(soluciones, start=1):
        print(f"x{i} = {valor:.3f}")

    return soluciones

def leer_entero(mensaje):
    """Lee un número entero con validación."""
    try:
        valor = int(input(mensaje))
        if valor <= 0:
            print(" El valor debe ser mayor que 0.")
            return None
        return valor
    except ValueError:
        print(" Entrada inválida, debe ser un número entero.")
        return None

def leer_fila(n_columnas, indice):
    """Lee una fila con validación de cantidad de valores numéricos."""
    try:
        fila = list(map(float, input(f"Fila {indice+1} ({n_columnas} valores separados por espacio): ").split()))
        if len(fila) != n_columnas:
            print(" Número incorrecto de valores en la fila.")
            return None
        return fila
    except ValueError:
        print(" Entrada inválida, debe contener solo números.")
        return None

def menu():
    while True:
        print("\n=== MÉTODO DE ELIMINACIÓN GAUSSIANA ===")
        print("1. Resolver un sistema de ecuaciones")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            n = leer_entero("Ingrese el número de ecuaciones (filas): ")
            if n is None:  # error -> volver al menú
                continue

            m = leer_entero("Ingrese el número de incógnitas (columnas): ")
            if m is None:  # error -> volver al menú
                continue

            if m != n:
                print(" Por simplicidad, el sistema debe ser cuadrado (mismo número de ecuaciones e incógnitas).")
                continue

            print("\nIngrese la matriz aumentada (coeficientes + términos independientes):")
            matriz = []
            valido = True
            for i in range(n):
                fila = leer_fila(m+1, i)
                if fila is None:  # error -> cancelar ingreso
                    valido = False
                    break
                matriz.append(fila)

            if not valido:
                print(" Error en el ingreso de datos. Regresando al menú principal...")
                continue

            eliminacion_gaussiana(matriz)

        elif opcion == "2":
            print(" Saliendo del programa...")
            break
        else:
            print(" Opción no válida.")

# Ejecutar programa
if __name__ == "__main__":
    menu()
