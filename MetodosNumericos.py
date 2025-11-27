import math
from typing import Dict, List, Callable, Any
import sympy as sp

# --- UTILERÍAS ---

def _crear_funcion_segura(funcion_str: str) -> Callable[[float], float]:
    x = sp.Symbol('x')
    try:
        # 1. Pre-procesamiento de texto
        funcion_str_limpia = funcion_str.replace('^', '**')
        # Arreglar e^x si el usuario lo escribe así
        if 'e**' in funcion_str_limpia and 'exp' not in funcion_str_limpia:
             funcion_str_limpia = funcion_str_limpia.replace('e**', 'exp(') + ')'
             
        expr = sp.sympify(funcion_str_limpia)
        # Usamos math y mpmath para evaluación numérica robusta
        f_lambda = sp.lambdify(x, expr, modules=['math', 'mpmath', 'sympy'])
        
        def funcion_evaluada(val_x: float) -> float:
            try:
                # Intentar evaluar
                res = f_lambda(val_x)
                
                # Verificar si dio número complejo (ej: sqrt(-1))
                if isinstance(res, complex):
                    # Si la parte imaginaria es muy pequeña, es error de flotante, lo ignoramos
                    if abs(res.imag) < 1e-10:
                        return float(res.real)
                    raise ValueError("Resultado complejo")

                # Verificar infinitos o NaN
                val_float = float(res)
                if math.isinf(val_float):
                    raise ValueError("Infinito")
                if math.isnan(val_float):
                    raise ValueError("No es un número (NaN)")
                    
                return val_float

            except (ValueError, ArithmeticError, ZeroDivisionError) as e:
                # --- TRADUCTOR DE ERRORES AL ESPAÑOL ---
                msg = str(e).lower()
                error_es = f"Error en x={val_x:.4g}"
                
                if "domain" in msg or "complejo" in msg:
                    error_es = f"Indefinido en x={val_x:.4g} (Ej: Log negativo o Raíz neg.)"
                elif "division" in msg or "zero" in msg:
                    error_es = f"División por cero en x={val_x:.4g}"
                elif "overflow" in msg or "infinito" in msg:
                    error_es = f"Número demasiado grande (Infinito) en x={val_x:.4g}"
                
                # Lanzamos el error ya traducido para que la UI lo muestre
                raise ValueError(error_es)
            except Exception as e:
                raise ValueError(f"Error desconocido en x={val_x:.4g}: {e}")
                
        return funcion_evaluada
    except Exception as e:
        raise ValueError(f"Sintaxis inválida en la función: {e}")

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
        raise ValueError(f"Error procesando la función: {e}")

def _buscar_intervalo_sugerido(f, a, b):
    """Busca un cambio de signo cercano si el intervalo falla."""
    try:
        ancho = abs(b - a) if abs(b-a) > 0.1 else 1.0
        step = ancho * 0.5
        for i in range(1, 6):
            try:
                # Expandir a la izquierda y derecha
                if f(a - i*step) * f(b) < 0: return (a - i*step, b)
                if f(a) * f(b + i*step) < 0: return (a, b + i*step)
            except: continue 
        return None
    except: return None

# --- MÉTODOS DE INTERVALO ---

