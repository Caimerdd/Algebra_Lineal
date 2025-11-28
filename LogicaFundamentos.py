import sympy as sp
import re

def _limpiar_entrada(expr_str):
    """Limpia la entrada (agrega multiplicaciones implícitas)."""
    if not expr_str: return ""
    expr = expr_str.replace('^', '**')
    # 2x -> 2*x, 2( -> 2*(, )x -> )*x
    expr = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr)
    expr = re.sub(r'(\))([a-zA-Z\d])', r'\1*\2', expr)
    return expr

def _formato_bonito(expr):
    """Devuelve formato visual limpio (sin puntos de multiplicación)."""
    try:
        s = sp.pretty(expr, use_unicode=True)
        return re.sub(r'⋅(?=\D)', '', s) 
    except:
        return str(expr)

def operar_polinomios(p1_str, p2_str, operacion):
    try:
        pasos = []
        x = sp.symbols('x')
        s_p1 = _limpiar_entrada(p1_str)
        s_p2 = _limpiar_entrada(p2_str)
        
        try:
            poly1 = sp.sympify(s_p1)
            poly2 = sp.sympify(s_p2)
        except: raise ValueError("Formato inválido.")

        pasos.append({'titulo': 'Entrada', 'math': f'P(x) = {_formato_bonito(poly1)}\nQ(x) = {_formato_bonito(poly2)}'})
        
        resultado = None
        
        # --- LÓGICA PASO A PASO DETALLADA ---
        
        if operacion == "Suma":
            pasos.append({'titulo': 'Paso 1: Planteamiento', 'math': f'({_formato_bonito(poly1)}) + ({_formato_bonito(poly2)})'})
            pasos.append({'titulo': 'Paso 2: Agrupación', 'math': 'Agrupamos términos semejantes (x² con x², x con x, constantes con constantes).'})
            
            # Resultado
            resultado = sp.simplify(poly1 + poly2)
            
        elif operacion == "Resta":
            pasos.append({'titulo': 'Paso 1: Planteamiento', 'math': f'({_formato_bonito(poly1)}) - ({_formato_bonito(poly2)})'})
            
            # Mostrar el cambio de signo
            poly2_neg = sp.expand(-1 * poly2)
            pasos.append({
                'titulo': 'Paso 2: Cambio de Signos', 
                'math': f'El signo negativo afecta a todo Q(x):\n{_formato_bonito(poly1)} + ({_formato_bonito(poly2_neg)})'
            })
            pasos.append({'titulo': 'Paso 3: Agrupación', 'math': 'Sumamos los términos semejantes.'})
            
            resultado = sp.simplify(poly1 - poly2)
            
        elif operacion == "Multiplicación":
            pasos.append({'titulo': 'Paso 1: Planteamiento', 'math': f'({_formato_bonito(poly1)}) · ({_formato_bonito(poly2)})'})
            
            # Mostrar propiedad distributiva si son binomios/polinomios simples
            if (poly1.is_Add or poly2.is_Add):
                pasos.append({'titulo': 'Paso 2: Propiedad Distributiva', 'math': 'Multiplicamos cada término del primer polinomio por cada término del segundo.'})
                
                # Intentamos mostrar un paso intermedio visual
                # (Ej: x * (x+1) + 1 * (x+1))
                if poly1.is_Add:
                    args = poly1.args
                    dist_text = []
                    for arg in args:
                        # Formatear bonito: arg * (poly2)
                        term_fmt = _formato_bonito(arg)
                        poly2_fmt = _formato_bonito(poly2)
                        dist_text.append(f"{term_fmt}·({poly2_fmt})")
                    
                    pasos.append({'titulo': 'Expansión', 'math': " + ".join(dist_text)})

            resultado = sp.expand(poly1 * poly2)
            
        elif operacion == "División":
            q, r = sp.div(poly1, poly2)
            pasos.append({'titulo': 'Planteamiento', 'math': f'{_formato_bonito(poly1)} ÷ {_formato_bonito(poly2)}'})
            pasos.append({'titulo': 'Algoritmo de División', 'math': 'Realizamos la división euclidiana de polinomios.'})
            
            res_txt = f"Cociente: {_formato_bonito(q)}\nResiduo: {_formato_bonito(r)}"
            pasos.append({'titulo': 'Resultado', 'math': res_txt})
            return {'estado': 'exito', 'resultado_math': res_txt, 'pasos': pasos}

        res_txt = _formato_bonito(resultado)
        pasos.append({'titulo': 'Resultado Final Simplificado', 'math': res_txt})
        
        return {'estado': 'exito', 'resultado_math': res_txt, 'pasos': pasos}
        
    except Exception as e: return {'estado': 'error', 'mensaje': str(e), 'pasos': []}

