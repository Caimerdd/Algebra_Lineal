# Complement.py - VERSIÓN COMPLETAMENTE CORREGIDA

"""
Módulo de complementos para operaciones de álgebra lineal y matrices.

Contiene implementaciones de:
- Eliminación Gaussiana y Gauss-Jordan
- Cálculo de determinantes
- Regla de Cramer
- Independencia lineal de vectores
- Cálculo de matriz inversa

Todas las funciones incluyen manejo robusto de errores y pasos detallados.
"""

import sympy as sp
import numpy as np
from typing import List, Dict, Any, Tuple, Union
import copy

# =============================================================================
# VALIDACIONES Y UTILIDADES
# =============================================================================

def _validar_matriz(matriz: List[List[float]]) -> bool:
    """
    Valida que la matriz sea válida para operaciones.
    
    Args:
        matriz: Matriz a validar
        
    Returns:
        bool: True si la matriz es válida
    """
    if not matriz or not isinstance(matriz, list):
        return False
    
    if not all(isinstance(fila, list) for fila in matriz):
        return False
    
    # Verificar que todas las filas tengan la misma longitud
    longitudes = [len(fila) for fila in matriz]
    if len(set(longitudes)) != 1:
        return False
    
    # Verificar que todos los elementos sean numéricos
    for fila in matriz:
        for elemento in fila:
            if not isinstance(elemento, (int, float)):
                return False
    
    return True

def _matriz_a_texto(matriz: List[List[float]], precision: int = 4) -> str:
    """
    Convierte una matriz a string legible.
    
    Args:
        matriz: Matriz a formatear
        precision: Número de decimales
        
    Returns:
        str: Matriz formateada como string
    """
    if not _validar_matriz(matriz):
        return "Matriz inválida"
    
    filas_str = []
    for fila in matriz:
        fila_str = [f"{elem:.{precision}f}".rstrip('0').rstrip('.') for elem in fila]
        filas_str.append("[" + "  ".join(fila_str) + "]")
    
    return "\n".join(filas_str)

def _es_matriz_cuadrada(matriz: List[List[float]]) -> bool:
    """Verifica si una matriz es cuadrada."""
    if not _validar_matriz(matriz):
        return False
    return len(matriz) == len(matriz[0])

def _crear_matriz_identidad(n: int) -> List[List[float]]:
    """Crea una matriz identidad de tamaño n x n."""
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

# =============================================================================
# ELIMINACIÓN GAUSSIANA
# =============================================================================

def gauss_steps(M: List[List[float]]) -> Dict[str, Any]:
    """
    Aplica eliminación gaussiana a una matriz aumentada mostrando pasos.
    
    Args:
        M: Matriz aumentada [A|b]
        
    Returns:
        Dict con pasos, operaciones y solución
    """
    pasos = []
    operaciones = []
    
    try:
        if not _validar_matriz(M):
            raise ValueError("Matriz aumentada inválida")
        
        # Crear copia para no modificar la original
        matriz = copy.deepcopy(M)
        n = len(matriz)
        
        pasos.append(copy.deepcopy(matriz))
        operaciones.append("Matriz inicial")
        
        # Eliminación hacia adelante
        for i in range(n):
            # Pivoteo parcial: encontrar fila con máximo elemento en columna i
            max_fila = i
            for k in range(i + 1, n):
                if abs(matriz[k][i]) > abs(matriz[max_fila][i]):
                    max_fila = k
            
            # Intercambiar filas si es necesario
            if max_fila != i:
                matriz[i], matriz[max_fila] = matriz[max_fila], matriz[i]
                pasos.append(copy.deepcopy(matriz))
                operaciones.append(f"Intercambio F{i+1} ↔ F{max_fila+1}")
            
            # Verificar que el pivote no sea cero
            if abs(matriz[i][i]) < 1e-10:
                pasos.append(copy.deepcopy(matriz))
                operaciones.append(f"Pivote cero en posición ({i+1},{i+1}) - Sistema singular")
                return {
                    'steps': pasos,
                    'ops': operaciones,
                    'status': 'singular',
                    'message': 'Matriz singular - no tiene solución única'
                }
            
            # Eliminación en columnas debajo del pivote
            for j in range(i + 1, n):
                factor = matriz[j][i] / matriz[i][i]
                
                # Aplicar eliminación a toda la fila
                for k in range(i, len(matriz[0])):
                    matriz[j][k] -= factor * matriz[i][k]
                
                pasos.append(copy.deepcopy(matriz))
                operaciones.append(f"F{j+1} ← F{j+1} - ({factor:.3f})·F{i+1}")
        
        # Sustitución hacia atrás
        solucion = [0.0] * n
        for i in range(n - 1, -1, -1):
            solucion[i] = matriz[i][n]  # Última columna (términos independientes)
            for j in range(i + 1, n):
                solucion[i] -= matriz[i][j] * solucion[j]
            solucion[i] /= matriz[i][i]
        
        # Verificar solución
        pasos.append(copy.deepcopy(matriz))
        operaciones.append("Matriz triangular superior - Sustitución completada")
        
        return {
            'steps': pasos,
            'ops': operaciones,
            'status': 'unique',
            'solution': solucion,
            'message': 'Solución única encontrada'
        }
        
    except Exception as e:
        return {
            'steps': pasos,
            'ops': operaciones,
            'status': 'error',
            'message': f'Error en eliminación gaussiana: {str(e)}'
        }

