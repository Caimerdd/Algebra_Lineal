import sympy as sp

def operar_polinomios(p1_str, p2_str, operacion):
    try:
        pasos = []
        x = sp.symbols('x')
        
        try:
            poly1 = sp.sympify(p1_str)
            poly2 = sp.sympify(p2_str)
        except Exception:
            raise ValueError("Formato inválido. Asegúrese de usar 'x' como variable.")

        pasos.append({
            'titulo': 'Entrada',
            'math': f'P(x) = {sp.latex(poly1)}\\nQ(x) = {sp.latex(poly2)}'
        })
        
        resultado_math = None
        
        if operacion == "Suma":
            resultado_math = sp.simplify(poly1 + poly2)
            pasos.append({'titulo': 'Operación', 'math': f'({sp.latex(poly1)}) + ({sp.latex(poly2)})'})
            
        elif operacion == "Resta":
            resultado_math = sp.simplify(poly1 - poly2)
            pasos.append({'titulo': 'Operación', 'math': f'({sp.latex(poly1)}) - ({sp.latex(poly2)})'})
            
        elif operacion == "Multiplicación":
            resultado_math = sp.expand(poly1 * poly2)
            pasos.append({'titulo': 'Operación', 'math': f'({sp.latex(poly1)}) \\cdot ({sp.latex(poly2)})'})
            
        elif operacion == "División":
            q, r = sp.div(poly1, poly2)
            pasos.append({
                'titulo': 'División', 
                'math': f'\\frac{{{sp.latex(poly1)}}}{{{sp.latex(poly2)}}}'
            })
            pasos.append({
                'titulo': 'Resultado',
                'math': f'Cociente: {sp.latex(q)} \\quad Residuo: {sp.latex(r)}'
            })
            return {
                'estado': 'exito',
                'resultado_math': str(q),
                'resultado_latex': f"Cociente: {sp.latex(q)}",
                'pasos': pasos
            }

        resultado_latex = sp.latex(resultado_math)
        
        pasos.append({
            'titulo': 'Resultado Final',
            'math': resultado_latex
        })
        
        return {
            'estado': 'exito',
            'resultado_math': str(resultado_math),
            'resultado_latex': resultado_latex,
            'pasos': pasos
        }
        
    except Exception as e:
        return {'estado': 'error', 'mensaje': f'Error: {str(e)}', 'pasos': []}

def factorizar_expresion(expr_str):
    try:
        pasos = []
        try:
            expr = sp.sympify(expr_str)
        except:
            raise ValueError("Expresión inválida.")

        pasos.append({
            'titulo': 'Expresión Original',
            'math': sp.latex(expr)
        })

        resultado = sp.factor(expr)

        if resultado == expr:
            pasos.append({'titulo': 'Análisis', 'math': 'La expresión ya es irreducible.'})
        else:
            pasos.append({'titulo': 'Factorización', 'math': f'{sp.latex(expr)} = {sp.latex(resultado)}'})

        return {
            'estado': 'exito',
            'resultado_math': str(resultado),
            'resultado_latex': sp.latex(resultado),
            'pasos': pasos
        }
    except Exception as e:
        return {'estado': 'error', 'mensaje': str(e), 'pasos': []}

def simplificar_expresion(expr_str):
    try:
        pasos = []
        try:
            expr = sp.sympify(expr_str)
        except:
            raise ValueError("Expresión inválida.")

        pasos.append({
            'titulo': 'Expresión Original',
            'math': sp.latex(expr)
        })

        resultado = sp.simplify(expr)

        pasos.append({
            'titulo': 'Expresión Simplificada',
            'math': sp.latex(resultado)
        })

        return {
            'estado': 'exito',
            'resultado_math': str(resultado),
            'resultado_latex': sp.latex(resultado),
            'pasos': pasos
        }
    except Exception as e:
        return {'estado': 'error', 'mensaje': str(e), 'pasos': []}

def resolver_polinomio(p1_str):
    try:
        pasos = []
        x = sp.symbols('x')
        try:
            poly = sp.sympify(p1_str)
        except:
            raise ValueError("Polinomio inválido.")
        
        pasos.append({'titulo': 'Ecuación', 'math': f'{sp.latex(poly)} = 0'})
        
        soluciones = sp.solve(poly, x, dict=False)
        
        sol_latex = []
        for s in soluciones:
            sol_latex.append(sp.latex(s))

        if not sol_latex:
            resultado_texto = "Sin solución."
        else:
            resultado_texto = "x \\in \\{" + ", ".join(sol_latex) + "\\}"

        pasos.append({
            'titulo': 'Conjunto Solución',
            'math': resultado_texto
        })
        
        return {
            'estado': 'exito',
            'resultado_math': str(soluciones),
            'resultado_latex': resultado_texto,
            'pasos': pasos
        }
    except Exception as e:
        return {'estado': 'error', 'mensaje': str(e), 'pasos': []}