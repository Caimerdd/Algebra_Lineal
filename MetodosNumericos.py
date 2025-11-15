import math
from typing import Dict, List, Callable, Any
<<<<<<< HEAD
import sympy as sp
=======
import sympy as sp  # Necesario para calcular la derivada en Newton
>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97

# Diccionario de funciones seguras
SAFE_MATH_FUNCTIONS = {
    'cos': math.cos,
    'sin': math.sin,
    'tan': math.tan,
    'acos': math.acos,
    'asin': math.asin,
    'atan': math.atan,
    'exp': math.exp,
    'log': math.log,
    'log10': math.log10,
    'sqrt': math.sqrt,
    'pow': math.pow,
    'pi': math.pi,
    'e': math.e,
    'abs': abs,
}


def _crear_funcion_segura(funcion_str: str) -> Callable[[float], float]:
    if any(c in funcion_str for c in '[]_{}'):
        raise ValueError("La función contiene caracteres no permitidos.")
    code = compile(funcion_str, "<string>", "eval")

    def funcion_evaluada(x: float) -> float:
        try:
            return eval(code, {"__builtins__": {}}, {**SAFE_MATH_FUNCTIONS, 'x': x})
        except ZeroDivisionError:
            return float('inf')
        except Exception as e:
            raise ValueError(f"Error al evaluar f({x}): {e}")

    return funcion_evaluada


def _crear_funcion_y_derivada_segura(funcion_str: str) -> Dict[str, Any]:
    x = sp.Symbol('x')
    try:
        funcion_str_sympy = funcion_str.replace('^', '**')
        f_sym = sp.sympify(funcion_str_sympy)
        df_sym = sp.diff(f_sym, x)

        f_lambda = sp.lambdify(x, f_sym, modules='math')
        df_lambda = sp.lambdify(x, df_sym, modules='math')

        return {
            'f': f_lambda,
            'df': df_lambda,
            'f_str': str(f_sym),
            'df_str': str(df_sym)
        }

    except Exception as e:
        raise ValueError(f"Error procesando la función con SymPy: {e}")


# ==========================================================
# MÉTODOS DE INTERVALO (BISECCIÓN Y FALSA POSICIÓN)
# ==========================================================

