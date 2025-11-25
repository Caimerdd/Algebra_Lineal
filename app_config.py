# app_config.py - VERSIÓN COMPLETA CORREGIDA

"""
Configuración centralizada para MathPro.
Define colores, temas y funciones auxiliares.
"""

# =============================================================================
# PALETA DE COLORES - MODOS CLARO/OSCURO
# =============================================================================

# Colores principales por área matemática (modo_claro, modo_oscuro)
COLOR_ALGEBRA = ("#3A86FF", "#2667CC")           # Azul
COLOR_NUMERICOS = ("#FF006E", "#CC0058")         # Rosa
COLOR_FUNDAMENTOS = ("#FB5607", "#C84505")       # Naranja
COLOR_DIFERENCIAL = ("#8338EC", "#5A2CA0")       # Púrpura
COLOR_INTEGRAL = ("#38B000", "#2C8A00")          # Verde

# Colores de UI
COLOR_PRIMARIO = ("#2A9D8F", "#21867A")
COLOR_SECUNDARIO = ("#E9C46A", "#D4B45B")
COLOR_ACENTO = ("#F4A261", "#C3824E")

# Colores de botones
COLOR_BOTON_PRIMARIO = COLOR_PRIMARIO
COLOR_BOTON_SECUNDARIO = ("#6C757D", "#5A6268")
COLOR_BOTON_SECUNDARIO_HOVER = ("#5A6268", "#495057")
COLOR_HOVER = ("#E76F51", "#B8573F")

# Colores de fondo
COLOR_FONDO_PRIMARIO = ("#F8F9FA", "#212529")
COLOR_FONDO_SECUNDARIO = ("#E9ECEF", "#343A40")
COLOR_TARJETA = ("#FFFFFF", "#495057")
COLOR_TEXTO_TARJETA = ("#212529", "#F8F9FA")

# =============================================================================
# FUNCIONES AUXILIARES - CRÍTICAS PARA EL FUNCIONAMIENTO
# =============================================================================

def parse_valor(texto: str) -> float:
    """
    Convierte un string a número, aceptando fracciones y expresiones matemáticas.
    Usado en múltiples módulos del proyecto.
    """
    if texto is None:
        return 0.0
    
    texto = str(texto).strip()
    
    if not texto:
        return 0.0
    
    # Reemplazar comas por puntos para decimales
    texto = texto.replace(',', '.')
    
    # Eliminar espacios en blanco
    texto = texto.replace(' ', '')
    
    # Manejar el símbolo de menos unario diferente
    texto = texto.replace('−', '-')
    
    # Caso especial: solo signo
    if texto in ('+', '-'):
        return 1.0 if texto == '+' else -1.0
    
    # Manejar fracciones simples (como "1/2")
    if '/' in texto:
        partes = texto.split('/')
        if len(partes) == 2:
            try:
                numerador = parse_valor(partes[0])  # Llamada recursiva
                denominador = parse_valor(partes[1])
                if denominador == 0:
                    raise ValueError("División por cero")
                return numerador / denominador
            except (ValueError, ZeroDivisionError):
                pass
    
    # Manejar notación científica
    if 'e' in texto.lower():
        try:
            return float(texto)
        except ValueError:
            pass
    
    # Manejar números mixtos (como "1_1/2" o "1 1/2")
    if ('_' in texto or ' ' in texto) and '/' in texto:
        try:
            if '_' in texto:
                entero_str, fraccion_str = texto.split('_', 1)
            else:
                entero_str, fraccion_str = texto.split(' ', 1)
            
            entero = parse_valor(entero_str)
            fraccion = parse_valor(fraccion_str)
            return entero + fraccion
        except (ValueError, IndexError):
            pass
    
    # Conversión normal a float
    try:
        # Manejar casos como ".5" -> "0.5"
        if texto.startswith('.') or texto.startswith('+.'):
            texto = '0' + texto
        elif texto.startswith('-.'):
            texto = '-0' + texto[1:]
            
        return float(texto)
    except ValueError as e:
        raise ValueError(f"No se pudo convertir '{texto}' a número: {str(e)}")

