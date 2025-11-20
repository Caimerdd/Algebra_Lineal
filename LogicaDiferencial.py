# LogicaDiferencial.py

"""
LogicaDiferencial.py - Módulo de lógica para Cálculo Diferencial en MathPro.

Incluye:
- Límite en un punto
- Derivada de f(x)
- Derivada de orden n
- Recta tangente y normal
- Tasa de cambio promedio e instantánea

Todas las funciones devuelven un diccionario con la forma:

{
    'estado': 'exito' | 'error',
    'resultado_math': str,      # Texto principal para la caja de resultado
    'resultado_str': str,       # (Opcional) Versión cruda de la expresión
    'mensaje': str,             # Mensaje de error si corresponde
    'pasos': [ {'titulo': str, 'math': str}, ... ]  # Bitácora paso a paso
}
"""

from typing import Dict, List
import sympy as sp

# Variable simbólica principal
x = sp.Symbol("x")


def _expr_to_str(expr: sp.Expr) -> str:
    """
    Convierte una expresión SymPy a string legible, usando ^ para potencias.
    """
    try:
        return sp.sstr(expr).replace("**", "^")
    except Exception:
        return str(expr)


def _parse_funcion(fx_str: str) -> sp.Expr:
    """
    Convierte un string como 'x^2 + 3*x - 4' en una expresión SymPy.
    Acepta funciones básicas: sin, cos, tan, log, exp, sqrt, etc.
    """
    if fx_str is None:
        fx_str = ""
    fx_str = fx_str.strip()
    if not fx_str:
        raise ValueError("La función f(x) no puede estar vacía.")

    # Reemplazar ^ por ** para potencias
    texto = fx_str.replace("^", "**")

    funciones = {
        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,
        "sec": sp.sec,
        "csc": sp.csc,
        "cot": sp.cot,
        "log": sp.log,
        "ln": sp.log,
        "exp": sp.exp,
        "sqrt": sp.sqrt,
        "abs": sp.Abs,
        "pi": sp.pi,
        "e": sp.E,
    }

    try:
        expr = sp.sympify(texto, locals={**funciones, "x": x})
    except Exception as e:
        raise ValueError(
            "No se pudo interpretar f(x). Revisa la sintaxis y usa 'x' como variable."
        ) from e

    if expr.free_symbols and expr.free_symbols != {x}:
        raise ValueError("Solo se permite la variable 'x' en f(x).")

    return expr


def _parse_valor(valor_str: str, nombre: str) -> sp.Expr:
    """
    Convierte un string como '1/2', '3', 'pi/4' a un número/expresión SymPy.
    """
    if valor_str is None:
        raise ValueError(f"El valor para {nombre} no puede estar vacío.")
    texto = valor_str.strip()
    if not texto:
        raise ValueError(f"El valor para {nombre} no puede estar vacío.")

    try:
        expr = sp.sympify(texto.replace("^", "**"), locals={"pi": sp.pi, "e": sp.E})
        return expr
    except Exception as e:
        raise ValueError(f"No se pudo interpretar el valor de {nombre}.") from e


# =========================================================
#   1) LÍMITE EN UN PUNTO
# =========================================================

