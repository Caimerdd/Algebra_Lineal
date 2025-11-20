"""
LogicaFundamentos.py - Módulo para operaciones con polinomios
Suma, resta, multiplicación y búsqueda de raíces
trabajando siempre con fracciones exactas (sin decimales).
"""

from __future__ import annotations

from typing import Dict, List, Tuple
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

# Variable simbólica principal
X = sp.Symbol("x")

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


# ==========================
#   FUNCIONES AUXILIARES
# ==========================

def _parse_polinomio(expr_str: str) -> sp.Poly:
    """
    Convierte un string como '1/2*x^2 - 3/4*x + 1/3'
    en un objeto Poly con coeficientes racionales.
    """
    if expr_str is None:
        expr_str = "0"

    expr_str = expr_str.strip()
    if not expr_str:
        raise ValueError("El polinomio no puede estar vacío.")

    try:
        expr = parse_expr(
            expr_str,
            local_dict={"x": X},
            transformations=TRANSFORMATIONS,
        )
        # Forzar fracciones exactas
        expr = sp.nsimplify(expr, [X])
    except Exception as e:
        raise ValueError(
            "No se pudo interpretar el polinomio. "
            "Usa la variable 'x' y operadores +, -, *, /, ^."
        ) from e

    if expr.free_symbols and expr.free_symbols != {X}:
        raise ValueError("Solo se permite la variable 'x' en Fundamentos.")

    try:
        poly = sp.Poly(expr, X)
    except Exception as e:
        raise ValueError(f"El texto ingresado no es un polinomio válido: {e}") from e

    return poly


def _rational_to_str(r: sp.Rational, usar_signo: bool = False) -> str:
    """
    Convierte un Rational a string tipo '3/4' o '2'.
    Si usar_signo=True incluye el signo en el string.
    """
    if not isinstance(r, sp.Rational):
        r = sp.Rational(r)

    num = int(r.p)
    den = int(r.q)

    if den == 1:
        s = str(abs(num)) if not usar_signo else str(num)
    else:
        s = f"{abs(num)}/{den}" if not usar_signo else f"{num}/{den}"

    return s


def _formatear_termino(coef: sp.Rational, grado: int, es_primero: bool) -> str | None:
    """
    Devuelve un string como '4x^3', '- 2x', '+ 5' para un término del polinomio.
    Si el coeficiente es 0 devuelve None.
    """
    coef = sp.Rational(coef)
    if coef == 0:
        return None

    num = int(coef.p)
    den = int(coef.q)

    signo_neg = num < 0
    abs_coef = sp.Rational(abs(num), den)

    # Parte numérica sin signo
    if abs_coef == 1 and grado != 0:
        coef_str = ""
    else:
        coef_str = _rational_to_str(abs_coef, usar_signo=False)

    # Parte de la variable
    if grado == 0:
        var_str = ""
    elif grado == 1:
        var_str = "x"
    else:
        var_str = f"x^{grado}"

    base = coef_str + (var_str if var_str or coef_str else "0")

    if es_primero:
        if signo_neg:
            return "-" + base
        else:
            return base

    # No es el primero, agregamos signo con espacio
    if signo_neg:
        return " - " + base
    else:
        return " + " + base


def _poly_to_string(poly: sp.Poly) -> str:
    """
    Convierte un Poly a string bonito estilo:
    4x^4 + 5x^3 - 2x^2 + 2x - 4
    """
    if poly.is_zero:
        return "0"

    términos: List[str] = []
    grados = sorted(poly.as_dict().keys(), reverse=True)  # [(4,), (3,), ...]
    primero = True
    for g_tuple in grados:
        grado = g_tuple[0]
        coef = poly.as_dict()[g_tuple]
        t = _formatear_termino(coef, grado, primero)
        if t is not None:
            términos.append(t)
            primero = False

    return "".join(términos) if términos else "0"


def _termino_individual(coef: sp.Rational, grado: int) -> str:
    """
    Devuelve un término individual sin signos externos, por ejemplo:
    coef=6, grado=4 -> '6x^4'
    coef=-3, grado=2 -> '-3x^2'
    """
    coef = sp.Rational(coef)
    num = int(coef.p)
    den = int(coef.q)

    if den == 1:
        coef_str = str(num)
    else:
        coef_str = f"{num}/{den}"

    if grado == 0:
        return coef_str
    elif grado == 1:
        if abs(coef) == 1:
            return f"{'-' if num < 0 else ''}x"
        else:
            return f"{coef_str}x"
    else:
        if abs(coef) == 1:
            return f"{'-' if num < 0 else ''}x^{grado}"
        else:
            return f"{coef_str}x^{grado}"


