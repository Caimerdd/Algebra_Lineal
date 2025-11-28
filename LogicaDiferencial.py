import sympy as sp
import re

def _limpiar_entrada(expr_str):
    """Limpia la entrada para que SymPy la entienda (agrega * implícitos)."""
    if not expr_str: return ""
    expr = expr_str.replace('^', '**')
    expr = expr.lower().replace('inf', 'oo') # Reconocer infinito
    # 2x -> 2*x, 2( -> 2*(, )x -> )*x
    expr = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr)
    expr = re.sub(r'(\))([a-zA-Z\d])', r'\1*\2', expr)
    return expr

def _formato_bonito(expr):
    """Devuelve formato visual limpio (LaTeX unicode sin puntos feos)."""
    try:
        s = sp.pretty(expr, use_unicode=True)
        return re.sub(r'⋅(?=\D)', '', s) 
    except:
        return str(expr)

def calcular_limite(funcion_str, punto_str, direccion="both"):
    """
    Calcula el límite de f(x) cuando x -> punto.
    direccion: '+' (derecha), '-' (izquierda), 'both' (bilateral).
    """
    try:
        pasos = []
        x = sp.symbols('x')
        
        # Limpieza
        s_func = _limpiar_entrada(funcion_str)
        s_punto = _limpiar_entrada(punto_str)
        
        try:
            func = sp.sympify(s_func)
            # Manejo de infinito
            if 'oo' in s_punto: punto = sp.oo
            elif '-oo' in s_punto: punto = -sp.oo
            else: punto = sp.sympify(s_punto)
        except: raise ValueError("Error en la función o el punto.")

        # Visualización del problema
        dir_simbolo = ""
        if direccion == '+': dir_simbolo = "⁺"
        elif direccion == '-': dir_simbolo = "⁻"
        
        lim_str = f"lim   {_formato_bonito(func)}"
        sub_str = f"x→{_formato_bonito(punto)}{dir_simbolo}"
        
        pasos.append({'titulo': 'Problema', 'math': f"{lim_str}\n{sub_str}"})

        # Paso 1: Evaluar directamente (Sustitución)
        try:
            val_sust = func.subs(x, punto)
            if not val_sust.is_infinite and not val_sust.is_nan:
                pasos.append({'titulo': 'Paso 1: Sustitución Directa', 
                              'math': f"Evaluamos en x = {_formato_bonito(punto)}:\nResulta: {_formato_bonito(val_sust)}"})
        except: pass

        # Cálculo real con SymPy
        if direccion == 'both':
            resultado = sp.limit(func, x, punto)
        else:
            resultado = sp.limit(func, x, punto, dir=direccion)

        res_fmt = _formato_bonito(resultado)
        pasos.append({'titulo': 'Resultado del Límite', 'math': f"{res_fmt}"})

        return {'estado': 'exito', 'resultado_math': res_fmt, 'pasos': pasos}

    except Exception as e: return {'estado': 'error', 'mensaje': str(e), 'pasos': []}

def calcular_derivada(funcion_str, orden=1):
    """
    Calcula la derivada de orden n de f(x).
    """
    try:
        pasos = []
        x = sp.symbols('x')
        s_func = _limpiar_entrada(funcion_str)
        
        try: func = sp.sympify(s_func)
        except: raise ValueError("Función inválida.")
        
        try: orden = int(orden)
        except: raise ValueError("El orden debe ser un número entero.")

        # Notación de derivada
        if orden == 1: op_str = "d/dx"
        else: op_str = f"d^{orden}/dx^{orden}"

        pasos.append({'titulo': 'Función Original', 'math': f"f(x) = {_formato_bonito(func)}"})
        
        # Cálculo
        derivada = sp.diff(func, x, orden)
        
        pasos.append({
            'titulo': f'Operación: Derivada de orden {orden}',
            'math': f"{op_str} [{_formato_bonito(func)}]"
        })

        res_fmt = _formato_bonito(derivada)
        pasos.append({'titulo': 'Resultado', 'math': f"f{''.join(['\'' for _ in range(min(orden, 3))])}(x) = {res_fmt}"})
        
        if orden > 3: # Si es derivada 4ta o mayor, usamos notación (n)
             pasos[-1]['math'] = f"f^({orden})(x) = {res_fmt}"

        return {'estado': 'exito', 'resultado_math': res_fmt, 'pasos': pasos}

    except Exception as e: return {'estado': 'error', 'mensaje': str(e), 'pasos': []}