# =============================================================================
# ELIMINACIÓN GAUSS-JORDAN
# =============================================================================

def gauss_jordan_steps(M: List[List[float]]) -> Dict[str, Any]:
    """
    Aplica eliminación Gauss-Jordan a una matriz aumentada mostrando pasos.
    
    Args:
        M: Matriz aumentada [A|b]
        
    Returns:
        Dict con pasos, operaciones y solución
    """
    pasos = []
    operaciones = []
    
    try:
        if not _validar_matriz(M):
            raise ValueError("Matriz aumentada inválida")
        
        matriz = copy.deepcopy(M)
        n = len(matriz)
        m = len(matriz[0]) - 1  # Columnas de A (excluyendo b)
        
        pasos.append(copy.deepcopy(matriz))
        operaciones.append("Matriz inicial")
        
        fila = 0
        col = 0
        
        while fila < n and col < m:
            # Encontrar pivote máximo en columna actual
            max_fila = fila
            for i in range(fila + 1, n):
                if abs(matriz[i][col]) > abs(matriz[max_fila][col]):
                    max_fila = i
            
            if abs(matriz[max_fila][col]) < 1e-10:
                # Columna es cero, pasar a siguiente columna
                col += 1
                continue
            
            # Intercambiar filas si es necesario
            if max_fila != fila:
                matriz[fila], matriz[max_fila] = matriz[max_fila], matriz[fila]
                pasos.append(copy.deepcopy(matriz))
                operaciones.append(f"Intercambio F{fila+1} ↔ F{max_fila+1}")
            
            # Normalizar fila pivote
            pivote = matriz[fila][col]
            for j in range(col, m + 1):
                matriz[fila][j] /= pivote
            
            pasos.append(copy.deepcopy(matriz))
            operaciones.append(f"F{fila+1} ← F{fila+1} / {pivote:.3f}")
            
            # Eliminar en otras filas
            for i in range(n):
                if i != fila and abs(matriz[i][col]) > 1e-10:
                    factor = matriz[i][col]
                    for j in range(col, m + 1):
                        matriz[i][j] -= factor * matriz[fila][j]
                    
                    pasos.append(copy.deepcopy(matriz))
                    operaciones.append(f"F{i+1} ← F{i+1} - ({factor:.3f})·F{fila+1}")
            
            fila += 1
            col += 1
        
        # Extraer solución
        solucion = [0.0] * m
        rango = fila
        
        if rango < m:
            return {
                'steps': pasos,
                'ops': operaciones,
                'status': 'infinite',
                'message': 'Sistema con infinitas soluciones',
                'rank': rango
            }
        
        # Leer solución de la matriz reducida
        for i in range(m):
            solucion[i] = matriz[i][m]  # Última columna
        
        # Verificar consistencia
        for i in range(rango, n):
            if abs(matriz[i][m]) > 1e-10:  # 0 ≠ 0?
                return {
                    'steps': pasos,
                    'ops': operaciones,
                    'status': 'inconsistent',
                    'message': 'Sistema inconsistente - sin solución'
                }
        
        return {
            'steps': pasos,
            'ops': operaciones,
            'status': 'unique',
            'solution': solucion,
            'message': 'Solución única encontrada'
        }
        
    except Exception as e:
        return {
            'steps': pasos,
            'ops': operaciones,
            'status': 'error',
            'message': f'Error en Gauss-Jordan: {str(e)}'
        }