def factorizar_expresion(expr_str):
    try:
        pasos = []
        x = sp.symbols('x')
        s_expr = _limpiar_entrada(expr_str)
        try: expr = sp.sympify(s_expr)
        except: raise ValueError("Expresión inválida.")

        pasos.append({'titulo': 'Expresión Original', 'math': _formato_bonito(expr)})
        
        expr_actual = expr
        
        # 1. FACTOR COMÚN
        terminos = sp.Add.make_args(expr_actual)
        if len(terminos) > 1:
            try:
                factor_comun = sp.gcd(tuple(terminos))
                if factor_comun != 1:
                    expr_resto = sp.simplify(expr_actual / factor_comun)
                    pasos.append({
                        'titulo': 'Paso 1: Factor Común',
                        'math': f"Extraemos el factor común {_formato_bonito(factor_comun)}:\n"
                                f"{_formato_bonito(factor_comun)} · ({_formato_bonito(expr_resto)})"
                    })
                    expr_actual = expr_resto 
            except: pass

        # 2. DIFERENCIA DE CUADRADOS Y TRINOMIOS
        if expr_actual.is_Add:
            if len(expr_actual.args) == 2:
                # Intento heurístico de diferencia de cuadrados
                a = expr_actual.args[0]
                b = expr_actual.args[1]
                # Si tienen signos opuestos
                if (a.is_positive != b.is_positive) or (str(a).startswith('-') or str(b).startswith('-')):
                     pasos.append({
                        'titulo': 'Paso 2: Análisis de Binomio',
                        'math': f"Verificamos si ({_formato_bonito(expr_actual)}) es una Diferencia de Cuadrados (a² - b²)."
                    })
            elif len(expr_actual.args) == 3:
                 pasos.append({
                        'titulo': 'Paso 2: Análisis de Trinomio',
                        'math': f"Verificamos si ({_formato_bonito(expr_actual)}) es Trinomio Cuadrado Perfecto o de la forma ax²+bx+c."
                    })

        # 3. RESULTADO
        resultado = sp.factor(expr)
        
        if resultado == expr:
            pasos.append({'titulo': 'Análisis', 'math': 'La expresión es irreducible.'})
        else:
            pasos.append({'titulo': 'Factorización Completa', 'math': _formato_bonito(resultado)})

        return {'estado': 'exito', 'resultado_math': _formato_bonito(resultado), 'pasos': pasos}
        
    except Exception as e: return {'estado': 'error', 'mensaje': str(e), 'pasos': []}

def simplificar_expresion(expr_str):
    try:
        pasos = []
        s_expr = _limpiar_entrada(expr_str)
        try: expr = sp.sympify(s_expr)
        except: raise ValueError("Expresión inválida.")

        pasos.append({'titulo': 'Original', 'math': _formato_bonito(expr)})
        
        if expr.is_Mul or expr.is_Pow or isinstance(expr, sp.Add): pass
        else:
             num, den = sp.fraction(expr)
             if den != 1:
                 num_fact = sp.factor(num)
                 den_fact = sp.factor(den)
                 if num_fact != num or den_fact != den:
                     pasos.append({
                         'titulo': 'Paso 1: Factorizar componentes',
                         'math': f"Numerador: {_formato_bonito(num_fact)}\nDenominador: {_formato_bonito(den_fact)}"
                     })
                     pasos.append({'titulo': 'Paso 2: Cancelación', 'math': "Cancelamos factores comunes."})

        resultado = sp.simplify(expr)
        pasos.append({'titulo': 'Resultado Simplificado', 'math': _formato_bonito(resultado)})

        return {'estado': 'exito', 'resultado_math': _formato_bonito(resultado), 'pasos': pasos}
    except Exception as e: return {'estado': 'error', 'mensaje': str(e), 'pasos': []}

def resolver_polinomio(p1_str):
    try:
        pasos = []
        x = sp.symbols('x')
        s_poly = _limpiar_entrada(p1_str)
        try: poly = sp.sympify(s_poly)
        except: raise ValueError("Polinomio inválido.")
        
        pasos.append({'titulo': 'Ecuación', 'math': f'{_formato_bonito(poly)} = 0'})
        
        factored = sp.factor(poly)
        if factored != poly:
             pasos.append({'titulo': 'Paso 1: Factorizar', 'math': f'{_formato_bonito(factored)} = 0'})
             pasos.append({'titulo': 'Paso 2: Igualar a cero', 'math': 'Cada factor se iguala a 0 para hallar las raíces.'})

        soluciones = sp.solve(poly, x, dict=False)
        sol_texto = ",  ".join([f"x = {_formato_bonito(s)}" for s in soluciones])
        if not sol_texto: sol_texto = "Sin solución real."
        
        pasos.append({'titulo': 'Soluciones', 'math': sol_texto})
        return {'estado': 'exito', 'resultado_math': sol_texto, 'pasos': pasos}
    except Exception as e: return {'estado': 'error', 'mensaje': str(e), 'pasos': []}