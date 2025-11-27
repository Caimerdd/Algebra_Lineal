# Constantes Globales
DETALLE_MAX = 6
BLOQUE_DETALLE = 3
MAX_SNAPSHOTS = 80
PASO_SALTOS = 5

# --- MEJORA DE COLORES (Tema Profesional) ---

# Acento: Cambiado de Rojo/Morado a Azul Índigo/Cian Eléctrico
# Esto se ve más "matemático" y evita parecer un mensaje de error.
COLOR_ACENTO = ("#3F51B5", "#738FFE")       # Indigo 500 / Indigo A200
COLOR_HOVER = ("#303F9F", "#536DFE")        # Indigo 700 / Indigo A400

# Fondos: Un gris un poco más oscuro en Dark Mode para mejor contraste
COLOR_FONDO_SECUNDARIO = ("gray92", "#1a1a1a") 
COLOR_BOTON_SECUNDARIO = ("gray80", "#333333")
COLOR_BOTON_SECUNDARIO_HOVER = ("gray70", "#404040")

# --- Colores de Módulos (Vibrantes y Distintos) ---
# Se mantienen similares pero ajustados para no chocar con el acento
COLOR_ALGEBRA = ("#1976D2", "#2196F3")     # Azul Profundo
COLOR_NUMERICOS = ("#0097A7", "#00BCD4")   # Cian Teal
COLOR_FUNDAMENTOS = ("#388E3C", "#4CAF50") # Verde
COLOR_DIFERENCIAL = ("#F57C00", "#FF9800") # Naranja
COLOR_INTEGRAL = ("#7B1FA2", "#9C27B0")    # Morado (Ahora único, no choca con el acento)
# ----------------------------------------

COLOR_FONDO_PRINCIPAL = ("#f8f9fa", "#121212") # Fondo casi blanco / casi negro
COLOR_TARJETA = ("white", "#1e1e1e") # Tarjetas flotantes
COLOR_TEXTO_TARJETA = ("#333333", "#ffffff")

# Funciones Auxiliares (Sin cambios, ya estaban bien)
def fmt(x: float) -> str:
    """Formatea números: muestra enteros sin decimales y decimales con 4 cifras."""
    if x is None: return ""
    if abs(x) < 1e-9: return "0"
    if abs(x - round(x)) < 1e-9: return f"{int(round(x))}"
    return f"{x:.4g}"

def parse_valor(texto: str) -> float:
    texto = texto.strip()
    if not texto: return 0.0
    if '/' in texto:
        try:
            partes = texto.split('/')
            if len(partes) != 2: raise ValueError(f"Formato inválido: {texto}")
            num = float(partes[0].strip())
            den = float(partes[1].strip())
            if den == 0: raise ValueError(f"División por cero: {texto}")
            return num / den
        except Exception as e:
            raise ValueError(f"Fracción inválida: '{texto}'")
    else:
        try:
            return float(texto)
        except ValueError:
            if 'e' in texto.lower():
                try: return float(texto)
                except: pass
            raise ValueError(f"Valor inválido: '{texto}'")