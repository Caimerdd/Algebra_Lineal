import sympy as sp
import re

def _limpiar_entrada(expr_str):
    if not expr_str: return ""
    expr = expr_str.replace('^', '**')
    expr = expr.lower().replace('inf', 'oo') # Para límites al infinito
    # Multiplicación implícita (2x -> 2*x)
    expr = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr)
    expr = re.sub(r'(\))([a-zA-Z\d])', r'\1*\2', expr)
    return expr

def _formato_bonito(expr):
    try:
        s = sp.pretty(expr, use_unicode=True)
        return re.sub(r'⋅(?=\D)', '', s)
    except: return str(expr)

def _detectar_regla(func, x):
    """Analiza la estructura para decir qué regla se aplica."""
    if func.is_Add: return "Regla de la Suma/Resta"
    if func.is_Mul: return "Regla del Producto"
    if func.is_Pow: return "Regla de la Potencia o Cadena"
    if isinstance(func, sp.exp) or isinstance(func, sp.log): return "Derivada Exponencial/Logarítmica"
    if func.has(sp.sin, sp.cos, sp.tan): return "Derivada Trigonométrica"
    return "Derivación Directa"

def calcular_limite(funcion_str, punto_str, direccion="both"):
    try:
        pasos = []
        x = sp.symbols('x')
        s_func = _limpiar_entrada(funcion_str)
        
        # Manejo de infinito
        if 'oo' in punto_str.lower(): 
            punto = sp.oo if '-' not in punto_str else -sp.oo
            punto_visual = "∞" if punto == sp.oo else "-∞"
        else: 
            punto = sp.sympify(_limpiar_entrada(punto_str))
            punto_visual = _formato_bonito(punto)

        try: func = sp.sympify(s_func)
        except: raise ValueError("Función inválida.")

        # Visualización
        dir_simbolo = ""
        if direccion == '+': dir_simbolo = "⁺"
        elif direccion == '-': dir_simbolo = "⁻"
        
        pasos.append({'titulo': 'Problema', 'math': f"lim (x→{punto_visual}{dir_simbolo})  {_formato_bonito(func)}"})

        # 1. Sustitución Directa (solo si es finito)
        if punto != sp.oo and punto != -sp.oo:
            try:
                val = func.subs(x, punto)
                if not val.is_nan and not val.is_infinite:
                    pasos.append({'titulo': 'Paso 1: Sustitución Directa', 
                                  'math': f"f({punto_visual}) = {_formato_bonito(val)}"})
                else:
                    pasos.append({'titulo': 'Paso 1: Sustitución', 'math': "Forma indeterminada o indefinida. Se requiere análisis."})
            except: pass

        # 2. Cálculo
        if direccion == 'both': res = sp.limit(func, x, punto)
        else: res = sp.limit(func, x, punto, dir=direccion)
        
        pasos.append({'titulo': 'Resultado del Límite', 'math': _formato_bonito(res)})

        return {'estado': 'exito', 'resultado_math': _formato_bonito(res), 'pasos': pasos}

    except Exception as e: return {'estado': 'error', 'mensaje': str(e), 'pasos': []}

def calcular_derivada(funcion_str, orden=1):
    try:
        pasos = []
        x = sp.symbols('x')
        s_func = _limpiar_entrada(funcion_str)
        func = sp.sympify(s_func)
        orden = int(orden)

        # Visualización
        op_str = "d/dx" if orden == 1 else f"d^{orden}/dx^{orden}"
        pasos.append({'titulo': 'Problema', 'math': f"{op_str} [{_formato_bonito(func)}]"})

        # Análisis de Regla (Solo para 1ra derivada)
        if orden == 1:
            regla = _detectar_regla(func, x)
            pasos.append({'titulo': 'Estrategia', 'math': f"Aplicar: {regla}"})

        # Cálculo
        res = sp.diff(func, x, orden)
        
        # Simplificación opcional
        res_simp = sp.simplify(res)
        
        titulo_res = "Primera Derivada f'(x)"
        if orden == 2: titulo_res = "Segunda Derivada f''(x)"
        elif orden > 2: titulo_res = f"Derivada de orden {orden}"

        pasos.append({'titulo': titulo_res, 'math': _formato_bonito(res)})
        
        if res != res_simp:
            pasos.append({'titulo': 'Simplificación', 'math': _formato_bonito(res_simp)})
            return {'estado': 'exito', 'resultado_math': _formato_bonito(res_simp), 'pasos': pasos}

        return {'estado': 'exito', 'resultado_math': _formato_bonito(res), 'pasos': pasos}

    except Exception as e: return {'estado': 'error', 'mensaje': str(e), 'pasos': []}

def analisis_puntos_criticos(funcion_str):
    """Aplicación de la derivada: Máximos y Mínimos."""
    try:
        pasos = []
        x = sp.symbols('x')
        func = sp.sympify(_limpiar_entrada(funcion_str))
        
        pasos.append({'titulo': 'Función', 'math': _formato_bonito(func)})
        
        # 1. Primera Derivada
        d1 = sp.diff(func, x)
        pasos.append({'titulo': '1. Primera Derivada f\'(x)', 'math': _formato_bonito(d1)})
        
        # 2. Puntos Críticos
        criticos = sp.solve(d1, x)
        criticos = [c for c in criticos if c.is_real] # Solo reales
        
        if not criticos:
            return {'estado': 'exito', 'resultado_math': "No se encontraron puntos críticos reales.", 'pasos': pasos}
            
        txt_criticos = ", ".join([_formato_bonito(c) for c in criticos])
        pasos.append({'titulo': '2. Puntos Críticos (f\'(x)=0)', 'math': f"x = {{ {txt_criticos} }}"})
        
        # 3. Segunda Derivada (Criterio)
        d2 = sp.diff(d1, x)
        pasos.append({'titulo': '3. Segunda Derivada f\'\'(x)', 'math': _formato_bonito(d2)})
        
        resumen = ""
        for c in criticos:
            val_d2 = d2.subs(x, c)
            tipo = "Inconcluso"
            if val_d2 > 0: tipo = "Mínimo Local ∪"
            elif val_d2 < 0: tipo = "Máximo Local ∩"
            
            # Calcular coordenada Y
            y_val = func.subs(x, c)
            resumen += f"x = {_formato_bonito(c)}  ->  {tipo} en ({_formato_bonito(c)}, {_formato_bonito(y_val)})\n"

        pasos.append({'titulo': '4. Clasificación', 'math': resumen})
        return {'estado': 'exito', 'resultado_math': resumen, 'pasos': pasos}

    except Exception as e: return {'estado': 'error', 'mensaje': str(e), 'pasos': []}