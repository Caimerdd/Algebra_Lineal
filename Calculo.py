# Calculo.py
# Módulo para manejar toda la lógica futura de derivadas e integrales.
# Por ahora SOLO prepara la información y devuelve textos para mostrar
# en la bitácora y en el resultado, sin hacer cálculos reales.

from typing import Dict, List


def preparar_derivada(funcion_str: str,
                      variable: str,
                      orden: int,
                      punto_eval: str) -> Dict[str, List[str]]:
    """
    Prepara la información de una derivada sin calcularla todavía.
    """
    pasos: List[str] = []
    pasos.append("=== Módulo de Cálculo: DERIVADAS ===")
    pasos.append(f"Función ingresada: f({variable}) = {funcion_str}")
    pasos.append(f"Orden de la derivada: {orden}")
    if punto_eval.strip() == "":
        pasos.append("Derivada simbólica (sin punto de evaluación específico).")
    else:
        pasos.append(f"Derivada evaluada en {variable} = {punto_eval}")
    pasos.append("")
    pasos.append("Nota: Esta versión solo registra los datos de entrada.")
    pasos.append("Más adelante aquí se implementará el cálculo real de la derivada.")
    return {"estado": "pendiente", "pasos": pasos}


def preparar_integral(funcion_str: str,
                      variable: str,
                      tipo: str,
                      limite_inferior: str,
                      limite_superior: str) -> Dict[str, List[str]]:
    """
    Prepara la información de una integral sin calcularla todavía.
    tipo: 'indefinida' o 'definida'
    """
    pasos: List[str] = []
    pasos.append("=== Módulo de Cálculo: INTEGRALES ===")
    pasos.append(f"Función ingresada: f({variable}) = {funcion_str}")
    pasos.append(f"Tipo de integral: {tipo.upper()}")

    if tipo == "definida":
        pasos.append(f"Intervalo de integración: [{limite_inferior}, {limite_superior}]")
    else:
        pasos.append("Integral indefinida (sin límites).")

    pasos.append("")
    pasos.append("Nota: Esta versión solo registra los datos de entrada.")
    pasos.append("Más adelante aquí se implementará el cálculo real de la integral.")
    return {"estado": "pendiente", "pasos": pasos}


