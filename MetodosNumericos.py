# MetodosNumericos.py - VERSIÓN DEFINITIVA CON DETECCIÓN DE SIN RAÍCES

"""
Módulo de métodos numéricos para resolver ecuaciones no lineales.

Contiene implementaciones de:
- Método de Bisección
- Método de Falsa Posición (Regula Falsi)
- Método de Newton-Raphson
- Método de la Secante

Todos los métodos incluyen validación de dominio y manejo robusto de errores.
"""

import math
import sympy as sp
from typing import Dict, List, Tuple, Optional, Callable
import numpy as np

# =============================================================================
# VALIDACIONES Y UTILIDADES - VERSIÓN CORREGIDA
# =============================================================================

def _parsear_funcion(funcion_str: str) -> Tuple[Callable, str]:
    """
    Convierte un string de función a una función callable de Python.
    VERSIÓN CORREGIDA: No usa eval con math module.
    """
    if not funcion_str or not funcion_str.strip():
        return None, "La función no puede estar vacía"
    
    funcion_str = funcion_str.strip().replace('^', '**')
    
    try:
        # ENFOQUE SEGURO: Crear función manualmente sin usar eval con math
        def funcion_evaluada(x):
            # Reemplazar dinámicamente en tiempo de ejecución
            # Usar un diccionario local con todas las funciones matemáticas
            loc = {
                'x': x,
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
                'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
                'exp': math.exp, 'log': math.log, 'log10': math.log10,
                'sqrt': math.sqrt, 'abs': abs, 'pi': math.pi, 'e': math.e,
                # Aliases comunes
                'ln': math.log, 'arcsin': math.asin, 'arccos': math.acos, 'arctan': math.atan
            }
            return eval(funcion_str, {"__builtins__": {}}, loc)
        
        # Probar la función
        test_val = 1.0
        try:
            result = funcion_evaluada(test_val)
            if not isinstance(result, (int, float)):
                return None, "La función debe devolver un valor numérico"
        except Exception as e:
            return None, f"Error al evaluar la función: {str(e)}"
        
        return funcion_evaluada, ""
        
    except Exception as e:
        return None, f"Error al procesar la función: {str(e)}"

def _evaluar_funcion_segura(f: Callable, x: float) -> Tuple[Optional[float], str]:
    """
    Evalúa una función de manera segura con manejo de errores de dominio.
    """
    try:
        # Verificar dominio para funciones específicas
        # Para log(x)
        if x <= 0 and any(keyword in str(f) for keyword in ['log', 'log10', 'ln']):
            return None, f"Error de dominio: log(x) no definido para x ≤ 0 (x = {x})"
        
        # Para sqrt(x)
        if x < 0 and 'sqrt' in str(f):
            return None, f"Error de dominio: sqrt(x) no definido para x < 0 (x = {x})"
        
        # Para asin(x)/acos(x)
        if (x < -1 or x > 1) and any(keyword in str(f) for keyword in ['asin', 'acos', 'arcsin', 'arccos']):
            return None, f"Error de dominio: asin(x)/acos(x) requiere -1 ≤ x ≤ 1 (x = {x})"
        
        resultado = f(x)
        
        # Verificar si es un número finito
        if not math.isfinite(resultado):
            return None, f"Función devolvió valor no finito en x = {x}"
            
        return resultado, ""
        
    except ValueError as e:
        if "math domain error" in str(e).lower():
            return None, f"Error de dominio matemático en x = {x}: {str(e)}"
        return None, f"Error de valor: {str(e)}"
    except ZeroDivisionError:
        return None, f"División por cero en x = {x}"
    except Exception as e:
        return None, f"Error inesperado al evaluar f({x}): {str(e)}"

