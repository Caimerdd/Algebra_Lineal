import sympy as sp
import re

def _limpiar_entrada(expr_str):
    if not expr_str: return ""
    expr = expr_str.replace('^', '**')
    expr = expr.lower().replace('inf', 'oo')
    # Multiplicación implícita: 2x -> 2*x
    expr = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr)
    expr = re.sub(r'(\))([a-zA-Z\d])', r'\1*\2', expr)
    return expr

def _formato_bonito(expr):
    try:
        s = sp.pretty(expr, use_unicode=True)
        return re.sub(r'⋅(?=\D)', '', s)
    except: return str(expr)

def _detectar_estrategia(func, x):
    """Analiza la función para sugerir la estrategia de integración."""
    if func.is_polynomial(x):
        return "Regla de la Potencia (Polinomios)"
    elif func.is_rational_function(x):
        return "Fracciones Parciales o Logaritmo Natural"
    elif func.has(sp.sin, sp.cos, sp.tan, sp.sec, sp.csc, sp.cot):
        return "Identidades o Sustitución Trigonométrica"
    elif func.has(sp.exp):
        return "Integración Exponencial"
    elif func.has(sp.log):
        return "Integración por Partes (probablemente)"
    elif isinstance(func, sp.Mul):
        return "Posible Integración por Partes o Sustitución (u-du)"
    return "Métodos de Integración General"

def calcular_integral_basica(funcion_str, a_str=None, b_str=None, tipo="Indefinida"):
    """Maneja integrales indefinidas y definidas con paso a paso educativo."""
    try:
        pasos = []
        x = sp.symbols('x')
        s_func = _limpiar_entrada(funcion_str)
        
        try: func = sp.sympify(s_func)
        except: raise ValueError("Función inválida.")

        # 1. Análisis del Problema
        if tipo == "Indefinida":
            pasos.append({'titulo': 'Problema', 'math': f"∫ ({_formato_bonito(func)}) dx"})
        else:
            try:
                a = sp.sympify(_limpiar_entrada(a_str))
                b = sp.sympify(_limpiar_entrada(b_str))
            except: raise ValueError("Límites inválidos.")
            pasos.append({'titulo': 'Problema', 'math': f"∫[{_formato_bonito(a)} a {_formato_bonito(b)}] ({_formato_bonito(func)}) dx"})

        # 2. Estrategia
        estrategia = _detectar_estrategia(func, x)
        pasos.append({'titulo': 'Análisis de la Función', 
                      'math': f"Tipo de función detectada. \nEstrategia sugerida: {estrategia}"})

        # 3. Calcular Antiderivada
        antiderivada = sp.integrate(func, x)
        
        if isinstance(antiderivada, sp.Integral):
            raise ValueError("No se encontró una solución analítica simple.")

        pasos.append({'titulo': 'Paso 1: Hallar la Antiderivada F(x)', 
                      'math': f"Integrando f(x) obtenemos:\nF(x) = {_formato_bonito(antiderivada)}"})

        res_final = ""

        # 4. Resultado según tipo
        if tipo == "Indefinida":
            res_final = f"{_formato_bonito(antiderivada)} + C"
            pasos.append({'titulo': 'Resultado Final', 'math': "Añadimos la constante de integración C."})
        else:
            # Teorema Fundamental del Cálculo
            F_b = antiderivada.subs(x, b)
            F_a = antiderivada.subs(x, a)
            
            pasos.append({'titulo': 'Paso 2: Teorema Fundamental del Cálculo', 
                          'math': f"Aplicamos F(b) - F(a):\n"
                                  f"Límite Superior: F({_formato_bonito(b)}) = {_formato_bonito(F_b)}\n"
                                  f"Límite Inferior: F({_formato_bonito(a)}) = {_formato_bonito(F_a)}"})
            
            resultado = sp.simplify(F_b - F_a)
            res_final = _formato_bonito(resultado)
            
            try:
                val_float = float(resultado.evalf())
                if not resultado.is_Integer:
                    res_final += f"\n(≈ {val_float:.4f})"
            except: pass
            
            pasos.append({'titulo': 'Resultado (Área neta)', 'math': f"{_formato_bonito(F_b)} - ({_formato_bonito(F_a)}) = {res_final}"})

        return {'estado': 'exito', 'resultado_math': res_final, 'pasos': pasos}

    except Exception as e: return {'estado': 'error', 'mensaje': str(e), 'pasos': []}