def _pasos_fracciones_por_grado(
    datos: List[Tuple[sp.Rational, sp.Rational, str]]
) -> List[str]:
    """
    Genera líneas tipo:
    1/2 + 2/3 = 3/6 + 4/6 = 7/6
    3/4 - 1/4 = 2/4 = 1/2
    Para cada grado con fracciones.
    datos: lista de (coef_P, coef_Q, op) donde op es '+' o '-'
    """
    lineas: List[str] = []

    for a, b, op in datos:
        a = sp.Rational(a)
        b = sp.Rational(b)

        # Strings originales
        sa = _rational_to_str(a, usar_signo=True)
        sb = _rational_to_str(b, usar_signo=True)

        # Operación real
        if op == "+":
            r = a + b
        else:
            r = a - b

        # Si ambos son enteros, basta una línea corta
        if a.q == 1 and b.q == 1:
            sr = _rational_to_str(r, usar_signo=True)
            lineas.append(f"{sa} {op} {sb} = {sr}")
            continue

        d1, d2 = int(a.q), int(b.q)

        if d1 == d2:
            # Misma base
            num_res = int(a.p + (b.p if op == "+" else -b.p))
            intermedia = f"{num_res}/{d1}"
            sr = _rational_to_str(r, usar_signo=True)
            if intermedia == sr:
                lineas.append(f"{sa} {op} {sb} = {sr}")
            else:
                lineas.append(f"{sa} {op} {sb} = {intermedia} = {sr}")
        else:
            # Distintas bases: usamos mcm
            mcm = sp.ilcm(d1, d2)
            mult1 = mcm // d1
            mult2 = mcm // d2

            num1 = int(a.p * mult1)
            num2 = int(b.p * mult2 if op == "+" else -b.p * mult2)

            inter1 = f"{num1}/{mcm}"
            inter2 = f"{num2}/{mcm}"

            sr = _rational_to_str(r, usar_signo=True)

            lineas.append(
                f"{sa} {op} {sb} = {inter1} + {inter2} = {sr}"
            )

    return lineas


# ==========================
#   OPERACIONES PRINCIPALES
# ==========================