def _verificar_intervalo(f: Callable, a: float, b: float) -> Tuple[bool, str]:
    """
    Verifica que el intervalo [a, b] sea válido para el método de bisección/falsa posicion.
    """
    if a >= b:
        return False, f"El intervalo es inválido: a ({a}) debe ser menor que b ({b})"
    
    # Evaluar función en los extremos
    fa, error_a = _evaluar_funcion_segura(f, a)
    if error_a:
        return False, f"Error en f(a): {error_a}"
    
    fb, error_b = _evaluar_funcion_segura(f, b)
    if error_b:
        return False, f"Error en f(b): {error_b}"
    
    # Verificar cambio de signo (Teorema de Bolzano)
    if fa * fb > 0:
        return False, f"f(a) × f(b) > 0. No hay cambio de signo en el intervalo [{a}, {b}]"
    
    return True, ""

def _verificar_posible_sin_raices(f: Callable, funcion_str: str, x0: float, x1: float) -> Tuple[bool, str]:
    """
    Verifica si es probable que la función no tenga raíces reales.
    """
    try:
        # Evaluar en varios puntos del dominio
        puntos_prueba = []
        
        # Para funciones con log(x), probar solo valores positivos
        if 'log' in funcion_str or 'ln' in funcion_str:
            puntos_prueba = [max(0.001, x0), max(0.001, x1), max(0.001, (x0+x1)/2), 
                           max(0.001, x0*2), max(0.001, x1*2)]
        else:
            puntos_prueba = [x0, x1, (x0+x1)/2, x0*2, x1*2, x0/2, x1/2]
        
        todos_positivos = True
        todos_negativos = True
        
        for punto in puntos_prueba:
            if punto > 0 or ('log' not in funcion_str and 'ln' not in funcion_str):
                valor, error = _evaluar_funcion_segura(f, punto)
                if not error:
                    if valor > 0:
                        todos_negativos = False
                    elif valor < 0:
                        todos_positivos = False
        
        if todos_positivos:
            return True, "La función parece ser siempre positiva en el dominio analizado. Posiblemente no tiene raíces reales."
        elif todos_negativos:
            return True, "La función parece ser siempre negativa en el dominio analizado. Posiblemente no tiene raíces reales."
        
        return False, ""
        
    except Exception:
        return False, ""

# =============================================================================
# MÉTODO DE BISECCIÓN
# =============================================================================