def calcular_area_entre_curvas(f_str, g_str, a_str, b_str):
    """Calcula el área entre f(x) y g(x)."""
    try:
        pasos = []
        x = sp.symbols('x')
        f = sp.sympify(_limpiar_entrada(f_str))
        g = sp.sympify(_limpiar_entrada(g_str))
        a = sp.sympify(_limpiar_entrada(a_str))
        b = sp.sympify(_limpiar_entrada(b_str))

        pasos.append({'titulo': 'Fórmula de Área', 'math': "Area = ∫ [ f(x) - g(x) ] dx"})
        
        integrando = sp.simplify(f - g)
        pasos.append({'titulo': '1. Simplificar Integrando', 
                      'math': f"({_formato_bonito(f)}) - ({_formato_bonito(g)}) = {_formato_bonito(integrando)}"})
        
        pasos.append({'titulo': '2. Plantear Integral Definida', 
                      'math': f"∫[{_formato_bonito(a)} a {_formato_bonito(b)}] ({_formato_bonito(integrando)}) dx"})

        # Calcular primitiva
        primitiva = sp.integrate(integrando, x)
        pasos.append({'titulo': '3. Antiderivada', 'math': _formato_bonito(primitiva)})

        # Evaluar
        res = sp.integrate(integrando, (x, a, b))
        # Usamos valor absoluto para el área física total si dio negativo por orden de f/g
        res_abs = sp.Abs(res)
        
        res_fmt = _formato_bonito(res_abs)
        try: res_fmt += f"\n(≈ {float(res_abs.evalf()):.4f} u²)"
        except: pass
        
        pasos.append({'titulo': 'Resultado Final', 'math': res_fmt})
        return {'estado': 'exito', 'resultado_math': res_fmt, 'pasos': pasos}
    except Exception as e: return {'estado': 'error', 'mensaje': str(e), 'pasos': []}

def calcular_volumen_revolucion(f_str, a_str, b_str, eje="x"):
    """Método de Discos."""
    try:
        pasos = []
        x = sp.symbols('x')
        f = sp.sympify(_limpiar_entrada(f_str))
        a = sp.sympify(_limpiar_entrada(a_str))
        b = sp.sympify(_limpiar_entrada(b_str))

        pasos.append({'titulo': 'Método de Discos (Eje X)', 'math': "V = π · ∫ [f(x)]² dx"})
        
        integrando = f**2
        pasos.append({'titulo': '1. Cuadrado de la función (Radio²)', 
                      'math': f"({_formato_bonito(f)})² = {_formato_bonito(sp.simplify(integrando))}"})

        pasos.append({'titulo': '2. Plantear Integral', 
                      'math': f"V = π · ∫[{_formato_bonito(a)} a {_formato_bonito(b)}] ({_formato_bonito(sp.simplify(integrando))}) dx"})

        integral_val = sp.integrate(integrando, (x, a, b))
        volumen = sp.pi * integral_val
        
        res_fmt = _formato_bonito(volumen)
        try: res_fmt += f"\n(≈ {float(volumen.evalf()):.4f} u³)"
        except: pass
        
        pasos.append({'titulo': 'Resultado Final', 'math': res_fmt})
        return {'estado': 'exito', 'resultado_math': res_fmt, 'pasos': pasos}
    except Exception as e: return {'estado': 'error', 'mensaje': str(e), 'pasos': []}

def calcular_longitud_arco(f_str, a_str, b_str):
    """Longitud de Arco."""
    try:
        pasos = []
        x = sp.symbols('x')
        f = sp.sympify(_limpiar_entrada(f_str))
        a = sp.sympify(_limpiar_entrada(a_str))
        b = sp.sympify(_limpiar_entrada(b_str))

        pasos.append({'titulo': 'Fórmula de Longitud de Arco', 'math': "L = ∫ √[1 + (f'(x))²] dx"})
        
        derivada = sp.diff(f, x)
        pasos.append({'titulo': '1. Derivada f\'(x)', 'math': _formato_bonito(derivada)})
        
        integrando = sp.sqrt(1 + derivada**2)
        pasos.append({'titulo': '2. Plantear Integral', 
                      'math': f"L = ∫[{_formato_bonito(a)} a {_formato_bonito(b)}] {_formato_bonito(integrando)} dx"})

        res = sp.integrate(integrando, (x, a, b))
        
        res_fmt = _formato_bonito(res)
        try: res_fmt += f"\n(≈ {float(res.evalf()):.4f} u)"
        except: pass
        
        pasos.append({'titulo': 'Resultado', 'math': res_fmt})
        return {'estado': 'exito', 'resultado_math': res_fmt, 'pasos': pasos}
    except Exception as e: return {'estado': 'error', 'mensaje': str(e), 'pasos': []}