# =============================================================================
# CÁLCULO DE DETERMINANTE
# =============================================================================

def pasos_determinante(A: List[List[float]]) -> Dict[str, Any]:
    """
    Calcula el determinante de una matriz mostrando pasos.
    
    Args:
        A: Matriz cuadrada
        
    Returns:
        Dict con pasos y resultado
    """
    pasos = []
    
    try:
        if not _validar_matriz(A):
            raise ValueError("Matriz inválida")
        
        if not _es_matriz_cuadrada(A):
            raise ValueError("El determinante solo existe para matrices cuadradas")
        
        n = len(A)
        matriz = copy.deepcopy(A)
        det = 1.0
        
        pasos.append(f"Matriz inicial {n}x{n}:")
        pasos.append(_matriz_a_texto(matriz))
        pasos.append("")
        
        # Para matrices 1x1 y 2x2, usar fórmulas directas
        if n == 1:
            resultado = matriz[0][0]
            pasos.append(f"Determinante 1x1 = {resultado}")
            return {
                'estado': 'exito',
                'determinante': resultado,
                'pasos': pasos
            }
        
        if n == 2:
            resultado = matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
            pasos.append(f"Fórmula 2x2: ({matriz[0][0]} × {matriz[1][1]}) - ({matriz[0][1]} × {matriz[1][0]})")
            pasos.append(f" = {resultado}")
            return {
                'estado': 'exito',
                'determinante': resultado,
                'pasos': pasos
            }
        
        if n == 3:
            # Regla de Sarrus
            a, b, c = matriz[0]
            d, e, f = matriz[1]
            g, h, i = matriz[2]
            
            resultado = (a*e*i + b*f*g + c*d*h) - (c*e*g + b*d*i + a*f*h)
            
            pasos.append("Regla de Sarrus para 3x3:")
            pasos.append(f"Positivos: ({a}×{e}×{i}) + ({b}×{f}×{g}) + ({c}×{d}×{h})")
            pasos.append(f"Negativos: - ({c}×{e}×{g}) - ({b}×{d}×{i}) - ({a}×{f}×{h})")
            pasos.append(f"Resultado: {resultado}")
            
            return {
                'estado': 'exito',
                'determinante': resultado,
                'pasos': pasos
            }
        
        # Para matrices n>3, usar eliminación gaussiana
        pasos.append(f"Matriz {n}x{n} - usando eliminación gaussiana:")
        
        for i in range(n):
            # Pivoteo parcial
            max_fila = i
            for k in range(i + 1, n):
                if abs(matriz[k][i]) > abs(matriz[max_fila][i]):
                    max_fila = k
            
            if max_fila != i:
                matriz[i], matriz[max_fila] = matriz[max_fila], matriz[i]
                det *= -1  # Cambio de signo por intercambio
                pasos.append(f"Intercambio F{i+1} ↔ F{max_fila+1} (det × -1)")
                pasos.append(_matriz_a_texto(matriz))
            
            if abs(matriz[i][i]) < 1e-12:
                pasos.append(f"Pivote cero en posición ({i+1},{i+1})")
                pasos.append("Determinante = 0")
                return {
                    'estado': 'exito',
                    'determinante': 0.0,
                    'pasos': pasos
                }
            
            # Multiplicar determinante por pivote
            det *= matriz[i][i]
            pasos.append(f"Pivote F{i+1} = {matriz[i][i]:.6f}")
            pasos.append(f"det acumulado = {det:.6f}")
            
            # Eliminación
            for j in range(i + 1, n):
                factor = matriz[j][i] / matriz[i][i]
                for k in range(i + 1, n):
                    matriz[j][k] -= factor * matriz[i][k]
        
        pasos.append("")
        pasos.append(f"Determinante final = {det:.6f}")
        
        return {
            'estado': 'exito',
            'determinante': det,
            'pasos': pasos
        }
        
    except Exception as e:
        return {
            'estado': 'error',
            'mensaje': f'Error calculando determinante: {str(e)}',
            'pasos': pasos
        }