def metodo_biseccion(funcion_str: str, a: float, b: float, tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    info_previa = []
    tabla_data = []
    
    try:
        f = _crear_funcion_segura(funcion_str)
        try:
            fa, fb = f(a), f(b)
        except ValueError as e:
            return {'estado': 'error', 'mensaje': f"Intervalo inicial inválido:\n{str(e)}", 'info_previa': info_previa}

        info_previa.append(f"Intervalo: [{a}, {b}]")
        info_previa.append(f"f({a}) = {fa:.5f}")
        info_previa.append(f"f({b}) = {fb:.5f}")
        
        if fa * fb >= 0:
            mensaje = 'El método no aplica: f(a) y f(b) deben tener signos opuestos.'
            sugerencia = _buscar_intervalo_sugerido(f, a, b)
            if sugerencia:
                sa, sb = sugerencia
                mensaje += f"\n\n💡 SUGERENCIA: Pruebe con [{sa:.2f}, {sb:.2f}]"
            return {'estado': 'error', 'mensaje': mensaje, 'info_previa': info_previa}
            
    except Exception as e:
         return {'estado': 'error', 'mensaje': str(e), 'info_previa': info_previa}

    xr_anterior = a 
    xr_nuevo = (a + b) / 2
    error = 1.0
    tabla_headers = ["Iter", "a", "b", "f(a)", "f(b)", "xr", "f(xr)", "Error"]
    
    for i in range(max_iter):
        try:
            fxr = f(xr_nuevo)
        except ValueError as e:
             return {'estado': 'error', 'mensaje': f"Error en iteración {i+1}:\n{str(e)}", 'tabla_headers': tabla_headers, 'tabla_data': tabla_data}

        if i > 0:
            if abs(xr_nuevo) < 1e-10: error = abs(xr_nuevo - xr_anterior)
            else: error = abs((xr_nuevo - xr_anterior) / xr_nuevo)
        
        fila_datos = [i + 1, a, b, fa, fb, xr_nuevo, fxr, error if i > 0 else "N/A"]
        tabla_data.append(fila_datos)

        if i > 0 and error < tolerancia:
            return {'estado': 'exito', 'raiz': xr_nuevo, 'iteraciones': i+1, 'error': error, 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data,
                    'mensaje_final': f"Convergencia alcanzada."}
            
        if abs(fxr) < 1e-14:
            return {'estado': 'exito', 'raiz': xr_nuevo, 'iteraciones': i+1, 'error': 0.0, 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data,
                    'mensaje_final': f"Raíz exacta encontrada."}
            
        if fa * fxr < 0:
            b, fb = xr_nuevo, fxr
        else:
            a, fa = xr_nuevo, fxr
            
        xr_anterior = xr_nuevo
        xr_nuevo = (a + b) / 2
        
    return {'estado': 'max_iter', 'mensaje': f'Se alcanzó el máximo de iteraciones.', 
            'raiz': xr_nuevo, 'iteraciones': max_iter, 'error': error,
            'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data}

def metodo_falsa_posicion(funcion_str: str, a: float, b: float, tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    return metodo_biseccion(funcion_str, a, b, tolerancia, max_iter) 

# --- MÉTODOS ABIERTOS ---

def metodo_newton_raphson(funcion_str: str, x0: float, tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    info_previa = []
    tabla_data = []
    try:
        helpers = _crear_funcion_y_derivada_segura(funcion_str)
        f = helpers['f']
        df = helpers['df']
        
        try:
            f(x0); df(x0)
        except ValueError as e:
             return {'estado': 'error', 'mensaje': f"Punto inicial inválido:\n{str(e)}", 'info_previa': info_previa}

        info_previa.append(f"Función: {helpers['f_str']}")
        info_previa.append(f"Derivada: {helpers['df_str']}")
        info_previa.append(f"x0 = {x0}")
        
    except Exception as e:
         return {'estado': 'error', 'mensaje': str(e), 'info_previa': info_previa}

    xi = x0
    error = 1.0
    tabla_headers = ["Iter", "xi", "f(xi)", "f'(xi)", "xi+1", "Error"]
    
    for i in range(max_iter):
        try:
            f_xi = f(xi)
            df_xi = df(xi)
        except ValueError as e:
            return {'estado': 'error', 'mensaje': f"Error matemático en iteración {i+1}:\n{str(e)}.\nIntente otro punto inicial.", 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data}
        
        if abs(df_xi) < 1e-10:
            return {'estado': 'error', 'mensaje': f"Derivada cero en x = {xi}. El método falla.", 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data}
            
        x_nuevo = xi - (f_xi / df_xi)
        if abs(x_nuevo) < 1e-10: error = abs(x_nuevo - xi)
        else: error = abs((x_nuevo - xi) / x_nuevo)
            
        fila_datos = [i + 1, xi, f_xi, df_xi, x_nuevo, error if i > 0 else "N/A"]
        tabla_data.append(fila_datos)

        if i > 0 and error < tolerancia:
            return {'estado': 'exito', 'raiz': x_nuevo, 'iteraciones': i+1, 'error': error, 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data,
                    'mensaje_final': f"Convergencia alcanzada."}
            
        if abs(f_xi) < 1e-14: 
            return {'estado': 'exito', 'raiz': xi, 'iteraciones': i+1, 'error': 0.0, 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data,
                    'mensaje_final': f"Raíz exacta encontrada."}
        xi = x_nuevo 
        
    return {'estado': 'max_iter', 'mensaje': f'Se alcanzó el máximo de iteraciones.', 
            'raiz': xi, 'iteraciones': max_iter, 'error': error,
            'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data}

def metodo_secante(funcion_str: str, x0: float, x1: float, tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    info_previa = []
    tabla_data = []
    try:
        f = _crear_funcion_segura(funcion_str)
        try:
            f(x0); f(x1)
        except ValueError as e:
             return {'estado': 'error', 'mensaje': f"Puntos iniciales inválidos:\n{str(e)}", 'info_previa': info_previa}
             
        info_previa.append(f"x0 = {x0}, x1 = {x1}")
    except Exception as e:
         return {'estado': 'error', 'mensaje': str(e), 'info_previa': info_previa}

    error = 1.0
    tabla_headers = ["Iter", "x_i-1", "x_i", "f(x_i-1)", "f(x_i)", "x_i+1", "Error"]
    
    for i in range(max_iter):
        try:
            f_x0 = f(x0)
            f_x1 = f(x1)
        except ValueError as e:
             return {'estado': 'error', 'mensaje': f"Error matemático en iteración {i+1}:\n{str(e)}.\nCambie los puntos iniciales.", 
                     'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data}
        
        denominador = f_x0 - f_x1
        if abs(denominador) < 1e-10:
            return {'estado': 'error', 'mensaje': "División por cero (f(x0) ≈ f(x1)). Los puntos están demasiado cerca.", 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data}
            
        x_nuevo = x1 - (f_x1 * (x0 - x1)) / denominador
        
        # Validar el nuevo punto antes de continuar
        try:
            f(x_nuevo)
        except ValueError as e:
             fila_datos = [i + 1, x0, x1, f_x0, f_x1, x_nuevo, "ERROR"]
             tabla_data.append(fila_datos)
             return {'estado': 'error', 'mensaje': f"El método saltó a un valor inválido:\n{str(e)}", 
                     'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data}

        if abs(x_nuevo) < 1e-10: error = abs(x_nuevo - x1)
        else: error = abs((x_nuevo - x1) / x_nuevo)
            
        fila_datos = [i + 1, x0, x1, f_x0, f_x1, x_nuevo, error if i > 0 else "N/A"]
        tabla_data.append(fila_datos)

        if i > 0 and error < tolerancia:
            return {'estado': 'exito', 'raiz': x_nuevo, 'iteraciones': i+1, 'error': error, 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data,
                    'mensaje_final': f"Convergencia alcanzada."}
            
        if abs(f(x_nuevo)) < 1e-14:
            return {'estado': 'exito', 'raiz': x_nuevo, 'iteraciones': i+1, 'error': 0.0, 
                    'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data,
                    'mensaje_final': f"Raíz exacta encontrada."}
        
        x0 = x1
        x1 = x_nuevo
        
    return {'estado': 'max_iter', 'mensaje': f'Máximo de iteraciones alcanzado.', 
            'raiz': x1, 'iteraciones': max_iter, 'error': error,
            'info_previa': info_previa, 'tabla_headers': tabla_headers, 'tabla_data': tabla_data}