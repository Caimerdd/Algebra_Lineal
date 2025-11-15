import customtkinter as ctk
<<<<<<< HEAD
# --- IMPORTACIONES MODIFICADAS ---
from app_config import (COLOR_BOTON_SECUNDARIO, COLOR_BOTON_SECUNDARIO_HOVER, 
                        COLOR_ACENTO, COLOR_HOVER, COLOR_ALGEBRA, COLOR_NUMERICOS,
                        COLOR_FUNDAMENTOS, COLOR_DIFERENCIAL, COLOR_INTEGRAL)
# ---------------------------------
=======
# Eliminados imports: os, webbrowser, pathlib, tkinter.messagebox

from app_config import (
    COLOR_BOTON_SECUNDARIO,
    COLOR_BOTON_SECUNDARIO_HOVER,
    COLOR_ACENTO,
    COLOR_HOVER,
    COLOR_ALGEBRA,
    COLOR_NUMERICOS,
)
>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97
from paginas.pagina_inicio import PaginaInicio
from paginas.pagina_sistemas_ecuaciones import PaginaSistemasEcuaciones
from paginas.pagina_operaciones_matriciales import PaginaOperacionesMatriciales
from paginas.pagina_propiedades_matrices import PaginaPropiedadesMatrices
from paginas.pagina_metodos_numericos import PaginaMetodosNumericos
from paginas.pagina_calculo import PaginaCalculo          # <<--- Cálculo
from ui_components.ventana_ayuda import VentanaAyudaSymPy

<<<<<<< HEAD
# --- IMPORTACIONES NUEVAS ---
from paginas.pagina_fundamentos import PaginaFundamentos
from paginas.pagina_diferencial import PaginaDiferencial
from paginas.pagina_integral import PaginaIntegral
# ----------------------------
=======
>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97

class AplicacionPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MathPro - Herramientas Matematicas Avanzadas")
        self.geometry("1200x800")
        self.minsize(1000, 700)
<<<<<<< HEAD
        
        self.menu_visible = False 
=======

        # --- VARIABLES DE ESTADO --
        self.menu_visible = False
>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97
        self.ancho_menu = 280

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.pantalla_actual = "inicio"

        self.crear_panel_nav()
        self.crear_panel_principal()
        self.inicializar_paginas()
        self.mostrar_pagina("inicio")

    def inicializar_paginas(self):
        self.paginas = {}
        
        self.paginas["inicio"] = PaginaInicio(self.area_contenido, self)
        self.paginas["sistemas_ecuaciones"] = PaginaSistemasEcuaciones(self.area_contenido, self)
        self.paginas["operaciones_matriciales"] = PaginaOperacionesMatriciales(self.area_contenido, self)
        self.paginas["propiedades_matrices"] = PaginaPropiedadesMatrices(self.area_contenido, self)
        self.paginas["metodos_numericos"] = PaginaMetodosNumericos(self.area_contenido, self)
<<<<<<< HEAD
        
        # --- NUEVAS PÁGINAS INICIALIZADAS ---
        self.paginas["fundamentos"] = PaginaFundamentos(self.area_contenido, self)
        self.paginas["diferencial"] = PaginaDiferencial(self.area_contenido, self)
        self.paginas["integral"] = PaginaIntegral(self.area_contenido, self)
        # -------------------------------------
        
=======
        self.paginas["calculo"] = PaginaCalculo(self.area_contenido, self)   # <<--- nueva página

>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97
        for pagina in self.paginas.values():
            pagina.grid_remove()

    def mostrar_pagina(self, nombre_pagina):
        if self.pantalla_actual in self.paginas:
            self.paginas[self.pantalla_actual].grid_remove()

        self.pantalla_actual = nombre_pagina
        pagina = self.paginas[nombre_pagina]
        pagina.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        if hasattr(pagina, "mostrar"):
            pagina.mostrar()

        if nombre_pagina == "inicio":
            self.btn_inicio.grid_remove()
        else:
            self.btn_inicio.grid()

    def crear_panel_nav(self):
        self.marco_nav = ctk.CTkFrame(self, width=0, corner_radius=0)
        self.marco_nav.grid(row=0, column=0, sticky="nswe")
        self.marco_nav.grid_propagate(False)