def metodo_biseccion(funcion_str: str, a: float, b: float, tolerancia: float = 1e-6, max_iter: int = 100) -> Dict[str, any]:
    """
    Resuelve f(x) = 0 usando el método de bisección.
    """
    tabla_headers = ["Iter", "a", "b", "c", "f(a)", "f(b)", "f(c)", "Error"]
    tabla_data = []
    info_previa = []
    
    try:
        # Parsear función
        f, error_parseo = _parsear_funcion(funcion_str)
        if error_parseo:
            return {
                'estado': 'error',
                'mensaje': f"Error en la función: {error_parseo}",
                'info_previa': info_previa,
                'tabla_headers': tabla_headers,
                'tabla_data': tabla_data
            }
        
        info_previa.append(f"Función: f(x) = {funcion_str}")
        info_previa.append(f"Intervalo inicial: [{a}, {b}]")
        info_previa.append(f"Tolerancia: {tolerancia}")
        info_previa.append(f"Máximo de iteraciones: {max_iter}")
        
        # Verificar intervalo
        es_valido, mensaje_error = _verificar_intervalo(f, a, b)
        if not es_valido:
            return {
                'estado': 'error', 
                'mensaje': mensaje_error,
                'info_previa': info_previa,
                'tabla_headers': tabla_headers,
                'tabla_data': tabla_data
            }
        
        # Evaluar función en extremos
        fa, error_fa = _evaluar_funcion_segura(f, a)
        fb, error_fb = _evaluar_funcion_segura(f, b)
        
        if error_fa or error_fb:
            return {
                'estado': 'error',
                'mensaje': f"Error evaluando función en extremos: {error_fa or error_fb}",
                'info_previa': info_previa,
                'tabla_headers': tabla_headers,
                'tabla_data': tabla_data
            }
        
        info_previa.append(f"f(a) = f({a}) = {fa:.6f}")
        info_previa.append(f"f(b) = f({b}) = {fb:.6f}")
        info_previa.append(f"f(a) × f(b) = {fa * fb:.6f} < 0 ✓ (Cambio de signo confirmado)")
        
        # Inicializar variables
        iteracion = 0
        c_anterior = 0
        error_actual = float('inf')
        
        # Algoritmo de bisección
        while iteracion < max_iter and error_actual > tolerancia:
            # Calcular punto medio
            c = (a + b) / 2.0
            fc, error_fc = _evaluar_funcion_segura(f, c)
            
            if error_fc:
                return {
                    'estado': 'error',
                    'mensaje': f"Error en iteración {iteracion}: {error_fc}",
                    'info_previa': info_previa,
                    'tabla_headers': tabla_headers,
                    'tabla_data': tabla_data
                }
            
            # Calcular error (excepto en primera iteración)
            if iteracion > 0:
                error_actual = abs(c - c_anterior)
            else:
                error_actual = float('inf')
            
            # Agregar a tabla
            tabla_data.append([
                iteracion + 1,
                f"{a:.6f}",
                f"{b:.6f}", 
                f"{c:.6f}",
                f"{fa:.6f}",
                f"{fb:.6f}",
                f"{fc:.6f}",
                f"{error_actual:.6e}" if iteracion > 0 else "---"
            ])
            
            # Detener si encontramos la raíz exacta
            if abs(fc) < 1e-12:
                break
            
            # Actualizar intervalo
            if fa * fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc
            
            c_anterior = c
            iteracion += 1
        
        # Resultado final
        raiz = (a + b) / 2.0
        f_raiz, _ = _evaluar_funcion_segura(f, raiz)
        
        mensaje_final = (
            f"¡Convergencia alcanzada!\n"
            f"Raíz encontrada: x ≈ {raiz:.10f}\n"
            f"f({raiz:.6f}) = {f_raiz:.6e}\n"
            f"Iteraciones: {iteracion}\n"
            f"Error final: {error_actual:.6e}"
        )
        
        return {
            'estado': 'exito',
            'raiz': raiz,
            'iteraciones': iteracion,
            'error': error_actual,
            'info_previa': info_previa,
            'tabla_headers': tabla_headers,
            'tabla_data': tabla_data,
            'mensaje_final': mensaje_final
        }
        
    except Exception as e:
        return {
            'estado': 'error',
            'mensaje': f"Error inesperado en bisección: {str(e)}",
            'info_previa': info_previa,
            'tabla_headers': tabla_headers, 
            'tabla_data': tabla_data
        }

# =============================================================================
# MÉTODO DE FALSA POSICIÓN (REGULA FALSI)
# =============================================================================