<<<<<<< HEAD
def metodo_biseccion(funcion_str: str, a: float, b: float, tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    # Lista para info de texto (antes de la tabla)
    info_previa = []
    # Lista para los datos de la tabla
    tabla_data = []
    
    try:
        f = _crear_funcion_segura(funcion_str.replace('math.', ''))
        fa, fb = f(a), f(b)
        info_previa.append(f"Intervalo inicial: [{a}, {b}]")
        info_previa.append(f"f(a) = {fa:.6e}")
        info_previa.append(f"f(b) = {fb:.6e}")
        
        if fa * fb >= 0:
            return {'estado': 'error', 'mensaje': 'El método no aplica: f(a) y f(b) deben tener signos opuestos.', 'info_previa': info_previa}
    except Exception as e:
         return {'estado': 'error', 'mensaje': str(e), 'info_previa': info_previa}
=======
def metodo_biseccion(funcion_str: str, a: float, b: float,
                     tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    pasos: List[str] = []
    try:
        f = _crear_funcion_segura(funcion_str.replace('math.', ''))
        fa, fb = f(a), f(b)
        pasos.append(f"Intervalo inicial: [{a}, {b}]")
        pasos.append(f"f(a) = {fa:.6e}")
        pasos.append(f"f(b) = {fb:.6e}")
>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97

        if fa * fb >= 0:
            pasos.append("Condición f(a) * f(b) < 0 no se cumple.")
            return {
                'estado': 'error',
                'mensaje': 'El método no aplica: f(a) y f(b) deben tener signos opuestos.',
                'pasos': pasos
            }
    except Exception as e:
        return {'estado': 'error', 'mensaje': str(e), 'pasos': pasos}

    xr_anterior = a
    error = 1.0
<<<<<<< HEAD
    
    # Definimos los encabezados de la tabla
    tabla_headers = ["Iter", "a", "b", "f(a)", "f(b)", "xr", "f(xr)", "Error"]
    
=======

    pasos.append("\n--- Iniciando iteraciones (Bisección) ---")

    header = (
        f"| {'Iter':^8} | {'a':^22} | {'b':^22} | {'f(a)':^24} | "
        f"{'f(b)':^24} | {'xr':^22} | {'f(xr)':^24} | {'Error':^24} |"
    )
    separador = "-" * len(header)

    pasos.append(separador)
    pasos.append(header)
    pasos.append(separador)

>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97
    for i in range(max_iter):
        # xr se calcula DENTRO del ciclo
        xr_nuevo = (a + b) / 2.0
        fxr = f(xr_nuevo)

        # Error relativo
        if i > 0:
<<<<<<< HEAD
            if abs(xr_nuevo) < 1e-10: error = abs(xr_nuevo - xr_anterior)
            else: error = abs((xr_nuevo - xr_anterior) / xr_nuevo)
        
        # Añadimos los NÚMEROS a la lista de datos
        fila_datos = [
            i + 1, a, b, fa, fb, xr_nuevo, fxr,
            error if i > 0 else "N/A"
        ]
        tabla_data.append(fila_datos)

        if i > 0 and error < tolerancia:
            return {'estado': 'exito', 'raiz': xr_nuevo, 'iteraciones': i+1, 'error': error, 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data,
                    'mensaje_final': f"Convergencia alcanzada en la iteración {i+1}."}
            
        if abs(fxr) < 1e-14:
            return {'estado': 'exito', 'raiz': xr_nuevo, 'iteraciones': i+1, 'error': 0.0, 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data,
                    'mensaje_final': f"Raíz exacta encontrada en la iteración {i+1}."}
            
=======
            if abs(xr_nuevo) < 1e-10:
                error = abs(xr_nuevo - xr_anterior)
            else:
                error = abs((xr_nuevo - xr_anterior) / xr_nuevo)
            error_str = f"{error:^24.5e}"
        else:
            error_str = f"{'N/A':^24}"

        paso_str = (
            f"| {i+1:^8d} | {a:^22.8f} | {b:^22.8f} | {fa:^24.5e} | {fb:^24.5e} | "
            f"{xr_nuevo:^22.8f} | {fxr:^24.5e} | {error_str} |"
        )
        pasos.append(paso_str)

        # Criterio de paro: error pequeño Y |f(xr)| pequeño
        if i > 0 and error < tolerancia and abs(fxr) < tolerancia:
            pasos.append(separador)
            pasos.append(f"\nConvergencia alcanzada en la iteración {i+1}.")
            return {
                'estado': 'exito',
                'raiz': xr_nuevo,
                'iteraciones': i+1,
                'error': error,
                'pasos': pasos
            }

        # Criterio de raíz prácticamente exacta
        if abs(fxr) < 1e-14:
            pasos.append(separador)
            pasos.append(f"\nRaíz exacta encontrada en la iteración {i+1}.")
            return {
                'estado': 'exito',
                'raiz': xr_nuevo,
                'iteraciones': i+1,
                'error': 0.0,
                'pasos': pasos
            }

        # Actualizar intervalo
>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97
        if fa * fxr < 0:
            b, fb = xr_nuevo, fxr
        else:
            a, fa = xr_nuevo, fxr
<<<<<<< HEAD
            
        xr_anterior = xr_nuevo
        xr_nuevo = (a + b) / 2
        
    return {'estado': 'max_iter', 'mensaje': f'Se alcanzó el máximo de {max_iter} iteraciones.', 
            'raiz': xr_nuevo, 'iteraciones': max_iter, 'error': error,
            'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data}

def metodo_falsa_posicion(funcion_str: str, a: float, b: float, tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    info_previa = []
    tabla_data = []
    try:
        f = _crear_funcion_segura(funcion_str.replace('math.', ''))
        fa, fb = f(a), f(b)
        info_previa.append(f"Intervalo inicial: [{a}, {b}]")
        info_previa.append(f"f(a) = {fa:.6e}")
        info_previa.append(f"f(b) = {fb:.6e}")
        
        if fa * fb >= 0:
            return {'estado': 'error', 'mensaje': 'El método requiere que f(a) y f(b) tengan signos opuestos.', 'info_previa': info_previa}
    except Exception as e:
         return {'estado': 'error', 'mensaje': str(e), 'info_previa': info_previa}

    if abs(fa - fb) < 1e-15:
         return {'estado': 'error', 'mensaje': 'División por cero: f(a) es casi igual a f(b).', 'info_previa': info_previa}

    xr_anterior = a 
    xr_nuevo = b - (fb * (a - b)) / (fa - fb)
    error = 1.0
    
    tabla_headers = ["Iter", "a", "b", "f(a)", "f(b)", "xr", "f(xr)", "Error"]
    
=======

        xr_anterior = xr_nuevo

    pasos.append(separador)
    return {
        'estado': 'max_iter',
        'mensaje': f'Se alcanzó el máximo de {max_iter} iteraciones.',
        'raiz': xr_nuevo,
        'iteraciones': max_iter,
        'error': error,
        'pasos': pasos
    }


def metodo_falsa_posicion(funcion_str: str, a: float, b: float,
                          tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    pasos: List[str] = []
    try:
        f = _crear_funcion_segura(funcion_str.replace('math.', ''))
        fa, fb = f(a), f(b)
        pasos.append(f"Intervalo inicial: [{a}, {b}]")
        pasos.append(f"f(a) = {fa:.6e}")
        pasos.append(f"f(b) = {fb:.6e}")

        if fa * fb >= 0:
            pasos.append("Error: f(a) y f(b) deben tener signos opuestos.")
            return {
                'estado': 'error',
                'mensaje': 'El método requiere que f(a) y f(b) tengan signos opuestos.',
                'pasos': pasos
            }
    except Exception as e:
        return {'estado': 'error', 'mensaje': str(e), 'pasos': pasos}

    pasos.append("\n--- Iniciando iteraciones (Falsa Posición) ---")

    header = (
        f"| {'Iter':^8} | {'a':^22} | {'b':^22} | {'f(a)':^24} | "
        f"{'f(b)':^24} | {'xr':^22} | {'f(xr)':^24} | {'Error':^24} |"
    )
    separador = "-" * len(header)

    pasos.append(separador)
    pasos.append(header)
    pasos.append(separador)

    xr_anterior = a
    error = 1.0

>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97
    for i in range(max_iter):
        # Evitar división por cero en la fórmula
        if abs(fa - fb) < 1e-15:
            pasos.append("\nAdvertencia: Diferencia entre f(a) y f(b) muy pequeña, terminando.")
            break

        # xr se calcula DENTRO del ciclo
        xr_nuevo = b - (fb * (a - b)) / (fa - fb)
        fxr = f(xr_nuevo)

        # Error relativo
        if i > 0:
<<<<<<< HEAD
            if abs(xr_nuevo) < 1e-10: error = abs(xr_nuevo - xr_anterior)
            else: error = abs((xr_nuevo - xr_anterior) / xr_nuevo)
        
        fila_datos = [
            i + 1, a, b, fa, fb, xr_nuevo, fxr,
            error if i > 0 else "N/A"
        ]
        tabla_data.append(fila_datos)

        if i > 0 and error < tolerancia:
            return {'estado': 'exito', 'raiz': xr_nuevo, 'iteraciones': i+1, 'error': error, 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data,
                    'mensaje_final': f"Convergencia alcanzada en la iteración {i+1}."}
            
        if abs(fxr) < 1e-14:
            return {'estado': 'exito', 'raiz': xr_nuevo, 'iteraciones': i+1, 'error': 0.0, 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data,
                    'mensaje_final': f"Raíz exacta encontrada en la iteración {i+1}."}
            
=======
            if abs(xr_nuevo) < 1e-10:
                error = abs(xr_nuevo - xr_anterior)
            else:
                error = abs((xr_nuevo - xr_anterior) / xr_nuevo)
            error_str = f"{error:^24.5e}"
        else:
            error_str = f"{'N/A':^24}"

        paso_str = (
            f"| {i+1:^8d} | {a:^22.8f} | {b:^22.8f} | {fa:^24.5e} | {fb:^24.5e} | "
            f"{xr_nuevo:^22.8f} | {fxr:^24.5e} | {error_str} |"
        )
        pasos.append(paso_str)

        # Criterio de paro: error pequeño Y |f(xr)| pequeño
        if i > 0 and error < tolerancia and abs(fxr) < tolerancia:
            pasos.append(separador)
            pasos.append(f"\nConvergencia alcanzada en la iteración {i+1}.")
            return {
                'estado': 'exito',
                'raiz': xr_nuevo,
                'iteraciones': i+1,
                'error': error,
                'pasos': pasos
            }

        # Criterio de raíz prácticamente exacta
        if abs(fxr) < 1e-14:
            pasos.append(separador)
            pasos.append(f"\nRaíz exacta encontrada en la iteración {i+1}.")
            return {
                'estado': 'exito',
                'raiz': xr_nuevo,
                'iteraciones': i+1,
                'error': 0.0,
                'pasos': pasos
            }

        # Actualizar intervalo
>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97
        if fa * fxr < 0:
            b, fb = xr_nuevo, fxr
        else:
            a, fa = xr_nuevo, fxr

        xr_anterior = xr_nuevo
<<<<<<< HEAD
        
        if abs(fa - fb) < 1e-15:
             info_previa.append("Advertencia: Diferencia entre f(a) y f(b) muy pequeña, terminando.")
             break
             
        xr_nuevo = b - (fb * (a - b)) / (fa - fb)
        
    return {'estado': 'max_iter', 'mensaje': f'Se alcanzó el máximo de {max_iter} iteraciones.', 
            'raiz': xr_nuevo, 'iteraciones': max_iter, 'error': error,
            'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data}
=======

    pasos.append(separador)
    return {
        'estado': 'max_iter',
        'mensaje': f'Se alcanzó el máximo de {max_iter} iteraciones.',
        'raiz': xr_nuevo,
        'iteraciones': max_iter,
        'error': error,
        'pasos': pasos
    }
>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97


<<<<<<< HEAD
def metodo_newton_raphson(funcion_str: str, x0: float, tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    info_previa = []
    tabla_data = []
=======
# ==========================================================
# MÉTODOS ABIERTOS (NEWTON-RAPHSON Y SECANTE)
# ==========================================================

def metodo_newton_raphson(funcion_str: str, x0: float,
                          tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    pasos: List[str] = []
>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97
    try:
        helpers = _crear_funcion_y_derivada_segura(funcion_str)
        f = helpers['f']
        df = helpers['df']
<<<<<<< HEAD
        info_previa.append(f"Función f(x) = {helpers['f_str']}")
        info_previa.append(f"Derivada f'(x) = {helpers['df_str']}")
        info_previa.append(f"Punto inicial x0 = {x0}")
        
    except Exception as e:
         return {'estado': 'error', 'mensaje': str(e), 'info_previa': info_previa}

    xi = x0
    error = 1.0
    
    tabla_headers = ["Iter", "xi", "f(xi)", "f'(xi)", "xi+1", "Error"]
    
=======
        pasos.append(f"Función f(x) = {helpers['f_str']}")
        pasos.append(f"Derivada f'(x) = {helpers['df_str']}")
        pasos.append(f"Punto inicial x0 = {x0}")

    except Exception as e:
        return {'estado': 'error', 'mensaje': str(e), 'pasos': pasos}

    xi = x0
    error = 1.0
    x_nuevo = x0

    pasos.append("\n--- Iniciando iteraciones (Newton-Raphson) ---")

    header_f_prime = "f'(xi)"
    header = (
        f"| {'Iter':^8} | {'xi':^22} | {'f(xi)':^24} | {header_f_prime:^24} | "
        f"{'xi+1':^22} | {'Error':^24} |"
    )
    separador = "-" * len(header)

    pasos.append(separador)
    pasos.append(header)
    pasos.append(separador)

>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97
    for i in range(max_iter):
        f_xi = f(xi)
        df_xi = df(xi)

        if abs(df_xi) < 1e-10:
<<<<<<< HEAD
            return {'estado': 'error', 'mensaje': f"División por cero: La derivada es cero en x = {xi}", 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data}
            
        x_nuevo = xi - (f_xi / df_xi)
        
        if abs(x_nuevo) < 1e-10: error = abs(x_nuevo - xi)
        else: error = abs((x_nuevo - xi) / x_nuevo)
            
        fila_datos = [
            i + 1, xi, f_xi, df_xi, x_nuevo,
            error if i > 0 else "N/A"
        ]
        tabla_data.append(fila_datos)

        if i > 0 and error < tolerancia:
            return {'estado': 'exito', 'raiz': x_nuevo, 'iteraciones': i+1, 'error': error, 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data,
                    'mensaje_final': f"Convergencia alcanzada en la iteración {i+1}."}
            
        if abs(f_xi) < 1e-14: 
            return {'estado': 'exito', 'raiz': xi, 'iteraciones': i+1, 'error': 0.0, 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data,
                    'mensaje_final': f"Raíz exacta encontrada en la iteración {i+1}."}
        
        xi = x_nuevo 
        
    return {'estado': 'max_iter', 'mensaje': f'Se alcanzó el máximo de {max_iter} iteraciones.', 
            'raiz': xi, 'iteraciones': max_iter, 'error': error,
            'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data}


def metodo_secante(funcion_str: str, x0: float, x1: float, tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    info_previa = []
    tabla_data = []
=======
            pasos.append(separador)
            pasos.append(f"\nError: Derivada cero encontrada en f'({xi:.6f}) = {df_xi:.6e}.")
            return {
                'estado': 'error',
                'mensaje': f"División por cero: La derivada es cero en x = {xi}",
                'pasos': pasos
            }

        x_nuevo = xi - (f_xi / df_xi)

        if abs(x_nuevo) < 1e-10:
            error = abs(x_nuevo - xi)
        else:
            error = abs((x_nuevo - xi) / x_nuevo)

        error_str = f"{error:^24.5e}" if i > 0 else f"{'N/A':^24}"

        paso_str = (
            f"| {i+1:^8d} | {xi:^22.8f} | {f_xi:^24.5e} | {df_xi:^24.5e} | "
            f"{x_nuevo:^22.8f} | {error_str} |"
        )
        pasos.append(paso_str)

        if i > 0 and error < tolerancia:
            pasos.append(separador)
            pasos.append(f"\nConvergencia alcanzada en la iteración {i+1}.")
            return {
                'estado': 'exito',
                'raiz': x_nuevo,
                'iteraciones': i+1,
                'error': error,
                'pasos': pasos
            }

        if abs(f_xi) < 1e-14:
            pasos.append(separador)
            pasos.append(f"\nRaíz exacta encontrada en la iteración {i+1} (xi={xi}).")
            return {
                'estado': 'exito',
                'raiz': xi,
                'iteraciones': i+1,
                'error': 0.0,
                'pasos': pasos
            }

        xi = x_nuevo

    pasos.append(separador)
    return {
        'estado': 'max_iter',
        'mensaje': f'Se alcanzó el máximo de {max_iter} iteraciones.',
        'raiz': xi,
        'iteraciones': max_iter,
        'error': error,
        'pasos': pasos
    }


def metodo_secante(funcion_str: str, x0: float, x1: float,
                   tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    pasos: List[str] = []
>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97
    try:
        f = _crear_funcion_segura(funcion_str.replace('math.', ''))
        info_previa.append(f"Punto inicial x0 = {x0}")
        info_previa.append(f"Punto inicial x1 = {x1}")
    except Exception as e:
<<<<<<< HEAD
         return {'estado': 'error', 'mensaje': str(e), 'info_previa': info_previa}

    error = 1.0
    
    tabla_headers = ["Iter", "x_i-1", "x_i", "f(x_i-1)", "f(x_i)", "x_i+1", "Error"]
    
=======
        return {'estado': 'error', 'mensaje': str(e), 'pasos': pasos}

    error = 1.0
    x_nuevo = x1

    pasos.append("\n--- Iniciando iteraciones (Secante) ---")

    header = (
        f"| {'Iter':^8} | {'x_i-1':^20} | {'x_i':^20} | {'f(x_i-1)':^24} | "
        f"{'f(x_i)':^24} | {'x_i+1':^20} | {'Error':^24} |"
    )
    separador = "-" * len(header)

    pasos.append(separador)
    pasos.append(header)
    pasos.append(separador)

>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97
    for i in range(max_iter):
        f_x0 = f(x0)
        f_x1 = f(x1)

        denominador = f_x0 - f_x1
        if abs(denominador) < 1e-10:
<<<<<<< HEAD
            return {'estado': 'error', 'mensaje': "División por cero: f(x0) y f(x1) son demasiado similares.", 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data}
            
        x_nuevo = x1 - (f_x1 * (x0 - x1)) / denominador
        
        if abs(x_nuevo) < 1e-10: error = abs(x_nuevo - x1)
        else: error = abs((x_nuevo - x1) / x_nuevo)
            
        fila_datos = [
            i + 1, x0, x1, f_x0, f_x1, x_nuevo,
            error if i > 0 else "N/A"
        ]
        tabla_data.append(fila_datos)

        if i > 0 and error < tolerancia:
            return {'estado': 'exito', 'raiz': x_nuevo, 'iteraciones': i+1, 'error': error, 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data,
                    'mensaje_final': f"Convergencia alcanzada en la iteración {i+1}."}
            
        if abs(f(x_nuevo)) < 1e-14:
            return {'estado': 'exito', 'raiz': x_nuevo, 'iteraciones': i+1, 'error': 0.0, 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data,
                    'mensaje_final': f"Raíz exacta encontrada en la iteración {i+1}."}
        
        x0 = x1
        x1 = x_nuevo
        
    return {'estado': 'max_iter', 'mensaje': f'Se alcanzó el máximo de {max_iter} iteraciones.', 
            'raiz': x1, 'iteraciones': max_iter, 'error': error,
            'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data}
=======
            pasos.append(separador)
            pasos.append("\nError: Denominador cero (f(x_i-1) - f(x_i) ≈ 0).")
            return {
                'estado': 'error',
                'mensaje': "División por cero: f(x0) y f(x1) son demasiado similares.",
                'pasos': pasos
            }

        x_nuevo = x1 - (f_x1 * (x0 - x1)) / denominador

        if abs(x_nuevo) < 1e-10:
            error = abs(x_nuevo - x1)
        else:
            error = abs((x_nuevo - x1) / x_nuevo)

        error_str = f"{error:^24.5e}" if i > 0 else f"{'N/A':^24}"

        paso_str = (
            f"| {i+1:^8d} | {x0:^20.8f} | {x1:^20.8f} | {f_x0:^24.5e} | "
            f"{f_x1:^24.5e} | {x_nuevo:^20.8f} | {error_str} |"
        )
        pasos.append(paso_str)

        if i > 0 and error < tolerancia:
            pasos.append(separador)
            pasos.append(f"\nConvergencia alcanzada en la iteración {i+1}.")
            return {
                'estado': 'exito',
                'raiz': x_nuevo,
                'iteraciones': i+1,
                'error': error,
                'pasos': pasos
            }

        if abs(f(x_nuevo)) < 1e-14:
            pasos.append(separador)
            pasos.append("\nRaíz exacta encontrada en la iteración {i+1}.")
            return {
                'estado': 'exito',
                'raiz': x_nuevo,
                'iteraciones': i+1,
                'error': 0.0,
                'pasos': pasos
            }

        x0 = x1
        x1 = x_nuevo

    pasos.append(separador)
    return {
        'estado': 'max_iter',
        'mensaje': f'Se alcanzó el máximo de {max_iter} iteraciones.',
        'raiz': x1,
        'iteraciones': max_iter,
        'error': error,
        'pasos': pasos
    }
>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97