<<<<<<< HEAD
        
        # --- CONFIGURACIÓN DE FILAS MODIFICADA ---
        # Aumentamos los números de fila para dar espacio a los nuevos botones
        self.marco_nav.grid_rowconfigure(15, weight=1)  # Espaciador
        self.marco_nav.grid_rowconfigure(16, weight=0) # Configuración
=======

        # Estructura de filas:
        # 0: Título
        # 1: Botón inicio
        # 2: Separador
        # 3: Label Álgebra
        # 4-6: Botones Álgebra
        # 7: Label Métodos Numéricos
        # 8: Botón Métodos Numéricos
        # 9: Label Cálculo
        # 10: Botón Cálculo
        # 11: Espaciador
        # 12: Config inferior
        self.marco_nav.grid_rowconfigure(11, weight=1)   # Espaciador flexible
        self.marco_nav.grid_rowconfigure(12, weight=0)   # Config
>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97
        self.marco_nav.grid_columnconfigure(0, weight=1)

        # -- Contenido del Menú --
        ctk.CTkLabel(
            self.marco_nav,
            text="MathPro",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(25, 15), sticky="w")

        self.btn_inicio = ctk.CTkButton(
            self.marco_nav,
            text="🏠 Regresar al Inicio",
            anchor="w",
            fg_color=COLOR_BOTON_SECUNDARIO,
            hover_color=COLOR_BOTON_SECUNDARIO_HOVER,
            command=lambda: self.mostrar_pagina("inicio")
        )
        self.btn_inicio.grid(row=1, column=0, sticky="ew", padx=12, pady=5)
        self.btn_inicio.grid_remove()

        ctk.CTkFrame(self.marco_nav, height=2).grid(row=2, column=0, sticky="ew", padx=10, pady=5)
