import re
import math
# --- NUEVO INICIO ---
# Forzar a Python a buscar módulos en el directorio actual
import sys
import os
# Añade la ruta del script actual a las rutas de búsqueda de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# --- NUEVO FIN ---
from datetime import datetime
import customtkinter as ctk
from typing import List, Dict # NUEVO: Añadido Dict

# --- Constantes Globales ---

# Define la cantidad máxima de filas/columnas antes de simplificar la vista (no usado actualmente)
DETALLE_MAX = 6
BLOQUE_DETALLE = 3
# Define el número máximo de "snapshots" (pasos intermedios) a mostrar para Gauss/Inversa
MAX_SNAPSHOTS = 80
# Define cada cuántos pasos mostrar un snapshot después de los primeros 20
PASO_SALTOS = 5

# --- Definición de Colores para Temas ---
# Define los colores de acento para modo claro (Rojo) y oscuro (Morado)
COLOR_ACENTO = ("#E53935", "#7E57C2")
COLOR_HOVER = ("#F44336", "#9575CD")
# Define colores de fondo secundarios para los marcos de las matrices
COLOR_FONDO_SECUNDARIO = ("gray92", "#212121")
# Define colores para botones secundarios (como "Limpiar")
COLOR_BOTON_SECUNDARIO = ("gray75", "gray30")
COLOR_BOTON_SECUNDARIO_HOVER = ("gray80", "gray35")

# --- Funciones Auxiliares ---

def _fmt(x: float) -> str:
    """Formatea un número flotante a una cadena con 4 decimales significativos."""
    return f"{x:.4g}"

def _parse_valor(texto: str) -> float:
    """
    Convierte un texto a float. Acepta números normales (ej: '1.5', '-2')
    y fracciones (ej: '1/3', '-5/2').
    """
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
            # NUEVO: Permitir 'e' para notación científica
            if 'e' in texto.lower():
                try:
                    return float(texto)
                except ValueError:
                     raise ValueError(f"Notación científica inválida: '{texto}'")
            raise ValueError(f"Valor numérico inválido: '{texto}'")

# --- Clase Principal de la Aplicación ---