# =============================================================================
# REGLA DE CRAMER
# =============================================================================

def resolver_por_cramer(M: List[List[float]]) -> Dict[str, Any]:
    """
    Resuelve un sistema de ecuaciones usando la regla de Cramer.
    
    Args:
        M: Matriz aumentada [A|b]
        
    Returns:
        Dict con pasos y solución
    """
    pasos = []
    
    try:
        if not _validar_matriz(M):
            raise ValueError("Matriz aumentada inválida")
        
        n = len(M)
        if n == 0:
            raise ValueError("Matriz vacía")
        
        # Separar A y b
        A = [fila[:-1] for fila in M]
        b = [fila[-1] for fila in M]
        
        if not _es_matriz_cuadrada(A):
            raise ValueError("La regla de Cramer requiere matriz A cuadrada")
        
        if len(A) != len(b):
            raise ValueError("Dimensiones incompatibles entre A y b")
        
        pasos.append("Sistema de ecuaciones:")
        for i in range(n):
            ecuacion = " + ".join([f"{A[i][j]:.2f}x{j+1}" for j in range(n)])
            pasos.append(f"{ecuacion} = {b[i]:.2f}")
        pasos.append("")
        
        # Calcular determinante de A
        det_A_result = pasos_determinante(A)
        if det_A_result['estado'] == 'error':
            raise ValueError(f"Error calculando det(A): {det_A_result['mensaje']}")
        
        det_A = det_A_result['determinante']
        pasos.append(f"det(A) = {det_A:.6f}")
        pasos.append("")
        
        if abs(det_A) < 1e-10:
            pasos.append("det(A) ≈ 0 → Sistema no tiene solución única")
            return {
                'estado': 'error',
                'mensaje': 'El determinante de A es cero - sistema no tiene solución única',
                'pasos': pasos
            }
        
        solucion = []
        
        # Para cada variable, calcular determinante de A con columna reemplazada
        for k in range(n):
            # Crear matriz A_k (reemplazar columna k por b)
            A_k = copy.deepcopy(A)
            for i in range(n):
                A_k[i][k] = b[i]
            
            pasos.append(f"Matriz A_{k+1} (columna {k+1} reemplazada por b):")
            pasos.append(_matriz_a_texto(A_k))
            
            # Calcular det(A_k)
            det_A_k_result = pasos_determinante(A_k)
            if det_A_k_result['estado'] == 'error':
                raise ValueError(f"Error calculando det(A_{k+1}): {det_A_k_result['mensaje']}")
            
            det_A_k = det_A_k_result['determinante']
            pasos.append(f"det(A_{k+1}) = {det_A_k:.6f}")
            
            # Calcular x_k = det(A_k) / det(A)
            x_k = det_A_k / det_A
            solucion.append(x_k)
            
            pasos.append(f"x_{k+1} = det(A_{k+1}) / det(A) = {x_k:.6f}")
            pasos.append("")
        
        pasos.append("Solución encontrada:")
        for i, x in enumerate(solucion):
            pasos.append(f"x_{i+1} = {x:.6f}")
        
        return {
            'estado': 'exito',
            'solucion': solucion,
            'pasos': pasos
        }
        
    except Exception as e:
        return {
            'estado': 'error',
            'mensaje': f'Error en regla de Cramer: {str(e)}',
            'pasos': pasos
        }

