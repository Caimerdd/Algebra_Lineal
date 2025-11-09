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
from typing import List, Dict
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sympy as sp
import numpy as np  # Mantenemos numpy solo para la creación de arrays en matplotlib

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
COLOR_FONDO_SECUNDARIO = ("gray92", "#212121")
COLOR_BOTON_SECUNDARIO = ("gray75", "gray30")
COLOR_BOTON_SECUNDARIO_HOVER = ("gray80", "gray35")

# --- NUEVOS COLORES ---
COLOR_ALGEBRA = ("#2196F3", "#1976D2")  # Azul para Álgebra Lineal
COLOR_NUMERICOS = ("#00BCD4", "#0097A7")  # Cyan para Métodos Numéricos
COLOR_FONDO_PRINCIPAL = ("#f8f9fa", "#121212")
COLOR_TARJETA = ("white", "#1e1e1e")
COLOR_TEXTO_TARJETA = ("#333333", "#ffffff")

# --- Clase para Ventana de Ayuda SymPy ---

class VentanaAyudaSymPy(ctk.CTkToplevel):
    """Ventana modal para mostrar la ayuda de sintaxis SymPy."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ayuda SymPy - Sintaxis Matemática")
        self.geometry("600x500")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()
        
        # Configurar la ventana
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Frame principal con scroll
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Canvas y scrollbar
        canvas = ctk.CTkCanvas(main_frame, highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(main_frame, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Contenido de la ayuda
        self._crear_contenido_ayuda(scrollable_frame)
        
        # Configurar eventos
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        scrollable_frame.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        
    def _crear_contenido_ayuda(self, parent):
        """Crea el contenido de la ayuda SymPy."""
        
        # Título
        titulo = ctk.CTkLabel(parent, text="Sintaxis Matemática - SymPy", 
                             font=ctk.CTkFont(size=18, weight="bold"))
        titulo.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))
        
        categorias = [
            {
                "titulo": "Operaciones Básicas",
                "items": [
                    ("Suma/Resta", "x + y, x - y"),
                    ("Multiplicación", "x * y  o  x y  (con espacio)"),
                    ("División", "x / y"),
                    ("Exponentes", "x**2  o  x^2"),
                    ("Raíz cuadrada", "sqrt(x)"),
                    ("Raíz n-ésima", "root(x, n)")
                ]
            },
            {
                "titulo": "Funciones Trigonométricas",
                "items": [
                    ("Seno", "sin(x)"),
                    ("Coseno", "cos(x)"),
                    ("Tangente", "tan(x)"),
                    ("Arcoseno", "asin(x)"),
                    ("Arcocoseno", "acos(x)"),
                    ("Arcotangente", "atan(x)")
                ]
            },
            {
                "titulo": "Logaritmos y Exponenciales",
                "items": [
                    ("Logaritmo natural", "log(x)  o  ln(x)"),
                    ("Logaritmo base 10", "log10(x)"),
                    ("Logaritmo base b", "log(x, b)"),
                    ("Exponencial", "exp(x)  o  E**x")
                ]
            },
            {
                "titulo": "Constantes Matemáticas",
                "items": [
                    ("Pi", "pi"),
                    ("Número e", "E"),
                    ("Infinito", "oo"),
                    ("Número imaginario", "I")
                ]
            },
            {
                "titulo": "Funciones Especiales",
                "items": [
                    ("Valor absoluto", "abs(x)"),
                    ("Factorial", "factorial(n)"),
                    ("Función gamma", "gamma(x)"),
                    ("Función error", "erf(x)"),
                    ("Función de Bessel", "besselj(n, x)")
                ]
            },
            {
                "titulo": "Ejemplos Completos",
                "items": [
                    ("Polinomio", "x**3 - 2*x**2 + x - 5"),
                    ("Función trigonométrica", "sin(x)**2 + cos(x)**2"),
                    ("Ecuación exponencial", "exp(-x) - log(x)"),
                    ("Función racional", "(x**2 - 1)/(x - 1)")
                ]
            }
        ]
        
        row = 1
        for categoria in categorias:
            # Marco de categoría
            marco_categoria = ctk.CTkFrame(parent, fg_color=COLOR_FONDO_SECUNDARIO)
            marco_categoria.grid(row=row, column=0, sticky="ew", padx=20, pady=10)
            marco_categoria.grid_columnconfigure(0, weight=1)
            
            # Título de categoría
            lbl_titulo = ctk.CTkLabel(marco_categoria, text=categoria["titulo"],
                                     font=ctk.CTkFont(size=14, weight="bold"))
            lbl_titulo.grid(row=0, column=0, sticky="w", padx=15, pady=8)
            
            row += 1
            
            # Items de la categoría
            for i, (nombre, sintaxis) in enumerate(categoria["items"]):
                marco_item = ctk.CTkFrame(parent)
                marco_item.grid(row=row, column=0, sticky="ew", padx=30, pady=2)
                marco_item.grid_columnconfigure(1, weight=1)
                
                lbl_nombre = ctk.CTkLabel(marco_item, text=nombre, width=120,
                                         font=ctk.CTkFont(size=12))
                lbl_nombre.grid(row=0, column=0, sticky="w", padx=10, pady=5)
                
                lbl_sintaxis = ctk.CTkLabel(marco_item, text=sintaxis,
                                           font=ctk.CTkFont(family="monospace", size=12),
                                           text_color=COLOR_ALGEBRA)
                lbl_sintaxis.grid(row=0, column=1, sticky="w", padx=10, pady=5)
                
                row += 1
        
        # Nota final
        nota = ctk.CTkLabel(parent, 
                           text="💡 Tip: Usa paréntesis para agrupar operaciones complejas",
                           font=ctk.CTkFont(size=12, slant="italic"),
                           text_color="gray70")
        nota.grid(row=row, column=0, sticky="w", padx=20, pady=20)

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
            # Permitir 'e' para notación científica
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
        
        self.title("MathPro - Herramientas Matemáticas Avanzadas")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.font_normal = ctk.CTkFont(size=13)
        self.font_bold_label = ctk.CTkFont(size=14, weight="bold")
        self.font_mono = ctk.CTkFont(family="monospace", size=14)
        self.font_titulo = ctk.CTkFont(size=16, weight="bold")
        self.font_titulo_grande = ctk.CTkFont(size=24, weight="bold")
        
        # Variables para tooltips
        self.tooltip_label = None
        self.tooltip_window = None
        self.tooltip_timer = None
        self.modo_presentacion = False
        
        # Estado de navegación
        self.pantalla_actual = "inicio"  # "inicio", "algebra", "numericos"
        self.seccion_actual = None
        
        self._crear_panel_nav()
        self._crear_panel_principal()
        
        self.mostrar_pantalla_inicio()
        self.actualizar_fecha_hora()

    def toggle_theme(self):
        """Cambia entre modo claro y oscuro basado en el estado del switch."""
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def _crear_tooltip(self, widget, text):
        """Crea un tooltip mejorado para un widget."""
        def show_tooltip():
            # Destruir cualquier tooltip existente primero
            if hasattr(self, 'tooltip_window') and self.tooltip_window:
                try:
                    self.tooltip_window.destroy()
                except:
                    pass
            
            x = widget.winfo_rootx() + 25
            y = widget.winfo_rooty() + 25
            
            self.tooltip_window = ctk.CTkToplevel(self)
            self.tooltip_window.wm_overrideredirect(True)
            self.tooltip_window.wm_geometry(f"+{x}+{y}")
            self.tooltip_window.attributes('-topmost', True)
            self.tooltip_window.attributes('-alpha', 0.95)
            
            # Obtener colores según el tema actual
            if ctk.get_appearance_mode() == "Dark":
                bg_color = "#2b2b2b"
                text_color = "white"
            else:
                bg_color = "#f0f0f0"
                text_color = "black"
            
            label = ctk.CTkLabel(self.tooltip_window, text=text, 
                               font=ctk.CTkFont(size=11),
                               corner_radius=6,
                               fg_color=bg_color,
                               text_color=text_color,
                               wraplength=300)
            label.pack(padx=8, pady=4)
            
        def schedule_tooltip(event):
            # Programar tooltip para mostrar después de 500ms
            if hasattr(self, 'tooltip_timer') and self.tooltip_timer:
                self.after_cancel(self.tooltip_timer)
            self.tooltip_timer = self.after(500, show_tooltip)
            
        def hide_tooltip(event):
            # Cancelar tooltip programado y destruir si existe
            if hasattr(self, 'tooltip_timer') and self.tooltip_timer:
                self.after_cancel(self.tooltip_timer)
                self.tooltip_timer = None
            if hasattr(self, 'tooltip_window') and self.tooltip_window:
                try:
                    self.tooltip_window.destroy()
                    self.tooltip_window = None
                except:
                    pass
                
        widget.bind("<Enter>", schedule_tooltip)
        widget.bind("<Leave>", hide_tooltip)
        widget.bind("<ButtonPress>", hide_tooltip)  # Destruir al hacer click

    def _crear_panel_nav(self):
        """Crea el panel de navegación lateral izquierdo con categorías organizadas."""
        self.marco_nav = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.marco_nav.grid(row=0, column=0, sticky="nswe")
        self.marco_nav.grid_rowconfigure(10, weight=1)
        
        # Título principal
        ctk.CTkLabel(self.marco_nav, text="MathPro", 
                    font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=12, pady=(15, 10), sticky="w")
        
        # Botón Regresar al Inicio (inicialmente oculto)
        self.btn_inicio = ctk.CTkButton(self.marco_nav, text="🏠 Regresar al Inicio", anchor="w",
                                      fg_color=COLOR_BOTON_SECUNDARIO, 
                                      hover_color=COLOR_BOTON_SECUNDARIO_HOVER,
                                      command=self.mostrar_pantalla_inicio)
        self.btn_inicio.grid(row=1, column=0, sticky="ew", padx=12, pady=5)
        self.btn_inicio.grid_remove()  # Oculto inicialmente
        
        # Separador
        ctk.CTkFrame(self.marco_nav, height=2).grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        # Categoría: Sistemas de Ecuaciones
        ctk.CTkLabel(self.marco_nav, text="SISTEMAS DE ECUACIONES", 
                    font=ctk.CTkFont(size=12, weight="bold"), 
                    text_color=COLOR_ALGEBRA).grid(row=3, column=0, sticky="w", padx=15, pady=(10, 5))
        
        btn_gauss = ctk.CTkButton(self.marco_nav, text="   Métodos de Solución", anchor="w",
                      fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER,
                      command=lambda: self.mostrar_seccion('Sistemas de Ecuaciones'))
        btn_gauss.grid(row=4, column=0, sticky="ew", padx=12, pady=3)
        self._crear_tooltip(btn_gauss, "Resuelve sistemas de ecuaciones lineales usando:\n• Eliminación Gaussiana\n• Gauss-Jordan\n• Regla de Cramer\n• Matriz Inversa")
        
        # Categoría: Operaciones Matriciales
        ctk.CTkLabel(self.marco_nav, text="OPERACIONES MATRICIALES", 
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=COLOR_ALGEBRA).grid(row=5, column=0, sticky="w", padx=15, pady=(15, 5))
        
        btn_operaciones = ctk.CTkButton(self.marco_nav, text="   Operaciones Básicas", anchor="w",
                      fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER,
                      command=lambda: self.mostrar_seccion('Operaciones Matriciales'))
        btn_operaciones.grid(row=6, column=0, sticky="ew", padx=12, pady=3)
        self._crear_tooltip(btn_operaciones, "Realiza operaciones básicas con matrices:\n• Suma y Resta\n• Multiplicación\n• Con escalares")
        
        # Categoría: Propiedades de Matrices
        ctk.CTkLabel(self.marco_nav, text="PROPIEDADES DE MATRICES", 
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=COLOR_ALGEBRA).grid(row=7, column=0, sticky="w", padx=15, pady=(15, 5))
        
        btn_propiedades = ctk.CTkButton(self.marco_nav, text="   Análisis Matricial", anchor="w",
                      fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER,
                      command=lambda: self.mostrar_seccion('Propiedades de Matrices'))
        btn_propiedades.grid(row=8, column=0, sticky="ew", padx=12, pady=3)
        self._crear_tooltip(btn_propiedades, "Analiza propiedades de matrices:\n• Determinante\n• Independencia Lineal\n• Rango")
        
        # Categoría: Métodos Numéricos
        ctk.CTkLabel(self.marco_nav, text="MÉTODOS NUMÉRICOS", 
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=COLOR_NUMERICOS).grid(row=9, column=0, sticky="w", padx=15, pady=(15, 5))
        
        btn_numericos = ctk.CTkButton(self.marco_nav, text="   Ecuaciones No Lineales", anchor="w",
                      fg_color=COLOR_NUMERICOS, hover_color=COLOR_HOVER,
                      command=lambda: self.mostrar_seccion('Métodos Numéricos'))
        btn_numericos.grid(row=10, column=0, sticky="ew", padx=12, pady=3)
        self._crear_tooltip(btn_numericos, "Resuelve ecuaciones no lineales:\n• Método de Bisección\n• Encuentra raíces de funciones")
        
        # Espacio flexible
        ctk.CTkLabel(self.marco_nav, text="").grid(row=11, column=0, sticky="nswe") 

        # Configuración de tema y ayuda
        marco_config = ctk.CTkFrame(self.marco_nav, fg_color="transparent")
        marco_config.grid(row=12, column=0, sticky="ew", padx=12, pady=15)
        
        # Botón de ayuda SymPy
        self.btn_ayuda = ctk.CTkButton(marco_config, text="📚 Ayuda SymPy",
                                     command=self.mostrar_ayuda_sympy,
                                     fg_color=COLOR_BOTON_SECUNDARIO,
                                     hover_color=COLOR_BOTON_SECUNDARIO_HOVER)
        self.btn_ayuda.pack(side="left", padx=(0, 10))
        
        # Switch de tema
        self.theme_switch = ctk.CTkSwitch(marco_config, text="Modo Oscuro", command=self.toggle_theme,
                                          progress_color=COLOR_ACENTO)
        self.theme_switch.pack(side="right")
        
        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()

    def _crear_panel_principal(self):
        """Crea el panel principal derecho que contendrá la cabecera y el contenido."""
        self.marco_principal = ctk.CTkFrame(self, corner_radius=0)
        self.marco_principal.grid(row=0, column=1, sticky="nswe", padx=12, pady=12)
        self.marco_principal.grid_rowconfigure(0, weight=0)
        self.marco_principal.grid_rowconfigure(1, weight=1)
        self.marco_principal.grid_columnconfigure(0, weight=1)

        self.cabecera = ctk.CTkFrame(self.marco_principal, height=70, corner_radius=8)
        self.cabecera.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.cabecera.grid_columnconfigure(0, weight=1)
        
        self.etiqueta_cabecera = ctk.CTkLabel(self.cabecera, text="", 
                                            font=ctk.CTkFont(size=22, weight="bold"))
        self.etiqueta_cabecera.grid(row=0, column=0, sticky="w", padx=20, pady=15)
        
        self.etiqueta_descripcion = ctk.CTkLabel(self.cabecera, text="", 
                                               font=ctk.CTkFont(size=12),
                                               text_color="gray70")
        self.etiqueta_descripcion.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 15))
        
        self.etiqueta_fecha_hora = ctk.CTkLabel(self.cabecera, text="", 
                                              font=ctk.CTkFont(size=11))
        self.etiqueta_fecha_hora.grid(row=0, column=1, sticky="e", padx=20, pady=15)

        # --- CONTENIDO CON SCROLL GENERAL ---
        self.contenido_frame = ctk.CTkFrame(self.marco_principal, corner_radius=8)
        self.contenido_frame.grid(row=1, column=0, sticky="nswe")
        self.contenido_frame.grid_rowconfigure(0, weight=1)
        self.contenido_frame.grid_columnconfigure(0, weight=1)
        
        # Crear canvas con scroll para TODO el contenido
        self.canvas_contenido = ctk.CTkCanvas(self.contenido_frame, highlightthickness=0)
        self.scrollbar_contenido = ctk.CTkScrollbar(self.contenido_frame, orientation="vertical", command=self.canvas_contenido.yview)
        self.scrollable_contenido_frame = ctk.CTkFrame(self.canvas_contenido)
        
        self.scrollable_contenido_frame.bind(
            "<Configure>",
            lambda e: self.canvas_contenido.configure(scrollregion=self.canvas_contenido.bbox("all"))
        )
        
        self.canvas_contenido.create_window((0, 0), window=self.scrollable_contenido_frame, anchor="nw")
        self.canvas_contenido.configure(yscrollcommand=self.scrollbar_contenido.set)
        
        self.canvas_contenido.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_contenido.grid(row=0, column=1, sticky="ns")
        
        # Configurar eventos de scroll con mouse
        self.canvas_contenido.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_contenido_frame.bind("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        """Maneja el scroll con la rueda del mouse."""
        self.canvas_contenido.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def mostrar_pantalla_inicio(self):
        """Muestra la pantalla de inicio con las tarjetas principales."""
        self.pantalla_actual = "inicio"
        self.seccion_actual = None
        
        # Ocultar botón de regreso en navegación
        self.btn_inicio.grid_remove()
        
        # Actualizar cabecera
        self.etiqueta_cabecera.configure(text="MathPro")
        self.etiqueta_descripcion.configure(text="Herramientas Matemáticas Avanzadas")
        
        # Limpiar contenido anterior
        for w in self.scrollable_contenido_frame.winfo_children(): 
            w.destroy()
        
        # Configurar grid para pantalla de inicio
        self.scrollable_contenido_frame.grid_rowconfigure(0, weight=1)
        self.scrollable_contenido_frame.grid_rowconfigure(1, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(2, weight=1)
        self.scrollable_contenido_frame.grid_columnconfigure(0, weight=1)
        
        # Espacio superior
        ctk.CTkLabel(self.scrollable_contenido_frame, text="").grid(row=0, column=0)
        
        # Marco principal de bienvenida
        marco_bienvenida = ctk.CTkFrame(self.scrollable_contenido_frame, corner_radius=12)
        marco_bienvenida.grid(row=1, column=0, sticky="nsew", padx=50, pady=20)
        marco_bienvenida.grid_columnconfigure(0, weight=1)
        marco_bienvenida.grid_rowconfigure(0, weight=1)
        marco_bienvenida.grid_rowconfigure(1, weight=0)
        marco_bienvenida.grid_rowconfigure(2, weight=0)
        marco_bienvenida.grid_rowconfigure(3, weight=1)
        
        # Título principal
        ctk.CTkLabel(marco_bienvenida, 
                    text="MathPro",
                    font=ctk.CTkFont(size=32, weight="bold")).grid(row=0, column=0, pady=(40, 10))
        
        ctk.CTkLabel(marco_bienvenida, 
                    text="Herramientas Matemáticas Avanzadas",
                    font=ctk.CTkFont(size=16),
                    text_color="gray70").grid(row=1, column=0, pady=(0, 40))
        
        # Marco para tarjetas
        marco_tarjetas = ctk.CTkFrame(marco_bienvenida, fg_color="transparent")
        marco_tarjetas.grid(row=2, column=0, sticky="nsew", padx=50, pady=20)
        marco_tarjetas.grid_columnconfigure(0, weight=1)
        marco_tarjetas.grid_columnconfigure(1, weight=1)
        marco_tarjetas.grid_rowconfigure(0, weight=1)
        
        # Tarjeta Álgebra Lineal
        self.tarjeta_algebra = ctk.CTkFrame(marco_tarjetas, corner_radius=12, 
                                          fg_color=COLOR_TARJETA, 
                                          border_width=2,
                                          border_color=COLOR_ALGEBRA[1] if ctk.get_appearance_mode() == "Dark" else COLOR_ALGEBRA[0])
        self.tarjeta_algebra.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        self.tarjeta_algebra.grid_columnconfigure(0, weight=1)
        self.tarjeta_algebra.grid_rowconfigure(0, weight=0)
        self.tarjeta_algebra.grid_rowconfigure(1, weight=0)
        self.tarjeta_algebra.grid_rowconfigure(2, weight=0)
        self.tarjeta_algebra.grid_rowconfigure(3, weight=1)
        
        # Icono y título Álgebra
        ctk.CTkLabel(self.tarjeta_algebra, text="📐", 
                    font=ctk.CTkFont(size=40)).grid(row=0, column=0, pady=(20, 10))
        
        ctk.CTkLabel(self.tarjeta_algebra, text="Álgebra Lineal", 
                    font=ctk.CTkFont(size=20, weight="bold"),
                    text_color=COLOR_TEXTO_TARJETA).grid(row=1, column=0, pady=(0, 10))
        
        # Descripción Álgebra
        desc_algebra = "Sistemas de ecuaciones\nOperaciones matriciales\nDeterminantes\nValores y vectores propios"
        ctk.CTkLabel(self.tarjeta_algebra, text=desc_algebra,
                    font=ctk.CTkFont(size=12),
                    text_color=COLOR_TEXTO_TARJETA,
                    justify="center").grid(row=2, column=0, pady=(0, 20))
        
        # Botón Álgebra
        btn_algebra = ctk.CTkButton(self.tarjeta_algebra, text="Explorar Álgebra Lineal",
                                  fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER,
                                  command=self.mostrar_seccion_algebra)
        btn_algebra.grid(row=3, column=0, sticky="s", padx=20, pady=20)
        
        # Tarjeta Métodos Numéricos
        self.tarjeta_numericos = ctk.CTkFrame(marco_tarjetas, corner_radius=12,
                                            fg_color=COLOR_TARJETA,
                                            border_width=2,
                                            border_color=COLOR_NUMERICOS[1] if ctk.get_appearance_mode() == "Dark" else COLOR_NUMERICOS[0])
        self.tarjeta_numericos.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        self.tarjeta_numericos.grid_columnconfigure(0, weight=1)
        self.tarjeta_numericos.grid_rowconfigure(0, weight=0)
        self.tarjeta_numericos.grid_rowconfigure(1, weight=0)
        self.tarjeta_numericos.grid_rowconfigure(2, weight=0)
        self.tarjeta_numericos.grid_rowconfigure(3, weight=1)
        
        # Icono y título Numéricos
        ctk.CTkLabel(self.tarjeta_numericos, text="🔢", 
                    font=ctk.CTkFont(size=40)).grid(row=0, column=0, pady=(20, 10))
        
        ctk.CTkLabel(self.tarjeta_numericos, text="Métodos Numéricos", 
                    font=ctk.CTkFont(size=20, weight="bold"),
                    text_color=COLOR_TEXTO_TARJETA).grid(row=1, column=0, pady=(0, 10))
        
        # Descripción Numéricos
        desc_numericos = "Ecuaciones no lineales\nInterpolación\nDiferenciación numérica\nEcuaciones diferenciales"
        ctk.CTkLabel(self.tarjeta_numericos, text=desc_numericos,
                    font=ctk.CTkFont(size=12),
                    text_color=COLOR_TEXTO_TARJETA,
                    justify="center").grid(row=2, column=0, pady=(0, 20))
        
        # Botón Numéricos
        btn_numericos = ctk.CTkButton(self.tarjeta_numericos, text="Explorar Métodos Numéricos",
                                    fg_color=COLOR_NUMERICOS, hover_color=COLOR_HOVER,
                                    command=self.mostrar_seccion_numericos)
        btn_numericos.grid(row=3, column=0, sticky="s", padx=20, pady=20)
        
        # Espacio inferior
        ctk.CTkLabel(self.scrollable_contenido_frame, text="").grid(row=2, column=0)
        
        # Configurar efectos hover
        self._configurar_hover_tarjetas()

    def _configurar_hover_tarjetas(self):
        """Configura efectos hover para las tarjetas."""
        def on_enter(event, tarjeta, color):
            tarjeta.configure(border_width=3)
            
        def on_leave(event, tarjeta, color):
            tarjeta.configure(border_width=2)
        
        # Álgebra
        self.tarjeta_algebra.bind("<Enter>", lambda e: on_enter(e, self.tarjeta_algebra, COLOR_ALGEBRA))
        self.tarjeta_algebra.bind("<Leave>", lambda e: on_leave(e, self.tarjeta_algebra, COLOR_ALGEBRA))
        
        # Numéricos
        self.tarjeta_numericos.bind("<Enter>", lambda e: on_enter(e, self.tarjeta_numericos, COLOR_NUMERICOS))
        self.tarjeta_numericos.bind("<Leave>", lambda e: on_leave(e, self.tarjeta_numericos, COLOR_NUMERICOS))

    def mostrar_seccion_algebra(self):
        """Muestra la sección de Álgebra Lineal."""
        self.pantalla_actual = "algebra"
        self.mostrar_seccion('Sistemas de Ecuaciones')
        self.btn_inicio.grid()

    def mostrar_seccion_numericos(self):
        """Muestra la sección de Métodos Numéricos."""
        self.pantalla_actual = "numericos"
        self.mostrar_seccion('Métodos Numéricos')
        self.btn_inicio.grid()

    def mostrar_seccion(self, nombre: str):
        """
        Carga la UI correspondiente a la sección 'nombre' en el panel 'contenido'.
        """
        self.seccion_actual = nombre
        self.etiqueta_cabecera.configure(text=nombre)
        
        # Actualizar descripción según la sección
        descripciones = {
            'Sistemas de Ecuaciones': 'Resuelve sistemas de ecuaciones lineales usando diferentes métodos numéricos',
            'Operaciones Matriciales': 'Realiza operaciones básicas con matrices y vectores',
            'Propiedades de Matrices': 'Analiza propiedades y características de matrices',
            'Métodos Numéricos': 'Encuentra raíces de ecuaciones no lineales'
        }
        self.etiqueta_descripcion.configure(text=descripciones.get(nombre, ''))
        
        # Limpiar contenido anterior
        for w in self.scrollable_contenido_frame.winfo_children(): 
            w.destroy()
        
        if nombre == 'Sistemas de Ecuaciones':
            self._cargar_ui_sistemas_ecuaciones()
        elif nombre == 'Operaciones Matriciales':
            self._cargar_ui_operaciones_matriciales()
        elif nombre == 'Propiedades de Matrices':
            self._cargar_ui_propiedades_matrices()
        elif nombre == 'Métodos Numéricos':
            self._cargar_ui_metodos_numericos()

    def mostrar_ayuda_sympy(self):
        """Muestra la ventana de ayuda SymPy."""
        VentanaAyudaSymPy(self)

    def toggle_modo_presentacion(self):
        """Alterna entre modo normal y modo presentación."""
        self.modo_presentacion = not self.modo_presentacion
        
        if self.modo_presentacion:
            # Ocultar toda la interfaz de entrada
            if hasattr(self, 'marco_entrada'):
                self.marco_entrada.grid_remove()
            if hasattr(self, 'marco_matrices_container'):
                self.marco_matrices_container.grid_remove()
            if hasattr(self, 'marco_controles'):
                self.marco_controles.grid_remove()
            
            # Expandir el marco de resultados
            if hasattr(self, 'marco_resultados'):
                self.marco_resultados.grid(row=0, column=0, sticky="nswe", padx=12, pady=12)
                self.marco_resultados.grid_rowconfigure(0, weight=1)
                self.marco_resultados.grid_columnconfigure(0, weight=1)
                self.marco_resultados.grid_columnconfigure(1, weight=1)
            
            self.btn_presentacion.configure(text="← Volver a Entrada", 
                                          fg_color=COLOR_ACENTO, hover_color=COLOR_HOVER)
        else:
            # Restaurar interfaz normal según la sección
            if self.seccion_actual == 'Sistemas de Ecuaciones':
                self._restaurar_ui_sistemas_ecuaciones()
            elif self.seccion_actual == 'Operaciones Matriciales':
                self._restaurar_ui_operaciones_matriciales()
            elif self.seccion_actual == 'Propiedades de Matrices':
                self._restaurar_ui_propiedades_matrices()
            elif self.seccion_actual == 'Métodos Numéricos':
                self._restaurar_ui_metodos_numericos()
            
            self.btn_presentacion.configure(text="📊 Ver Paso a Paso", 
                                          fg_color=COLOR_BOTON_SECUNDARIO, 
                                          hover_color=COLOR_BOTON_SECUNDARIO_HOVER)

    # --- SECCIÓN: SISTEMAS DE ECUACIONES ---
    def _cargar_ui_sistemas_ecuaciones(self):
        """Interfaz para resolver sistemas de ecuaciones."""
        self.scrollable_contenido_frame.grid_rowconfigure(0, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(1, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(2, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(3, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(4, weight=1)
        self.scrollable_contenido_frame.grid_columnconfigure(0, weight=1)

        # --- Selector de Método ---
        marco_metodo = ctk.CTkFrame(self.scrollable_contenido_frame, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_metodo.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        self.marco_entrada = marco_metodo
        
        ctk.CTkLabel(marco_metodo, text="Método de Solución:", font=self.font_titulo).grid(row=0, column=0, padx=(12, 8), pady=12)
        
        self.metodo_sistema_var = ctk.StringVar(value="Gauss-Jordan")
        metodos = [
            ("Gauss-Jordan", "Reducción completa a forma escalonada reducida"),
            ("Eliminación Gaussiana", "Reducción a forma escalonada"),
            ("Regla de Cramer", "Usando determinantes (solo para sistemas n×n)"),
            ("Matriz Inversa", "Solución mediante A⁻¹·b")
        ]
        
        for i, (metodo, desc) in enumerate(metodos):
            rb = ctk.CTkRadioButton(marco_metodo, text=metodo, variable=self.metodo_sistema_var, 
                                   value=metodo, font=self.font_normal)
            rb.grid(row=0, column=i+1, padx=8, pady=12)
            self._crear_tooltip(rb, desc)

        # --- Entrada de Ecuaciones ---
        marco_ecuaciones = ctk.CTkFrame(self.scrollable_contenido_frame)
        marco_ecuaciones.grid(row=1, column=0, sticky="ew", padx=12, pady=(4, 8))
        marco_ecuaciones.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(marco_ecuaciones, text="Ingrese el sistema de ecuaciones:", 
                    font=self.font_bold_label).grid(row=0, column=0, sticky="w", padx=8, pady=(8, 4))
        
        self.caja_ecuaciones = ctk.CTkTextbox(marco_ecuaciones, height=120, font=self.font_normal)
        self.caja_ecuaciones.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        self.caja_ecuaciones.insert("0.0", "2x + 3y - z = 5\nx - y + 2z = 10\n3x + 2y = 0")
        
        ctk.CTkButton(marco_ecuaciones, text="Generar Matriz Aumentada", 
                     command=self.parsear_y_poblar_ecuaciones,
                     fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=1, column=1, sticky="ns", padx=(0, 8), pady=(0, 8))

        # --- Marco contenedor para matrices ---
        self.marco_matrices_container = ctk.CTkFrame(self.scrollable_contenido_frame)
        self.marco_matrices_container.grid(row=2, column=0, sticky="nsew", padx=12, pady=8)
        self.marco_matrices_container.grid_rowconfigure(0, weight=1)
        self.marco_matrices_container.grid_columnconfigure(0, weight=1)

        # --- Matrices ---
        marco_matrices = ctk.CTkFrame(self.marco_matrices_container)
        marco_matrices.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        marco_matrices.grid_columnconfigure(0, weight=1)
        marco_matrices.grid_columnconfigure(1, weight=1)

        # Matriz A con botón de expandir/contraer
        self.marco_a = ctk.CTkFrame(marco_matrices, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_a.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=4)
        self.marco_a.grid_rowconfigure(2, weight=1)
        
        # Header con botón de expandir
        header_a = ctk.CTkFrame(self.marco_a, fg_color="transparent")
        header_a.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        header_a.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(header_a, text="Matriz de Coeficientes (A)", 
                    font=self.font_bold_label).grid(row=0, column=0, sticky="w")
        
        self.btn_expandir_a = ctk.CTkButton(header_a, text="−", width=30, height=30,
                                          command=lambda: self.toggle_matriz_visibility('a'),
                                          fg_color=COLOR_BOTON_SECUNDARIO)
        self.btn_expandir_a.grid(row=0, column=1, sticky="e")
        
        marco_dims_a = ctk.CTkFrame(self.marco_a, fg_color="transparent")
        marco_dims_a.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        ctk.CTkLabel(marco_dims_a, text="Filas:", font=self.font_normal).grid(row=0, column=0, padx=(0, 4))
        self.var_filas_a = ctk.StringVar(value="3")
        self.ent_filas_a = ctk.CTkEntry(marco_dims_a, width=60, textvariable=self.var_filas_a)
        self.ent_filas_a.grid(row=0, column=1, padx=(0, 12))
        ctk.CTkLabel(marco_dims_a, text="Columnas:", font=self.font_normal).grid(row=0, column=2, padx=(0, 4))
        self.ent_columnas_a = ctk.CTkEntry(marco_dims_a, width=60)
        self.ent_columnas_a.insert(0, "3")
        self.ent_columnas_a.grid(row=0, column=3)

        # Marco para la cuadrícula de A
        self.marco_grilla_a = ctk.CTkFrame(self.marco_a)
        self.marco_grilla_a.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))

        # Matriz B con botón de expandir/contraer
        self.marco_b = ctk.CTkFrame(marco_matrices, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_b.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=4)
        self.marco_b.grid_rowconfigure(2, weight=1)
        
        # Header con botón de expandir
        header_b = ctk.CTkFrame(self.marco_b, fg_color="transparent")
        header_b.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        header_b.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(header_b, text="Vector de Términos Independientes (B)", 
                    font=self.font_bold_label).grid(row=0, column=0, sticky="w")
        
        self.btn_expandir_b = ctk.CTkButton(header_b, text="−", width=30, height=30,
                                          command=lambda: self.toggle_matriz_visibility('b'),
                                          fg_color=COLOR_BOTON_SECUNDARIO)
        self.btn_expandir_b.grid(row=0, column=1, sticky="e")
        
        marco_dims_b = ctk.CTkFrame(self.marco_b, fg_color="transparent")
        marco_dims_b.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        ctk.CTkLabel(marco_dims_b, text="Filas:", font=self.font_normal).grid(row=0, column=0, padx=(0, 4))
        self.ent_filas_b = ctk.CTkEntry(marco_dims_b, width=60)
        self.ent_filas_b.insert(0, "3")
        self.ent_filas_b.grid(row=0, column=1)

        # Marco para la cuadrícula de B
        self.marco_grilla_b = ctk.CTkFrame(self.marco_b)
        self.marco_grilla_b.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))

        # Listas para entradas de matrices
        self.entradas_a = []
        self.entradas_b = []
        self.grilla_a = []
        self.grilla_b = []
        self.matriz_a_visible = True
        self.matriz_b_visible = True

        # --- Controles ---
        self.marco_controles = ctk.CTkFrame(self.scrollable_contenido_frame)
        self.marco_controles.grid(row=3, column=0, sticky="ew", padx=12, pady=8)
        
        ctk.CTkButton(self.marco_controles, text="Generar Cuadrículas", 
                     command=self.generar_cuadriculas_matriz,
                     fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        
        ctk.CTkButton(self.marco_controles, text="Resolver Sistema", 
                     command=self.calcular_sistema_ecuaciones,
                     fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=1, padx=6)
        
        ctk.CTkButton(self.marco_controles, text="Limpiar", 
                     command=self.limpiar_matrices,
                     fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=2, padx=6)

        # Botón para modo presentación
        self.btn_presentacion = ctk.CTkButton(self.marco_controles, text="📊 Ver Paso a Paso",
                     command=self.toggle_modo_presentacion,
                     fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER)
        self.btn_presentacion.grid(row=0, column=3, padx=6)

        # --- Resultados ---
        self.marco_resultados = ctk.CTkFrame(self.scrollable_contenido_frame)
        self.marco_resultados.grid(row=4, column=0, sticky="nswe", padx=12, pady=(0, 12))
        self.marco_resultados.grid_rowconfigure(0, weight=1)
        self.marco_resultados.grid_columnconfigure(0, weight=1)
        self.marco_resultados.grid_columnconfigure(1, weight=1)

        # Pasos con scrollbar
        marco_pasos = ctk.CTkFrame(self.marco_resultados)
        marco_pasos.grid(row=0, column=0, sticky="nswe", padx=(0, 6), pady=8)
        marco_pasos.grid_columnconfigure(0, weight=1)
        marco_pasos.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_pasos, text="Bitácora Paso a Paso", font=self.font_titulo).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        
        # Frame para textbox y scrollbar
        frame_pasos = ctk.CTkFrame(marco_pasos)
        frame_pasos.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        frame_pasos.grid_columnconfigure(0, weight=1)
        frame_pasos.grid_rowconfigure(0, weight=1)
        
        self.pasos_caja = ctk.CTkTextbox(frame_pasos, font=self.font_mono)
        scrollbar_pasos = ctk.CTkScrollbar(frame_pasos, command=self.pasos_caja.yview)
        self.pasos_caja.configure(yscrollcommand=scrollbar_pasos.set)
        
        self.pasos_caja.grid(row=0, column=0, sticky="nsew")
        scrollbar_pasos.grid(row=0, column=1, sticky="ns")

        # Resultado con scrollbar
        marco_resultado = ctk.CTkFrame(self.marco_resultados)
        marco_resultado.grid(row=0, column=1, sticky="nswe", padx=(6, 0), pady=8)
        marco_resultado.grid_columnconfigure(0, weight=1)
        marco_resultado.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_resultado, text="Resultado Final", font=self.font_titulo).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        
        # Frame para textbox y scrollbar
        frame_resultado = ctk.CTkFrame(marco_resultado)
        frame_resultado.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        frame_resultado.grid_columnconfigure(0, weight=1)
        frame_resultado.grid_rowconfigure(0, weight=1)
        
        self.resultado_caja = ctk.CTkTextbox(frame_resultado, font=self.font_mono)
        scrollbar_resultado = ctk.CTkScrollbar(frame_resultado, command=self.resultado_caja.yview)
        self.resultado_caja.configure(yscrollcommand=scrollbar_resultado.set)
        
        self.resultado_caja.grid(row=0, column=0, sticky="nsew")
        scrollbar_resultado.grid(row=0, column=1, sticky="ns")

        # Generar cuadrículas iniciales
        self.generar_cuadriculas_matriz()

    def _restaurar_ui_sistemas_ecuaciones(self):
        """Restaura la UI normal de sistemas de ecuaciones."""
        self.scrollable_contenido_frame.grid_rowconfigure(0, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(1, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(2, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(3, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(4, weight=1)
        
        self.marco_entrada.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        self.scrollable_contenido_frame.grid_slaves(row=1, column=0)[0].grid(row=1, column=0, sticky="ew", padx=12, pady=(4, 8))
        self.marco_matrices_container.grid(row=2, column=0, sticky="nsew", padx=12, pady=8)
        self.marco_controles.grid(row=3, column=0, sticky="ew", padx=12, pady=8)
        self.marco_resultados.grid(row=4, column=0, sticky="nswe", padx=12, pady=(0, 12))

    def toggle_matriz_visibility(self, matriz: str):
        """Alterna la visibilidad de las matrices."""
        if matriz == 'a':
            if self.matriz_a_visible:
                self.marco_grilla_a.grid_remove()
                self.btn_expandir_a.configure(text="+")
                self.matriz_a_visible = False
            else:
                self.marco_grilla_a.grid()
                self.btn_expandir_a.configure(text="−")
                self.matriz_a_visible = True
        elif matriz == 'b':
            if self.matriz_b_visible:
                self.marco_grilla_b.grid_remove()
                self.btn_expandir_b.configure(text="+")
                self.matriz_b_visible = False
            else:
                self.marco_grilla_b.grid()
                self.btn_expandir_b.configure(text="−")
                self.matriz_b_visible = True

    # --- SECCIÓN: OPERACIONES MATRICIALES ---
    def _cargar_ui_operaciones_matriciales(self):
        """Interfaz para operaciones básicas con matrices."""
        self.scrollable_contenido_frame.grid_rowconfigure(0, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(1, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(2, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(3, weight=1)
        self.scrollable_contenido_frame.grid_columnconfigure(0, weight=1)

        # --- Selector de Operación ---
        marco_operacion = ctk.CTkFrame(self.scrollable_contenido_frame, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_operacion.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        self.marco_entrada = marco_operacion
        
        ctk.CTkLabel(marco_operacion, text="Operación:", font=self.font_titulo).grid(row=0, column=0, padx=(12, 8), pady=12)
        
        self.operacion_matricial_var = ctk.StringVar(value="Suma")
        operaciones = [
            ("Suma", "A + B - Suma elemento a elemento"),
            ("Resta", "A - B - Resta elemento a elemento"), 
            ("Multiplicación", "A × B - Producto matricial"),
            ("Multiplicación por Escalar", "k × A - Multiplica cada elemento por k")
        ]
        
        for i, (op, desc) in enumerate(operaciones):
            rb = ctk.CTkRadioButton(marco_operacion, text=op, variable=self.operacion_matricial_var,
                                   value=op, font=self.font_normal)
            rb.grid(row=0, column=i+1, padx=8, pady=12)
            self._crear_tooltip(rb, desc)

        # --- Marco contenedor para matrices ---
        self.marco_matrices_container = ctk.CTkFrame(self.scrollable_contenido_frame)
        self.marco_matrices_container.grid(row=1, column=0, sticky="nsew", padx=12, pady=8)
        self.marco_matrices_container.grid_rowconfigure(0, weight=1)
        self.marco_matrices_container.grid_columnconfigure(0, weight=1)

        # --- Matrices y Escalares ---
        marco_matrices = ctk.CTkFrame(self.marco_matrices_container)
        marco_matrices.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        marco_matrices.grid_columnconfigure(0, weight=1)
        marco_matrices.grid_columnconfigure(1, weight=1)

        # Matriz A
        self.marco_a_op = ctk.CTkFrame(marco_matrices, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_a_op.grid(row=0, column=0, sticky="nswe", padx=(0, 6), pady=4)
        self.marco_a_op.grid_rowconfigure(2, weight=1)
        
        # Header con botón de expandir
        header_a_op = ctk.CTkFrame(self.marco_a_op, fg_color="transparent")
        header_a_op.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        header_a_op.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(header_a_op, text="Matriz A", 
                    font=self.font_bold_label).grid(row=0, column=0, sticky="w")
        
        self.btn_expandir_a_op = ctk.CTkButton(header_a_op, text="−", width=30, height=30,
                                             command=lambda: self.toggle_matriz_visibility_op('a'),
                                             fg_color=COLOR_BOTON_SECUNDARIO)
        self.btn_expandir_a_op.grid(row=0, column=1, sticky="e")
        
        marco_dims_a = ctk.CTkFrame(self.marco_a_op, fg_color="transparent")
        marco_dims_a.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        ctk.CTkLabel(marco_dims_a, text="Filas:", font=self.font_normal).grid(row=0, column=0, padx=(0, 4))
        self.var_filas_a_op = ctk.StringVar(value="2")
        self.ent_filas_a_op = ctk.CTkEntry(marco_dims_a, width=60, textvariable=self.var_filas_a_op)
        self.ent_filas_a_op.grid(row=0, column=1, padx=(0, 12))
        ctk.CTkLabel(marco_dims_a, text="Columnas:", font=self.font_normal).grid(row=0, column=2, padx=(0, 4))
        self.ent_columnas_a_op = ctk.CTkEntry(marco_dims_a, width=60)
        self.ent_columnas_a_op.insert(0, "2")
        self.ent_columnas_a_op.grid(row=0, column=3)

        # Escalar para A
        marco_escalar_a = ctk.CTkFrame(self.marco_a_op, fg_color="transparent")
        marco_escalar_a.grid(row=1, column=0, sticky="ew", padx=8, pady=(4, 8))
        ctk.CTkLabel(marco_escalar_a, text="Escalar α:", font=self.font_normal).grid(row=0, column=0, padx=(0, 4))
        self.ent_coef_a_op = ctk.CTkEntry(marco_escalar_a, width=80)
        self.ent_coef_a_op.insert(0, "1")
        self.ent_coef_a_op.grid(row=0, column=1)

        # Marco para la cuadrícula de A
        self.marco_grilla_a_op = ctk.CTkFrame(self.marco_a_op)
        self.marco_grilla_a_op.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))

        # Matriz B
        self.marco_b_op = ctk.CTkFrame(marco_matrices, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_b_op.grid(row=0, column=1, sticky="nswe", padx=(6, 0), pady=4)
        self.marco_b_op.grid_rowconfigure(2, weight=1)
        
        # Header con botón de expandir
        header_b_op = ctk.CTkFrame(self.marco_b_op, fg_color="transparent")
        header_b_op.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        header_b_op.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(header_b_op, text="Matriz B", 
                    font=self.font_bold_label).grid(row=0, column=0, sticky="w")
        
        self.btn_expandir_b_op = ctk.CTkButton(header_b_op, text="−", width=30, height=30,
                                             command=lambda: self.toggle_matriz_visibility_op('b'),
                                             fg_color=COLOR_BOTON_SECUNDARIO)
        self.btn_expandir_b_op.grid(row=0, column=1, sticky="e")
        
        marco_dims_b = ctk.CTkFrame(self.marco_b_op, fg_color="transparent")
        marco_dims_b.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        ctk.CTkLabel(marco_dims_b, text="Filas:", font=self.font_normal).grid(row=0, column=0, padx=(0, 4))
        self.ent_filas_b_op = ctk.CTkEntry(marco_dims_b, width=60)
        self.ent_filas_b_op.insert(0, "2")
        self.ent_filas_b_op.grid(row=0, column=1, padx=(0, 12))
        ctk.CTkLabel(marco_dims_b, text="Columnas:", font=self.font_normal).grid(row=0, column=2, padx=(0, 4))
        self.ent_columnas_b_op = ctk.CTkEntry(marco_dims_b, width=60)
        self.ent_columnas_b_op.insert(0, "2")
        self.ent_columnas_b_op.grid(row=0, column=3)

        # Escalar para B
        marco_escalar_b = ctk.CTkFrame(self.marco_b_op, fg_color="transparent")
        marco_escalar_b.grid(row=1, column=0, sticky="ew", padx=8, pady=(4, 8))
        ctk.CTkLabel(marco_escalar_b, text="Escalar β:", font=self.font_normal).grid(row=0, column=0, padx=(0, 4))
        self.ent_coef_b_op = ctk.CTkEntry(marco_escalar_b, width=80)
        self.ent_coef_b_op.insert(0, "1")
        self.ent_coef_b_op.grid(row=0, column=1)

        # Marco para la cuadrícula de B
        self.marco_grilla_b_op = ctk.CTkFrame(self.marco_b_op)
        self.marco_grilla_b_op.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))

        # Listas para entradas de matrices
        self.entradas_a_op = []
        self.entradas_b_op = []
        self.grilla_a_op = []
        self.grilla_b_op = []
        self.matriz_a_op_visible = True
        self.matriz_b_op_visible = True

        # --- Controles ---
        self.marco_controles = ctk.CTkFrame(self.scrollable_contenido_frame)
        self.marco_controles.grid(row=2, column=0, sticky="ew", padx=12, pady=8)
        
        ctk.CTkButton(self.marco_controles, text="Generar Cuadrículas", 
                     command=self.generar_cuadriculas_operaciones,
                     fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        
        ctk.CTkButton(self.marco_controles, text="Calcular Operación", 
                     command=self.calcular_operacion_matricial,
                     fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=1, padx=6)
        
        ctk.CTkButton(self.marco_controles, text="Limpiar", 
                     command=self.limpiar_operaciones,
                     fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=2, padx=6)

        # Botón para modo presentación
        self.btn_presentacion = ctk.CTkButton(self.marco_controles, text="📊 Ver Paso a Paso",
                     command=self.toggle_modo_presentacion,
                     fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER)
        self.btn_presentacion.grid(row=0, column=3, padx=6)

        # --- Resultados ---
        self.marco_resultados = ctk.CTkFrame(self.scrollable_contenido_frame)
        self.marco_resultados.grid(row=3, column=0, sticky="nswe", padx=12, pady=(0, 12))
        self.marco_resultados.grid_rowconfigure(0, weight=1)
        self.marco_resultados.grid_columnconfigure(0, weight=1)
        self.marco_resultados.grid_columnconfigure(1, weight=1)

        # Pasos con scrollbar
        marco_pasos = ctk.CTkFrame(self.marco_resultados)
        marco_pasos.grid(row=0, column=0, sticky="nswe", padx=(0, 6), pady=8)
        marco_pasos.grid_columnconfigure(0, weight=1)
        marco_pasos.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_pasos, text="Bitácora Paso a Paso", font=self.font_titulo).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        
        # Frame para textbox y scrollbar
        frame_pasos = ctk.CTkFrame(marco_pasos)
        frame_pasos.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        frame_pasos.grid_columnconfigure(0, weight=1)
        frame_pasos.grid_rowconfigure(0, weight=1)
        
        self.pasos_caja_op = ctk.CTkTextbox(frame_pasos, font=self.font_mono)
        scrollbar_pasos_op = ctk.CTkScrollbar(frame_pasos, command=self.pasos_caja_op.yview)
        self.pasos_caja_op.configure(yscrollcommand=scrollbar_pasos_op.set)
        
        self.pasos_caja_op.grid(row=0, column=0, sticky="nsew")
        scrollbar_pasos_op.grid(row=0, column=1, sticky="ns")

        # Resultado con scrollbar
        marco_resultado = ctk.CTkFrame(self.marco_resultados)
        marco_resultado.grid(row=0, column=1, sticky="nswe", padx=(6, 0), pady=8)
        marco_resultado.grid_columnconfigure(0, weight=1)
        marco_resultado.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_resultado, text="Resultado Final", font=self.font_titulo).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        
        # Frame para textbox y scrollbar
        frame_resultado = ctk.CTkFrame(marco_resultado)
        frame_resultado.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        frame_resultado.grid_columnconfigure(0, weight=1)
        frame_resultado.grid_rowconfigure(0, weight=1)
        
        self.resultado_caja_op = ctk.CTkTextbox(frame_resultado, font=self.font_mono)
        scrollbar_resultado_op = ctk.CTkScrollbar(frame_resultado, command=self.resultado_caja_op.yview)
        self.resultado_caja_op.configure(yscrollcommand=scrollbar_resultado_op.set)
        
        self.resultado_caja_op.grid(row=0, column=0, sticky="nsew")
        scrollbar_resultado_op.grid(row=0, column=1, sticky="ns")

        # Generar cuadrículas iniciales
        self.generar_cuadriculas_operaciones()

    def _restaurar_ui_operaciones_matriciales(self):
        """Restaura la UI normal de operaciones matriciales."""
        self.scrollable_contenido_frame.grid_rowconfigure(0, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(1, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(2, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(3, weight=1)
        
        self.marco_entrada.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        self.marco_matrices_container.grid(row=1, column=0, sticky="nsew", padx=12, pady=8)
        self.marco_controles.grid(row=2, column=0, sticky="ew", padx=12, pady=8)
        self.marco_resultados.grid(row=3, column=0, sticky="nswe", padx=12, pady=(0, 12))

    def toggle_matriz_visibility_op(self, matriz: str):
        """Alterna la visibilidad de las matrices en operaciones."""
        if matriz == 'a':
            if self.matriz_a_op_visible:
                self.marco_grilla_a_op.grid_remove()
                self.btn_expandir_a_op.configure(text="+")
                self.matriz_a_op_visible = False
            else:
                self.marco_grilla_a_op.grid()
                self.btn_expandir_a_op.configure(text="−")
                self.matriz_a_op_visible = True
        elif matriz == 'b':
            if self.matriz_b_op_visible:
                self.marco_grilla_b_op.grid_remove()
                self.btn_expandir_b_op.configure(text="+")
                self.matriz_b_op_visible = False
            else:
                self.marco_grilla_b_op.grid()
                self.btn_expandir_b_op.configure(text="−")
                self.matriz_b_op_visible = True

    # --- SECCIÓN: PROPIEDADES DE MATRICES ---  
    def _cargar_ui_propiedades_matrices(self):
        """Interfaz para análisis de propiedades matriciales."""
        self.scrollable_contenido_frame.grid_rowconfigure(0, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(1, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(2, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(3, weight=1)
        self.scrollable_contenido_frame.grid_columnconfigure(0, weight=1)

        # --- Selector de Propiedad ---
        marco_propiedad = ctk.CTkFrame(self.scrollable_contenido_frame, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_propiedad.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        self.marco_entrada = marco_propiedad
        
        ctk.CTkLabel(marco_propiedad, text="Propiedad a Calcular:", font=self.font_titulo).grid(row=0, column=0, padx=(12, 8), pady=12)
        
        self.propiedad_matricial_var = ctk.StringVar(value="Determinante")
        propiedades = [
            ("Determinante", "Calcula el determinante de una matriz cuadrada"),
            ("Independencia Lineal", "Verifica si los vectores son linealmente independientes"), 
            ("Rango", "Calcula el rango de la matriz")
        ]
        
        for i, (prop, desc) in enumerate(propiedades):
            rb = ctk.CTkRadioButton(marco_propiedad, text=prop, variable=self.propiedad_matricial_var,
                                   value=prop, font=self.font_normal)
            rb.grid(row=0, column=i+1, padx=8, pady=12)
            self._crear_tooltip(rb, desc)

        # --- Marco contenedor para matriz ---
        self.marco_matrices_container = ctk.CTkFrame(self.scrollable_contenido_frame)
        self.marco_matrices_container.grid(row=1, column=0, sticky="nsew", padx=12, pady=8)
        self.marco_matrices_container.grid_rowconfigure(0, weight=1)
        self.marco_matrices_container.grid_columnconfigure(0, weight=1)

        # --- Matriz ---
        marco_matriz = ctk.CTkFrame(self.marco_matrices_container)
        marco_matriz.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        self.marco_a_prop = ctk.CTkFrame(marco_matriz, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_a_prop.grid(row=0, column=0, sticky="nswe", padx=(0, 0), pady=4)
        self.marco_a_prop.grid_rowconfigure(2, weight=1)
        
        # Header con botón de expandir
        header_a_prop = ctk.CTkFrame(self.marco_a_prop, fg_color="transparent")
        header_a_prop.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        header_a_prop.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(header_a_prop, text="Matriz A", 
                    font=self.font_bold_label).grid(row=0, column=0, sticky="w")
        
        self.btn_expandir_a_prop = ctk.CTkButton(header_a_prop, text="−", width=30, height=30,
                                               command=lambda: self.toggle_matriz_visibility_prop('a'),
                                               fg_color=COLOR_BOTON_SECUNDARIO)
        self.btn_expandir_a_prop.grid(row=0, column=1, sticky="e")
        
        marco_dims_a = ctk.CTkFrame(self.marco_a_prop, fg_color="transparent")
        marco_dims_a.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        ctk.CTkLabel(marco_dims_a, text="Filas:", font=self.font_normal).grid(row=0, column=0, padx=(0, 4))
        self.var_filas_a_prop = ctk.StringVar(value="2")
        self.ent_filas_a_prop = ctk.CTkEntry(marco_dims_a, width=60, textvariable=self.var_filas_a_prop)
        self.ent_filas_a_prop.grid(row=0, column=1, padx=(0, 12))
        ctk.CTkLabel(marco_dims_a, text="Columnas:", font=self.font_normal).grid(row=0, column=2, padx=(0, 4))
        self.ent_columnas_a_prop = ctk.CTkEntry(marco_dims_a, width=60)
        self.ent_columnas_a_prop.insert(0, "2")
        self.ent_columnas_a_prop.grid(row=0, column=3)

        # Marco para la cuadrícula de A
        self.marco_grilla_a_prop = ctk.CTkFrame(self.marco_a_prop)
        self.marco_grilla_a_prop.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))

        # Listas para entradas de matrices
        self.entradas_a_prop = []
        self.grilla_a_prop = []
        self.matriz_a_prop_visible = True

        # --- Controles ---
        self.marco_controles = ctk.CTkFrame(self.scrollable_contenido_frame)
        self.marco_controles.grid(row=2, column=0, sticky="ew", padx=12, pady=8)
        
        ctk.CTkButton(self.marco_controles, text="Generar Cuadrícula", 
                     command=self.generar_cuadriculas_propiedades,
                     fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        
        ctk.CTkButton(self.marco_controles, text="Calcular Propiedad", 
                     command=self.calcular_propiedad_matricial,
                     fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=1, padx=6)
        
        ctk.CTkButton(self.marco_controles, text="Limpiar", 
                     command=self.limpiar_propiedades,
                     fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=2, padx=6)

        # Botón para modo presentación
        self.btn_presentacion = ctk.CTkButton(self.marco_controles, text="📊 Ver Paso a Paso",
                     command=self.toggle_modo_presentacion,
                     fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER)
        self.btn_presentacion.grid(row=0, column=3, padx=6)

        # --- Resultados ---
        self.marco_resultados = ctk.CTkFrame(self.scrollable_contenido_frame)
        self.marco_resultados.grid(row=3, column=0, sticky="nswe", padx=12, pady=(0, 12))
        self.marco_resultados.grid_rowconfigure(0, weight=1)
        self.marco_resultados.grid_columnconfigure(0, weight=1)
        self.marco_resultados.grid_columnconfigure(1, weight=1)

        # Pasos con scrollbar
        marco_pasos = ctk.CTkFrame(self.marco_resultados)
        marco_pasos.grid(row=0, column=0, sticky="nswe", padx=(0, 6), pady=8)
        marco_pasos.grid_columnconfigure(0, weight=1)
        marco_pasos.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_pasos, text="Bitácora Paso a Paso", font=self.font_titulo).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        
        # Frame para textbox y scrollbar
        frame_pasos = ctk.CTkFrame(marco_pasos)
        frame_pasos.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        frame_pasos.grid_columnconfigure(0, weight=1)
        frame_pasos.grid_rowconfigure(0, weight=1)
        
        self.pasos_caja_prop = ctk.CTkTextbox(frame_pasos, font=self.font_mono)
        scrollbar_pasos_prop = ctk.CTkScrollbar(frame_pasos, command=self.pasos_caja_prop.yview)
        self.pasos_caja_prop.configure(yscrollcommand=scrollbar_pasos_prop.set)
        
        self.pasos_caja_prop.grid(row=0, column=0, sticky="nsew")
        scrollbar_pasos_prop.grid(row=0, column=1, sticky="ns")

        # Resultado con scrollbar
        marco_resultado = ctk.CTkFrame(self.marco_resultados)
        marco_resultado.grid(row=0, column=1, sticky="nswe", padx=(6, 0), pady=8)
        marco_resultado.grid_columnconfigure(0, weight=1)
        marco_resultado.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_resultado, text="Resultado Final", font=self.font_titulo).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        
        # Frame para textbox y scrollbar
        frame_resultado = ctk.CTkFrame(marco_resultado)
        frame_resultado.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        frame_resultado.grid_columnconfigure(0, weight=1)
        frame_resultado.grid_rowconfigure(0, weight=1)
        
        self.resultado_caja_prop = ctk.CTkTextbox(frame_resultado, font=self.font_mono)
        scrollbar_resultado_prop = ctk.CTkScrollbar(frame_resultado, command=self.resultado_caja_prop.yview)
        self.resultado_caja_prop.configure(yscrollcommand=scrollbar_resultado_prop.set)
        
        self.resultado_caja_prop.grid(row=0, column=0, sticky="nsew")
        scrollbar_resultado_prop.grid(row=0, column=1, sticky="ns")

        # Generar cuadrículas iniciales
        self.generar_cuadriculas_propiedades()

    def _restaurar_ui_propiedades_matrices(self):
        """Restaura la UI normal de propiedades de matrices."""
        self.scrollable_contenido_frame.grid_rowconfigure(0, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(1, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(2, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(3, weight=1)
        
        self.marco_entrada.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        self.marco_matrices_container.grid(row=1, column=0, sticky="nsew", padx=12, pady=8)
        self.marco_controles.grid(row=2, column=0, sticky="ew", padx=12, pady=8)
        self.marco_resultados.grid(row=3, column=0, sticky="nswe", padx=12, pady=(0, 12))

    def toggle_matriz_visibility_prop(self, matriz: str):
        """Alterna la visibilidad de la matriz en propiedades."""
        if matriz == 'a':
            if self.matriz_a_prop_visible:
                self.marco_grilla_a_prop.grid_remove()
                self.btn_expandir_a_prop.configure(text="+")
                self.matriz_a_prop_visible = False
            else:
                self.marco_grilla_a_prop.grid()
                self.btn_expandir_a_prop.configure(text="−")
                self.matriz_a_prop_visible = True

    # --- SECCIÓN: MÉTODOS NUMÉRICOS ---
    def _cargar_ui_metodos_numericos(self):
        """Interfaz para métodos numéricos."""
        self.scrollable_contenido_frame.grid_rowconfigure(0, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(1, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(2, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(3, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(4, weight=1)
        self.scrollable_contenido_frame.grid_columnconfigure(0, weight=1)

        # --- Selector de Método ---
        marco_metodo = ctk.CTkFrame(self.scrollable_contenido_frame, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_metodo.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        self.marco_entrada = marco_metodo
        
        ctk.CTkLabel(marco_metodo, text="Método Numérico:", font=self.font_titulo).grid(row=0, column=0, padx=(12, 8), pady=12)
        
        self.metodo_numerico_var = ctk.StringVar(value="Bisección")
        metodos = [
            ("Bisección", "Encuentra raíces dividiendo intervalos a la mitad")
        ]
        
        for i, (metodo, desc) in enumerate(metodos):
            rb = ctk.CTkRadioButton(marco_metodo, text=metodo, variable=self.metodo_numerico_var,
                                   value=metodo, font=self.font_normal)
            rb.grid(row=0, column=i+1, padx=8, pady=12)
            self._crear_tooltip(rb, desc)

        # --- Entrada de Función ---
        marco_funcion = ctk.CTkFrame(self.scrollable_contenido_frame, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_funcion.grid(row=1, column=0, sticky="ew", padx=12, pady=(4, 8))
        marco_funcion.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_funcion, text="Función f(x) =", font=self.font_normal).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.ent_funcion_fx = ctk.CTkEntry(marco_funcion, placeholder_text="Ej: cos(x) - x  (usar 'x' como variable)")
        self.ent_funcion_fx.grid(row=0, column=1, columnspan=5, sticky="ew", padx=8, pady=6)
        
        # Fila 1: Intervalo y Tolerancia
        ctk.CTkLabel(marco_funcion, text="Intervalo [a, b]:", font=self.font_normal).grid(row=1, column=0, sticky="w", padx=8, pady=6)
        self.ent_intervalo_a = ctk.CTkEntry(marco_funcion, width=100, placeholder_text="a")
        self.ent_intervalo_a.grid(row=1, column=1, sticky="w", padx=(8,2), pady=6)
        self.ent_intervalo_b = ctk.CTkEntry(marco_funcion, width=100, placeholder_text="b")
        self.ent_intervalo_b.grid(row=1, column=2, sticky="w", padx=(2,8), pady=6)
        
        ctk.CTkLabel(marco_funcion, text="Tolerancia (E):", font=self.font_normal).grid(row=1, column=3, sticky="w", padx=(20, 2), pady=6)
        self.ent_tolerancia_e = ctk.CTkEntry(marco_funcion, width=100, placeholder_text="Ej: 0.0001")
        self.ent_tolerancia_e.grid(row=1, column=4, sticky="w", padx=(2, 8), pady=6)
        
        # --- Marco para botones de ejemplos ---
        marco_ejemplos = ctk.CTkFrame(self.scrollable_contenido_frame)
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
        
        # --- Marco para botones de control ---
        self.marco_controles = ctk.CTkFrame(self.scrollable_contenido_frame)
        self.marco_controles.grid(row=3, column=0, sticky="ew", padx=12, pady=(6,12))
        
        ctk.CTkButton(self.marco_controles, text="Calcular", command=self.calcular_operacion_numerica,
                      fg_color=COLOR_NUMERICOS, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        
        ctk.CTkButton(self.marco_controles, text="Limpiar", command=self.limpiar_numerico,
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=1, padx=6)
        
        ctk.CTkButton(self.marco_controles, text="Graficar Función",
                      command=self.graficar_funcion_interna,
                      fg_color=COLOR_BOTON_SECUNDARIO, 
                      hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=2, padx=6)

        # Botón para modo presentación
        self.btn_presentacion = ctk.CTkButton(self.marco_controles, text="📊 Ver Paso a Paso",
                     command=self.toggle_modo_presentacion,
                     fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER)
        self.btn_presentacion.grid(row=0, column=3, padx=6)

        # --- Contenedor inferior para Pasos y Resultado ---
        self.marco_resultados = ctk.CTkFrame(self.scrollable_contenido_frame)
        self.marco_resultados.grid(row=4, column=0, sticky="nswe", padx=12, pady=(6,12))
        self.marco_resultados.grid_rowconfigure(0, weight=1)
        self.marco_resultados.grid_columnconfigure(0, weight=2)
        self.marco_resultados.grid_columnconfigure(1, weight=1)
        
        # --- Marco para Pasos ---
        marco_pasos = ctk.CTkFrame(self.marco_resultados)
        marco_pasos.grid(row=0, column=0, sticky="nswe", padx=(0,6))
        marco_pasos.grid_columnconfigure(0, weight=1)
        marco_pasos.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_pasos, text="Bitácora Paso a Paso", font=self.font_titulo).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        
        # Frame para textbox y scrollbar
        frame_pasos_num = ctk.CTkFrame(marco_pasos)
        frame_pasos_num.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))
        frame_pasos_num.grid_columnconfigure(0, weight=1)
        frame_pasos_num.grid_rowconfigure(0, weight=1)
        
        self.pasos_caja_num = ctk.CTkTextbox(frame_pasos_num, height=220, font=self.font_mono, wrap="none")
        scrollbar_pasos_num = ctk.CTkScrollbar(frame_pasos_num, command=self.pasos_caja_num.yview)
        self.pasos_caja_num.configure(yscrollcommand=scrollbar_pasos_num.set)
        
        self.pasos_caja_num.grid(row=0, column=0, sticky="nsew")
        scrollbar_pasos_num.grid(row=0, column=1, sticky="ns")
        
        # --- Marco para Resultado ---
        marco_resultado = ctk.CTkFrame(self.marco_resultados)
        marco_resultado.grid(row=0, column=1, sticky="nswe", padx=(6,0))
        marco_resultado.grid_columnconfigure(0, weight=1)
        marco_resultado.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_resultado, text="Resultado Final", font=self.font_titulo).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        
        # Frame para textbox y scrollbar
        frame_resultado_num = ctk.CTkFrame(marco_resultado)
        frame_resultado_num.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))
        frame_resultado_num.grid_columnconfigure(0, weight=1)
        frame_resultado_num.grid_rowconfigure(0, weight=1)
        
        self.resultado_caja_num = ctk.CTkTextbox(frame_resultado_num, height=220, font=self.font_mono)
        scrollbar_resultado_num = ctk.CTkScrollbar(frame_resultado_num, command=self.resultado_caja_num.yview)
        self.resultado_caja_num.configure(yscrollcommand=scrollbar_resultado_num.set)
        
        self.resultado_caja_num.grid(row=0, column=0, sticky="nsew")
        scrollbar_resultado_num.grid(row=0, column=1, sticky="ns")

    def _restaurar_ui_metodos_numericos(self):
        """Restaura la UI normal de métodos numéricos."""
        self.scrollable_contenido_frame.grid_rowconfigure(0, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(1, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(2, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(3, weight=0)
        self.scrollable_contenido_frame.grid_rowconfigure(4, weight=1)
        
        self.marco_entrada.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        self.scrollable_contenido_frame.grid_slaves(row=1, column=0)[0].grid(row=1, column=0, sticky="ew", padx=12, pady=(4, 8))
        self.scrollable_contenido_frame.grid_slaves(row=2, column=0)[0].grid(row=2, column=0, sticky="ew", padx=12, pady=4)
        self.marco_controles.grid(row=3, column=0, sticky="ew", padx=12, pady=(6,12))
        self.marco_resultados.grid(row=4, column=0, sticky="nswe", padx=12, pady=(6,12))

    # --- MÉTODOS AUXILIARES ---
    
    def _sincronizar_filas_cramer(self):
        """Sincroniza filas para Cramer."""
        if hasattr(self, 'metodo_sistema_var') and self.metodo_sistema_var.get() == 'Regla de Cramer':
            filas_a_val = self.var_filas_a.get()
            if hasattr(self, 'ent_filas_b') and self.ent_filas_b.get() != filas_a_val:
                estado_previo = self.ent_filas_b.cget("state")
                self.ent_filas_b.configure(state="normal")
                self.ent_filas_b.delete(0, 'end')
                self.ent_filas_b.insert(0, filas_a_val)
                self.ent_filas_b.configure(state=estado_previo)

    def _set_resultado(self, texto: str, limpiar_pasos=False):
        """Escribe texto en la caja de resultados."""
        if limpiar_pasos: 
            self.pasos_caja.delete('0.0', 'end')
        self.resultado_caja.delete('0.0', 'end')
        self.resultado_caja.insert('0.0', texto)

    def _append_matriz(self, M, titulo=None):
        """Añade matriz a los pasos."""
        if titulo: 
            self.pasos_caja.insert('end', f'{titulo}\n')
        for f in M: 
            self.pasos_caja.insert('end', '  '.join(_fmt(v) for v in f) + '\n')
        self.pasos_caja.insert('end', '\n')

    def _leer_escalar(self, e):
        """Lee valor de escalar."""
        t = e.get().strip() if e else ''
        if t in ('','+'): return 1.0
        if t == '-': return -1.0
        try: return _parse_valor(t)
        except ValueError as err: raise ValueError(f"Valor de escalar inválido: {err}")

    def generar_cuadriculas_matriz(self):
        """Genera cuadrículas para matrices en sistemas de ecuaciones."""
        try:
            filas_a = int(self.ent_filas_a.get())
            cols_a = int(self.ent_columnas_a.get())
            filas_b = int(self.ent_filas_b.get())
            
            if filas_a <= 0 or cols_a <= 0 or filas_b <= 0:
                raise ValueError("Las dimensiones deben ser números enteros positivos")

            # Limpiar cuadrículas existentes
            for widget in self.grilla_a: widget.destroy()
            for widget in self.grilla_b: widget.destroy()
            self.grilla_a = []
            self.grilla_b = []

            # Inicializar listas
            self.entradas_a = [[None]*cols_a for _ in range(filas_a)]
            self.entradas_b = [[None]*1 for _ in range(filas_b)]

            # Crear cuadrícula para A
            for i in range(filas_a):
                for j in range(cols_a):
                    e = ctk.CTkEntry(self.marco_grilla_a, width=60)
                    e.grid(row=i, column=j, padx=2, pady=2)
                    self.grilla_a.append(e)
                    self.entradas_a[i][j] = e

            # Crear cuadrícula para B
            for i in range(filas_b):
                e2 = ctk.CTkEntry(self.marco_grilla_b, width=60)
                e2.grid(row=i, column=0, padx=2, pady=2)
                self.grilla_b.append(e2)
                self.entradas_b[i][0] = e2

            self._set_resultado('Matrices listas para ingresar datos')

        except ValueError as e:
            self._set_resultado(f'Error: {e}')

    def generar_cuadriculas_operaciones(self):
        """Genera cuadrículas para operaciones matriciales."""
        try:
            filas_a = int(self.ent_filas_a_op.get())
            cols_a = int(self.ent_columnas_a_op.get())
            filas_b = int(self.ent_filas_b_op.get())
            cols_b = int(self.ent_columnas_b_op.get())
            
            if filas_a <= 0 or cols_a <= 0 or filas_b <= 0 or cols_b <= 0:
                raise ValueError("Las dimensiones deben ser números enteros positivos")

            # Limpiar cuadrículas existentes
            for widget in self.grilla_a_op: widget.destroy()
            for widget in self.grilla_b_op: widget.destroy()
            self.grilla_a_op = []
            self.grilla_b_op = []

            # Inicializar listas
            self.entradas_a_op = [[None]*cols_a for _ in range(filas_a)]
            self.entradas_b_op = [[None]*cols_b for _ in range(filas_b)]

            # Crear cuadrícula para A
            for i in range(filas_a):
                for j in range(cols_a):
                    e = ctk.CTkEntry(self.marco_grilla_a_op, width=60)
                    e.grid(row=i, column=j, padx=2, pady=2)
                    self.grilla_a_op.append(e)
                    self.entradas_a_op[i][j] = e

            # Crear cuadrícula para B
            for i in range(filas_b):
                for j in range(cols_b):
                    e2 = ctk.CTkEntry(self.marco_grilla_b_op, width=60)
                    e2.grid(row=i, column=j, padx=2, pady=2)
                    self.grilla_b_op.append(e2)
                    self.entradas_b_op[i][j] = e2

            self.resultado_caja_op.delete('0.0', 'end')
            self.resultado_caja_op.insert('0.0', 'Matrices listas para ingresar datos')

        except ValueError as e:
            self.resultado_caja_op.delete('0.0', 'end')
            self.resultado_caja_op.insert('0.0', f'Error: {e}')

    def generar_cuadriculas_propiedades(self):
        """Genera cuadrículas para propiedades de matrices."""
        try:
            filas_a = int(self.ent_filas_a_prop.get())
            cols_a = int(self.ent_columnas_a_prop.get())
            
            if filas_a <= 0 or cols_a <= 0:
                raise ValueError("Las dimensiones deben ser números enteros positivos")

            # Limpiar cuadrículas existentes
            for widget in self.grilla_a_prop: widget.destroy()
            self.grilla_a_prop = []

            # Inicializar listas
            self.entradas_a_prop = [[None]*cols_a for _ in range(filas_a)]

            # Crear cuadrícula para A
            for i in range(filas_a):
                for j in range(cols_a):
                    e = ctk.CTkEntry(self.marco_grilla_a_prop, width=60)
                    e.grid(row=i, column=j, padx=2, pady=2)
                    self.grilla_a_prop.append(e)
                    self.entradas_a_prop[i][j] = e

            self.resultado_caja_prop.delete('0.0', 'end')
            self.resultado_caja_prop.insert('0.0', 'Matriz lista para ingresar datos')

        except ValueError as e:
            self.resultado_caja_prop.delete('0.0', 'end')
            self.resultado_caja_prop.insert('0.0', f'Error: {e}')

    def _poblar_cuadricula(self, entradas_grid: List[List[ctk.CTkEntry]], datos: List[List[float]]):
        """Poblar cuadrícula con datos."""
        filas_grid = len(entradas_grid)
        cols_grid = len(entradas_grid[0]) if filas_grid > 0 else 0
        filas_datos = len(datos)
        cols_datos = len(datos[0]) if filas_datos > 0 else 0

        for i in range(min(filas_grid, filas_datos)):
            for j in range(min(cols_grid, cols_datos)):
                if entradas_grid[i][j]:
                    entradas_grid[i][j].delete(0, 'end')
                    entradas_grid[i][j].insert(0, _fmt(datos[i][j]))

    def parsear_y_poblar_ecuaciones(self):
        """Parsea y pobla ecuaciones en las matrices."""
        try:
            texto_completo = self.caja_ecuaciones.get('1.0', 'end')
            lineas = [linea.strip() for linea in texto_completo.split('\n') if linea.strip() and '=' in linea]
            if not lineas:
                raise ValueError("No se encontraron ecuaciones válidas (deben contener '=')")

            var_map: Dict[str, int] = {}
            var_ordenadas: List[str] = []
            matriz_coef_dict: List[Dict[str, float]] = []
            vector_const: List[float] = []

            regex_termino = re.compile(r'([+-]?)(\d*\.?\d*)\s*\*?\s*([a-zA-Z]\w*)')

            for linea in lineas:
                partes = linea.split('=', 1)
                if len(partes) != 2: continue
                lhs, rhs = partes[0].strip(), partes[1].strip()

                constante = _parse_valor(rhs)
                vector_const.append(constante)
                
                fila_coef: Dict[str, float] = {}
                lhs_limpio = lhs.replace(' ', '').replace('−', '-')
                
                if lhs_limpio and lhs_limpio[0] not in ('+', '-'):
                    lhs_limpio = '+' + lhs_limpio
                
                for match in regex_termino.finditer(lhs_limpio):
                    signo, coeff_str, var_str = match.groups()
                    
                    if var_str not in var_map:
                        var_map[var_str] = len(var_ordenadas)
                        var_ordenadas.append(var_str)
                    
                    coeff_val = 1.0
                    if coeff_str:
                        coeff_val = _parse_valor(coeff_str)
                    
                    if signo == '-':
                        coeff_val = -coeff_val
                    
                    fila_coef[var_str] = fila_coef.get(var_str, 0.0) + coeff_val

                matriz_coef_dict.append(fila_coef)

            num_filas = len(lineas)
            num_vars = len(var_ordenadas)
            
            # Construye las matrices finales
            matriz_a = [[0.0] * num_vars for _ in range(num_filas)]
            for i, fila_coef in enumerate(matriz_coef_dict):
                for var_str, coeff_val in fila_coef.items():
                    j = var_map[var_str]
                    matriz_a[i][j] = coeff_val
            
            matriz_b = [[val] for val in vector_const]

            # Actualiza la UI
            self.var_filas_a.set(str(num_filas))
            self.ent_columnas_a.delete(0, 'end')
            self.ent_columnas_a.insert(0, str(num_vars))
            
            self.ent_filas_b.delete(0, 'end')
            self.ent_filas_b.insert(0, str(num_filas))

            # Regenerar cuadrículas y poblar
            self.generar_cuadriculas_matriz()
            self._poblar_cuadricula(self.entradas_a, matriz_a)
            self._poblar_cuadricula(self.entradas_b, matriz_b)
            
            self._set_resultado(f"Sistema de {num_filas} ecuaciones con {num_vars} variables cargado.\nVariables: {', '.join(var_ordenadas)}")
                
        except ValueError as e:
            self._set_resultado(f"Error al analizar ecuaciones: {e}")
        except Exception as e:
            self._set_resultado(f"Error inesperado: {e}")

    def _leer_entradas_de_cuadricula(self, entradas: List[List[ctk.CTkEntry]]):
        """Lee entradas de cuadrícula."""
        if not entradas:
            return []
            
        if not entradas[0] and len(entradas) > 0 :
            raise ValueError("Primero debe generar la matriz")

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
                            matriz[i][j] = _parse_valor(texto)
                        except ValueError as e:
                            raise ValueError(f'Valor inválido en ({i+1},{j+1}): {e}')

        if celdas_no_vacias == 0 and filas * cols > 0:
            raise ValueError("La matriz no puede estar vacía, ingrese al menos un valor.")

        return matriz

    def calcular_sistema_ecuaciones(self):
        """Calcula la solución del sistema de ecuaciones."""
        try:
            from Complement import (
                gauss_steps, gauss_jordan_steps, inverse_steps, 
                resolver_por_cramer, independenciaVectores, pasos_determinante
            )
        except ImportError:
            self._set_resultado("ERROR: No se pudo cargar Complement.py")
            return

        try:
            A = self._leer_entradas_de_cuadricula(self.entradas_a)
            B = self._leer_entradas_de_cuadricula(self.entradas_b)
                 
        except ValueError as e:
            self._set_resultado(f'Error de entrada: {e}', limpiar_pasos=True)
            return
        except Exception as e:
            self._set_resultado(f'Error inesperado al leer matrices: {e}', limpiar_pasos=True)
            return

        metodo = self.metodo_sistema_var.get()
        
        if metodo == 'Regla de Cramer':
            try:
                if not A: raise ValueError("La matriz A no puede estar vacía")
                if not B: raise ValueError("El vector B no puede estar vacío")
                if len(A) != len(B): raise ValueError(f"Las filas de A ({len(A)}) y B ({len(B)}) no coinciden")
                if not A[0]: raise ValueError("La matriz A no tiene columnas")
                if len(A) != len(A[0]): raise ValueError("La matriz A debe ser cuadrada (n x n)")
                if not B[0] or len(B[0]) != 1: raise ValueError("B debe ser un vector columna (n x 1)")

                matriz_aumentada = [A[i] + [B[i][0]] for i in range(len(A))]
            except Exception as e:
                 self._set_resultado(f'Error al preparar Cramer: {e}', limpiar_pasos=True)
                 return

            res = resolver_por_cramer(matriz_aumentada)
            
            self.pasos_caja.delete('0.0', 'end')
            if res.get('pasos'):
                 self.pasos_caja.insert('0.0', '\n'.join(res['pasos']))

            if res['estado'] == 'exito':
                 sol_texto = '\n'.join(f'x{i+1} = {_fmt(v)}' for i,v in enumerate(res['solucion']))
                 self._set_resultado(f"Solución única encontrada:\n{sol_texto}")
            elif res['estado'] == 'sin_solucion_unica':
                 self._set_resultado(res['mensaje'])
            else:
                 self._set_resultado(f"Error: {res['mensaje']}")
            return

        elif metodo == 'Matriz Inversa':
            n = len(A)
            res = inverse_steps(A) 
            
            self.pasos_caja.delete('0.0','end')
            steps, ops = res.get('steps',[]), res.get('ops',[])
            total = len(steps); shown = 0
            for i, M in enumerate(steps):
                if i < 20 or i % PASO_SALTOS == 0:
                    if i < len(ops) and ops[i]: self.pasos_caja.insert('end', f'Op: {ops[i]}\n')
                    self._append_matriz(M, f'Paso {i}:'); shown += 1
                if shown >= MAX_SNAPSHOTS: break
            if total > shown: self.pasos_caja.insert('end', f'… ({total-shown} pasos omitidos)\n\n')
            
            if res.get('status') == 'invertible':
                inv = res['inverse']
                # Calcular solución: x = A⁻¹ * b
                solucion = []
                for i in range(len(inv)):
                    suma = 0.0
                    for j in range(len(inv[0])):
                        suma += inv[i][j] * B[j][0]
                    solucion.append(suma)
                
                sol_texto = '\n'.join(f'x{i+1} = {_fmt(v)}' for i,v in enumerate(solucion))
                self._set_resultado(f"A es invertible. Solución:\n{sol_texto}")
            elif res.get('status') == 'singular':
                 self._set_resultado('A es singular (no tiene inversa)')
            else:
                 self._set_resultado(f"Error: {res.get('mensaje','error desconocido en inversa')}")
            return

        else:  # Gauss o Gauss-Jordan
            matriz_aumentada = [A[i] + B[i] for i in range(len(A))]
            
            if metodo == 'Gauss-Jordan':
                res = gauss_jordan_steps(matriz_aumentada)
            else:  # Eliminación Gaussiana
                res = gauss_steps(matriz_aumentada)
            
            self.pasos_caja.delete('0.0','end')
            steps, ops = res.get('steps',[]), res.get('ops',[])
            total = len(steps); shown = 0
            
            for i, paso in enumerate(steps):
                if i < 20 or i % PASO_SALTOS == 0:
                    if i < len(ops) and ops[i]: self.pasos_caja.insert('end', f'Op: {ops[i]}\n')
                    self._append_matriz(paso, f'Paso {i}:'); shown += 1
                if shown >= MAX_SNAPSHOTS: break
            if total > shown: self.pasos_caja.insert('end', f'… ({total-shown} pasos omitidos)\n\n')
            
            status = res.get('status'); sol = res.get('solution')
            if status=='unique' and sol is not None:
                txt = 'Solución única:\n' + '\n'.join(f'x{i+1} = {v:.6g}' for i,v in enumerate(sol))
            elif status=='inconsistent': txt = 'El sistema es inconsistente (sin solución)'
            elif status=='infinite':
                libres = res.get('free_vars', []); base = res.get('basic_solution', {})
                m = len(A[0])
                lineas=[]
                for i in range(m):
                    if i in libres: lineas.append(f'x{i+1} = variable libre')
                    else: lineas.append(f'x{i+1} = {base.get(i,0.0):.6g}  (con libres = 0)')
                txt = 'Soluciones infinitas:\n' + '\n'.join(lineas)
            elif status=='empty': txt = 'Matriz vacía'
            else: txt = f"Estado: {status}"
            self._set_resultado(txt)

    def calcular_operacion_matricial(self):
        """Calcula operaciones matriciales."""
        try:
            A = self._leer_entradas_de_cuadricula(self.entradas_a_op)
            B = self._leer_entradas_de_cuadricula(self.entradas_b_op)
                 
        except ValueError as e:
            self.resultado_caja_op.delete('0.0', 'end')
            self.resultado_caja_op.insert('0.0', f'Error de entrada: {e}')
            self.pasos_caja_op.delete('0.0', 'end')
            return
        except Exception as e:
            self.resultado_caja_op.delete('0.0', 'end')
            self.resultado_caja_op.insert('0.0', f'Error inesperado al leer matrices: {e}')
            self.pasos_caja_op.delete('0.0', 'end')
            return

        operacion = self.operacion_matricial_var.get()
        fa, ca = len(A), len(A[0]) if A else 0
        fb, cb = len(B), len(B[0]) if B else 0
        
        self.pasos_caja_op.delete('0.0','end')
        try:
            if operacion in ('Suma','Resta'):
                alpha = self._leer_escalar(self.ent_coef_a_op)
                beta = self._leer_escalar(self.ent_coef_b_op)
                sgn = 1.0 if operacion=='Suma' else -1.0
                
                if fa != fb or ca != cb:
                    raise ValueError(f"Para {operacion.lower()}: dims(A)={fa}x{ca} != dims(B)={fb}x{cb}")

                Aesc = [[alpha*A[i][j] for j in range(ca)] for i in range(fa)]
                Besc = [[sgn*beta*B[i][j] for j in range(cb)] for i in range(fb)]
                C = [[Aesc[i][j]+Besc[i][j] for j in range(ca)] for i in range(fa)]
                R = C
                
                self._append_matriz(A,'Matriz A:')
                self._append_matriz(B,'Matriz B:')
                self._append_matriz(Aesc, f'α·A (α={_fmt(alpha)}):')
                self._append_matriz(Besc, f'{"+" if sgn>0 else "-"} β·B (β={_fmt(beta)}):')
                
                for i in range(fa):
                    for j in range(ca):
                        self.pasos_caja_op.insert('end', f'C[{i+1},{j+1}] = {_fmt(alpha)}·{_fmt(A[i][j])} {"+" if sgn>0 else "-"} {_fmt(beta)}·{_fmt(B[i][j])} = {_fmt(C[i][j])}\n')
                self._append_matriz(C, 'Resultado C = αA ' + ('+' if sgn>0 else '−') + ' βB:')

            elif operacion == 'Multiplicación':
                if ca != fb:
                    raise ValueError(f"Para multiplicación: cols(A)={ca} != filas(B)={fb}")

                C = [[sum(A[i][k]*B[k][j] for k in range(ca)) for j in range(cb)] for i in range(fa)]
                R = C
                
                self._append_matriz(A,'Matriz A:')
                self._append_matriz(B,'Matriz B:')
                
                for i in range(fa):
                    for j in range(cb):
                        terms = [f'{_fmt(A[i][k])}·{_fmt(B[k][j])}' for k in range(ca)]
                        self.pasos_caja_op.insert('end', f'C[{i+1},{j+1}] = ' + ' + '.join(terms) + f' = {_fmt(C[i][j])}\n')
                self._append_matriz(C,'Resultado C = A·B:')

            elif operacion == 'Multiplicación por Escalar':
                alpha = self._leer_escalar(self.ent_coef_a_op)
                C = [[alpha*A[i][j] for j in range(ca)] for i in range(fa)]
                R = C
                
                self._append_matriz(A,'Matriz A:')
                
                for i in range(fa):
                    for j in range(ca):
                        self.pasos_caja_op.insert('end', f'C[{i+1},{j+1}] = {_fmt(alpha)}·{_fmt(A[i][j])} = {_fmt(C[i][j])}\n')
                self._append_matriz(C, f'Resultado C = {_fmt(alpha)}·A:')

            else:
                raise ValueError('Operación desconocida')

            self.resultado_caja_op.delete('0.0','end')
            self.resultado_caja_op.insert('0.0','\n'.join('  '.join(_fmt(v) for v in fila) for fila in R))

        except ValueError as e:
            self.resultado_caja_op.delete('0.0','end')
            self.resultado_caja_op.insert('0.0', f'Error: {e}')
        except Exception as e:
            self.resultado_caja_op.delete('0.0','end')
            self.resultado_caja_op.insert('0.0', f'Error inesperado al calcular: {e}')

    def calcular_propiedad_matricial(self):
        """Calcula propiedades de matrices."""
        try:
            from Complement import (
                pasos_determinante, independenciaVectores
            )
        except ImportError:
            self.resultado_caja_prop.delete('0.0', 'end')
            self.resultado_caja_prop.insert('0.0', "ERROR: No se pudo cargar Complement.py")
            return

        try:
            A = self._leer_entradas_de_cuadricula(self.entradas_a_prop)
                 
        except ValueError as e:
            self.resultado_caja_prop.delete('0.0', 'end')
            self.resultado_caja_prop.insert('0.0', f'Error de entrada: {e}')
            self.pasos_caja_prop.delete('0.0', 'end')
            return
        except Exception as e:
            self.resultado_caja_prop.delete('0.0', 'end')
            self.resultado_caja_prop.insert('0.0', f'Error inesperado al leer matriz: {e}')
            self.pasos_caja_prop.delete('0.0', 'end')
            return

        propiedad = self.propiedad_matricial_var.get()
        
        self.pasos_caja_prop.delete('0.0','end')
        try:
            if propiedad == 'Determinante':
                if len(A) != len(A[0]):
                    raise ValueError("El determinante solo existe para matrices cuadradas")
                
                res = pasos_determinante(A) 
                if res['estado'] == 'exito':
                    self.pasos_caja_prop.delete('0.0', 'end')
                    self.pasos_caja_prop.insert('0.0', '\n'.join(res['pasos']))
                    self.resultado_caja_prop.delete('0.0', 'end')
                    self.resultado_caja_prop.insert('0.0', f"El determinante es: {_fmt(res['determinante'])}")
                else:
                    self.resultado_caja_prop.delete('0.0', 'end')
                    self.resultado_caja_prop.insert('0.0', f"Error: {res['mensaje']}")

            elif propiedad == 'Independencia Lineal':
                ver = independenciaVectores(A)
                
                if ver.get('num_vectors',0)==0: 
                    self.resultado_caja_prop.delete('0.0', 'end')
                    self.resultado_caja_prop.insert('0.0', 'No hay vectores (matriz vacía)')
                else:
                    r,k = ver.get('rank'), ver.get('num_vectors')
                    self.resultado_caja_prop.delete('0.0', 'end')
                    self.resultado_caja_prop.insert('0.0', f"Rango = {r} / {k} vectores\n" + 
                                                  ('Linealmente Independiente' if ver.get('independent') else 'Linealmente Dependiente'))

            elif propiedad == 'Rango':
                # Usar independenciaVectores para calcular el rango
                ver = independenciaVectores(A)
                rango = ver.get('rank', 0)
                self.resultado_caja_prop.delete('0.0', 'end')
                self.resultado_caja_prop.insert('0.0', f"El rango de la matriz es: {rango}")

        except ValueError as e:
            self.resultado_caja_prop.delete('0.0','end')
            self.resultado_caja_prop.insert('0.0', f'Error: {e}')
        except Exception as e:
            self.resultado_caja_prop.delete('0.0','end')
            self.resultado_caja_prop.insert('0.0', f'Error inesperado al calcular: {e}')

    def cargar_ejemplo_biseccion(self, ej_num: int):
        """Carga ejemplos para métodos numéricos."""
        self.limpiar_numerico()
        
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
        elif ej_num == 3:
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

    def calcular_operacion_numerica(self):
        """Calcula métodos numéricos."""
        try:
            from MetodosNumericos import metodo_biseccion
        except ImportError:
            self.resultado_caja_num.delete('0.0', 'end')
            self.resultado_caja_num.insert('0.0', "ERROR: No se pudo cargar MetodosNumericos.py.")
            return

        metodo = self.metodo_numerico_var.get()
        
        if metodo == 'Bisección':
            try:
                funcion_str = self.ent_funcion_fx.get()
                a_str = self.ent_intervalo_a.get()
                b_str = self.ent_intervalo_b.get()
                tol_str = self.ent_tolerancia_e.get()
                
                if not funcion_str or not a_str or not b_str or not tol_str:
                    raise ValueError("Todos los campos son obligatorios.")
                
                a = _parse_valor(a_str)
                b = _parse_valor(b_str)
                tolerancia = _parse_valor(tol_str)
                
                if tolerancia <= 0:
                    raise ValueError("La tolerancia debe ser un número positivo.")
                if a >= b:
                    raise ValueError("El intervalo es inválido (a debe ser menor que b).")

                res = metodo_biseccion(funcion_str, a, b, tolerancia)
                
                self.pasos_caja_num.delete('0.0', 'end')
                self.pasos_caja_num.insert('0.0', '\n'.join(res.get('pasos', ['No se generaron pasos.'])))
                
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
                else:
                    self.resultado_caja_num.insert('0.0', f"Error:\n{res['mensaje']}")

            except ValueError as e:
                self.pasos_caja_num.delete('0.0', 'end')
                self.resultado_caja_num.delete('0.0', 'end')
                self.resultado_caja_num.insert('0.0', f"Error de entrada:\n{e}")
            except Exception as e:
                self.pasos_caja_num.delete('0.0', 'end')
                self.resultado_caja_num.delete('0.0', 'end')
                self.resultado_caja_num.insert('0.0', f"Error inesperado en el cálculo:\n{e}")

    def graficar_funcion_interna(self):
        """Grafica función usando sympy."""
        try:
            funcion_str = self.ent_funcion_fx.get()
            if not funcion_str:
                raise ValueError("El campo de la función está vacío.")

            a_str = self.ent_intervalo_a.get()
            b_str = self.ent_intervalo_b.get()
            
            a = -10 if not a_str else _parse_valor(a_str)
            b = 10 if not b_str else _parse_valor(b_str)
            
            if a >= b:
                raise ValueError("El intervalo es inválido (a debe ser menor que b).")

            ventana_grafica = ctk.CTkToplevel(self)
            ventana_grafica.title(f"Gráfica de f(x) = {funcion_str}")
            ventana_grafica.geometry("1000x700")
            ventana_grafica.transient(self)
            ventana_grafica.grab_set()

            ventana_grafica.grid_rowconfigure(0, weight=1)
            ventana_grafica.grid_columnconfigure(0, weight=1)

            fig = Figure(figsize=(10, 8), dpi=100)
            ax = fig.add_subplot(111)

            try:
                x_sym = sp.Symbol('x')
                funcion_sympy = sp.sympify(funcion_str.replace('^', '**'))
                funcion_lambdified = sp.lambdify(x_sym, funcion_sympy, modules=['numpy', 'math'])
                
                x = np.linspace(a, b, 2000)
                y = funcion_lambdified(x)
                
                ax.plot(x, y, 'b-', linewidth=2.5, label=f'f(x) = {funcion_str}', alpha=0.8)
                ax.axhline(y=0, color='black', linewidth=1.5, alpha=0.7)
                ax.axvline(x=0, color='black', linewidth=1.5, alpha=0.7)
                ax.axvline(x=a, color='red', linestyle='--', alpha=0.6, linewidth=1, label=f'a = {a}')
                ax.axvline(x=b, color='green', linestyle='--', alpha=0.6, linewidth=1, label=f'b = {b}')
                ax.axvspan(a, b, alpha=0.1, color='gray', label='Intervalo de búsqueda')
                ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
                ax.set_axisbelow(True)
                ax.set_xlabel('x', fontsize=12, fontweight='bold')
                ax.set_ylabel('f(x)', fontsize=12, fontweight='bold')
                ax.set_title(f'Gráfica de f(x) = {funcion_str}\nIntervalo: [{a}, {b}]', 
                           fontsize=14, fontweight='bold', pad=20)
                ax.tick_params(axis='both', which='major', labelsize=10)
                
                y_min, y_max = np.nanmin(y), np.nanmax(y)
                y_range = y_max - y_min if y_max != y_min else 2
                ax.set_ylim(y_min - 0.1*y_range, y_max + 0.1*y_range)
                ax.legend(loc='best', fontsize=10, framealpha=0.9, shadow=True)
                
                if hasattr(self, 'resultado_caja_num'):
                    contenido = self.resultado_caja_num.get('1.0', 'end-1c')
                    if 'Raíz encontrada' in contenido:
                        lineas = contenido.split('\n')
                        for linea in lineas:
                            if 'Raíz encontrada' in contenido:
                                try:
                                    for line in lineas:
                                        if 'Raíz encontrada' in line:
                                            raiz_str = line.split(':')[1].strip()
                                            raiz = float(raiz_str)
                                            f_raiz = float(funcion_sympy.subs(x_sym, raiz))
                                            ax.plot(raiz, f_raiz, 'ro', markersize=10, 
                                                   label=f'Raíz ≈ {raiz:.6f}', zorder=5)
                                            ax.plot([raiz, raiz], [0, f_raiz], 'r--', alpha=0.7, linewidth=1)
                                            ax.annotate(f'x ≈ {raiz:.6f}', 
                                                       xy=(raiz, f_raiz), 
                                                       xytext=(10, 20), 
                                                       textcoords='offset points',
                                                       fontsize=10,
                                                       bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
                                                       arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0"))
                                            ax.legend(loc='best', fontsize=9)
                                            break
                                except:
                                    pass

            except Exception as e:
                ax.text(0.5, 0.5, f'Error al graficar la función:\n\n{str(e)}', 
                       horizontalalignment='center', verticalalignment='center',
                       transform=ax.transAxes, fontsize=12, color='red',
                       bbox=dict(boxstyle="round,pad=1", facecolor="lightcoral", alpha=0.8))
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
                ax.set_title('Error en la gráfica', fontsize=14, fontweight='bold', color='red')

            canvas = FigureCanvasTkAgg(fig, ventana_grafica)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

            marco_controles = ctk.CTkFrame(ventana_grafica)
            marco_controles.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
            
            def guardar_imagen():
                from tkinter import filedialog
                archivo = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("All files", "*.*")],
                    title="Guardar gráfica como..."
                )
                if archivo:
                    try:
                        fig.savefig(archivo, dpi=300, bbox_inches='tight', facecolor='white')
                        self.resultado_caja_num.insert('0.0', f"\nGràfica guardada en: {archivo}")
                    except Exception as e:
                        self.resultado_caja_num.insert('0.0', f"\nError al guardar: {e}")

            ctk.CTkButton(marco_controles, text="Guardar Imagen", 
                         command=guardar_imagen,
                         fg_color=COLOR_BOTON_SECUNDARIO, 
                         hover_color=COLOR_BOTON_SECUNDARIO_HOVER).pack(side="left", padx=5)
            
            ctk.CTkButton(marco_controles, text="Cerrar", 
                         command=ventana_grafica.destroy,
                         fg_color=COLOR_ACENTO, hover_color=COLOR_HOVER).pack(side="right", padx=5)

        except ValueError as e:
            self.resultado_caja_num.delete('0.0', 'end')
            self.resultado_caja_num.insert('0.0', f"Error para graficar: {e}")
        except Exception as e:
            self.resultado_caja_num.delete('0.0', 'end')
            self.resultado_caja_num.insert('0.0', f"Error inesperado al crear la gráfica:\n{e}")

    def limpiar_matrices(self):
        """Limpia matrices de sistemas de ecuaciones."""
        for fila_entradas in self.entradas_a:
            for entrada in fila_entradas:
                if entrada: entrada.delete(0,'end')
        for fila_entradas in self.entradas_b:
            for entrada in fila_entradas:
                if entrada: entrada.delete(0,'end')
        
        self.resultado_caja.delete('0.0','end')
        self.pasos_caja.delete('0.0','end')
        self.caja_ecuaciones.delete('1.0', 'end')
        self.caja_ecuaciones.insert("0.0", "2x + 3y - z = 5\nx - y + 2z = 10\n3x + 2y = 0")

    def limpiar_operaciones(self):
        """Limpia operaciones matriciales."""
        for fila_entradas in self.entradas_a_op:
            for entrada in fila_entradas:
                if entrada: entrada.delete(0,'end')
        for fila_entradas in self.entradas_b_op:
            for entrada in fila_entradas:
                if entrada: entrada.delete(0,'end')
        
        self.resultado_caja_op.delete('0.0','end')
        self.pasos_caja_op.delete('0.0','end')
        self.ent_coef_a_op.delete(0, 'end')
        self.ent_coef_a_op.insert(0, "1")
        self.ent_coef_b_op.delete(0, 'end')
        self.ent_coef_b_op.insert(0, "1")

    def limpiar_propiedades(self):
        """Limpia propiedades de matrices."""
        for fila_entradas in self.entradas_a_prop:
            for entrada in fila_entradas:
                if entrada: entrada.delete(0,'end')
        
        self.resultado_caja_prop.delete('0.0','end')
        self.pasos_caja_prop.delete('0.0','end')

    def limpiar_numerico(self):
        """Limpia métodos numéricos."""
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

    def actualizar_fecha_hora(self):
        """Actualiza fecha y hora."""
        self.etiqueta_fecha_hora.configure(text=datetime.now().strftime("%A, %d %B %Y | %H:%M:%S"))
        self.after(1000, self.actualizar_fecha_hora)

# --- Punto de Entrada ---
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = AplicacionPrincipal()
    app.mainloop()