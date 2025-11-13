import math
from typing import Dict, List, Callable, Any

# Diccionario de funciones seguras
SAFE_MATH_FUNCTIONS = {
    'cos': math.cos,
    'sin': math.sin,
    'tan': math.tan,
    'acos': math.acos,
    'asin': math.asin,
    'atan': math.atan,
    'exp': math.exp,
    'log': math.log,    # Logaritmo natural
    'log10': math.log10, # Logaritmo base 10
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

def metodo_biseccion(funcion_str: str, a: float, b: float, tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    pasos: List[str] = []
    try:
        f = _crear_funcion_segura(funcion_str.replace('math.', ''))
        fa, fb = f(a), f(b)
        pasos.append(f"Intervalo inicial: [{a}, {b}]")
        pasos.append(f"f(a) = {fa:.6e}")
        pasos.append(f"f(b) = {fb:.6e}")
        
        if fa * fb >= 0:
            return {'estado': 'error', 'mensaje': 'El método no aplica: f(a) y f(b) deben tener signos opuestos.', 'pasos': pasos}
    except Exception as e:
         return {'estado': 'error', 'mensaje': str(e), 'pasos': pasos}

    xr_anterior = a 
    xr_nuevo = (a + b) / 2
    error = 1.0
    
    pasos.append("\n--- Iniciando iteraciones (Bisección) ---")
    
    # --- TABLA SÚPER ESPACIOSA ---
    # Hemos aumentado drásticamente el ancho (^22 y ^24) para que sobre espacio a los lados
    header = f"| {'Iter':^8} | {'a':^22} | {'b':^22} | {'f(a)':^24} | {'f(b)':^24} | {'xr':^22} | {'f(xr)':^24} | {'Error':^24} |"
    separador = "-" * len(header)
    
    pasos.append(separador)
    pasos.append(header)
    pasos.append(separador)
    
    for i in range(max_iter):
        fxr = f(xr_nuevo)
        
        if i > 0:
            if abs(xr_nuevo) < 1e-10: error = abs(xr_nuevo - xr_anterior)
            else: error = abs((xr_nuevo - xr_anterior) / xr_nuevo)
            error_str = f"{error:^24.5e}" # Centrado en 24 espacios
        else:
            error_str = f"{'N/A':^24}"

        # Fila de datos: Usamos los mismos anchos masivos (22 y 24)
        paso_str = (
            f"| {i+1:^8d} | {a:^22.8f} | {b:^22.8f} | {fa:^24.5e} | {fb:^24.5e} | "
            f"{xr_nuevo:^22.8f} | {fxr:^24.5e} | {error_str} |"
        )
        pasos.append(paso_str)

        if i > 0 and error < tolerancia:
            pasos.append(separador)
            pasos.append(f"\nConvergencia alcanzada en la iteración {i+1}.")
            return {'estado': 'exito', 'raiz': xr_nuevo, 'iteraciones': i+1, 'error': error, 'pasos': pasos}
            
        if abs(fxr) < 1e-14:
            pasos.append(separador)
            pasos.append(f"\nRaíz exacta encontrada en la iteración {i+1}.")
            return {'estado': 'exito', 'raiz': xr_nuevo, 'iteraciones': i+1, 'error': 0.0, 'pasos': pasos}
            
        if fa * fxr < 0:
            b, fb = xr_nuevo, fxr
        else:
            a, fa = xr_nuevo, fxr
            
        xr_anterior = xr_nuevo
        xr_nuevo = (a + b) / 2
        
    pasos.append(separador)
    return {'estado': 'max_iter', 'mensaje': f'Se alcanzó el máximo de {max_iter} iteraciones.', 'raiz': xr_nuevo, 'iteraciones': max_iter, 'error': error, 'pasos': pasos}

def metodo_falsa_posicion(funcion_str: str, a: float, b: float, tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    pasos: List[str] = []
    try:
        f = _crear_funcion_segura(funcion_str.replace('math.', ''))
        fa, fb = f(a), f(b)
        pasos.append(f"Intervalo inicial: [{a}, {b}]")
        pasos.append(f"f(a) = {fa:.6e}")
        pasos.append(f"f(b) = {fb:.6e}")
        
        if fa * fb >= 0:
            return {'estado': 'error', 'mensaje': 'El método requiere que f(a) y f(b) tengan signos opuestos.', 'pasos': pasos}
    except Exception as e:
         return {'estado': 'error', 'mensaje': str(e), 'pasos': pasos}

    if abs(fa - fb) < 1e-15:
         return {'estado': 'error', 'mensaje': 'División por cero: f(a) es casi igual a f(b).', 'pasos': pasos}

    xr_anterior = a 
    xr_nuevo = b - (fb * (a - b)) / (fa - fb)
    error = 1.0
    
    pasos.append("\n--- Iniciando iteraciones (Falsa Posición) ---")
    
    # --- TABLA SÚPER ESPACIOSA (Mismo formato) ---
    header = f"| {'Iter':^8} | {'a':^22} | {'b':^22} | {'f(a)':^24} | {'f(b)':^24} | {'xr':^22} | {'f(xr)':^24} | {'Error':^24} |"
    separador = "-" * len(header)
    
    pasos.append(separador)
    pasos.append(header)
    pasos.append(separador)
    
    for i in range(max_iter):
        fxr = f(xr_nuevo)
        
        if i > 0:
            if abs(xr_nuevo) < 1e-10: error = abs(xr_nuevo - xr_anterior)
            else: error = abs((xr_nuevo - xr_anterior) / xr_nuevo)
            error_str = f"{error:^24.5e}"
        else:
            error_str = f"{'N/A':^24}"

        paso_str = (
            f"| {i+1:^8d} | {a:^22.8f} | {b:^22.8f} | {fa:^24.5e} | {fb:^24.5e} | "
            f"{xr_nuevo:^22.8f} | {fxr:^24.5e} | {error_str} |"
        )
        pasos.append(paso_str)

        if i > 0 and error < tolerancia:
            pasos.append(separador)
            pasos.append(f"\nConvergencia alcanzada en la iteración {i+1}.")
            return {'estado': 'exito', 'raiz': xr_nuevo, 'iteraciones': i+1, 'error': error, 'pasos': pasos}
            
        if abs(fxr) < 1e-14:
            pasos.append(separador)
            pasos.append(f"\nRaíz exacta encontrada en la iteración {i+1}.")
            return {'estado': 'exito', 'raiz': xr_nuevo, 'iteraciones': i+1, 'error': 0.0, 'pasos': pasos}
            
        if fa * fxr < 0:
            b, fb = xr_nuevo, fxr
        else:
            a, fa = xr_nuevo, fxr
            
        xr_anterior = xr_nuevo
        
        if abs(fa - fb) < 1e-15:
             pasos.append("\nAdvertencia: Diferencia entre f(a) y f(b) muy pequeña, terminando.")
             break
             
        xr_nuevo = b - (fb * (a - b)) / (fa - fb)
        
    pasos.append(separador)
    return {'estado': 'max_iter', 'mensaje': f'Se alcanzó el máximo de {max_iter} iteraciones.', 'raiz': xr_nuevo, 'iteraciones': max_iter, 'error': error, 'pasos': pasos}