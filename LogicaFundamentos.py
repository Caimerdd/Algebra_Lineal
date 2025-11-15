import sympy as sp
from typing import Dict, List, Any

def operar_polinomios(p1_str: str, p2_str: str, operacion: str) -> Dict[str, Any]:
    """
    Realiza operaciones con polinomios: suma, resta, multiplicación
    """
    pasos = []
    
    try:
        # Definir la variable simbólica
        x = sp.Symbol('x')
        
        # Convertir strings a expresiones sympy
        p1 = sp.sympify(p1_str.replace('^', '**'))
        p2 = sp.sympify(p2_str.replace('^', '**'))
        
        pasos.append({
            'titulo': 'Polinomios de entrada',
            'math': f'P(x) = {sp.pretty(p1, use_unicode=False)}\nQ(x) = {sp.pretty(p2, use_unicode=False)}'
        })
        
        # Realizar la operación según el tipo
        if operacion == "Suma":
            resultado = p1 + p2
            pasos.append({
                'titulo': 'Realizando suma',
                'math': f'P(x) + Q(x) = {sp.pretty(p1, use_unicode=False)} + {sp.pretty(p2, use_unicode=False)}'
            })
            
        elif operacion == "Resta":
            resultado = p1 - p2
            pasos.append({
                'titulo': 'Realizando resta',
                'math': f'P(x) - Q(x) = {sp.pretty(p1, use_unicode=False)} - {sp.pretty(p2, use_unicode=False)}'
            })
            
        elif operacion == "Multiplicación":
            resultado = p1 * p2
            pasos.append({
                'titulo': 'Realizando multiplicación',
                'math': f'P(x) × Q(x) = ({sp.pretty(p1, use_unicode=False)}) × ({sp.pretty(p2, use_unicode=False)})'
            })
        
        # Simplificar el resultado
        resultado_simplificado = sp.expand(resultado)
        pasos.append({
            'titulo': 'Resultado simplificado',
            'math': f'Resultado = {sp.pretty(resultado_simplificado, use_unicode=False)}'
        })
        
        return {
            'estado': 'exito',
            'resultado_math': sp.pretty(resultado_simplificado, use_unicode=False),
            'pasos': pasos
        }
        
    except Exception as e:
        return {
            'estado': 'error',
            'mensaje': f'Error al procesar los polinomios: {str(e)}',
            'pasos': []
        }

def resolver_polinomio(p1_str: str) -> Dict[str, Any]:
    """
    Encuentra las raíces de un polinomio
    """
    pasos = []
    
    try:
        # Definir la variable simbólica
        x = sp.Symbol('x')
        
        # Convertir string a expresión sympy
        polinomio = sp.sympify(p1_str.replace('^', '**'))
        
        pasos.append({
            'titulo': 'Polinomio de entrada',
            'math': f'P(x) = {sp.pretty(polinomio, use_unicode=False)}'
        })
        
        # Intentar factorizar primero
        polinomio_factorizado = sp.factor(polinomio)
        if polinomio_factorizado != polinomio:
            pasos.append({
                'titulo': 'Polinomio factorizado',
                'math': f'P(x) = {sp.pretty(polinomio_factorizado, use_unicode=False)}'
            })
        
        # Encontrar las raíces
        raices = sp.solve(polinomio, x)
        
        pasos.append({
            'titulo': 'Encontrando raíces',
            'math': f'Resolviendo P(x) = 0'
        })
        
        if raices:
            raices_texto = []
            for i, raiz in enumerate(raices):
                raices_texto.append(f'x_{i+1} = {sp.pretty(raiz, use_unicode=False)}')
            
            pasos.append({
                'titulo': 'Raíces encontradas',
                'math': '\n'.join(raices_texto)
            })
            
            resultado_final = f"Raíces del polinomio:\n" + '\n'.join(raices_texto)
        else:
            pasos.append({
                'titulo': 'Sin raíces reales',
                'math': 'El polinomio no tiene raíces reales'
            })
            resultado_final = "El polinomio no tiene raíces reales"
        
        return {
            'estado': 'exito',
            'resultado_math': resultado_final,
            'pasos': pasos
        }
        
    except Exception as e:
        return {
            'estado': 'error',
            'mensaje': f'Error al resolver el polinomio: {str(e)}',
            'pasos': []
        }

# Funciones adicionales que podrías necesitar
def simplificar_polinomio(p_str: str) -> Dict[str, Any]:
    """Simplifica un polinomio"""
    try:
        x = sp.Symbol('x')
        polinomio = sp.sympify(p_str.replace('^', '**'))
        simplificado = sp.expand(polinomio)
        
        return {
            'estado': 'exito',
            'resultado_math': sp.pretty(simplificado, use_unicode=False),
            'pasos': [
                {
                    'titulo': 'Polinomio original',
                    'math': f'P(x) = {sp.pretty(polinomio, use_unicode=False)}'
                },
                {
                    'titulo': 'Polinomio simplificado',
                    'math': f'P(x) = {sp.pretty(simplificado, use_unicode=False)}'
                }
            ]
        }
    except Exception as e:
        return {
            'estado': 'error',
            'mensaje': f'Error al simplificar: {str(e)}'
        }