def calcular_limite_en_punto(fx_str: str, x0_str: str) -> Dict:
    pasos: List[Dict] = []

    try:
        expr = _parse_funcion(fx_str)
        a = _parse_valor(x0_str, "x0")

        fx_pretty = _expr_to_str(expr)
        a_pretty = _expr_to_str(a)

        # Paso 1: Datos de entrada
        pasos.append(
            {
                "titulo": "Datos de entrada",
                "math": f"f(x) = {fx_pretty}\nx → {a_pretty}",
            }
        )

        # Paso 2: Reescritura / simplificación simbólica
        expr_simpl = sp.simplify(expr)
        if not sp.simplify(expr_simpl - expr) == 0:
            pasos.append(
                {
                    "titulo": "Reescritura de la función",
                    "math": (
                        "Se simplifica algebraicamente f(x) (factorización, "
                        "cancelación de términos, etc.):\n"
                        f"f(x) = {fx_pretty}\n"
                        f"= { _expr_to_str(expr_simpl) }"
                    ),
                }
            )
        else:
            pasos.append(
                {
                    "titulo": "Reescritura de la función",
                    "math": f"f(x) = {fx_pretty}",
                }
            )

        # Paso 3: Sustitución directa (si es posible)
        sust = expr_simpl.subs(x, a)
        sust_simpl = sp.simplify(sust)

        if sust_simpl.is_finite is True:
            pasos.append(
                {
                    "titulo": "Sustitución directa",
                    "math": (
                        f"Se evalúa directamente f(x) en x = {a_pretty}:\n"
                        f"f({a_pretty}) = { _expr_to_str(sust) }\n"
                        f"= { _expr_to_str(sust_simpl) }"
                    ),
                }
            )
            limite_expr = sust_simpl
        else:
            # Paso 3 alternativo: indeterminación
            pasos.append(
                {
                    "titulo": "Sustitución directa",
                    "math": (
                        f"Al sustituir x = {a_pretty} se obtiene una forma indeterminada.\n"
                        "Se requiere simplificar y aplicar propiedades de límites."
                    ),
                }
            )
            # Paso 4: Cálculo del límite simbólico
            limite_expr = sp.limit(expr_simpl, x, a)

        pasos.append(
            {
                "titulo": "Cálculo del límite",
                "math": (
                    f"lim(x→{a_pretty}) f(x)\n"
                    f"= lim(x→{a_pretty}) { _expr_to_str(expr_simpl) }\n"
                    f"= { _expr_to_str(limite_expr) }"
                ),
            }
        )

        resultado_texto = (
            f"Límite en el punto:\n"
            f"lim(x→{a_pretty}) f(x) = { _expr_to_str(limite_expr) }"
        )

        pasos.append(
            {
                "titulo": "Conclusión",
                "math": (
                    "Se ha utilizado la combinación de:\n"
                    "= Reescritura algebraica de f(x) (simplificación simbólica)\n"
                    "= Sustitución directa cuando es posible\n"
                    "= Cálculo simbólico del límite con propiedades de límites"
                ),
            }
        )

        return {
            "estado": "exito",
            "resultado_math": resultado_texto,
            "resultado_str": _expr_to_str(limite_expr),
            "pasos": pasos,
        }

    except Exception as e:
        return {
            "estado": "error",
            "mensaje": str(e),
            "pasos": pasos,
        }


# =========================================================
#   2) DERIVADA DE f(x)
# =========================================================

def derivada_fx(fx_str: str) -> Dict:
    pasos: List[Dict] = []

    try:
        expr = _parse_funcion(fx_str)
        fx_pretty = _expr_to_str(expr)

        # Paso 1: función de entrada
        pasos.append(
            {
                "titulo": "Función de entrada",
                "math": f"f(x) = {fx_pretty}",
            }
        )

        # Paso 2: explicación de reglas
        pasos.append(
            {
                "titulo": "Preparación",
                "math": (
                    "Se deriva f(x) respecto a x aplicando las reglas básicas:\n"
                    "= Regla de la potencia\n"
                    "= Regla de la suma y resta\n"
                    "= Regla del producto / cociente (si aparecen)\n"
                    "= Regla de la cadena (si hay funciones compuestas)"
                ),
            }
        )

        # Paso 3: derivada simbólica
        deriv_expr = sp.diff(expr, x)
        deriv_pretty = _expr_to_str(deriv_expr)

        pasos.append(
            {
                "titulo": "Derivada simbólica",
                "math": (
                    "f'(x) = d/dx [ f(x) ]\n"
                    f"= d/dx [ {fx_pretty} ]\n"
                    f"= {deriv_pretty}"
                ),
            }
        )

        # Paso 4: simplificación
        deriv_simpl = sp.simplify(deriv_expr)
        deriv_simpl_pretty = _expr_to_str(deriv_simpl)

        if not sp.simplify(deriv_simpl - deriv_expr) == 0:
            pasos.append(
                {
                    "titulo": "Simplificación de la derivada",
                    "math": (
                        f"f'(x) = {deriv_pretty}\n"
                        f"= {deriv_simpl_pretty}"
                    ),
                }
            )

        resultado_texto = f"Derivada de f(x):\n f'(x) = {deriv_simpl_pretty}"

        pasos.append(
            {
                "titulo": "Conclusión",
                "math": (
                    "El resultado se obtuvo aplicando reglas de derivación "
                    "término a término y simplificando la expresión final."
                ),
            }
        )

        return {
            "estado": "exito",
            "resultado_math": resultado_texto,
            "resultado_str": deriv_simpl_pretty,
            "pasos": pasos,
        }

    except Exception as e:
        return {
            "estado": "error",
            "mensaje": str(e),
            "pasos": pasos,
        }


