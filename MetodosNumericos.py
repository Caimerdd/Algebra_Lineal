import math
from typing import Dict, List, Callable, Any

# Define un diccionario de funciones matemáticas seguras para eval()
# Esto permite al usuario usar "cos(x)", "log(x)", "exp(x)", etc., en su string de función.
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
}

def _crear_funcion_segura(funcion_str: str) -> Callable[[float], float]:
    """
    Crea una función de Python segura a partir de un string, usando eval().
    Solo permite acceso a funciones matemáticas seguras.
    """
    # Valida que el string no contenga caracteres peligrosos
    if any(c in funcion_str for c in '[]_{}'):
        raise ValueError("La función contiene caracteres no permitidos.")
        
    # Prepara el código para compilar
    # 'x' será el argumento
    # '__builtins__': {} previene el acceso a funciones built-in de Python (como open())
    # {**SAFE_MATH_FUNCTIONS} inserta todas las funciones seguras (cos, sin, etc.)
    code = compile(funcion_str, "<string>", "eval")
    
    def funcion_evaluada(x: float) -> float:
        try:
            # Pasa 'x' y las funciones seguras al scope de eval()
            return eval(code, {"__builtins__": {}}, {**SAFE_MATH_FUNCTIONS, 'x': x})
        except ZeroDivisionError:
            # Maneja divisiones por cero de forma elegante
            return float('inf')
        except Exception as e:
            # Captura otros errores matemáticos (ej. log(-1))
            raise ValueError(f"Error al evaluar f({x}): {e}")
            
    return funcion_evaluada

def metodo_biseccion(funcion_str: str, a: float, b: float, tolerancia: float, max_iter: int = 100) -> Dict[str, Any]:
    """
    Calcula una raíz de la función f(x) en el intervalo [a, b] usando el método de bisección.
    
    Args:
        funcion_str: El string de la función (ej: "math.cos(x) - x").
        a: Límite inferior del intervalo.
        b: Límite superior del intervalo.
        tolerancia: El criterio de paro (error relativo decimal, ej: 0.0001).
        max_iter: Número máximo de iteraciones para prevenir bucles infinitos.
        
    Returns:
        Un diccionario con el resultado.
    """
    pasos: List[str] = []
    
    try:
        # 1. Crear la función a partir del string
        # Usamos la versión con math. ya que el usuario podría escribirlo
        # El helper _crear_funcion_segura lo maneja
        funcion_str_limpia = funcion_str.replace('math.', '')
        f = _crear_funcion_segura(funcion_str_limpia)
    except Exception as e:
        return {'estado': 'error', 'mensaje': f"Error en la sintaxis de la función: {e}", 'pasos': pasos}
        
    try:
        # 2. Verificar la condición inicial (Teorema de Bolzano)
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

    # 3. Inicializar variables de iteración
    xr_anterior = a  # O cualquier valor, solo importa después de la 1ra iteración
    xr_nuevo = (a + b) / 2
    error = 1.0  # Error inicial al 100%
    
    pasos.append("\n--- Iniciando iteraciones ---")
    pasos.append("Iter |     a     |     b     |    xr_nuevo   |   f(xr_nuevo)  |   Error Rel.  |")
    pasos.append("-" * 75)
    
    for i in range(max_iter):
        
        fxr = f(xr_nuevo)
        
        # Calcular error relativo (después de la primera iteración)
        if i > 0:
            if abs(xr_nuevo) < 1e-10: # Evitar división por cero si la raíz es 0
                error = abs(xr_nuevo - xr_anterior)
            else:
                error = abs((xr_nuevo - xr_anterior) / xr_nuevo) # No multiplicamos por 100
                
        # Formatear datos para la tabla de pasos
        paso_str = f"{i+1:4} | {a:9.6f} | {b:9.6f} | {xr_nuevo:12.8f} | {fxr:14.6e} |"
        if i > 0:
            paso_str += f" {error:13.6e} |"
        else:
            paso_str += "       N/A       |"
            
        pasos.append(paso_str)

        # 4. Criterio de paro (Error vs Tolerancia)
        if error < tolerancia and i > 0:
            pasos.append("-" * 75)
            pasos.append(f"\nConvergencia alcanzada en la iteración {i+1}.")
            pasos.append(f"Error ({error:.6e}) < Tolerancia ({tolerancia:.6e})")
            return {'estado': 'exito', 'raiz': xr_nuevo, 'iteraciones': i+1, 'error': error, 'pasos': pasos}
            
        # 5. Criterio de paro (Raíz exacta encontrada)
        if abs(fxr) < 1e-14: # Cerca de cero
            pasos.append("-" * 75)
            pasos.append(f"\nRaíz exacta encontrada en la iteración {i+1}.")
            return {'estado': 'exito', 'raiz': xr_nuevo, 'iteraciones': i+1, 'error': 0.0, 'pasos': pasos}
            
        # 6. Actualizar el intervalo
        if fa * fxr < 0:
            # La raíz está en [a, xr_nuevo]
            b = xr_nuevo
            fb = fxr # Actualizamos fb para la siguiente iteración
        else:
            # La raíz está en [xr_nuevo, b]
            a = xr_nuevo
            fa = fxr # Actualizamos fa para la siguiente iteración
            
        # 7. Calcular nuevo xr y actualizar xr_anterior
        xr_anterior = xr_nuevo
        xr_nuevo = (a + b) / 2
        
    pasos.append("-" * 75)
    pasos.append(f"\nSe alcanzó el máximo de {max_iter} iteraciones sin convergencia.")
    return {'estado': 'max_iter', 'mensaje': f'Se alcanzó el máximo de {max_iter} iteraciones.', 'raiz': xr_nuevo, 'iteraciones': max_iter, 'error': error, 'pasos': pasos}