# =============================================================================
# INDEPENDENCIA LINEAL Y RANGO
# =============================================================================

def independenciaVectores(vectores: List[List[float]]) -> Dict[str, Any]:
    """
    Determina si un conjunto de vectores es linealmente independiente.
    
    Args:
        vectores: Lista de vectores (cada vector es una lista)
        
    Returns:
        Dict con análisis de independencia lineal
    """
    try:
        if not vectores:
            return {
                'independent': True,
                'rank': 0,
                'num_vectors': 0,
                'message': 'Conjunto vacío - trivialmente independiente'
            }
        
        # Convertir a matriz (vectores como columnas)
        n = len(vectores[0])  # Dimensión de cada vector
        m = len(vectores)     # Número de vectores
        
        # Crear matriz donde cada columna es un vector
        matriz = [[vectores[j][i] for j in range(m)] for i in range(n)]
        
        # Usar numpy para calcular el rango (más robusto)
        try:
            import numpy as np
            matriz_np = np.array(matriz)
            rango = np.linalg.matrix_rank(matriz_np)
        except ImportError:
            # Fallback: método manual básico
            rango = _calcular_rango_manual(matriz)
        
        es_independiente = (rango == m)
        
        mensaje = (f"Linealmente independiente (rango = {rango}, vectores = {m})" 
                  if es_independiente else 
                  f"Linealmente dependiente (rango = {rango}, vectores = {m})")
        
        return {
            'independent': es_independiente,
            'rank': rango,
            'num_vectors': m,
            'message': mensaje
        }
        
    except Exception as e:
        return {
            'independent': False,
            'rank': 0,
            'num_vectors': 0,
            'message': f'Error analizando independencia: {str(e)}'
        }

def _calcular_rango_manual(matriz: List[List[float]]) -> int:
    """
    Calcula el rango de una matriz manualmente (fallback).
    """
    if not matriz:
        return 0
    
    matriz_copy = copy.deepcopy(matriz)
    n = len(matriz_copy)
    m = len(matriz_copy[0])
    
    rango = 0
    for j in range(m):
        # Encontrar fila con pivote no cero
        fila_pivote = -1
        for i in range(rango, n):
            if abs(matriz_copy[i][j]) > 1e-10:
                fila_pivote = i
                break
        
        if fila_pivote == -1:
            continue
        
        # Intercambiar filas
        if fila_pivote != rango:
            matriz_copy[rango], matriz_copy[fila_pivote] = matriz_copy[fila_pivote], matriz_copy[rango]
        
        # Normalizar
        pivote = matriz_copy[rango][j]
        for k in range(j, m):
            matriz_copy[rango][k] /= pivote
        
        # Eliminar
        for i in range(n):
            if i != rango and abs(matriz_copy[i][j]) > 1e-10:
                factor = matriz_copy[i][j]
                for k in range(j, m):
                    matriz_copy[i][k] -= factor * matriz_copy[rango][k]
        
        rango += 1
    
    return rango

# =============================================================================
# MATRIZ INVERSA
# =============================================================================

