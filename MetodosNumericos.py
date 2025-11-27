import math
from typing import Dict, List, Callable, Any
import sympy as sp

def _crear_funcion_segura(funcion_str: str) -> Callable[[float], float]:
    x = sp.Symbol('x')
    try:
        funcion_str_limpia = funcion_str.replace('^', '**')
        expr = sp.sympify(funcion_str_limpia)
        f_lambda = sp.lambdify(x, expr, modules=['math', 'mpmath', 'sympy'])
        
        def funcion_evaluada(val_x: float) -> float:
            try:
                res = f_lambda(val_x)
                if isinstance(res, complex):
                    raise ValueError("Resultado complejo no soportado")
                return float(res)
            except ZeroDivisionError:
                return float('inf')
            except Exception as e:
                raise ValueError(f"Error evaluando en {val_x}: {e}")
                
        return funcion_evaluada
    except Exception as e:
        raise ValueError(f"Error al procesar la función: {e}")

def _crear_funcion_y_derivada_segura(funcion_str: str) -> Dict[str, Any]:
    x = sp.Symbol('x')
    try:
        funcion_str_sympy = funcion_str.replace('^', '**')
        f_sym = sp.sympify(funcion_str_sympy)
        df_sym = sp.diff(f_sym, x)
        
        f_lambda = sp.lambdify(x, f_sym, modules=['math', 'mpmath', 'sympy'])
        df_lambda = sp.lambdify(x, df_sym, modules=['math', 'mpmath', 'sympy'])
        
        return {
            'f': f_lambda,
            'df': df_lambda,
            'f_str': sp.latex(f_sym),
            'df_str': sp.latex(df_sym)
        }
        
    except Exception as e:
        raise ValueError(f"Error procesando la función con SymPy: {e}")

def metodo_biseccion(funcion_str: str, a: float, b: float, tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    info_previa = []
    tabla_data = []
    
    try:
        f = _crear_funcion_segura(funcion_str)
        fa, fb = f(a), f(b)
        info_previa.append(f"Intervalo inicial: [{a}, {b}]")
        info_previa.append(f"f(a) = {fa:.6e}")
        info_previa.append(f"f(b) = {fb:.6e}")
        
        if fa * fb >= 0:
            return {'estado': 'error', 'mensaje': 'El método no aplica: f(a) y f(b) deben tener signos opuestos.', 'info_previa': info_previa}
    except Exception as e:
         return {'estado': 'error', 'mensaje': str(e), 'info_previa': info_previa}

    xr_anterior = a 
    xr_nuevo = (a + b) / 2
    error = 1.0
    
    tabla_headers = ["Iter", "a", "b", "f(a)", "f(b)", "xr", "f(xr)", "Error"]
    
    for i in range(max_iter):
        fxr = f(xr_nuevo)
        
        if i > 0:
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
            
        if fa * fxr < 0:
            b, fb = xr_nuevo, fxr
        else:
            a, fa = xr_nuevo, fxr
            
        xr_anterior = xr_nuevo
        xr_nuevo = (a + b) / 2
        
    return {'estado': 'max_iter', 'mensaje': f'Se alcanzó el máximo de {max_iter} iteraciones.', 
            'raiz': xr_nuevo, 'iteraciones': max_iter, 'error': error,
            'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data}

def metodo_falsa_posicion(funcion_str: str, a: float, b: float, tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    info_previa = []
    tabla_data = []
    try:
        f = _crear_funcion_segura(funcion_str)
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
    
    for i in range(max_iter):
        fxr = f(xr_nuevo)
        
        if i > 0:
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
            
        if fa * fxr < 0:
            b, fb = xr_nuevo, fxr
        else:
            a, fa = xr_nuevo, fxr
            
        xr_anterior = xr_nuevo
        
        if abs(fa - fb) < 1e-15:
             info_previa.append("Advertencia: Diferencia entre f(a) y f(b) muy pequeña, terminando.")
             break
             
        xr_nuevo = b - (fb * (a - b)) / (fa - fb)
        
    return {'estado': 'max_iter', 'mensaje': f'Se alcanzó el máximo de {max_iter} iteraciones.', 
            'raiz': xr_nuevo, 'iteraciones': max_iter, 'error': error,
            'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data}

def metodo_newton_raphson(funcion_str: str, x0: float, tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    info_previa = []
    tabla_data = []
    try:
        helpers = _crear_funcion_y_derivada_segura(funcion_str)
        f = helpers['f']
        df = helpers['df']
        info_previa.append(f"Función f(x) = {helpers['f_str']}")
        info_previa.append(f"Derivada f'(x) = {helpers['df_str']}")
        info_previa.append(f"Punto inicial x0 = {x0}")
        
    except Exception as e:
         return {'estado': 'error', 'mensaje': str(e), 'info_previa': info_previa}

    xi = x0
    error = 1.0
    
    tabla_headers = ["Iter", "xi", "f(xi)", "f'(xi)", "xi+1", "Error"]
    
    for i in range(max_iter):
        try:
            f_xi = f(xi)
            df_xi = df(xi)
        except Exception as e:
            return {'estado': 'error', 'mensaje': f"Error evaluando función: {e}", 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data}
        
        if abs(df_xi) < 1e-10:
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
    try:
        f = _crear_funcion_segura(funcion_str)
        info_previa.append(f"Punto inicial x0 = {x0}")
        info_previa.append(f"Punto inicial x1 = {x1}")
    except Exception as e:
         return {'estado': 'error', 'mensaje': str(e), 'info_previa': info_previa}

    error = 1.0
    
    tabla_headers = ["Iter", "x_i-1", "x_i", "f(x_i-1)", "f(x_i)", "x_i+1", "Error"]
    
    for i in range(max_iter):
        f_x0 = f(x0)
        f_x1 = f(x1)
        
        denominador = f_x0 - f_x1
        if abs(denominador) < 1e-10:
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