def fmt(valor: float, precision: int = 6) -> str:
    """
    Formatea un número para mostrar en la interfaz de manera elegante.
    
    Args:
        valor: Número a formatear
        precision: Número de dígitos significativos
    
    Returns:
        String formateado
    """
    if valor is None:
        return "0"
    
    # Manejar valores infinitos
    if abs(valor) == float('inf'):
        return "∞" if valor > 0 else "-∞"
    
    # Manejar NaN
    if valor != valor:  # NaN check
        return "NaN"
    
    # Redondear a 0 para valores muy cercanos a 0
    if abs(valor) < 1e-15:
        return "0"
    
    # Para números enteros, mostrar sin decimales
    if abs(valor - round(valor)) < 1e-10:
        return str(int(round(valor)))
    
    # Para números muy grandes o muy pequeños, usar notación científica
    if abs(valor) > 1e6 or (abs(valor) < 1e-4 and valor != 0):
        return f"{valor:.{precision}g}"
    
    # Para números decimales normales
    formatted = f"{valor:.{precision}f}"
    
    # Eliminar ceros decimales innecesarios
    if '.' in formatted:
        formatted = formatted.rstrip('0').rstrip('.')
    
    return formatted

# =============================================================================
# CONFIGURACIÓN DE TEMA
# =============================================================================

def configurar_tema():
    """
    Configura el tema de customtkinter según la apariencia del sistema.
    """
    import customtkinter as ctk
    
    # Configuración global
    ctk.set_appearance_mode("system")  # "light", "dark", o "system"
    ctk.set_default_color_theme("blue")
    
    # Configuración de fuentes
    config_fuentes = {
        "titulo": ("Arial", 20, "bold"),
        "subtitulo": ("Arial", 16, "bold"),
        "normal": ("Arial", 14),
        "monospace": ("Courier New", 12)
    }
    
    return config_fuentes

# =============================================================================
# VALIDACIONES
# =============================================================================

def validar_dimension_matriz(filas: int, columnas: int) -> bool:
    """
    Valida que las dimensiones de una matriz sean válidas.
    """
    if not isinstance(filas, int) or not isinstance(columnas, int):
        return False
    if filas <= 0 or columnas <= 0:
        return False
    if filas > 20 or columnas > 20:  # Límite razonable
        return False
    return True

def validar_rango_numerico(valor: float, min_val: float = -1e10, max_val: float = 1e10) -> bool:
    """
    Valida que un número esté en un rango razonable.
    """
    if not isinstance(valor, (int, float)):
        return False
    if valor < min_val or valor > max_val:
        return False
    return True

# =============================================================================
# CONSTANTES NUMÉRICAS
# =============================================================================

# Tolerancia para comparaciones numéricas
TOLERANCIA = 1e-10

# Límites para operaciones matriciales
MAX_FILAS = 10
MAX_COLUMNAS = 10

# Configuración de gráficas
CONFIG_GRAFICAS = {
    "ancho": 8,
    "alto": 6,
    "dpi": 100,
    "color_curva": "#1f77b4",
    "color_puntos": "#ff7f0e",
    "color_grid": "#cccccc"
}

if __name__ == "__main__":
    # Tests básicos de las funciones
    print("=== Tests app_config.py ===")
    
    # Test parse_valor
    tests = ["1", "2.5", "1/2", "3/4", "-2", "1_1/2", ".5", "1e-3"]
    for test in tests:
        try:
            resultado = parse_valor(test)
            print(f"parse_valor('{test}') = {resultado}")
        except Exception as e:
            print(f"ERROR en '{test}': {e}")
    
    # Test fmt
    tests_fmt = [0, 1, 1.0, 1.5, 0.00001, 1000000, 123.456789]
    for test in tests_fmt:
        print(f"fmt({test}) = '{fmt(test)}'")