# =========================================================
#   3) DERIVADA DE ORDEN n
# =========================================================

def derivada_orden_n(fx_str: str, n_str: str) -> Dict:
    pasos: List[Dict] = []

    try:
        expr = _parse_funcion(fx_str)
        fx_pretty = _expr_to_str(expr)

        n_expr = _parse_valor(n_str, "n")
        try:
            n_int = int(n_expr)
        except Exception:
            raise ValueError("El orden n debe ser un número entero.")

        if n_int < 1:
            raise ValueError("El orden n debe ser mayor o igual que 1.")

        # Paso 1: función y orden
        pasos.append(
            {
                "titulo": "Datos de entrada",
                "math": f"f(x) = {fx_pretty}\nOrden n = {n_int}",
            }
        )

        # Paso 2: idea del procedimiento
        pasos.append(
            {
                "titulo": "Idea del procedimiento",
                "math": (
                    "Se aplica la derivada sucesivamente n veces:\n"
                    "f^(1)(x) = f'(x)\n"
                    "f^(2)(x) = (f'(x))'\n"
                    "...\n"
                    f"f^({n_int})(x) = d^({n_int})/dx^({n_int}) [ f(x) ]"
                ),
            }
        )

        # Paso 3: cálculo simbólico
        deriv_n = sp.diff(expr, (x, n_int))
        deriv_n_pretty = _expr_to_str(deriv_n)

        pasos.append(
            {
                "titulo": "Derivada de orden n",
                "math": (
                    f"f^({n_int})(x) = d^({n_int})/dx^({n_int}) [ {fx_pretty} ]\n"
                    f"= {deriv_n_pretty}"
                ),
            }
        )

        deriv_n_simpl = sp.simplify(deriv_n)
        deriv_n_simpl_pretty = _expr_to_str(deriv_n_simpl)

        if not sp.simplify(deriv_n_simpl - deriv_n) == 0:
            pasos.append(
                {
                    "titulo": "Simplificación de la derivada",
                    "math": (
                        f"f^({n_int})(x) = {deriv_n_pretty}\n"
                        f"= {deriv_n_simpl_pretty}"
                    ),
                }
            )

        resultado_texto = (
            f"Derivada de orden {n_int}:\n"
            f"f^({n_int})(x) = {deriv_n_simpl_pretty}"
        )

        pasos.append(
            {
                "titulo": "Conclusión",
                "math": (
                    "Se ha aplicado la derivación sucesiva n veces, "
                    "usando las reglas de derivación y simplificando al final."
                ),
            }
        )

        return {
            "estado": "exito",
            "resultado_math": resultado_texto,
            "resultado_str": deriv_n_simpl_pretty,
            "pasos": pasos,
        }

    except Exception as e:
        return {
            "estado": "error",
            "mensaje": str(e),
            "pasos": pasos,
        }


# =========================================================
#   4) RECTA TANGENTE Y NORMAL
# =========================================================

