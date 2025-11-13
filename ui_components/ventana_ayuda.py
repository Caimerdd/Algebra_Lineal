import customtkinter as ctk
from app_config import COLOR_FONDO_SECUNDARIO, COLOR_ALGEBRA

class VentanaAyudaSymPy(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ayuda SymPy - Sintaxis Matematica")
        self.geometry("700x600")
        self.resizable(True, True)
        
        # Hacemos que la ventana sea modal (bloquea la de atrás mientras está abierta)
        self.transient(parent)
        self.grab_set()
        
        # Configuramos el grid principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # --- CAMBIO PRINCIPAL: Usamos CTkScrollableFrame ---
        # Esto elimina el fondo blanco y simplifica el código (no hace falta canvas ni scrollbar manual)
        self.frame_scroll = ctk.CTkScrollableFrame(self, label_text="Guía de Referencia")
        self.frame_scroll.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.frame_scroll.grid_columnconfigure(0, weight=1)
        
        # Contenido de la ayuda
        self.crear_contenido_ayuda(self.frame_scroll)
        
    def crear_contenido_ayuda(self, parent):
        # Título dentro del scroll
        titulo = ctk.CTkLabel(parent, text="Sintaxis Matemática - SymPy", 
                             font=ctk.CTkFont(size=18, weight="bold"))
        titulo.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 20))
        
        # He agregado la categoría "Constantes y Otros" que faltaba
        categorias = [
            {
                "titulo": "Operaciones Básicas",
                "items": [
                    ("Suma/Resta", "x + y, x - y"),
                    ("Multiplicación", "x*y  o  x y (con espacio)"),
                    ("División", "x / y"),
                    ("Potencia/Exponente", "x**2  o  x^2"),
                    ("Raíz cuadrada", "sqrt(x)"),
                    ("Raíz n-ésima", "root(x, n)"),
                    ("Valor Absoluto", "abs(x)"), # Agregado
                    ("Módulo/Resto", "x % y")
                ]
            },
            {
                "titulo": "Constantes y Especiales", # Categoría Nueva Importante
                "items": [
                    ("Pi (π)", "pi"),
                    ("Número e (Euler)", "E  o  exp(1)"),
                    ("Infinito", "oo"),
                    ("Unidad Imaginaria", "I")
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
                    ("Arcotangente", "atan(x)"),
                    ("Seno hiperbólico", "sinh(x)"),
                    ("Coseno hiperbólico", "cosh(x)")
                ]
            },
            {
                "titulo": "Logaritmos y Exponenciales",
                "items": [
                    ("Logaritmo natural (ln)", "log(x)  o  ln(x)"),
                    ("Logaritmo base 10", "log(x, 10)"), # Corregido para sintaxis estándar SymPy
                    ("Logaritmo base b", "log(x, b)"),
                    ("Exponencial (e^x)", "exp(x)"),
                    ("Logaritmo de 5x", "log(5*x)"),
                ]
            }
        ]
        
        row = 1
        for categoria in categorias:
            # Marco de la categoría (Tarjeta)
            marco_categoria = ctk.CTkFrame(parent, fg_color=COLOR_FONDO_SECUNDARIO)
            marco_categoria.grid(row=row, column=0, sticky="ew", padx=10, pady=10)
            marco_categoria.grid_columnconfigure(0, weight=1)
            
            # Título de la categoría
            lbl_titulo = ctk.CTkLabel(marco_categoria, text=categoria["titulo"],
                                     font=ctk.CTkFont(size=14, weight="bold"))
            lbl_titulo.grid(row=0, column=0, sticky="w", padx=15, pady=8)
            
            row_item = 1
            # Items de la categoría
            for nombre, sintaxis in categoria["items"]:
                marco_item = ctk.CTkFrame(marco_categoria, fg_color="transparent")
                marco_item.grid(row=row_item, column=0, sticky="ew", padx=10, pady=2)
                marco_item.grid_columnconfigure(1, weight=1)
                
                # Nombre de la operación
                lbl_nombre = ctk.CTkLabel(marco_item, text=nombre, width=150, anchor="w",
                                         font=ctk.CTkFont(size=12))
                lbl_nombre.grid(row=0, column=0, sticky="w", padx=10, pady=5)
                
                # Código/Sintaxis
                lbl_sintaxis = ctk.CTkLabel(marco_item, text=sintaxis, anchor="w",
                                           font=ctk.CTkFont(family="monospace", size=12, weight="bold"),
                                           text_color=COLOR_ALGEBRA)
                lbl_sintaxis.grid(row=0, column=1, sticky="w", padx=10, pady=5)
                
                row_item += 1
            
            row += 1
        
        # Nota final
        nota = ctk.CTkLabel(parent, 
                           text="💡 Tip: SymPy es sensible a mayúsculas/minúsculas.\nUsa paréntesis para agrupar operaciones complejas.",
                           font=ctk.CTkFont(size=12, slant="italic"),
                           text_color="gray70")
        nota.grid(row=row, column=0, sticky="ew", padx=20, pady=20)