def operar_polinomios(p1_str: str, p2_str: str, operacion: str) -> Dict:
    """
    Realiza Suma, Resta o Multiplicación entre dos polinomios.

    Devuelve:
        {
            'estado': 'exito' / 'error',
            'resultado_math': str,
            'resultado_str': str,
            'pasos': [ {'titulo': str, 'math': str}, ... ]
        }
    """
    pasos: List[Dict] = []

    try:
        op_original = (operacion or "").strip()
        op_norm = op_original.lower()

        if op_norm in ("suma", "sumar", "+"):
            tipo = "Suma"
            simbolo_op = "+"
            es_suma = True
            es_resta = False
            es_mult = False
        elif op_norm in ("resta", "restar", "-"):
            tipo = "Resta"
            simbolo_op = "-"
            es_suma = False
            es_resta = True
            es_mult = False
        elif op_norm in ("multiplicacion", "multiplicación", "multiplicar", "*", "producto"):
            tipo = "Multiplicación"
            simbolo_op = "·"
            es_suma = es_resta = False
            es_mult = True
        else:
            raise ValueError(
                f"Operación no soportada: {operacion}. Usa Suma, Resta o Multiplicación."
            )

        p1_str = (p1_str or "").strip()
        p2_str = (p2_str or "").strip()

        if not p1_str:
            raise ValueError("El polinomio P(x) no puede estar vacío.")
        if not p2_str and not es_mult:
            raise ValueError("El polinomio Q(x) no puede estar vacío.")

        # Paso 1: mostrar polinomios de entrada
        pasos.append(
            {
                "titulo": f"{tipo} de polinomios",
                "math": f"{tipo}:\nP(x) = {p1_str}\nQ(x) = {p2_str}",
            }
        )

        # Parseo y normalización
        P = _parse_polinomio(p1_str)
        Q = _parse_polinomio(p2_str or "0")

        P_str = _poly_to_string(P)
        Q_str = _poly_to_string(Q)

        pasos.append(
            {
                "titulo": "Polinomios ordenados",
                "math": (
                    "Se ordenan los polinomios por grados descendentes, "
                    "manteniendo coeficientes fraccionarios:\n"
                    f"P(x) = {P_str}\n"
                    f"Q(x) = {Q_str}"
                ),
            }
        )

        # Conjuntos de grados
        dict_P = P.as_dict()  # {(grado,): coef}
        dict_Q = Q.as_dict()

        grados = sorted(
            {g[0] for g in dict_P.keys()} | {g[0] for g in dict_Q.keys()},
            reverse=True,
        )

        # Construcción de la línea intermedia estilo:
        # = (6x^4 + (-2x^4)) + (5x^3) + ...
        partes_intermedias: List[str] = []
        datos_fracciones: List[Tuple[sp.Rational, sp.Rational, str]] = []

        for g in grados:
            coef_P = sp.Rational(dict_P.get((g,), 0))
            coef_Q = sp.Rational(dict_Q.get((g,), 0))

            if es_mult:
                # Para multiplicación no hacemos detalle por grado aquí
                continue

            if coef_P == 0 and coef_Q == 0:
                continue

            terminos = []

            if coef_P != 0:
                terminos.append(_termino_individual(coef_P, g))

            if coef_Q != 0:
                if es_resta:
                    terminos.append(_termino_individual(-coef_Q, g))
                else:
                    terminos.append(_termino_individual(coef_Q, g))

            if not terminos:
                continue

            parentesis = "(" + " + ".join(terminos) + ")"
            partes_intermedias.append(parentesis)

            if coef_P != 0 and coef_Q != 0:
                if isinstance(coef_P, sp.Rational) and isinstance(coef_Q, sp.Rational):
                    op_sign = "+" if es_suma else "-"
                    datos_fracciones.append((coef_P, coef_Q, op_sign))

        # Operación simbólica completa
        if es_suma:
            R = P + Q
        elif es_resta:
            R = P - Q
        else:
            R = P * Q

        R_str = _poly_to_string(R)

        if es_mult:
            desarrollo = []
            desarrollo.append(
                f"P(x) {simbolo_op} Q(x) = ({P_str}) {simbolo_op} ({Q_str})"
            )
            desarrollo.append("= " + _poly_to_string(sp.Poly(sp.expand(P.as_expr() * Q.as_expr()), X)))
            desarrollo.append(f"= {R_str}")

            math_text = (
                "\n".join(desarrollo)
                + "\n\nReglas utilizadas: propiedad distributiva del producto, "
                  "producto de monomios (se suman exponentes) y agrupación de términos semejantes."
            )

            pasos.append(
                {
                    "titulo": "Desarrollo de la multiplicación",
                    "math": math_text,
                }
            )
        else:
            linea1 = f"P(x) {simbolo_op} Q(x) = ({P_str}) {simbolo_op} ({Q_str})"
            linea2 = "= " + " + ".join(partes_intermedias) if partes_intermedias else ""
            linea3 = f"= {R_str}"

            math_text = linea1
            if linea2.strip():
                math_text += "\n" + linea2
            math_text += "\n" + linea3
            math_text += (
                "\n\nReglas utilizadas: agrupación de términos semejantes, "
                "suma/resta de coeficientes fraccionarios y simplificación de signos."
            )

            pasos.append(
                {
                    "titulo": "Desarrollo algebraico paso a paso",
                    "math": math_text,
                }
            )

            if datos_fracciones:
                lineas_frac = _pasos_fracciones_por_grado(datos_fracciones)
                if lineas_frac:
                    pasos.append(
                        {
                            "titulo": "Operaciones con fracciones en los coeficientes",
                            "math": "\n".join(lineas_frac),
                        }
                    )

        return {
            "estado": "exito",
            "resultado_math": f"R(x) = {R_str}",
            "resultado_str": str(R.as_expr()),
            "pasos": pasos,
        }

    except Exception as e:
        return {
            "estado": "error",
            "mensaje": str(e),
            "pasos": pasos,
        }