def recta_tangente_y_normal(fx_str: str, x0_str: str) -> Dict:
    pasos: List[Dict] = []

    try:
        expr = _parse_funcion(fx_str)
        fx_pretty = _expr_to_str(expr)
        x0 = _parse_valor(x0_str, "x0")
        x0_pretty = _expr_to_str(x0)

        # Paso 1: datos de entrada
        pasos.append(
            {
                "titulo": "Datos de entrada",
                "math": f"f(x) = {fx_pretty}\nx0 = {x0_pretty}",
            }
        )

        # Paso 2: punto de la curva
        y0 = sp.simplify(expr.subs(x, x0))
        y0_pretty = _expr_to_str(y0)

        pasos.append(
            {
                "titulo": "Punto sobre la curva",
                "math": (
                    "Se evalúa la función en x0 para obtener el punto de tangencia:\n"
                    f"y0 = f(x0) = f({x0_pretty})\n"
                    f"= {y0_pretty}\n"
                    f"P(x0, y0) = ({x0_pretty}, {y0_pretty})"
                ),
            }
        )

        # Paso 3: derivada y pendiente de la tangente
        deriv_expr = sp.diff(expr, x)
        deriv_pretty = _expr_to_str(deriv_expr)

        m_tan = sp.simplify(deriv_expr.subs(x, x0))
        m_tan_pretty = _expr_to_str(m_tan)

        pasos.append(
            {
                "titulo": "Pendiente de la recta tangente",
                "math": (
                    "Se calcula la derivada para obtener la pendiente de la tangente:\n"
                    f"f'(x) = {deriv_pretty}\n"
                    f"m_tan = f'({x0_pretty}) = {m_tan_pretty}"
                ),
            }
        )

        # Paso 4: ecuación de la recta tangente
        t_y = sp.simplify(m_tan * (x - x0) + y0)
        t_y_pretty = _expr_to_str(t_y)

        pasos.append(
            {
                "titulo": "Ecuación de la recta tangente",
                "math": (
                    "Usamos la forma punto-pendiente:\n"
                    "y - y0 = m_tan (x - x0)\n"
                    f"y - {y0_pretty} = {m_tan_pretty}(x - {x0_pretty})\n"
                    f"y = {t_y_pretty}"
                ),
            }
        )

        # Paso 5: ecuación de la recta normal
        if m_tan == 0:
            normal_info = (
                "La pendiente de la tangente es 0, por lo que la recta normal "
                "es vertical:\n"
                f"x = {x0_pretty}"
            )
            normal_resumen = f"x = {x0_pretty}"
        else:
            m_norm = sp.simplify(-1 / m_tan)
            m_norm_pretty = _expr_to_str(m_norm)
            n_y = sp.simplify(m_norm * (x - x0) + y0)
            n_y_pretty = _expr_to_str(n_y)

            normal_info = (
                "La recta normal es perpendicular a la tangente, por lo que:\n"
                "m_norm = -1 / m_tan\n"
                f"m_norm = {m_norm_pretty}\n"
                "Ecuación punto-pendiente:\n"
                f"y - {y0_pretty} = {m_norm_pretty}(x - {x0_pretty})\n"
                f"y = {n_y_pretty}"
            )
            normal_resumen = f"y = {n_y_pretty}"

        pasos.append(
            {
                "titulo": "Ecuación de la recta normal",
                "math": normal_info,
            }
        )

        resultado_texto = (
            "Recta tangente y normal en el punto x0:\n"
            f"Punto: ({x0_pretty}, {y0_pretty})\n"
            f"Tangente: y = {t_y_pretty}\n"
            f"Normal: {normal_resumen}"
        )

        pasos.append(
            {
                "titulo": "Conclusión",
                "math": (
                    "Se utilizaron:\n"
                    "= Derivada de f(x) para obtener la pendiente de la tangente\n"
                    "= Forma punto-pendiente para construir las ecuaciones\n"
                    "= Pendiente opuesta e inversa para la recta normal"
                ),
            }
        )

        return {
            "estado": "exito",
            "resultado_math": resultado_texto,
            "resultado_str": resultado_texto,
            "pasos": pasos,
        }

    except Exception as e:
        return {
            "estado": "error",
            "mensaje": str(e),
            "pasos": pasos,
        }


