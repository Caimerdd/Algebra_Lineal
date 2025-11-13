# Constantes Globales
DETALLE_MAX = 6
BLOQUE_DETALLE = 3
MAX_SNAPSHOTS = 80
PASO_SALTOS = 5

# Definición de Colores para Temas
COLOR_ACENTO = ("#E53935", "#7E57C2")
COLOR_HOVER = ("#F44336", "#9575CD")
COLOR_FONDO_SECUNDARIO = ("gray92", "#212121")
COLOR_BOTON_SECUNDARIO = ("gray75", "gray30")
COLOR_BOTON_SECUNDARIO_HOVER = ("gray80", "gray35")

COLOR_ALGEBRA = ("#2196F3", "#1976D2")
COLOR_NUMERICOS = ("#00BCD4", "#0097A7")
COLOR_FONDO_PRINCIPAL = ("#f8f9fa", "#121212")
COLOR_TARJETA = ("white", "#1e1e1e")
COLOR_TEXTO_TARJETA = ("#333333", "#ffffff")

# Funciones Auxiliares
def fmt(x: float) -> str:
    return f"{x:.4g}"

def parse_valor(texto: str) -> float:
    texto = texto.strip()
    if not texto:
        return 0.0

    if '/' in texto:
        try:
            partes = texto.split('/')
            if len(partes) != 2:
                raise ValueError(f"Formato de fracción inválido: {texto}")
            
            numerador = float(partes[0].strip())
            denominador = float(partes[1].strip())
            
            if denominador == 0:
                raise ValueError(f"División por cero en fracción: {texto}")
                
            return numerador / denominador
        except ValueError as e:
            raise ValueError(f"Fracción inválida: '{texto}' ({e})")
        except Exception as e:
            raise ValueError(f"Error al procesar fracción '{texto}': {e}")
    else:
        try:
            return float(texto)
        except ValueError:
            if 'e' in texto.lower():
                try:
                    return float(texto)
                except ValueError:
                     raise ValueError(f"Notación científica inválida: '{texto}'")
            raise ValueError(f"Valor numérico inválido: '{texto}'")