def resolver_polinomio(p_str: str) -> Dict:
    """
    Encuentra las raíces exactas de un polinomio P(x).

    Devuelve:
        {
            'estado': 'exito' / 'error',
            'resultado_math': str,
            'resultado_str': str,
            'pasos': [ {'titulo': str, 'math': str}, ... ]
        }
    """
    pasos: List[Dict] = []

    try:
        p_str = (p_str or "").strip()
        if not p_str:
            raise ValueError("El polinomio P(x) no puede estar vacío.")

        # Paso 1: entrada
        pasos.append(
            {
                "titulo": "Polinomio de entrada",
                "math": f"P(x) = {p_str}",
            }
        )

        # Paso 2: parseo y normalización
        P = _parse_polinomio(p_str)
        expr = P.as_expr()
        P_str = _poly_to_string(P)

        pasos.append(
            {
                "titulo": "Normalización (forma polinómica)",
                "math": (
                    "Se escribe el polinomio ordenado por grados "
                    "y con coeficientes fraccionarios exactos:\n"
                    f"P(x) = {P_str}"
                ),
            }
        )

        # Paso 3: grado del polinomio
        grado = P.degree()
        pasos.append(
            {
                "titulo": "Grado del polinomio",
                "math": f"deg(P) = {grado}",
            }
        )

        # Caso grado 0
        if grado < 1:
            c = P.all_coeffs()[0] if P.all_coeffs() else 0
            if c == 0:
                texto = (
                    "P(x) es el polinomio nulo (0).\n"
                    "Cualquier número real es raíz: P(x) = 0 para todo x."
                )
            else:
                texto = (
                    f"P(x) = {c} ≠ 0.\n"
                    "La ecuación P(x) = 0 no tiene soluciones reales."
                )

            pasos.append(
                {
                    "titulo": "Caso especial (grado 0)",
                    "math": texto,
                }
            )
            return {
                "estado": "exito",
                "resultado_math": texto,
                "resultado_str": texto,
                "pasos": pasos,
            }

        # Paso 4: factorización simbólica
        fact = sp.factor(expr)
        if fact != expr:
            pasos.append(
                {
                    "titulo": "Factorización de P(x)",
                    "math": (
                        "Se intenta factorizar el polinomio usando reglas "
                        "como factor común, trinomio cuadrado y otras "
                        "identidades notables:\n\n"
                        f"P(x) = {sp.sstr(fact).replace('**', '^')}"
                    ),
                }
            )
        else:
            pasos.append(
                {
                    "titulo": "Factorización de P(x)",
                    "math": (
                        "El polinomio no admite una factorización sencilla "
                        "sobre los racionales.\n"
                        "Se continúa con métodos algebraicos simbólicos para "
                        "encontrar las raíces."
                    ),
                }
            )

        # Paso 5: raíces exactas (sin decimales)
        raices_dict = sp.roots(expr)  # {raiz: multiplicidad}

        if not raices_dict:
            texto = (
                "P(x) = 0 no tiene raíces reales.\n"
                "Las soluciones, si existen, son complejas o algebraicas avanzadas."
            )
            pasos.append(
                {
                    "titulo": "Conclusión",
                    "math": texto,
                }
            )
            return {
                "estado": "exito",
                "resultado_math": texto,
                "resultado_str": texto,
                "pasos": pasos,
            }

        lineas = []
        for raiz, mult in raices_dict.items():
            s_raiz = sp.sstr(raiz).replace("**", "^")
            if mult == 1:
                lineas.append(f"x = {s_raiz}")
            else:
                lineas.append(f"x = {s_raiz}   (multiplicidad {mult})")

        texto_raices = "Soluciones de P(x) = 0:\n" + "\n".join(lineas)

        pasos.append(
            {
                "titulo": "Raíces del polinomio",
                "math": texto_raices,
            }
        )

        # Paso 6: explicación del método (igual que antes)
        pasos.append(
            {
                "titulo": "Método utilizado",
                "math": (
                    "Se combinan dos ideas principales para encontrar las raíces:\n"
                    "1) Factorización simbólica de P(x), aplicando reglas como\n"
                    "   factor común, trinomios cuadráticos y otras identidades.\n"
                    "2) Cuando la factorización no es directa, SymPy resuelve la\n"
                    "   ecuación P(x) = 0 utilizando métodos algebraicos (por ejemplo,\n"
                    "   fórmula general en grado 2 y descomposición en factores "
                    "   irreducibles en grados mayores), manteniendo fracciones\n"
                    "   y radicales de forma exacta, sin convertir a decimales."
                ),
            }
        )

        return {
            "estado": "exito",
            "resultado_math": texto_raices,
            "resultado_str": texto_raices,
            "pasos": pasos,
        }

    except Exception as e:
        return {
            "estado": "error",
            "mensaje": str(e),
            "pasos": pasos,
        }
