import math
from typing import Dict, List, Callable, Any

# Define un diccionario de funciones matemáticas seguras para eval()
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
    """
    Crea una función de Python segura a partir de un string, usando eval().
    """
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
    """
    Calcula una raíz usando el método de bisección: xr = (a + b) / 2
    """
    pasos: List[str] = []
    
    try:
        funcion_str_limpia = funcion_str.replace('math.', '')
        f = _crear_funcion_segura(funcion_str_limpia)
    except Exception as e:
        return {'estado': 'error', 'mensaje': f"Error en la sintaxis de la función: {e}", 'pasos': pasos}
        
    try:
        fa = f(a)
        fb = f(b)
        pasos.append(f"Intervalo inicial: [{a}, {b}]")
        pasos.append(f"f(a) = f({a:.6g}) = {fa:.6e}")
        pasos.append(f"f(b) = f({b:.6g}) = {fb:.6e}")
        
        if fa * fb >= 0:
            pasos.append(f"Condición f(a) * f(b) < 0 no se cumple ({fa*fb:.6e} >= 0).")
            return {'estado': 'error', 'mensaje': 'El método de bisección no aplica: f(a) y f(b) deben tener signos opuestos.', 'pasos': pasos}
            
    except ValueError as e:
         return {'estado': 'error', 'mensaje': str(e), 'pasos': pasos}

    xr_anterior = a 
    xr_nuevo = (a + b) / 2
    error = 1.0
    
    pasos.append("\n--- Iniciando iteraciones (Bisección) ---")
    pasos.append("Iter |     a     |     b     |    xr_nuevo   |   f(xr_nuevo)  |   Error Rel.  |")
    pasos.append("-" * 75)
    
    for i in range(max_iter):
        fxr = f(xr_nuevo)
        
        if i > 0:
            if abs(xr_nuevo) < 1e-10:
                error = abs(xr_nuevo - xr_anterior)
            else:
                error = abs((xr_nuevo - xr_anterior) / xr_nuevo)
                
        paso_str = f"{i+1:4} | {a:9.6f} | {b:9.6f} | {xr_nuevo:12.8f} | {fxr:14.6e} |"
        if i > 0:
            paso_str += f" {error:13.6e} |"
        else:
            paso_str += "       N/A       |"
        pasos.append(paso_str)

        if error < tolerancia and i > 0:
            pasos.append("-" * 75)
            pasos.append(f"\nConvergencia alcanzada en la iteración {i+1}.")
            return {'estado': 'exito', 'raiz': xr_nuevo, 'iteraciones': i+1, 'error': error, 'pasos': pasos}
            
        if abs(fxr) < 1e-14:
            pasos.append("-" * 75)
            pasos.append(f"\nRaíz exacta encontrada en la iteración {i+1}.")
            return {'estado': 'exito', 'raiz': xr_nuevo, 'iteraciones': i+1, 'error': 0.0, 'pasos': pasos}
            
        if fa * fxr < 0:
            b = xr_nuevo
            fb = fxr
        else:
            a = xr_nuevo
            fa = fxr
            
        xr_anterior = xr_nuevo
        xr_nuevo = (a + b) / 2
        
    pasos.append("-" * 75)
    return {'estado': 'max_iter', 'mensaje': f'Se alcanzó el máximo de {max_iter} iteraciones.', 'raiz': xr_nuevo, 'iteraciones': max_iter, 'error': error, 'pasos': pasos}

def metodo_falsa_posicion(funcion_str: str, a: float, b: float, tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    """
    Calcula una raíz usando el método de Falsa Posición: 
    xr = b - (f(b)*(a-b)) / (f(a)-f(b))
    """
    pasos: List[str] = []
    
    try:
        funcion_str_limpia = funcion_str.replace('math.', '')
        f = _crear_funcion_segura(funcion_str_limpia)
    except Exception as e:
        return {'estado': 'error', 'mensaje': f"Error en la sintaxis de la función: {e}", 'pasos': pasos}
        
    try:
        fa = f(a)
        fb = f(b)
        pasos.append(f"Intervalo inicial: [{a}, {b}]")
        pasos.append(f"f(a) = {fa:.6e}")
        pasos.append(f"f(b) = {fb:.6e}")
        
        if fa * fb >= 0:
            pasos.append(f"Error: f(a) y f(b) deben tener signos opuestos.")
            return {'estado': 'error', 'mensaje': 'El método requiere que f(a) y f(b) tengan signos opuestos.', 'pasos': pasos}
            
    except ValueError as e:
         return {'estado': 'error', 'mensaje': str(e), 'pasos': pasos}

    xr_anterior = a 
    # Fórmula de Falsa Posición
    # Evitar división por cero si f(a) == f(b), aunque con signos opuestos es imposible a menos que sean 0
    if abs(fa - fb) < 1e-15:
         return {'estado': 'error', 'mensaje': 'División por cero: f(a) es casi igual a f(b).', 'pasos': pasos}

    xr_nuevo = b - (fb * (a - b)) / (fa - fb)
    error = 1.0
    
    pasos.append("\n--- Iniciando iteraciones (Falsa Posición) ---")
    pasos.append("Iter |     a     |     b     |    xr_nuevo   |   f(xr_nuevo)  |   Error Rel.  |")
    pasos.append("-" * 75)
    
    for i in range(max_iter):
        fxr = f(xr_nuevo)
        
        # Cálculo del error relativo
        if i > 0:
            if abs(xr_nuevo) < 1e-10:
                error = abs(xr_nuevo - xr_anterior)
            else:
                error = abs((xr_nuevo - xr_anterior) / xr_nuevo)
                
        paso_str = f"{i+1:4} | {a:9.6f} | {b:9.6f} | {xr_nuevo:12.8f} | {fxr:14.6e} |"
        if i > 0:
            paso_str += f" {error:13.6e} |"
        else:
            paso_str += "       N/A       |"
        pasos.append(paso_str)

        # Criterio de paro por tolerancia
        if error < tolerancia and i > 0:
            pasos.append("-" * 75)
            pasos.append(f"\nConvergencia alcanzada en la iteración {i+1}.")
            return {'estado': 'exito', 'raiz': xr_nuevo, 'iteraciones': i+1, 'error': error, 'pasos': pasos}
            
        # Criterio de paro por raíz exacta
        if abs(fxr) < 1e-14:
            pasos.append("-" * 75)
            pasos.append(f"\nRaíz exacta encontrada en la iteración {i+1}.")
            return {'estado': 'exito', 'raiz': xr_nuevo, 'iteraciones': i+1, 'error': 0.0, 'pasos': pasos}
            
        # Actualizar intervalo
        if fa * fxr < 0:
            b = xr_nuevo
            fb = fxr
        else:
            a = xr_nuevo
            fa = fxr
            
        xr_anterior = xr_nuevo
        # Recalcular xr con la fórmula de falsa posición
        if abs(fa - fb) < 1e-15:
             pasos.append("\nAdvertencia: Diferencia entre f(a) y f(b) muy pequeña, terminando.")
             break
             
        xr_nuevo = b - (fb * (a - b)) / (fa - fb)
        
    pasos.append("-" * 75)
    return {'estado': 'max_iter', 'mensaje': f'Se alcanzó el máximo de {max_iter} iteraciones.', 'raiz': xr_nuevo, 'iteraciones': max_iter, 'error': error, 'pasos': pasos}