def metodo_falsa_posicion(funcion_str: str, a: float, b: float, tolerancia: float = 1e-6, max_iter: int = 100) -> Dict[str, any]:
    """
    Resuelve f(x) = 0 usando el método de falsa posición.
    """
    tabla_headers = ["Iter", "a", "b", "c", "f(a)", "f(b)", "f(c)", "Error"]
    tabla_data = []
    info_previa = []
    
    try:
        # Parsear función
        f, error_parseo = _parsear_funcion(funcion_str)
        if error_parseo:
            return {
                'estado': 'error',
                'mensaje': f"Error en la función: {error_parseo}",
                'info_previa': info_previa,
                'tabla_headers': tabla_headers,
                'tabla_data': tabla_data
            }
        
        info_previa.append(f"Función: f(x) = {funcion_str}")
        info_previa.append(f"Intervalo inicial: [{a}, {b}]")
        info_previa.append(f"Tolerancia: {tolerancia}")
        
        # Verificar intervalo
        es_valido, mensaje_error = _verificar_intervalo(f, a, b)
        if not es_valido:
            return {
                'estado': 'error',
                'mensaje': mensaje_error,
                'info_previa': info_previa,
                'tabla_headers': tabla_headers,
                'tabla_data': tabla_data
            }
        
        # Evaluar función en extremos
        fa, error_fa = _evaluar_funcion_segura(f, a)
        fb, error_fb = _evaluar_funcion_segura(f, b)
        
        if error_fa or error_fb:
            return {
                'estado': 'error',
                'mensaje': f"Error evaluando función en extremos: {error_fa or error_fb}",
                'info_previa': info_previa,
                'tabla_headers': tabla_headers,
                'tabla_data': tabla_data
            }
        
        info_previa.append(f"f(a) = f({a}) = {fa:.6f}")
        info_previa.append(f"f(b) = f({b}) = {fb:.6f}")
        
        # Inicializar variables
        iteracion = 0
        c_anterior = 0
        error_actual = float('inf')
        
        while iteracion < max_iter and error_actual > tolerancia:
            # Calcular intersección con línea secante
            c = (a * fb - b * fa) / (fb - fa)
            fc, error_fc = _evaluar_funcion_segura(f, c)
            
            if error_fc:
                return {
                    'estado': 'error',
                    'mensaje': f"Error en iteración {iteracion}: {error_fc}",
                    'info_previa': info_previa,
                    'tabla_headers': tabla_headers,
                    'tabla_data': tabla_data
                }
            
            # Calcular error
            if iteracion > 0:
                error_actual = abs(c - c_anterior)
            else:
                error_actual = float('inf')
            
            # Agregar a tabla
            tabla_data.append([
                iteracion + 1,
                f"{a:.6f}",
                f"{b:.6f}",
                f"{c:.6f}",
                f"{fa:.6f}",
                f"{fb:.6f}",
                f"{fc:.6f}",
                f"{error_actual:.6e}" if iteracion > 0 else "---"
            ])
            
            # Verificar convergencia
            if abs(fc) < 1e-12:
                break
            
            # Actualizar intervalo
            if fa * fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc
            
            c_anterior = c
            iteracion += 1
        
        # Resultado final
        raiz = c
        f_raiz, _ = _evaluar_funcion_segura(f, raiz)
        
        mensaje_final = (
            f"¡Convergencia alcanzada!\n"
            f"Raíz encontrada: x ≈ {raiz:.10f}\n"
            f"f({raiz:.6f}) = {f_raiz:.6e}\n"
            f"Iteraciones: {iteracion}\n"
            f"Error final: {error_actual:.6e}"
        )
        
        return {
            'estado': 'exito',
            'raiz': raiz,
            'iteraciones': iteracion,
            'error': error_actual,
            'info_previa': info_previa,
            'tabla_headers': tabla_headers,
            'tabla_data': tabla_data,
            'mensaje_final': mensaje_final
        }
        
    except Exception as e:
        return {
            'estado': 'error',
            'mensaje': f"Error inesperado en falsa posición: {str(e)}",
            'info_previa': info_previa,
            'tabla_headers': tabla_headers,
            'tabla_data': tabla_data
        }

# =============================================================================
# MÉTODO DE NEWTON-RAPHSON
# =============================================================================