<<<<<<< HEAD
        
        # Algebra (Filas 3-6)
        ctk.CTkLabel(self.marco_nav, text="ÁLGEBRA LINEAL", 
                    font=ctk.CTkFont(size=12, weight="bold"), 
                    text_color=COLOR_ALGEBRA).grid(row=3, column=0, sticky="w", padx=15, pady=(10, 5))
        
        ctk.CTkButton(self.marco_nav, text="   Sistemas de Ecuaciones", anchor="w",
                      fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER,
                      command=lambda: self.mostrar_pagina("sistemas_ecuaciones")).grid(row=4, column=0, sticky="ew", padx=12, pady=3)
        
        ctk.CTkButton(self.marco_nav, text="   Operaciones Matriciales", anchor="w",
                      fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER,
                      command=lambda: self.mostrar_pagina("operaciones_matriciales")).grid(row=5, column=0, sticky="ew", padx=12, pady=3)
        
        ctk.CTkButton(self.marco_nav, text="   Propiedades de Matrices", anchor="w",
                      fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER,
                      command=lambda: self.mostrar_pagina("propiedades_matrices")).grid(row=6, column=0, sticky="ew", padx=12, pady=3)
        
        # Numericos (Filas 7-8)
        ctk.CTkLabel(self.marco_nav, text="MÉTODOS NUMÉRICOS", 
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=COLOR_NUMERICOS).grid(row=7, column=0, sticky="w", padx=15, pady=(15, 5))
        
        ctk.CTkButton(self.marco_nav, text="   Ecuaciones No Lineales", anchor="w",
                      fg_color=COLOR_NUMERICOS, hover_color=COLOR_HOVER,
                      command=lambda: self.mostrar_pagina("metodos_numericos")).grid(row=8, column=0, sticky="ew", padx=12, pady=3)

        # --- SECCIÓN FUNDAMENTOS (Filas 9-10) ---
        ctk.CTkLabel(self.marco_nav, text="FUNDAMENTOS DE ÁLGEBRA", 
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=COLOR_FUNDAMENTOS).grid(row=9, column=0, sticky="w", padx=15, pady=(15, 5))
        ctk.CTkButton(self.marco_nav, text="   Funciones y Polinomios", anchor="w",
                      fg_color=COLOR_FUNDAMENTOS, hover_color=COLOR_HOVER,
                      command=lambda: self.mostrar_pagina("fundamentos")).grid(row=10, column=0, sticky="ew", padx=12, pady=3)

        # --- SECCIÓN CÁLCULO DIFERENCIAL (Filas 11-12) ---
        ctk.CTkLabel(self.marco_nav, text="CÁLCULO DIFERENCIAL", 
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=COLOR_DIFERENCIAL).grid(row=11, column=0, sticky="w", padx=15, pady=(15, 5))
        ctk.CTkButton(self.marco_nav, text="   Límites y Derivadas", anchor="w",
                      fg_color=COLOR_DIFERENCIAL, hover_color=COLOR_HOVER,
                      command=lambda: self.mostrar_pagina("diferencial")).grid(row=12, column=0, sticky="ew", padx=12, pady=3)

        # --- SECCIÓN CÁLCULO INTEGRAL (Filas 13-14) ---
        ctk.CTkLabel(self.marco_nav, text="CÁLCULO INTEGRAL", 
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=COLOR_INTEGRAL).grid(row=13, column=0, sticky="w", padx=15, pady=(15, 5))
        ctk.CTkButton(self.marco_nav, text="   Integrales y Series", anchor="w",
                      fg_color=COLOR_INTEGRAL, hover_color=COLOR_HOVER,
                      command=lambda: self.mostrar_pagina("integral")).grid(row=14, column=0, sticky="ew", padx=12, pady=3)

        # --- ESPACIADOR (Fila 15) ---
        ctk.CTkFrame(self.marco_nav, fg_color="transparent").grid(row=15, column=0, sticky="nsew")

        # --- CONFIGURACIÓN INFERIOR (Fila 16) ---
        marco_config = ctk.CTkFrame(self.marco_nav, fg_color="transparent")
        marco_config.grid(row=16, column=0, sticky="ews", padx=12, pady=20)
        
        self.btn_ayuda = ctk.CTkButton(marco_config, text="📚 Ayuda",
                                     command=self.mostrar_ayuda_sympy,
                                     width=80,
                                     fg_color=COLOR_BOTON_SECUNDARIO,
                                     hover_color=COLOR_BOTON_SECUNDARIO_HOVER)