def inverse_steps(A: List[List[float]]) -> Dict[str, Any]:
    """
    Calcula la matriz inversa mostrando pasos.
    
    Args:
        A: Matriz cuadrada invertible
        
    Returns:
        Dict con pasos y matriz inversa
    """
    pasos = []
    operaciones = []
    
    try:
        if not _validar_matriz(A):
            raise ValueError("Matriz inválida")
        
        if not _es_matriz_cuadrada(A):
            raise ValueError("La matriz inversa solo existe para matrices cuadradas")
        
        n = len(A)
        
        # Verificar si es invertible calculando determinante
        det_result = pasos_determinante(A)
        if det_result['estado'] == 'error':
            raise ValueError(f"Error verificando invertibilidad: {det_result['mensaje']}")
        
        if abs(det_result['determinante']) < 1e-10:
            return {
                'steps': pasos,
                'ops': operaciones,
                'status': 'singular',
                'message': 'Matriz singular - determinante cero'
            }
        
        # Crear matriz aumentada [A|I]
        matriz_aumentada = []
        for i in range(n):
            fila = A[i] + [1.0 if i == j else 0.0 for j in range(n)]
            matriz_aumentada.append(fila)
        
        pasos.append(copy.deepcopy(matriz_aumentada))
        operaciones.append("Matriz aumentada [A|I]")
        
        # Aplicar Gauss-Jordan a la matriz aumentada
        for i in range(n):
            # Pivoteo
            max_fila = i
            for k in range(i + 1, n):
                if abs(matriz_aumentada[k][i]) > abs(matriz_aumentada[max_fila][i]):
                    max_fila = k
            
            if max_fila != i:
                matriz_aumentada[i], matriz_aumentada[max_fila] = matriz_aumentada[max_fila], matriz_aumentada[i]
                pasos.append(copy.deepcopy(matriz_aumentada))
                operaciones.append(f"Intercambio F{i+1} ↔ F{max_fila+1}")
            
            # Normalizar fila pivote
            pivote = matriz_aumentada[i][i]
            for j in range(2 * n):
                matriz_aumentada[i][j] /= pivote
            
            pasos.append(copy.deepcopy(matriz_aumentada))
            operaciones.append(f"F{i+1} ← F{i+1} / {pivote:.3f}")
            
            # Eliminar en otras filas
            for k in range(n):
                if k != i and abs(matriz_aumentada[k][i]) > 1e-10:
                    factor = matriz_aumentada[k][i]
                    for j in range(2 * n):
                        matriz_aumentada[k][j] -= factor * matriz_aumentada[i][j]
                    
                    pasos.append(copy.deepcopy(matriz_aumentada))
                    operaciones.append(f"F{k+1} ← F{k+1} - ({factor:.3f})·F{i+1}")
        
        # Extraer la inversa (parte derecha de la matriz aumentada)
        inversa = [fila[n:] for fila in matriz_aumentada]
        
        pasos.append(copy.deepcopy(matriz_aumentada))
        operaciones.append("Matriz identidad [I|A⁻¹] - inversa encontrada")
        
        return {
            'steps': pasos,
            'ops': operaciones,
            'status': 'invertible',
            'inverse': inversa,
            'message': 'Matriz inversa calculada exitosamente'
        }
        
    except Exception as e:
        return {
            'steps': pasos,
            'ops': operaciones,
            'status': 'error',
            'message': f'Error calculando matriz inversa: {str(e)}'
        }

# =============================================================================
# PRUEBAS Y EJEMPLOS
# =============================================================================

if __name__ == "__main__":
    print("=== Pruebas Complement.py ===")
    
    # Matriz de prueba 2x2
    A = [[2, 1], [1, 3]]
    b = [4, 5]
    M = [[2, 1, 4], [1, 3, 5]]
    
    print("1. Eliminación Gaussiana:")
    resultado_gauss = gauss_steps(M)
    print(f"Estado: {resultado_gauss['status']}")
    print(f"Mensaje: {resultado_gauss['message']}")
    
    print("\n2. Determinante:")
    resultado_det = pasos_determinante(A)
    print(f"det(A) = {resultado_det['determinante']}")
    
    print("\n3. Regla de Cramer:")
    resultado_cramer = resolver_por_cramer(M)
    print(f"Estado: {resultado_cramer['estado']}")
    
    print("\n4. Independencia lineal:")
    vectores = [[1, 0], [0, 1], [1, 1]]
    resultado_indep = independenciaVectores(vectores)
    print(f"Independiente: {resultado_indep['independent']}")
    print(f"Rango: {resultado_indep['rank']}")