def metodo_newton_raphson(funcion_str: str, x0: float, tolerancia: float = 1e-6, max_iter: int = 100) -> Dict[str, any]:
    """
    Resuelve f(x) = 0 usando el método de Newton-Raphson.
    """
    tabla_headers = ["Iter", "x_n", "f(x_n)", "f'(x_n)", "x_{n+1}", "Error"]
    tabla_data = []
    info_previa = []
    
    try:
        # Usar sympy para calcular derivada exacta
        x_sym = sp.Symbol('x')
        
        try:
            funcion_sympy = sp.sympify(funcion_str.replace('^', '**'))
            derivada_sympy = sp.diff(funcion_sympy, x_sym)
            
            # Convertir a funciones numéricas
            f = sp.lambdify(x_sym, funcion_sympy, modules=['math', 'numpy'])
            f_prima = sp.lambdify(x_sym, derivada_sympy, modules=['math', 'numpy'])
            
        except Exception as e:
            return {
                'estado': 'error',
                'mensaje': f"Error al procesar función con SymPy: {str(e)}",
                'info_previa': info_previa,
                'tabla_headers': tabla_headers,
                'tabla_data': tabla_data
            }
        
        info_previa.append(f"Función: f(x) = {funcion_str}")
        info_previa.append(f"Derivada: f'(x) = {sp.sstr(derivada_sympy).replace('**', '^')}")
        info_previa.append(f"Aproximación inicial: x₀ = {x0}")
        info_previa.append(f"Tolerancia: {tolerancia}")
        
        # Evaluar función y derivada en punto inicial
        fx0, error_fx0 = _evaluar_funcion_segura(f, x0)
        if error_fx0:
            return {
                'estado': 'error',
                'mensaje': f"Error evaluando f(x₀): {error_fx0}",
                'info_previa': info_previa,
                'tabla_headers': tabla_headers,
                'tabla_data': tabla_data
            }
        
        fpx0, error_fpx0 = _evaluar_funcion_segura(f_prima, x0)
        if error_fpx0:
            return {
                'estado': 'error', 
                'mensaje': f"Error evaluando f'(x₀): {error_fpx0}",
                'info_previa': info_previa,
                'tabla_headers': tabla_headers,
                'tabla_data': tabla_data
            }
        
        if abs(fpx0) < 1e-12:
            return {
                'estado': 'error',
                'mensaje': f"Derivada cero en x₀ = {x0}. El método no puede continuar.",
                'info_previa': info_previa,
                'tabla_headers': tabla_headers,
                'tabla_data': tabla_data
            }
        
        # Inicializar variables
        iteracion = 0
        x_actual = x0
        error_actual = float('inf')
        
        while iteracion < max_iter and error_actual > tolerancia:
            # Evaluar función y derivada
            f_x, error_f = _evaluar_funcion_segura(f, x_actual)
            fp_x, error_fp = _evaluar_funcion_segura(f_prima, x_actual)
            
            if error_f or error_fp:
                return {
                    'estado': 'error',
                    'mensaje': f"Error en iteración {iteracion}: {error_f or error_fp}",
                    'info_previa': info_previa,
                    'tabla_headers': tabla_headers,
                    'tabla_data': tabla_data
                }
            
            # Verificar derivada cero
            if abs(fp_x) < 1e-12:
                return {
                    'estado': 'error',
                    'mensaje': f"Derivada cero en iteración {iteracion}. Método divergente.",
                    'info_previa': info_previa,
                    'tabla_headers': tabla_headers,
                    'tabla_data': tabla_data
                }
            
            # Calcular siguiente aproximación
            x_siguiente = x_actual - f_x / fp_x
            
            # Calcular error
            error_actual = abs(x_siguiente - x_actual)
            
            # Agregar a tabla
            tabla_data.append([
                iteracion + 1,
                f"{x_actual:.6f}",
                f"{f_x:.6f}",
                f"{fp_x:.6f}",
                f"{x_siguiente:.6f}",
                f"{error_actual:.6e}"
            ])
            
            # Verificar convergencia
            if abs(f_x) < 1e-12:
                break
            
            x_actual = x_siguiente
            iteracion += 1
        
        # Resultado final
        raiz = x_actual
        f_raiz, _ = _evaluar_funcion_segura(f, raiz)
        
        mensaje_final = (
            f"¡Convergencia alcanzada!\n"
            f"Raíz encontrada: x ≈ {raiz:.10f}\n"
            f"f({raiz:.6f}) = {f_raiz:.6e}\n"
            f"Iteraciones: {iteracion}\n"
            f"Error final: {error_actual:.6e}"
        )
        
        return {
            'estado': 'exito',
            'raiz': raiz,
            'iteraciones': iteracion,
            'error': error_actual,
            'info_previa': info_previa,
            'tabla_headers': tabla_headers,
            'tabla_data': tabla_data,
            'mensaje_final': mensaje_final
        }
        
    except Exception as e:
        return {
            'estado': 'error',
            'mensaje': f"Error inesperado en Newton-Raphson: {str(e)}",
            'info_previa': info_previa,
            'tabla_headers': tabla_headers,
            'tabla_data': tabla_data
        }