=======

        # ALGEBRA LINEAL
        ctk.CTkLabel(
            self.marco_nav,
            text="ALGEBRA LINEAL",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLOR_ALGEBRA
        ).grid(row=3, column=0, sticky="w", padx=15, pady=(10, 5))

        ctk.CTkButton(
            self.marco_nav,
            text="   Sistemas de Ecuaciones",
            anchor="w",
            fg_color=COLOR_ALGEBRA,
            hover_color=COLOR_HOVER,
            command=lambda: self.mostrar_pagina("sistemas_ecuaciones")
        ).grid(row=4, column=0, sticky="ew", padx=12, pady=3)

        ctk.CTkButton(
            self.marco_nav,
            text="   Operaciones Matriciales",
            anchor="w",
            fg_color=COLOR_ALGEBRA,
            hover_color=COLOR_HOVER,
            command=lambda: self.mostrar_pagina("operaciones_matriciales")
        ).grid(row=5, column=0, sticky="ew", padx=12, pady=3)

        ctk.CTkButton(
            self.marco_nav,
            text="   Propiedades de Matrices",
            anchor="w",
            fg_color=COLOR_ALGEBRA,
            hover_color=COLOR_HOVER,
            command=lambda: self.mostrar_pagina("propiedades_matrices")
        ).grid(row=6, column=0, sticky="ew", padx=12, pady=3)

        # METODOS NUMERICOS
        ctk.CTkLabel(
            self.marco_nav,
            text="METODOS NUMERICOS",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLOR_NUMERICOS
        ).grid(row=7, column=0, sticky="w", padx=15, pady=(15, 5))

        ctk.CTkButton(
            self.marco_nav,
            text="   Ecuaciones No Lineales",
            anchor="w",
            fg_color=COLOR_NUMERICOS,
            hover_color=COLOR_HOVER,
            command=lambda: self.mostrar_pagina("metodos_numericos")
        ).grid(row=8, column=0, sticky="ew", padx=12, pady=3)

        # CALCULO (sección propia)
        ctk.CTkLabel(
            self.marco_nav,
            text="CALCULO",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLOR_NUMERICOS  # puedes cambiar a otro color si luego creas COLOR_CALCULO
        ).grid(row=9, column=0, sticky="w", padx=15, pady=(15, 5))

        ctk.CTkButton(
            self.marco_nav,
            text="   Cálculo (Derivadas / Integrales)",
            anchor="w",
            fg_color=COLOR_NUMERICOS,
            hover_color=COLOR_HOVER,
            command=lambda: self.mostrar_pagina("calculo")
        ).grid(row=10, column=0, sticky="ew", padx=12, pady=3)

        # ESPACIADOR
        ctk.CTkFrame(self.marco_nav, fg_color="transparent").grid(row=11, column=0, sticky="nsew")

        # CONFIG INFERIOR
        marco_config = ctk.CTkFrame(self.marco_nav, fg_color="transparent")
        marco_config.grid(row=12, column=0, sticky="ews", padx=12, pady=20)

        self.btn_ayuda = ctk.CTkButton(
            marco_config,
            text="📚 Ayuda",
            command=self.mostrar_ayuda_sympy,
            width=80,
            fg_color=COLOR_BOTON_SECUNDARIO,
            hover_color=COLOR_BOTON_SECUNDARIO_HOVER
        )
>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97
        self.btn_ayuda.pack(side="left", padx=(0, 5))

        self.theme_switch = ctk.CTkSwitch(
            marco_config,
            text="Oscuro",
            command=self.toggle_theme,
            width=80,
            progress_color=COLOR_ACENTO
        )
        self.theme_switch.pack(side="right")

        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()

    def crear_panel_principal(self):
        self.marco_derecho = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.marco_derecho.grid(row=0, column=1, sticky="nswe", padx=0, pady=0)
        self.marco_derecho.grid_rowconfigure(1, weight=1)
        self.marco_derecho.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkFrame(self.marco_derecho, height=50, corner_radius=0, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
<<<<<<< HEAD
        
        self.btn_menu = ctk.CTkButton(self.header, text="☰", width=40, height=40,
                                    font=ctk.CTkFont(size=20),
                                    fg_color="transparent",
                                    text_color=("black", "white"),
                                    hover_color=("gray80", "gray30"),
                                    command=self.toggle_menu)
=======

        # Botón Menú
        self.btn_menu = ctk.CTkButton(
            self.header,
            text="☰",
            width=40,
            height=40,
            font=ctk.CTkFont(size=20),
            fg_color="transparent",
            text_color=("black", "white"),
            hover_color=("gray80", "gray30"),
            command=self.toggle_menu
        )
>>>>>>> 4404025c4e63a591ca2cda39423ab241357cbc97
        self.btn_menu.pack(side="left", padx=10, pady=5)

        self.area_contenido = ctk.CTkFrame(self.marco_derecho, corner_radius=0)
        self.area_contenido.grid(row=1, column=0, sticky="nswe", padx=0, pady=0)
        self.area_contenido.grid_rowconfigure(0, weight=1)
        self.area_contenido.grid_columnconfigure(0, weight=1)

        self.marco_principal = self.area_contenido

    def toggle_menu(self):
        if self.menu_visible:
            self.marco_nav.configure(width=0)
            self.menu_visible = False
        else:
            self.marco_nav.configure(width=self.ancho_menu)
            self.menu_visible = True

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def mostrar_ayuda_sympy(self):
        VentanaAyudaSymPy(self)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = AplicacionPrincipal()
    app.mainloop()
