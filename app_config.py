# Constantes Globales
DETALLE_MAX = 6
BLOQUE_DETALLE = 3
MAX_SNAPSHOTS = 80
PASO_SALTOS = 5

# --- FUENTES ---
FONT_MAIN = "Segoe UI"  
FONT_MONO = "Consolas"

# --- PALETA DE COLORES "ROYAL NAVY" (Basada en tu imagen) ---

# 1. Fondos Principales (El lienzo de atrás)
# Light: Gris muy pálido (Casi blanco)
# Dark: #021024 (Tu azul más profundo) -> Se ve increíblemente elegante.
COLOR_FONDO_PRINCIPAL = ("#F8FAFC", "#050821") 

# 2. Fondos Secundarios (Barra Lateral y Tarjetas)
# Light: Blanco Puro
# Dark: #052659 (Tu azul intermedio) -> Da un contraste perfecto con el fondo.
COLOR_FONDO_SECUNDARIO = ("#FFFFFF", "#00183B") 

# 3. Textos
# Light: Usamos tu azul oscuro (#021024) en lugar de negro. ¡Se ve muy pro!
# Dark: Blanco Humo (#F1F5F9) para máxima legibilidad sobre el azul.
COLOR_TEXTO_PRINCIPAL = ("#021024", "#F1F5F9")
COLOR_TEXTO_SECUNDARIO = ("#475569", "#94A3B8")

# 4. Botones de Navegación
# Se funden con el panel correspondiente
COLOR_BOTON_SECUNDARIO = ("#FFFFFF", "#031C41") 
# Hover: Un tono ligeramente distinto para dar feedback visual
COLOR_BOTON_SECUNDARIO_HOVER = ("#E2E8F0", "#0A3A80") 

# 5. Acentos (El color de los botones principales y switches)
# Light: Tu azul intermedio
# Dark: Un azul acero claro (#5483B3) para que resalte sobre el fondo oscuro.
COLOR_ACENTO = ("#052659", "#5483B3") 
COLOR_HOVER = ("#021024", "#7DA0CA")

# --- COLORES DE MÓDULOS (Ajustados para combinar con el azul) ---
# Mantenemos colores distintivos pero que no "vibren" feo con el azul oscuro
COLOR_ALGEBRA = ("#0284C7", "#38BDF8")     # Sky Blue
COLOR_NUMERICOS = ("#059669", "#34D399")   # Emerald
COLOR_FUNDAMENTOS = ("#D97706", "#FBBF24") # Amber
COLOR_DIFERENCIAL = ("#DC2626", "#F87171") # Red
COLOR_INTEGRAL = ("#7C3AED", "#A78BFA")    # Violet

# Alias para compatibilidad
COLOR_TARJETA = COLOR_FONDO_SECUNDARIO 
COLOR_TEXTO_TARJETA = COLOR_TEXTO_PRINCIPAL

# Funciones Auxiliares
def fmt(x: float) -> str:
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
            if len(partes) != 2: raise ValueError
            return float(partes[0]) / float(partes[1])
        except: raise ValueError
    else:
        try: return float(texto)
        except: raise ValueError