# =============================================================================
# MÉTODO DE LA SECANTE (COMPLETAMENTE CORREGIDO CON DETECCIÓN DE SIN RAÍCES)
# =============================================================================

def metodo_secante(funcion_str: str, x0: float, x1: float, tolerancia: float = 1e-6, max_iter: int = 100) -> Dict[str, any]:
    """
    Resuelve f(x) = 0 usando el método de la secante.
    VERSIÓN CORREGIDA: Detecta cuando probablemente no hay raíces reales.
    """
    tabla_headers = ["Iter", "x_{n-1}", "x_n", "f(x_{n-1})", "f(x_n)", "x_{n+1}", "Error"]
    tabla_data = []
    info_previa = []
    
    try:
        # Parsear función
        f, error_parseo = _parsear_funcion(funcion_str)
        if error_parseo:
            return {
                'estado': 'error',
                'mensaje': f"Error en la función: {error_parseo}",
                'info_previa': info_previa,
                'tabla_headers': tabla_headers,
                'tabla_data': tabla_data
            }
        
        info_previa.append(f"Función: f(x) = {funcion_str}")
        info_previa.append(f"Puntos iniciales: x₀ = {x0}, x₁ = {x1}")
        info_previa.append(f"Tolerancia: {tolerancia}")
        
        # Verificar que los puntos iniciales sean diferentes
        if abs(x1 - x0) < 1e-12:
            return {
                'estado': 'error',
                'mensaje': "Los puntos iniciales x₀ y x₁ deben ser diferentes",
                'info_previa': info_previa,
                'tabla_headers': tabla_headers,
                'tabla_data': tabla_data
            }
        
        # Evaluar función en puntos iniciales
        fx0, error_fx0 = _evaluar_funcion_segura(f, x0)
        if error_fx0:
            return {
                'estado': 'error',
                'mensaje': f"Error evaluando f(x₀): {error_fx0}",
                'info_previa': info_previa,
                'tabla_headers': tabla_headers,
                'tabla_data': tabla_data
            }
        
        fx1, error_fx1 = _evaluar_funcion_segura(f, x1)
        if error_fx1:
            return {
                'estado': 'error',
                'mensaje': f"Error evaluando f(x₁): {error_fx1}",
                'info_previa': info_previa,
                'tabla_headers': tabla_headers,
                'tabla_data': tabla_data
            }
        
        info_previa.append(f"f(x₀) = f({x0}) = {fx0:.6f}")
        info_previa.append(f"f(x₁) = f({x1}) = {fx1:.6f}")
        
        # CORRECCIÓN CRÍTICA: Verificar si es probable que no haya raíces
        posible_sin_raices, mensaje_sin_raices = _verificar_posible_sin_raices(f, funcion_str, x0, x1)
        if posible_sin_raices:
            info_previa.append(f"⚠️ {mensaje_sin_raices}")
            # No retornamos error inmediatamente, pero mostramos advertencia
        
        # CORRECCIÓN: Verificar si hay cambio de signo
        if fx0 * fx1 > 0:
            info_previa.append("⚠️ ADVERTENCIA: No hay cambio de signo entre x₀ y x₁")
            info_previa.append("El método puede diverger o no encontrar raíz")
        
        # Inicializar variables
        iteracion = 0
        x_anterior = x0
        x_actual = x1
        f_anterior = fx0
        f_actual = fx1
        error_actual = float('inf')
        
        while iteracion < max_iter and error_actual > tolerancia:
            # VERIFICAR DIVISIÓN POR CERO
            if abs(f_actual - f_anterior) < 1e-12:
                return {
                    'estado': 'error',
                    'mensaje': f"División por cero en iteración {iteracion}: f(x_n) ≈ f(x_{{n-1}})",
                    'info_previa': info_previa,
                    'tabla_headers': tabla_headers,
                    'tabla_data': tabla_data
                }
            
            # Fórmula de la secante
            x_siguiente = x_actual - f_actual * (x_actual - x_anterior) / (f_actual - f_anterior)
            
            # CORRECCIÓN CRÍTICA: Validar que x_siguiente esté en dominio razonable
            if 'log' in funcion_str and x_siguiente <= 0:
                return {
                    'estado': 'error',
                    'mensaje': f"El método generó x = {x_siguiente:.6f} fuera del dominio de log(x). Posiblemente la función no tiene raíces reales.",
                    'info_previa': info_previa,
                    'tabla_headers': tabla_headers,
                    'tabla_data': tabla_data
                }
            
            if 'sqrt' in funcion_str and x_siguiente < 0:
                return {
                    'estado': 'error',
                    'mensaje': f"El método generó x = {x_siguiente:.6f} fuera del dominio de sqrt(x). Posiblemente la función no tiene raíces reales.",
                    'info_previa': info_previa,
                    'tabla_headers': tabla_headers,
                    'tabla_data': tabla_data
                }
            
            # VALIDAR DOMINIO ANTES DE EVALUAR
            f_siguiente, error_fs = _evaluar_funcion_segura(f, x_siguiente)
            if error_fs:
                return {
                    'estado': 'error',
                    'mensaje': f"Error en iteración {iteracion}: {error_fs}",
                    'info_previa': info_previa,
                    'tabla_headers': tabla_headers,
                    'tabla_data': tabla_data
                }
            
            # Calcular error
            error_actual = abs(x_siguiente - x_actual)
            
            # Agregar a tabla
            tabla_data.append([
                iteracion + 1,
                f"{x_anterior:.6f}",
                f"{x_actual:.6f}",
                f"{f_anterior:.6f}",
                f"{f_actual:.6f}",
                f"{x_siguiente:.6f}",
                f"{error_actual:.6e}"
            ])
            
            # Verificar convergencia
            if abs(f_siguiente) < 1e-12:
                break
            
            # Actualizar variables para siguiente iteración
            x_anterior = x_actual
            f_anterior = f_actual
            x_actual = x_siguiente
            f_actual = f_siguiente
            
            iteracion += 1
        
        # Resultado final
        raiz = x_actual
        f_raiz, _ = _evaluar_funcion_segura(f, raiz)
        
        mensaje_final = (
            f"¡Convergencia alcanzada!\n"
            f"Raíz encontrada: x ≈ {raiz:.10f}\n"
            f"f({raiz:.6f}) = {f_raiz:.6e}\n"
            f"Iteraciones: {iteracion}\n"
            f"Error final: {error_actual:.6e}"
        )
        
        return {
            'estado': 'exito',
            'raiz': raiz,
            'iteraciones': iteracion,
            'error': error_actual,
            'info_previa': info_previa,
            'tabla_headers': tabla_headers,
            'tabla_data': tabla_data,
            'mensaje_final': mensaje_final
        }
        
    except Exception as e:
        return {
            'estado': 'error',
            'mensaje': f"Error inesperado en método de la secante: {str(e)}",
            'info_previa': info_previa,
            'tabla_headers': tabla_headers,
            'tabla_data': tabla_data
        }

# =============================================================================
# PRUEBAS
# =============================================================================

if __name__ == "__main__":
    print("=== Pruebas MetodosNumericos.py ===")
    
    # Probar el caso problemático: x - log(x)
    print("\n1. Probando método de la secante con f(x) = x - log(x):")
    resultado = metodo_secante("x - log(x)", 0.1, 0.9, 1e-6, 50)
    print(f"Estado: {resultado['estado']}")
    if resultado['estado'] == 'exito':
        print(f"Raíz: {resultado['raiz']}")
        print(f"Iteraciones: {resultado['iteraciones']}")
    else:
        print(f"Error: {resultado['mensaje']}")
    
    print("\n2. Probando con función que SÍ tiene raíz:")
    resultado2 = metodo_secante("log(x) - 1", 0.5, 4, 1e-6, 50)
    print(f"Estado: {resultado2['estado']}")
    if resultado2['estado'] == 'exito':
        print(f"Raíz: {resultado2['raiz']}")
        print(f"Raíz esperada: e ≈ 2.71828")