class AplicacionPrincipal(ctk.CTk):
    """
    Clase principal que hereda de ctk.CTk y maneja toda la aplicación,
    incluyendo la ventana, navegación y paneles de contenido.
    """
    
    def __init__(self):
        """Constructor de la aplicación. Inicializa la ventana y los componentes principales."""
        super().__init__()
        
        self.title("Menú Principal Mathpro")
        self.geometry("900x650")
        self.minsize(800, 600)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.font_normal = ctk.CTkFont(size=13)
        self.font_bold_label = ctk.CTkFont(size=14, weight="bold")
        # NUEVO: Fuente monoespaciada para tablas y resultados
        self.font_mono = ctk.CTkFont(family="monospace", size=14)
        
        self._crear_panel_nav()
        self._crear_panel_principal()
        
        self.seccion_actual = None
        self.mostrar_seccion('Álgebra Lineal')
        
        self.actualizar_fecha_hora()

    def toggle_theme(self):
        """Cambia entre modo claro y oscuro basado en el estado del switch."""
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def _crear_panel_nav(self):
        """Crea el panel de navegación lateral izquierdo."""
        self.marco_nav = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.marco_nav.grid(row=0, column=0, sticky="nswe")
        # NUEVO: Ajustada la fila del espacio flexible (de 6 a 7)
        self.marco_nav.grid_rowconfigure(7, weight=1) 
        
        ctk.CTkLabel(self.marco_nav, text="Menú", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=12, pady=(12, 8), sticky="w")
        
        ctk.CTkButton(self.marco_nav, text="   Álgebra Lineal", anchor="w",
                      fg_color=COLOR_ACENTO, hover_color=COLOR_HOVER,
                      command=lambda: self.mostrar_seccion('Álgebra Lineal')).grid(row=1, column=0, sticky="ew", padx=12, pady=6)
        
        # NUEVO: Botón para Métodos Numéricos
        ctk.CTkButton(self.marco_nav, text="   Métodos Numéricos", anchor="w",
                      fg_color=COLOR_ACENTO, hover_color=COLOR_HOVER,
                      command=lambda: self.mostrar_seccion('Métodos Numéricos')).grid(row=2, column=0, sticky="ew", padx=12, pady=6)
        
        # NUEVO: Fila del espacio flexible ajustada (de 6 a 7)
        ctk.CTkLabel(self.marco_nav, text="").grid(row=7, column=0, sticky="nswe") 

        self.theme_switch = ctk.CTkSwitch(self.marco_nav, text="Modo Oscuro", command=self.toggle_theme,
                                          progress_color=COLOR_ACENTO)
        # NUEVO: Fila del switch ajustada (de 7 a 8)
        self.theme_switch.grid(row=8, column=0, padx=12, pady=10, sticky="w")
        
        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()

    def _crear_panel_principal(self):
        """Crea el panel principal derecho que contendrá la cabecera y el contenido."""
        self.marco_principal = ctk.CTkFrame(self, corner_radius=0)
        self.marco_principal.grid(row=0, column=1, sticky="nswe", padx=12, pady=12)
        self.marco_principal.grid_rowconfigure(0, weight=0)
        self.marco_principal.grid_rowconfigure(1, weight=1)
        self.marco_principal.grid_columnconfigure(0, weight=1)

        self.cabecera = ctk.CTkFrame(self.marco_principal, height=60, corner_radius=0)
        self.cabecera.grid(row=0, column=0, sticky="ew")
        self.cabecera.grid_columnconfigure(0, weight=1)
        
        self.etiqueta_cabecera = ctk.CTkLabel(self.cabecera, text="", font=ctk.CTkFont(size=20, weight="bold"))
        self.etiqueta_cabecera.grid(row=0, column=0, sticky="w", padx=10)
        
        self.etiqueta_fecha_hora = ctk.CTkLabel(self.cabecera, text="", font=ctk.CTkFont(size=11))
        self.etiqueta_fecha_hora.grid(row=0, column=1, sticky="e", padx=10)

        self.contenido = ctk.CTkFrame(self.marco_principal, corner_radius=6)
        self.contenido.grid(row=1, column=0, sticky="nswe", pady=(12, 0))
        self.contenido.grid_rowconfigure(0, weight=1)
        self.contenido.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.contenido, text="Selecciona una sección del menú a la izquierda.", anchor="w").grid(row=0, column=0, sticky="nw", padx=12, pady=12)

    def mostrar_seccion(self, nombre: str):
        """
        Carga la UI correspondiente a la sección 'nombre' en el panel 'contenido'.
        """
        self.seccion_actual = nombre
        self.etiqueta_cabecera.configure(text=nombre)
        
        for w in self.contenido.winfo_children(): w.destroy()
        
        if nombre == 'Álgebra Lineal':
            self._cargar_ui_algebra_lineal()
        # NUEVO: Caso para la nueva sección
        elif nombre == 'Métodos Numéricos':
            self._cargar_ui_metodos_numericos()
        else:
            ctk.CTkLabel(self.contenido, text=f"Has seleccionado: {nombre}\n\nContenido de ejemplo.", justify="left").grid(row=0, column=0, sticky="nw", padx=12, pady=12)

    # --- (Inicio de la sección de Álgebra Lineal) ---
    def _cargar_ui_algebra_lineal(self):
        """Construye y carga todos los widgets para la calculadora de Álgebra Lineal."""
        
        # Configura el layout del panel 'contenido' para esta sección
        self.contenido.grid_rowconfigure(0, weight=0) # Barra de operación
        self.contenido.grid_rowconfigure(1, weight=0) # Cuadro de ecuaciones
        self.contenido.grid_rowconfigure(2, weight=1) # Área de matrices (A y B)
        self.contenido.grid_rowconfigure(3, weight=0) # Botones (Calcular, Limpiar)
        self.contenido.grid_rowconfigure(4, weight=1) # Área de resultados (Pasos, Resultado)
        self.contenido.grid_columnconfigure(0, weight=1)

        # --- Barra superior de controles (Operación, Gauss, Generar) ---
        barra = ctk.CTkFrame(self.contenido)
        barra.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        
        self.opcion_var = ctk.StringVar(value="Gauss/Gauss-Jordan")
        ctk.CTkLabel(barra, text="Operación:", font=self.font_normal).grid(row=0, column=0, padx=(4,2))
        
        # Dropdown para seleccionar la operación
        ctk.CTkOptionMenu(barra, values=["Suma","Resta","Multiplicación","Gauss/Gauss-Jordan", "Regla de Cramer", "Independencia","Inversa", "Determinante"],
                          variable=self.opcion_var, fg_color=COLOR_ACENTO, button_color=COLOR_ACENTO, button_hover_color=COLOR_HOVER,
                          dropdown_fg_color=COLOR_FONDO_SECUNDARIO, dropdown_hover_color=COLOR_HOVER
                          ).grid(row=0, column=1, padx=(8,8))
        
        # Dropdown para el modo Gauss (se muestra/oculta)
        self.modo_gauss_var = ctk.StringVar(value="Gauss-Jordan")
        self.menu_modo_gauss = ctk.CTkOptionMenu(barra, values=["Gauss","Gauss-Jordan"], variable=self.modo_gauss_var,
                                                 fg_color=COLOR_ACENTO, button_color=COLOR_ACENTO, button_hover_color=COLOR_HOVER,
                                                 dropdown_fg_color=COLOR_FONDO_SECUNDARIO, dropdown_hover_color=COLOR_HOVER)
        self.menu_modo_gauss.grid(row=0, column=2, padx=(4,4))
        self.menu_modo_gauss.grid_remove() # Oculto por defecto

        try: self.opcion_var.trace_add('write', lambda *_: self.al_cambiar_operacion())
        except Exception: self.opcion_var.trace('w', lambda *_: self.al_cambiar_operacion()) 

        ctk.CTkButton(barra, text="Generar Cuadrícula Matricial", command=self.generar_cuadriculas_matriz,
                      fg_color=COLOR_ACENTO, hover_color=COLOR_HOVER).grid(row=0, column=3, padx=(16,4))

        # --- Marco para ingresar ecuaciones (para Gauss y Cramer) ---
        self.marco_ecuaciones = ctk.CTkFrame(self.contenido)
        self.marco_ecuaciones.grid(row=1, column=0, sticky="ew", padx=12, pady=(4, 8))
        self.marco_ecuaciones.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.marco_ecuaciones, text="O ingrese ecuaciones (para Gauss/Cramer):", font=self.font_normal).grid(row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(4,2))
        
        self.caja_ecuaciones = ctk.CTkTextbox(self.marco_ecuaciones, height=100, font=self.font_normal)
        self.caja_ecuaciones.grid(row=1, column=0, sticky="ew", padx=(8,4), pady=4)
        self.caja_ecuaciones.insert("0.0", "Ej: 2x + 3y - z = 5\n     x - y + 2z = 10\n     3x + 2y = 0")
        
        ctk.CTkButton(self.marco_ecuaciones, text="↓ Poblar Matrices ↓", command=self.parsear_y_poblar_ecuaciones,
                      fg_color=COLOR_ACENTO, hover_color=COLOR_HOVER).grid(row=1, column=1, sticky="ns", padx=(4,8), pady=4)

        # --- Contenedor central para las matrices A y B ---
        medio = ctk.CTkFrame(self.contenido)
        medio.grid(row=2, column=0, sticky="nswe", padx=8, pady=4)
        medio.grid_columnconfigure(0, weight=1)
        medio.grid_columnconfigure(1, weight=1)

        # --- Marco para Matriz A ---
        self.marco_a = ctk.CTkFrame(medio, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_a.grid(row=0, column=0, sticky="nswe", padx=(0,6))
        self.etiqueta_a = ctk.CTkLabel(self.marco_a, text="Matriz A", font=self.font_bold_label)
        self.etiqueta_a.grid(row=0, column=0, columnspan=4, sticky="w", padx=8, pady=6)
        
        marco_dims_a = ctk.CTkFrame(self.marco_a, fg_color="transparent")
        marco_dims_a.grid(row=1, column=0, columnspan=4, sticky="ew", padx=8, pady=(0, 4))
        ctk.CTkLabel(marco_dims_a, text="Filas:", font=self.font_normal).grid(row=0, column=0, padx=(0,2))
        
        self.var_filas_a = ctk.StringVar(value="2")
        self.ent_filas_a = ctk.CTkEntry(marco_dims_a, width=50, textvariable=self.var_filas_a, border_color=COLOR_ACENTO)
        self.ent_filas_a.grid(row=0, column=1, padx=(0,8))
        
        try: self.var_filas_a.trace_add('write', lambda *_: self._sincronizar_filas_cramer())
        except Exception: self.var_filas_a.trace('w', lambda *_: self._sincronizar_filas_cramer())
        
        ctk.CTkLabel(marco_dims_a, text="Cols:", font=self.font_normal).grid(row=0, column=2, padx=(4,2))
        self.ent_columnas_a = ctk.CTkEntry(marco_dims_a, width=50, border_color=COLOR_ACENTO)
        self.ent_columnas_a.insert(0,"2")
        self.ent_columnas_a.grid(row=0, column=3)
        
        self.lbl_coef_a = ctk.CTkLabel(self.marco_a, text="α:", font=self.font_normal)
        self.lbl_coef_a.grid(row=11, column=0, sticky="w", padx=(8,2), pady=(4,2))
        self.ent_coef_a = ctk.CTkEntry(self.marco_a, width=48, border_color=COLOR_ACENTO)
        self.ent_coef_a.grid(row=11, column=0, sticky="w", padx=(36,0), pady=(4,2))

        # --- Marco para Matriz B ---
        self.marco_b = ctk.CTkFrame(medio, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_b.grid(row=0, column=1, sticky="nswe", padx=(6,0))
        self.etiqueta_b = ctk.CTkLabel(self.marco_b, text="Matriz B", font=self.font_bold_label)
        self.etiqueta_b.grid(row=0, column=0, columnspan=4, sticky="w", padx=8, pady=6)
        
        self.marco_dims_b = ctk.CTkFrame(self.marco_b, fg_color="transparent")
        self.marco_dims_b.grid(row=1, column=0, columnspan=4, sticky="ew", padx=8, pady=(0, 4))
        ctk.CTkLabel(self.marco_dims_b, text="Filas:", font=self.font_normal).grid(row=0, column=0, padx=(0,2))
        self.ent_filas_b = ctk.CTkEntry(self.marco_dims_b, width=50, border_color=COLOR_ACENTO)
        self.ent_filas_b.insert(0,"2")
        self.ent_filas_b.grid(row=0, column=1, padx=(0,8))
        
        self.lbl_cols_b = ctk.CTkLabel(self.marco_dims_b, text="Cols:", font=self.font_normal)
        self.lbl_cols_b.grid(row=0, column=2, padx=(4,2))
        
        self.ent_columnas_b = ctk.CTkEntry(self.marco_dims_b, width=50, border_color=COLOR_ACENTO)
        self.ent_columnas_b.insert(0,"2")
        self.ent_columnas_b.grid(row=0, column=3)
        
        self.lbl_coef_b = ctk.CTkLabel(self.marco_b, text="β:", font=self.font_normal)
        self.lbl_coef_b.grid(row=11, column=0, sticky="w", padx=(8,2), pady=(4,2))
        self.ent_coef_b = ctk.CTkEntry(self.marco_b, width=48, border_color=COLOR_ACENTO)
        self.ent_coef_b.grid(row=11, column=0, sticky="w", padx=(36,0), pady=(4,2))

        # --- Marco para botones de control (Calcular, Limpiar) ---
        controles = ctk.CTkFrame(self.contenido)
        controles.grid(row=3, column=0, sticky="ew", padx=12, pady=(6,12))
        
        ctk.CTkButton(controles, text="Calcular", command=self.calcular_operacion,
                      fg_color=COLOR_ACENTO, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        
        ctk.CTkButton(controles, text="Limpiar", command=self.limpiar_matrices,
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=1, padx=6)

        # --- Contenedor inferior para Pasos y Resultado ---
        inferior = ctk.CTkFrame(self.contenido)
        inferior.grid(row=4, column=0, sticky="nswe", padx=12, pady=(6,12))
        inferior.grid_rowconfigure(0, weight=1)
        inferior.grid_columnconfigure(0, weight=1)
        inferior.grid_columnconfigure(1, weight=1)
        
        # --- Marco para Pasos ---
        self.marco_pasos = ctk.CTkFrame(inferior)
        self.marco_pasos.grid(row=0, column=0, sticky="nswe", padx=(0,6))
        self.marco_pasos.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.marco_pasos, text="Pasos:", font=self.font_bold_label).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        # NUEVO: Fuente monoespaciada y más grande
        self.pasos_caja = ctk.CTkTextbox(self.marco_pasos, height=220, font=self.font_mono)
        self.pasos_caja.grid(row=1, column=0, sticky="nswe", padx=8, pady=(0,8))
        
        # --- Marco para Resultado ---
        self.marco_resultado = ctk.CTkFrame(inferior)
        self.marco_resultado.grid(row=0, column=1, sticky="nswe", padx=(6,0))
        self.marco_resultado.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.marco_resultado, text="Resultado:", font=self.font_bold_label).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        # NUEVO: Fuente monoespaciada y más grande
        self.resultado_caja = ctk.CTkTextbox(self.marco_resultado, height=220, font=self.font_mono)
        self.resultado_caja.grid(row=1, column=0, sticky="nswe", padx=8, pady=(0,8))

        # Listas para almacenar las referencias a los widgets de entrada (las celdas de la matriz)
        self.entradas_a = []
        self.entradas_b = []
        self.grilla_a = [] # Almacena widgets para poder destruirlos luego
        self.grilla_b = []
        
        # Llama a la función para ajustar la UI al modo por defecto (Gauss)
        self.al_cambiar_operacion()

    def _sincronizar_filas_cramer(self):
        """
        Función especial para Cramer: se asegura que las filas de B
        siempre coincidan con las filas de A y bloquea la entrada de filas en B.
        """
        if hasattr(self, 'opcion_var') and self.opcion_var.get() == 'Regla de Cramer':
            filas_a_val = self.var_filas_a.get()
            if hasattr(self, 'ent_filas_b') and self.ent_filas_b.get() != filas_a_val:
                estado_previo = self.ent_filas_b.cget("state")
                self.ent_filas_b.configure(state="normal") # Habilita para escribir
                self.ent_filas_b.delete(0, 'end')
                self.ent_filas_b.insert(0, filas_a_val)
                self.ent_filas_b.configure(state=estado_previo) # Restaura estado (readonly)

    def _set_resultado(self, texto: str, limpiar_pasos=False):
        """Helper para escribir texto en la caja de resultados."""
        if limpiar_pasos: 
            self.pasos_caja.delete('0.0', 'end')
        self.resultado_caja.delete('0.0', 'end')
        self.resultado_caja.insert('0.0', texto)

    def _append_matriz(self, M, titulo=None):
        """Helper para formatear e imprimir una matriz en la caja de pasos."""
        if titulo: 
            self.pasos_caja.insert('end', f'{titulo}\n')
        for f in M: 
            self.pasos_caja.insert('end', '  '.join(_fmt(v) for v in f) + '\n')
        self.pasos_caja.insert('end', '\n')

    def _leer_escalar(self, e):
        """Lee el valor de un escalar (alfa/beta). Devuelve 1.0 o -1.0 por defecto."""
        t = e.get().strip() if e else ''
        if t in ('','+'): return 1.0 # Vacío o '+' es 1.0
        if t == '-': return -1.0      # '-' es -1.0
        try:
            return _parse_valor(t)
        except ValueError as err:
            raise ValueError(f"Valor de escalar inválido: {err}")

    def _es_grande(self, f, c):
        """Comprueba si las dimensiones son mayores que el máximo de detalle."""
        return max(f, c) > DETALLE_MAX

    def generar_cuadriculas_matriz(self):
        """
        Crea dinámicamente las celdas de entrada (CTkEntry) para
        las matrices A y B según las dimensiones especificadas.
        """
        op = self.opcion_var.get()
        # Determina si la Matriz B es necesaria para la operación actual
        usa_b = op not in ('Gauss/Gauss-Jordan','Independencia','Inversa', 'Determinante')
        filas_a, cols_a, filas_b, cols_b = 0, 0, 0, 0 

        try:
            # --- Validación de Dimensiones de A ---
            try:
                filas_a = int(self.ent_filas_a.get())
                cols_a = int(self.ent_columnas_a.get())
                if filas_a <= 0 or cols_a <= 0:
                    raise ValueError("positivas")
            except ValueError:
                raise ValueError("las dimensiones de A deben ser números enteros positivos")

            # --- Validación de Dimensiones de B (si se usa) ---
            if usa_b:
                try:
                    filas_b = int(self.ent_filas_b.get())
                    cols_b = int(self.ent_columnas_b.get())
                    if filas_b <= 0 or cols_b <= 0:
                        raise ValueError("positivas")
                except ValueError:
                    raise ValueError("las dimensiones de B deben ser números enteros positivos")

            # --- Validación Específica por Operación ---
            if op == 'Regla de Cramer':
                if filas_a != cols_a:
                    raise ValueError(f"para Cramer, A ({filas_a}x{cols_a}) debe ser cuadrada (n x n)")
                if not usa_b: 
                    raise ValueError("error interno: Cramer requiere matriz B")
                if cols_b != 1:
                    raise ValueError(f"para Cramer, B ({filas_b}x{cols_b}) debe ser un vector columna (n x 1)")
                if filas_a != filas_b:
                    raise ValueError(f"para Cramer: filas(A)={filas_a} != filas(B)={filas_b}")
            elif op in ('Inversa', 'Determinante'):
                 if filas_a != cols_a:
                       raise ValueError(f"para {op.lower()}, A ({filas_a}x{cols_a}) debe ser cuadrada")
            elif op == 'Multiplicación':
                if cols_a != filas_b:
                    raise ValueError(f"para multiplicación: cols(A)={cols_a} != filas(B)={filas_b}")
            elif op in ('Suma', 'Resta'):
                 if filas_a != filas_b or cols_a != cols_b:
                       raise ValueError(f"para suma/resta: dims(A)={filas_a}x{cols_a} != dims(B)={filas_b}x{cols_b}")

        except ValueError as e:
            self._set_resultado(f'Error: {e}')
            return
        except Exception as e:
            self._set_resultado(f'Error inesperado al leer dimensiones: {e}')
            return

        # --- Creación de Cuadrículas ---
        # Destruye los widgets de entrada (celdas) antiguos
        for widget in self.grilla_a: widget.destroy()
        for widget in self.grilla_b: widget.destroy()
        self.grilla_a = []
        self.grilla_b = []

        # Inicializa las listas que contendrán las referencias a los widgets
        self.entradas_a = [[None]*cols_a for _ in range(filas_a)]
        self.entradas_b = [[None]*cols_b for _ in range(filas_b)] if usa_b else []

        # Fila donde empiezan a dibujarse las celdas (debajo de los controles de dims)
        start_row = 2
        
        # Crea la cuadrícula para A
        for i in range(filas_a):
            for j in range(cols_a):
                e = ctk.CTkEntry(self.marco_a, width=60, border_color=COLOR_ACENTO)
                e.grid(row=start_row + i, column=j, padx=2, pady=2, columnspan=1)
                self.grilla_a.append(e) # Guarda para destruir luego
                self.entradas_a[i][j] = e # Guarda en la matriz 2D de referencias

        # Crea la cuadrícula para B (si se usa)
        if usa_b:
            for i in range(filas_b):
                for j in range(cols_b):
                    e2 = ctk.CTkEntry(self.marco_b, width=60, border_color=COLOR_ACENTO)
                    e2.grid(row=start_row + i, column=j, padx=2, pady=2, columnspan=1)
                    self.grilla_b.append(e2)
                    self.entradas_b[i][j] = e2

        # Mensaje de éxito
        if op == 'Gauss/Gauss-Jordan': self._set_resultado('Matriz aumentada [A | b] lista')
        elif op == 'Regla de Cramer': self._set_resultado('Matriz A (n x n) y vector B (n x 1) listos')
        elif op in ('Inversa', 'Determinante'): self._set_resultado('Matriz A (cuadrada) lista')
        else: self._set_resultado('Matrices listas')

    def _poblar_cuadricula(self, entradas_grid: List[List[ctk.CTkEntry]], datos: List[List[float]]):
        """
        Rellena una cuadrícula de widgets CTkEntry (entradas_grid)
        con los valores de una matriz 2D (datos).
        """
        filas_grid = len(entradas_grid)
        cols_grid = len(entradas_grid[0]) if filas_grid > 0 else 0
        filas_datos = len(datos)
        cols_datos = len(datos[0]) if filas_datos > 0 else 0

        # Itera solo hasta las dimensiones mínimas de la cuadrícula y los datos
        for i in range(min(filas_grid, filas_datos)):
            for j in range(min(cols_grid, cols_datos)):
                if entradas_grid[i][j]:
                    entradas_grid[i][j].delete(0, 'end')
                    entradas_grid[i][j].insert(0, _fmt(datos[i][j]))

    def parsear_y_poblar_ecuaciones(self):
        """
        Analiza el texto de la 'caja_ecuaciones', extrae las variables
        y coeficientes, y rellena las cuadrículas de matrices.
        """
        op = self.opcion_var.get()
        if op not in ('Gauss/Gauss-Jordan', 'Regla de Cramer'):
            self._set_resultado("La importación de ecuaciones solo funciona con 'Gauss/Gauss-Jordan' y 'Regla de Cramer'.")
            return
            
        try:
            texto_completo = self.caja_ecuaciones.get('1.0', 'end')
            # Filtra líneas vacías o sin '='
            lineas = [linea.strip() for linea in texto_completo.split('\n') if linea.strip() and '=' in linea]
            if not lineas:
                raise ValueError("No se encontraron ecuaciones válidas (deben contener '=')")

            var_map: Dict[str, int] = {} # Diccionario para mapear nombre de variable a índice (ej: 'x' -> 0, 'y' -> 1)
            var_ordenadas: List[str] = [] # Lista para mantener el orden de las variables
            matriz_coef_dict: List[Dict[str, float]] = [] # Lista de diccionarios (uno por fila)
            vector_const: List[float] = [] # Lista para los valores a la derecha del '='

            # Expresión regular para encontrar términos como +2x, -3.5y, z, -x2
            # Captura: (signo), (coeficiente), (variable)
            regex_termino = re.compile(r'([+-]?)(\d*\.?\d*)\s*\*?\s*([a-zA-Z]\w*)')

            for linea in lineas:
                partes = linea.split('=', 1)
                if len(partes) != 2: continue
                lhs, rhs = partes[0].strip(), partes[1].strip()

                # Parsea el lado derecho (constante)
                constante = _parse_valor(rhs)
                vector_const.append(constante)
                
                # Diccionario para los coeficientes de esta fila
                fila_coef: Dict[str, float] = {}
                # Limpia el lado izquierdo
                lhs_limpio = lhs.replace(' ', '').replace('−', '-')
                
                # Asegura que el primer término tenga un signo para el regex
                if lhs_limpio and lhs_limpio[0] not in ('+', '-'):
                    lhs_limpio = '+' + lhs_limpio
                
                # Itera sobre todos los términos encontrados por el regex
                for match in regex_termino.finditer(lhs_limpio):
                    signo, coeff_str, var_str = match.groups()
                    
                    # Si es una variable nueva, la registra
                    if var_str not in var_map:
                        var_map[var_str] = len(var_ordenadas)
                        var_ordenadas.append(var_str)
                    
                    # Determina el valor del coeficiente (ej: 'z' -> 1.0, '3.5y' -> 3.5)
                    coeff_val = 1.0
                    if coeff_str:
                        coeff_val = _parse_valor(coeff_str)
                    
                    # Aplica el signo
                    if signo == '-':
                        coeff_val = -coeff_val
                    
                    # Acumula el coeficiente (en caso de '2x + 3x')
                    fila_coef[var_str] = fila_coef.get(var_str, 0.0) + coeff_val

                matriz_coef_dict.append(fila_coef)

            num_filas = len(lineas)
            num_vars = len(var_ordenadas)
            
            # --- Construye las matrices finales ---
            
            # Construye la matriz de coeficientes A
            matriz_a = [[0.0] * num_vars for _ in range(num_filas)]
            for i, fila_coef in enumerate(matriz_coef_dict):
                for var_str, coeff_val in fila_coef.items():
                    j = var_map[var_str] # Obtiene el índice de columna para esta variable
                    matriz_a[i][j] = coeff_val
            
            # Construye el vector B (n x 1)
            matriz_b = [[val] for val in vector_const]

            # --- Actualiza la UI ---
            
            # Actualiza los campos de dimensiones en la UI
            self.var_filas_a.set(str(num_filas))
            self.ent_columnas_a.delete(0, 'end')
            self.ent_columnas_a.insert(0, str(num_vars))
            
            self.ent_filas_b.delete(0, 'end')
            self.ent_filas_b.insert(0, str(num_filas))
            self.ent_columnas_b.delete(0, 'end')
            self.ent_columnas_b.insert(0, "1")

            # Genera las cuadrículas vacías con las nuevas dimensiones
            self.generar_cuadriculas_matriz()
            
            # Rellena las cuadrículas según la operación
            if op == 'Gauss/Gauss-Jordan':
                # Para Gauss, A es la matriz aumentada [A|B]
                matriz_aumentada = [matriz_a[i] + matriz_b[i] for i in range(num_filas)]
                
                # Ajusta las columnas de A para incluir B
                self.ent_columnas_a.delete(0, 'end')
                self.ent_columnas_a.insert(0, str(num_vars + 1)) # n x (n+1)
                
                self.generar_cuadriculas_matriz() # Regenerar con tamaño [A|B]
                
                self._poblar_cuadricula(self.entradas_a, matriz_aumentada)
                self._set_resultado(f"Matriz aumentada [A|B] poblada desde {num_filas} ecuaciones.\nVariables: {', '.join(var_ordenadas)}")
            
            elif op == 'Regla de Cramer':
                # Para Cramer, son A y B por separado
                self._poblar_cuadricula(self.entradas_a, matriz_a)
                self._poblar_cuadricula(self.entradas_b, matriz_b)
                self._set_resultado(f"Matriz A y vector B poblados desde {num_filas} ecuaciones.\nVariables: {', '.join(var_ordenadas)}")
                
        except ValueError as e:
            self._set_resultado(f"Error al analizar ecuaciones: {e}")
        except Exception as e:
            self._set_resultado(f"Error inesperado: {e}")

    def al_cambiar_operacion(self):
        """
        Actualiza la visibilidad y configuración de los widgets
        de la UI según la operación matemática seleccionada.
        """
        op = self.opcion_var.get()
        
        # Visibilidad del cuadro de ecuaciones
        if op in ('Gauss/Gauss-Jordan', 'Regla de Cramer'):
            self.marco_ecuaciones.grid() # Muestra
        else:
            self.marco_ecuaciones.grid_remove() # Oculta

        # Actualiza la etiqueta de la Matriz A
        if op == 'Independencia': self.etiqueta_a.configure(text='Conjunto de Vectores (por filas)')
        elif op == 'Gauss/Gauss-Jordan': self.etiqueta_a.configure(text='Matriz Aumentada [A|B]')
        elif op == 'Regla de Cramer': self.etiqueta_a.configure(text='Matriz A (Coeficientes)')
        elif op in ('Inversa', 'Determinante'): self.etiqueta_a.configure(text='Matriz A (Cuadrada)')
        else: self.etiqueta_a.configure(text='Matriz A')
        
        # Configuración especial para Cramer (Vector B)
        if op == 'Regla de Cramer':
            self.etiqueta_b.configure(text='Vector B (Resultados)')
            self._sincronizar_filas_cramer() # Sincroniza filas A y B
            self.ent_columnas_b.delete(0, 'end')
            self.ent_columnas_b.insert(0, "1")
            self.lbl_cols_b.grid_remove() # Oculta control de columnas de B
            self.ent_columnas_b.grid_remove()
            self.ent_filas_b.configure(state="readonly") # Bloquea filas de B
        else:
            self.etiqueta_b.configure(text='Matriz B')
            self.lbl_cols_b.grid() # Muestra control de columnas de B
            self.ent_columnas_b.grid()
            self.ent_filas_b.configure(state="normal") # Desbloquea filas de B

        # Muestra/oculta el dropdown de modo Gauss
        self.menu_modo_gauss.grid() if op=='Gauss/Gauss-Jordan' else self.menu_modo_gauss.grid_remove()

        # Muestra/oculta el panel completo de Matriz B
        if op in ('Gauss/Gauss-Jordan','Independencia','Inversa', 'Determinante'):
            self.marco_b.grid_remove()
            self.marco_dims_b.grid_remove()
        else:
            self.marco_b.grid()
            self.marco_dims_b.grid()

        # Muestra/oculta las entradas de escalares (alfa, beta)
        usa_escalares = op in ('Suma','Resta')
        if usa_escalares:
            self.lbl_coef_a.grid(); self.ent_coef_a.grid()
            self.lbl_coef_b.grid(); self.ent_coef_b.grid()
        else:
            self.lbl_coef_a.grid_remove(); self.ent_coef_a.grid_remove()
            self.lbl_coef_b.grid_remove(); self.ent_coef_b.grid_remove()

    def _leer_entradas_de_cuadricula(self, entradas: List[List[ctk.CTkEntry]]):
        """
        Lee los valores de una cuadrícula de widgets (ej: self.entradas_a)
        y los devuelve como una matriz 2D de floats.
        """
        if not entradas:
            return []
            
        # Comprueba si la matriz ha sido generada pero está vacía
        if not entradas[0] and len(entradas) > 0 :
             if hasattr(self,'marco_a') and self.marco_a.winfo_ismapped():
                 raise ValueError("Primero debe generar la Matriz A")
             elif hasattr(self,'marco_b') and self.marco_b.winfo_ismapped():
                  raise ValueError("Primero debe generar la Matriz B")
             else:
                   raise ValueError("Primero debe generar las matrices")

        filas = len(entradas)
        cols = len(entradas[0]) if filas > 0 else 0

        matriz = [[0.0]*cols for _ in range(filas)]
        celdas_no_vacias = 0
        for i in range(filas):
            for j in range(cols):
                if entradas[i][j] is not None:
                    texto = entradas[i][j].get().strip()
                    if texto:
                        celdas_no_vacias += 1
                        try:
                            # Usa el parser para aceptar fracciones
                            matriz[i][j] = _parse_valor(texto)
                        except ValueError as e:
                            raise ValueError(f'Valor inválido en ({i+1},{j+1}): {e}')

        # Lanza error si la matriz fue generada pero no se rellenó
        if celdas_no_vacias == 0 and filas * cols > 0:
            raise ValueError("La matriz no puede estar vacía, ingrese al menos un valor.")

        return matriz

    def _detalle_bloque(self, fa, ca):
        """Helper para obtener dimensiones de bloque (no usado actualmente)."""
        return min(BLOQUE_DETALLE, fa), min(BLOQUE_DETALLE, ca)

    def calcular_operacion(self):
        """
        Función principal llamada por el botón "Calcular". (Para Álgebra Lineal)
        Lee las matrices, llama a la función de lógica (del archivo Complement.py)
        y muestra los resultados.
        """
        op = self.opcion_var.get()
        # Importación de Complement.py aquí para asegurar que las funciones estén disponibles
        try:
            from Complement import (
                gauss_steps, gauss_jordan_steps, inverse_steps, pasos_determinante,
                resolver_por_cramer, independenciaVectores
            )
        except ImportError:
            self._set_resultado("ERROR: No se pudo cargar Complement.py. Verifique que el archivo esté en la carpeta correcta.")
            return

        try:
            # 1. Leer datos de la UI
            A = self._leer_entradas_de_cuadricula(self.entradas_a)
            B = []
            if self.marco_b.winfo_ismapped(): # Solo lee B si su panel es visible
                 B = self._leer_entradas_de_cuadricula(self.entradas_b)
                 
        except ValueError as e:
            self._set_resultado(f'Error de entrada: {e}', limpiar_pasos=True); return
        except Exception as e:
            self._set_resultado(f'Error inesperado al leer matrices: {e}', limpiar_pasos=True); return

        # --- 2. Ejecutar Lógica de Cálculo (importando desde Complement.py) ---

        if op == 'Regla de Cramer':
            try:
                # Validación de dimensiones específica para Cramer
                if not A: raise ValueError("La matriz A no puede estar vacía")
                if not B: raise ValueError("El vector B no puede estar vacío")
                if len(A) != len(B): raise ValueError(f"Las filas de A ({len(A)}) y B ({len(B)}) no coinciden")
                if not A[0]: raise ValueError("La matriz A no tiene columnas")
                if len(A) != len(A[0]): raise ValueError("La matriz A debe ser cuadrada (n x n)")
                if not B[0] or len(B[0]) != 1: raise ValueError("B debe ser un vector columna (n x 1)")

                # La función 'resolver_por_cramer' espera una matriz aumentada [A|B]
                matriz_aumentada = [A[i] + [B[i][0]] for i in range(len(A))]
            except Exception as e:
                 self._set_resultado(f'Error al preparar Cramer: {e}', limpiar_pasos=True); return

            res = resolver_por_cramer(matriz_aumentada) # Llama a la lógica
            
            # Muestra los pasos
            self.pasos_caja.delete('0.0', 'end')
            if res.get('pasos'):
                 self.pasos_caja.insert('0.0', '\n'.join(res['pasos']))

            # Muestra el resultado
            if res['estado'] == 'exito':
                 sol_texto = '\n'.join(f'x{i+1} = {_fmt(v)}' for i,v in enumerate(res['solucion']))
                 self._set_resultado(f"Solución única encontrada:\n{sol_texto}")
            elif res['estado'] == 'sin_solucion_unica':
                 self._set_resultado(res['mensaje'])
            else:
                 self._set_resultado(f"Error: {res['mensaje']}")
            return

        if op == 'Determinante':
            res = pasos_determinante(A) 
            if res['estado'] == 'exito':
                self.pasos_caja.delete('0.0', 'end')
                self.pasos_caja.insert('0.0', '\n'.join(res['pasos']))
                self._set_resultado(f"El determinante es: {_fmt(res['determinante'])}")
            else:
                self._set_resultado(f"Error: {res['mensaje']}", limpiar_pasos=True)
            return

        if op == 'Gauss/Gauss-Jordan':
            modo = self.modo_gauss_var.get()
            
            # Matriz aumentada [A|B] si B existe, o solo A si B no existe (Independencia conceptual)
            if self.marco_b.winfo_ismapped():
                 matriz_aumentada = [A[i] + B[i] for i in range(len(A))]
            else:
                 matriz_aumentada = A
            
            # Llama a la función de lógica correspondiente
            res = gauss_steps(matriz_aumentada) if modo=='Gauss' else gauss_jordan_steps(matriz_aumentada)
            
            self.pasos_caja.delete('0.0','end')
            steps, ops = res.get('steps',[]), res.get('ops',[])
            total = len(steps); shown = 0
            
            # Lógica para mostrar pasos (evita sobrecargar la UI)
            for i, paso in enumerate(steps):
                # Muestra los primeros 20, luego cada 'PASO_SALTOS', hasta 'MAX_SNAPSHOTS'
                if i < 20 or i % PASO_SALTOS == 0:
                    if i < len(ops) and ops[i]: self.pasos_caja.insert('end', f'Op: {ops[i]}\n')
                    self._append_matriz(paso, f'Paso {i}:'); shown += 1
                if shown >= MAX_SNAPSHOTS: break
            if total > shown: self.pasos_caja.insert('end', f'… ({total-shown} pasos omitidos)\n\n')
            
            # Formatea la solución según el tipo
            status = res.get('status'); sol = res.get('solution')
            if status=='unique' and sol is not None:
                txt = 'Solución única:\n' + '\n'.join(f'x{i+1} = {v:.6g}' for i,v in enumerate(sol))
            elif status=='inconsistent': txt = 'El sistema es inconsistente (sin solución)'
            elif status=='infinite':
                libres = res.get('free_vars', []); base = res.get('basic_solution', {})
                # Número de variables (asume la última columna es el vector b)
                m = len(A[0]) if not self.marco_b.winfo_ismapped() else len(A[0]) 
                lineas=[]
                for i in range(m):
                    if i in libres: lineas.append(f'x{i+1} = variable libre')
                    else: lineas.append(f'x{i+1} = {base.get(i,0.0):.6g}  (con libres = 0)')
                txt = 'Soluciones infinitas:\n' + '\n'.join(lineas)
            elif status=='empty': txt = 'Matriz vacía'
            else: txt = f"Estado: {status}"
            self._set_resultado(txt); return

        if op == 'Inversa':
            n = len(A)
            res = inverse_steps(A) 
            
            # Muestra los pasos (similar a Gauss)
            self.pasos_caja.delete('0.0','end')
            steps, ops = res.get('steps',[]), res.get('ops',[])
            total = len(steps); shown = 0
            for i, M in enumerate(steps):
                if i < 20 or i % PASO_SALTOS == 0:
                    if i < len(ops) and ops[i]: self.pasos_caja.insert('end', f'Op: {ops[i]}\n')
                    self._append_matriz(M, f'Paso {i}:'); shown += 1
                if shown >= MAX_SNAPSHOTS: break
            if total > shown: self.pasos_caja.insert('end', f'… ({total-shown} pasos omitidos)\n\n')
            
            # Muestra el resultado
            if res.get('status') == 'invertible':
                inv = res['inverse']
                self._set_resultado('A es invertible. A⁻¹ =\n' + '\n'.join('  '.join(_fmt(x) for x in fila) for fila in inv))
            elif res.get('status') == 'singular':
                 self._set_resultado('A es singular (no tiene inversa)')
            else:
                 self._set_resultado(f"Error: {res.get('mensaje','error desconocido en inversa')}")
            return

        if op == 'Independencia':
            # 'A' aquí es un conjunto de vectores por filas
            ver = independenciaVectores(A)
            
            self.pasos_caja.delete('0.0','end')
            # Muestra los pasos (RREF de la matriz)
            try:
                matriz_para_pasos = self._leer_entradas_de_cuadricula(self.entradas_a)
                if matriz_para_pasos:
                    # Se crea una matriz aumentada [A|0] para Gauss-Jordan
                    matriz_gj = [fila + [0.0] for fila in matriz_para_pasos]
                    if matriz_gj:
                        rref = gauss_jordan_steps(matriz_gj); steps, ops = rref.get('steps',[]), rref.get('ops',[])
                        total=len(steps); shown=0
                        for i,paso in enumerate(steps):
                             paso_real = [fila[:-1] for fila in paso] # Quita la columna de ceros
                             if i<20 or i%PASO_SALTOS==0:
                                 if i<len(ops) and ops[i]: self.pasos_caja.insert('end', f'Op: {ops[i]}\n')
                                 self._append_matriz(paso_real, f'Paso {i} (RREF):'); shown+=1
                             if shown>=MAX_SNAPSHOTS: break
                        if total>shown: self.pasos_caja.insert('end', f'… ({total-shown} pasos omitidos)\n\n')
                    else:
                        self.pasos_caja.insert('end', 'No se pudo generar matriz para pasos de RREF\n')
            except Exception as e:
                self.pasos_caja.insert('end', f'No se pudo mostrar el paso a paso: {e}\n')

            # Muestra el resultado
            if ver.get('num_vectors',0)==0: self._set_resultado('No hay vectores (matriz vacía)')
            else:
                r,k = ver.get('rank'), ver.get('num_vectors')
                self._set_resultado(f"Rango = {r} / {k} vectores\n" + ('Linealmente Independiente' if ver.get('independent') else 'Linealmente Dependiente'))
            return

        # --- Operaciones Básicas (Suma, Resta, Multiplicación) ---
        
        fa, ca = len(A), len(A[0]) if A else 0
        fb, cb = len(B), len(B[0]) if B else 0
        self.pasos_caja.delete('0.0','end')
        try:
            if op in ('Suma','Resta'):
                alpha = self._leer_escalar(self.ent_coef_a)
                beta = self._leer_escalar(self.ent_coef_b)
                sgn = 1.0 if op=='Suma' else -1.0 # Signo para resta
                
                # Cálculo: C = (alfa * A) + (signo * beta * B)
                Aesc = [[alpha*A[i][j] for j in range(ca)] for i in range(fa)]
                Besc = [[sgn*beta*B[i][j] for j in range(cb)] for i in range(fb)]
                C = [[Aesc[i][j]+Besc[i][j] for j in range(ca)] for i in range(fa)]
                R = C # Resultado final
                
                # Muestra pasos
                self._append_matriz(A,'Matriz A:')
                self._append_matriz(B,'Matriz B:')
                self._append_matriz(Aesc, f'α·A (α={_fmt(alpha)}):')
                self._append_matriz(Besc, f'{"+" if sgn>0 else "-"} β·B (β={_fmt(beta)}):')
                # Muestra el detalle de la suma celda por celda
                for i in range(fa):
                    for j in range(ca):
                        self.pasos_caja.insert('end', f'C[{i+1},{j+1}] = {_fmt(alpha)}·{_fmt(A[i][j])} {"+" if sgn>0 else "-"} {_fmt(beta)}·{_fmt(B[i][j])} = {_fmt(C[i][j])}\n')
                self._append_matriz(C, 'Resultado C = αA ' + ('+' if sgn>0 else '−') + ' βB:')

            elif op == 'Multiplicación':
                # Cálculo: C[i,j] = suma(A[i,k] * B[k,j] para todo k)
                C = [[sum(A[i][k]*B[k][j] for k in range(ca)) for j in range(cb)] for i in range(fa)]
                R = C # Resultado final
                
                # Muestra pasos
                self._append_matriz(A,'Matriz A:')
                self._append_matriz(B,'Matriz B:')
                # Muestra el detalle de la multiplicación celda por celda
                for i in range(fa):
                    for j in range(cb):
                        terms = [f'{_fmt(A[i][k])}·{_fmt(B[k][j])}' for k in range(ca)]
                        self.pasos_caja.insert('end', f'C[{i+1},{j+1}] = ' + ' + '.join(terms) + f' = {_fmt(C[i][j])}\n')
                self._append_matriz(C,'Resultado C = A·B:')
            else:
                raise ValueError('Operación desconocida')

            # Muestra la matriz resultado final
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0','\n'.join('  '.join(_fmt(v) for v in fila) for fila in R))

        except ValueError as e:
            self._set_resultado(f'Error: {e}', limpiar_pasos=True)
        except Exception as e:
            self._set_resultado(f'Error inesperado al calcular: {e}', limpiar_pasos=True)

    def limpiar_matrices(self):
        """Limpia todas las celdas de entrada y las cajas de texto de resultados/pasos."""
        # Limpia cuadrícula A
        for fila_entradas in self.entradas_a:
            for entrada in fila_entradas:
                if entrada: entrada.delete(0,'end')
        # Limpia cuadrícula B
        for fila_entradas in self.entradas_b:
            for entrada in fila_entradas:
                if entrada: entrada.delete(0,'end')
        
        # Limpia cajas de texto
        self.resultado_caja.delete('0.0','end')
        self.pasos_caja.delete('0.0','end')
        
        # Restaura el texto de ejemplo en la caja de ecuaciones
        self.caja_ecuaciones.delete('1.0', 'end')
        self.caja_ecuaciones.insert("0.0", "Ej: 2x + 3y - z = 5\n     x - y + 2z = 10\n     3x + 2y = 0")

    # --- (Fin de la sección de Álgebra Lineal) ---
    
    # --- (NUEVO: Inicio de la sección de Métodos Numéricos) ---
    
    def _cargar_ui_metodos_numericos(self):
        """Construye y carga la UI para la sección de Métodos Numéricos."""
        
        # Configura el layout del panel 'contenido' para esta sección
        self.contenido.grid_rowconfigure(0, weight=0) # Barra de método
        self.contenido.grid_rowconfigure(1, weight=0) # Entradas (función, intervalo, etc.)
        self.contenido.grid_rowconfigure(2, weight=0) # Botones de ejemplos
        self.contenido.grid_rowconfigure(3, weight=0) # Botones (Calcular, Limpiar)
        self.contenido.grid_rowconfigure(4, weight=1) # Área de resultados (Pasos, Resultado)
        self.contenido.grid_columnconfigure(0, weight=1)

        # --- Barra superior de controles (Método) ---
        barra_metodo = ctk.CTkFrame(self.contenido)
        barra_metodo.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        
        ctk.CTkLabel(barra_metodo, text="Método:", font=self.font_normal).grid(row=0, column=0, padx=(4,2))
        
        self.metodo_num_var = ctk.StringVar(value="Bisección")
        ctk.CTkOptionMenu(barra_metodo, values=["Bisección"], # Solo Bisección por ahora
                          variable=self.metodo_num_var, fg_color=COLOR_ACENTO, button_color=COLOR_ACENTO, button_hover_color=COLOR_HOVER,
                          dropdown_fg_color=COLOR_FONDO_SECUNDARIO, dropdown_hover_color=COLOR_HOVER
                          ).grid(row=0, column=1, padx=(8,8))

        # --- Marco para entradas de la función ---
        marco_entradas = ctk.CTkFrame(self.contenido, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_entradas.grid(row=1, column=0, sticky="ew", padx=12, pady=(4, 8))
        marco_entradas.grid_columnconfigure(1, weight=1) # Columna de la función se expande
        
        # Fila 0: Función f(x)
        ctk.CTkLabel(marco_entradas, text="Función f(x) =", font=self.font_normal).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.ent_funcion_fx = ctk.CTkEntry(marco_entradas, placeholder_text="Ej: cos(x) - x  (usar 'x' como variable)", border_color=COLOR_ACENTO)
        self.ent_funcion_fx.grid(row=0, column=1, columnspan=5, sticky="ew", padx=8, pady=6)
        
        # Fila 1: Intervalo y Tolerancia
        ctk.CTkLabel(marco_entradas, text="Intervalo [a, b]:", font=self.font_normal).grid(row=1, column=0, sticky="w", padx=8, pady=6)
        self.ent_intervalo_a = ctk.CTkEntry(marco_entradas, width=100, placeholder_text="a", border_color=COLOR_ACENTO)
        self.ent_intervalo_a.grid(row=1, column=1, sticky="w", padx=(8,2), pady=6)
        self.ent_intervalo_b = ctk.CTkEntry(marco_entradas, width=100, placeholder_text="b", border_color=COLOR_ACENTO)
        self.ent_intervalo_b.grid(row=1, column=2, sticky="w", padx=(2,8), pady=6)
        
        ctk.CTkLabel(marco_entradas, text="Tolerancia (E):", font=self.font_normal).grid(row=1, column=3, sticky="w", padx=(20, 2), pady=6)
        self.ent_tolerancia_e = ctk.CTkEntry(marco_entradas, width=100, placeholder_text="Ej: 0.0001", border_color=COLOR_ACENTO)
        self.ent_tolerancia_e.grid(row=1, column=4, sticky="w", padx=(2, 8), pady=6)
        
        # --- Marco para botones de ejemplos ---
        marco_ejemplos = ctk.CTkFrame(self.contenido)
        marco_ejemplos.grid(row=2, column=0, sticky="ew", padx=12, pady=4)
        ctk.CTkLabel(marco_ejemplos, text="Cargar ejemplos:", font=self.font_normal).grid(row=0, column=0, padx=(4,6))
        
        # Usamos partial para pasar argumentos al comando del botón
        from functools import partial
        ctk.CTkButton(marco_ejemplos, text="Ej 1: cos(x)-x", command=partial(self.cargar_ejemplo_biseccion, 1),
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, width=120).grid(row=0, column=1, padx=4)
        ctk.CTkButton(marco_ejemplos, text="Ej 2: log(x)-exp(-x)", command=partial(self.cargar_ejemplo_biseccion, 2),
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, width=120).grid(row=0, column=2, padx=4)
        ctk.CTkButton(marco_ejemplos, text="Ej 4: x**10 - 1", command=partial(self.cargar_ejemplo_biseccion, 4),
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, width=120).grid(row=0, column=3, padx=4)
        ctk.CTkButton(marco_ejemplos, text="Ej 5: Polinomio", command=partial(self.cargar_ejemplo_biseccion, 5),
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, width=120).grid(row=0, column=4, padx=4)
        ctk.CTkButton(marco_ejemplos, text="Falla: x**2 + 4", command=partial(self.cargar_ejemplo_biseccion, 3),
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, width=120).grid(row=0, column=5, padx=4)
        
        # --- Marco para botones de control (Calcular, Limpiar) ---
        controles_num = ctk.CTkFrame(self.contenido)
        controles_num.grid(row=3, column=0, sticky="ew", padx=12, pady=(6,12))
        
        ctk.CTkButton(controles_num, text="Calcular", command=self.calcular_operacion_numerica,
                      fg_color=COLOR_ACENTO, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        
        ctk.CTkButton(controles_num, text="Limpiar", command=self.limpiar_numerico,
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=1, padx=6)

        # --- Contenedor inferior para Pasos y Resultado ---
        inferior_num = ctk.CTkFrame(self.contenido)
        inferior_num.grid(row=4, column=0, sticky="nswe", padx=12, pady=(6,12))
        inferior_num.grid_rowconfigure(0, weight=1)
        inferior_num.grid_columnconfigure(0, weight=2) # Pasos más anchos
        inferior_num.grid_columnconfigure(1, weight=1)
        
        # --- Marco para Pasos ---
        marco_pasos_num = ctk.CTkFrame(inferior_num)
        marco_pasos_num.grid(row=0, column=0, sticky="nswe", padx=(0,6))
        marco_pasos_num.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(marco_pasos_num, text="Pasos:", font=self.font_bold_label).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        # NUEVO: Fuente monoespaciada y más grande
        self.pasos_caja_num = ctk.CTkTextbox(marco_pasos_num, height=220, font=self.font_mono, wrap="none") # wrap="none" para tabla
        self.pasos_caja_num.grid(row=1, column=0, sticky="nswe", padx=8, pady=(0,8))
        
        # --- Marco para Resultado ---
        marco_resultado_num = ctk.CTkFrame(inferior_num)
        marco_resultado_num.grid(row=0, column=1, sticky="nswe", padx=(6,0))
        marco_resultado_num.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(marco_resultado_num, text="Resultado:", font=self.font_bold_label).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        # NUEVO: Fuente monoespaciada y más grande
        self.resultado_caja_num = ctk.CTkTextbox(marco_resultado_num, height=220, font=self.font_mono)
        self.resultado_caja_num.grid(row=1, column=0, sticky="nswe", padx=8, pady=(0,8))

    def cargar_ejemplo_biseccion(self, ej_num: int):
        """Carga los datos de los ejemplos en los campos de entrada."""
        self.limpiar_numerico() # Limpia campos anteriores
        
        if ej_num == 1:
            self.ent_funcion_fx.insert(0, "cos(x) - x")
            self.ent_intervalo_a.insert(0, "0")
            self.ent_intervalo_b.insert(0, "1")
            self.ent_tolerancia_e.insert(0, "0.0001")
        elif ej_num == 2:
            self.ent_funcion_fx.insert(0, "log(x) - exp(-x)")
            self.ent_intervalo_a.insert(0, "0.5")
            self.ent_intervalo_b.insert(0, "2")
            self.ent_tolerancia_e.insert(0, "0.0001")
        elif ej_num == 3: # Caso de falla
            self.ent_funcion_fx.insert(0, "x**2 + 4")
            self.ent_intervalo_a.insert(0, "-2")
            self.ent_intervalo_b.insert(0, "2")
            self.ent_tolerancia_e.insert(0, "0.0001")
        elif ej_num == 4:
            self.ent_funcion_fx.insert(0, "x**10 - 1")
            self.ent_intervalo_a.insert(0, "0")
            self.ent_intervalo_b.insert(0, "1.3")
            self.ent_tolerancia_e.insert(0, "0.0001")
        elif ej_num == 5:
            self.ent_funcion_fx.insert(0, "x**4 - 5*x**3 + 0.5*x**2 - 11*x + 10")
            self.ent_intervalo_a.insert(0, "0.55")
            self.ent_intervalo_b.insert(0, "1.1")
            self.ent_tolerancia_e.insert(0, "0.0001")

    def limpiar_numerico(self):
        """Limpia los campos de entrada y salida de la UI de Métodos Numéricos."""
        if hasattr(self, 'ent_funcion_fx'):
            self.ent_funcion_fx.delete(0, 'end')
        if hasattr(self, 'ent_intervalo_a'):
            self.ent_intervalo_a.delete(0, 'end')
        if hasattr(self, 'ent_intervalo_b'):
            self.ent_intervalo_b.delete(0, 'end')
        if hasattr(self, 'ent_tolerancia_e'):
            self.ent_tolerancia_e.delete(0, 'end')
            
        if hasattr(self, 'pasos_caja_num'):
            self.pasos_caja_num.delete('0.0', 'end')
        if hasattr(self, 'resultado_caja_num'):
            self.resultado_caja_num.delete('0.0', 'end')

    def calcular_operacion_numerica(self):
        """
        Función principal llamada por el botón "Calcular" en la sección de Métodos Numéricos.
        """
        # Importa la lógica desde el nuevo archivo
        try:
            from MetodosNumericos import metodo_biseccion
        except ImportError:
            self.resultado_caja_num.delete('0.0', 'end')
            self.resultado_caja_num.insert('0.0', "ERROR: No se pudo cargar MetodosNumericos.py.")
            return

        metodo = self.metodo_num_var.get()
        
        if metodo == 'Bisección':
            try:
                # 1. Leer entradas
                funcion_str = self.ent_funcion_fx.get()
                a_str = self.ent_intervalo_a.get()
                b_str = self.ent_intervalo_b.get()
                tol_str = self.ent_tolerancia_e.get()
                
                if not funcion_str or not a_str or not b_str or not tol_str:
                    raise ValueError("Todos los campos (función, a, b, tolerancia) son obligatorios.")
                
                a = _parse_valor(a_str)
                b = _parse_valor(b_str)
                tolerancia = _parse_valor(tol_str)
                
                if tolerancia <= 0:
                    raise ValueError("La tolerancia debe ser un número positivo.")
                if a >= b:
                    raise ValueError("El intervalo es inválido (a debe ser menor que b).")

                # 2. Llamar a la lógica
                res = metodo_biseccion(funcion_str, a, b, tolerancia)
                
                # 3. Mostrar Pasos
                self.pasos_caja_num.delete('0.0', 'end')
                self.pasos_caja_num.insert('0.0', '\n'.join(res.get('pasos', ['No se generaron pasos.'])))
                
                # 4. Mostrar Resultado
                self.resultado_caja_num.delete('0.0', 'end')
                if res['estado'] == 'exito':
                    resultado_txt = (
                        f"Raíz encontrada (xr):\n{res['raiz']:.10f}\n\n"
                        f"Iteraciones: {res['iteraciones']}\n"
                        f"Error relativo final: {res.get('error', 'N/A'):.6e}"
                    )
                    self.resultado_caja_num.insert('0.0', resultado_txt)
                elif res['estado'] == 'max_iter':
                    resultado_txt = (
                        f"Se alcanzó el máximo de iteraciones.\n\n"
                        f"Última aproximación (xr):\n{res['raiz']:.10f}\n\n"
                        f"Último error: {res.get('error', 'N/A'):.6e}"
                    )
                    self.resultado_caja_num.insert('0.0', resultado_txt)
                else: # 'error'
                    self.resultado_caja_num.insert('0.0', f"Error:\n{res['mensaje']}")

            except ValueError as e:
                self.pasos_caja_num.delete('0.0', 'end')
                self.resultado_caja_num.delete('0.0', 'end')
                self.resultado_caja_num.insert('0.0', f"Error de entrada:\n{e}")
            except Exception as e:
                self.pasos_caja_num.delete('0.0', 'end')
                self.resultado_caja_num.delete('0.0', 'end')
                self.resultado_caja_num.insert('0.0', f"Error inesperado en el cálculo:\n{e}")

    # --- (FIN de la sección de Métodos Numéricos) ---
    
    def actualizar_fecha_hora(self):
        """Actualiza la etiqueta de la fecha y hora cada segundo."""
        self.etiqueta_fecha_hora.configure(text=datetime.now().strftime("%A, %d %B %Y | %H:%M:%S"))
        # Vuelve a llamar a esta función después de 1000ms (1 segundo)
        self.after(1000, self.actualizar_fecha_hora)

# --- Punto de Entrada de la Aplicación ---
if __name__ == "__main__":
    ctk.set_appearance_mode("dark") # Modo oscuro por defecto
    ctk.set_default_color_theme("blue") # Tema de color base
    
    app = AplicacionPrincipal() # Crea la instancia de la aplicación
    app.mainloop()