# =========================================================
#   5) TASA DE CAMBIO PROMEDIO E INSTANTÁNEA
# =========================================================

def tasa_cambio_promedio_e_instantanea(fx_str: str, a_str: str, b_str: str) -> Dict:
    pasos: List[Dict] = []

    try:
        expr = _parse_funcion(fx_str)
        fx_pretty = _expr_to_str(expr)

        a = _parse_valor(a_str, "a")
        b = _parse_valor(b_str, "b")
        a_pretty = _expr_to_str(a)
        b_pretty = _expr_to_str(b)

        if sp.simplify(a - b) == 0:
            raise ValueError("Para la tasa promedio se necesita que a y b sean distintos.")

        # Paso 1: datos de entrada
        pasos.append(
            {
                "titulo": "Datos de entrada",
                "math": (
                    f"f(x) = {fx_pretty}\n"
                    f"Intervalo [a, b] = [{a_pretty}, {b_pretty}]"
                ),
            }
        )

        # Paso 2: evaluación de f(a) y f(b)
        fa = sp.simplify(expr.subs(x, a))
        fb = sp.simplify(expr.subs(x, b))
        fa_pretty = _expr_to_str(fa)
        fb_pretty = _expr_to_str(fb)

        pasos.append(
            {
                "titulo": "Valores de la función",
                "math": (
                    "Se evalúa la función en los extremos del intervalo:\n"
                    f"f(a) = f({a_pretty}) = {fa_pretty}\n"
                    f"f(b) = f({b_pretty}) = {fb_pretty}"
                ),
            }
        )

        # Paso 3: tasa de cambio promedio
        tasa_prom = sp.simplify((fb - fa) / (b - a))
        tasa_prom_pretty = _expr_to_str(tasa_prom)

        pasos.append(
            {
                "titulo": "Tasa de cambio promedio",
                "math": (
                    "Usamos la fórmula de la tasa de cambio promedio:\n"
                    "m_prom = [f(b) - f(a)] / (b - a)\n"
                    f"= [{fb_pretty} - {fa_pretty}] / ({b_pretty} - {a_pretty})\n"
                    f"= {tasa_prom_pretty}"
                ),
            }
        )

        # Paso 4: tasa de cambio instantánea (en a)
        deriv_expr = sp.diff(expr, x)
        deriv_pretty = _expr_to_str(deriv_expr)
        m_inst = sp.simplify(deriv_expr.subs(x, a))
        m_inst_pretty = _expr_to_str(m_inst)

        pasos.append(
            {
                "titulo": "Tasa de cambio instantánea",
                "math": (
                    "La tasa de cambio instantánea en x = a se obtiene de la derivada:\n"
                    f"f'(x) = {deriv_pretty}\n"
                    f"m_inst = f'({a_pretty}) = {m_inst_pretty}"
                ),
            }
        )

        resultado_texto = (
            "Tasa de cambio promedio e instantánea:\n"
            f"m_promedio en [{a_pretty}, {b_pretty}] = {tasa_prom_pretty}\n"
            f"m_instantánea en x = {a_pretty} = {m_inst_pretty}"
        )

        pasos.append(
            {
                "titulo": "Conclusión",
                "math": (
                    "La tasa de cambio promedio corresponde a la pendiente de la "
                    "recta secante que une (a, f(a)) y (b, f(b))\n"
                    "La tasa de cambio instantánea corresponde a la pendiente de la "
                    "recta tangente en x = a, calculada con la derivada f'(x)"
                ),
            }
        )

        return {
            "estado": "exito",
            "resultado_math": resultado_texto,
            "resultado_str": resultado_texto,
            "pasos": pasos,
        }

    except Exception as e:
        return {
            "estado": "error",
            "mensaje": str(e),
            "pasos": pasos,
        }
