import customtkinter as ctk
from app_config import COLOR_FONDO_SECUNDARIO, COLOR_ALGEBRA

class VentanaAyudaSymPy(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ayuda SymPy - Sintaxis Matematica")
        self.geometry("700x600")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()
        
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
        self.crear_contenido_ayuda(scrollable_frame)
        
        # Configurar eventos
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        scrollable_frame.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        
    def crear_contenido_ayuda(self, parent):
        # Título
        titulo = ctk.CTkLabel(parent, text="Sintaxis Matematica - SymPy", 
                             font=ctk.CTkFont(size=18, weight="bold"))
        titulo.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))
        
        categorias = [
            {
                "titulo": "Operaciones Basicas",
                "items": [
                    ("Suma/Resta", "x + y, x - y"),
                    ("Multiplicacion", "x * y  o  x y  (con espacio)"),
                    ("Division", "x / y"),
                    ("Exponentes", "x**2  o  x^2"),
                    ("Raiz cuadrada", "sqrt(x)"),
                    ("Raiz n-esima", "root(x, n)"),
                    ("Modulo/Resto", "x % y")
                ]
            },
            {
                "titulo": "Funciones Trigonometricas",
                "items": [
                    ("Seno", "sin(x)"),
                    ("Coseno", "cos(x)"),
                    ("Tangente", "tan(x)"),
                    ("Arcoseno", "asin(x)"),
                    ("Arcocoseno", "acos(x)"),
                    ("Arcotangente", "atan(x)"),
                    ("Seno hiperbolico", "sinh(x)"),
                    ("Coseno hiperbolico", "cosh(x)")
                ]
            },
            {
                "titulo": "Logaritmos y Exponenciales",
                "items": [
                    ("Logaritmo natural", "log(x)  o  ln(x)"),
                    ("Logaritmo base 10", "log10(x)"),
                    ("Logaritmo base b", "log(x, b)"),
                    ("Exponencial", "exp(x)  o  E**x"),
                    ("Logaritmo de 5x", "log(5*x)"),
                    ("Exponencial compleja", "exp(2*x + 1)")
                ]
            }
        ]
        
        row = 1
        for categoria in categorias:
            # Marco de categoria
            marco_categoria = ctk.CTkFrame(parent, fg_color=COLOR_FONDO_SECUNDARIO)
            marco_categoria.grid(row=row, column=0, sticky="ew", padx=20, pady=10)
            marco_categoria.grid_columnconfigure(0, weight=1)
            
            # Titulo de categoria
            lbl_titulo = ctk.CTkLabel(marco_categoria, text=categoria["titulo"],
                                     font=ctk.CTkFont(size=14, weight="bold"))
            lbl_titulo.grid(row=0, column=0, sticky="w", padx=15, pady=8)
            
            row += 1
            
            # Items de la categoria
            for i, (nombre, sintaxis) in enumerate(categoria["items"]):
                marco_item = ctk.CTkFrame(parent)
                marco_item.grid(row=row, column=0, sticky="ew", padx=30, pady=2)
                marco_item.grid_columnconfigure(1, weight=1)
                
                lbl_nombre = ctk.CTkLabel(marco_item, text=nombre, width=150,
                                         font=ctk.CTkFont(size=12))
                lbl_nombre.grid(row=0, column=0, sticky="w", padx=10, pady=5)
                
                lbl_sintaxis = ctk.CTkLabel(marco_item, text=sintaxis,
                                           font=ctk.CTkFont(family="monospace", size=12),
                                           text_color=COLOR_ALGEBRA)
                lbl_sintaxis.grid(row=0, column=1, sticky="w", padx=10, pady=5)
                
                row += 1
        
        # Nota final
        nota = ctk.CTkLabel(parent, 
                           text="💡 Tip: Usa parentesis para agrupar operaciones complejas\nEj: log(5*x) en lugar de log5*x",
                           font=ctk.CTkFont(size=12, slant="italic"),
                           text_color="gray70")
        nota.grid(row=row, column=0, sticky="w", padx=20, pady=20)