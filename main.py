import customtkinter as ctk
from app_config import COLOR_BOTON_SECUNDARIO, COLOR_BOTON_SECUNDARIO_HOVER, COLOR_ACENTO, COLOR_HOVER, COLOR_ALGEBRA, COLOR_NUMERICOS
from paginas.pagina_inicio import PaginaInicio
from paginas.pagina_sistemas_ecuaciones import PaginaSistemasEcuaciones
from paginas.pagina_operaciones_matriciales import PaginaOperacionesMatriciales
from paginas.pagina_propiedades_matrices import PaginaPropiedadesMatrices
from paginas.pagina_metodos_numericos import PaginaMetodosNumericos
from ui_components.ventana_ayuda import VentanaAyudaSymPy

class AplicacionPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("MathPro - Herramientas Matematicas Avanzadas")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        # Configurar grid principal para que ocupe toda la ventana
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.pantalla_actual = "inicio"
        
        self.crear_panel_nav()
        self.crear_panel_principal()
        self.inicializar_paginas()
        self.mostrar_pagina("inicio")

    def inicializar_paginas(self):
        self.paginas = {}
        
        self.paginas["inicio"] = PaginaInicio(self.marco_principal, self)
        self.paginas["sistemas_ecuaciones"] = PaginaSistemasEcuaciones(self.marco_principal, self)
        self.paginas["operaciones_matriciales"] = PaginaOperacionesMatriciales(self.marco_principal, self)
        self.paginas["propiedades_matrices"] = PaginaPropiedadesMatrices(self.marco_principal, self)
        self.paginas["metodos_numericos"] = PaginaMetodosNumericos(self.marco_principal, self)
        
        for pagina in self.paginas.values():
            pagina.grid_remove()

    def mostrar_pagina(self, nombre_pagina):
        if self.pantalla_actual in self.paginas:
            self.paginas[self.pantalla_actual].grid_remove()
        
        self.pantalla_actual = nombre_pagina
        pagina = self.paginas[nombre_pagina]
        pagina.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        pagina.mostrar()
        
        if nombre_pagina == "inicio":
            self.btn_inicio.grid_remove()
        else:
            self.btn_inicio.grid()

    def crear_panel_nav(self):
        self.marco_nav = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.marco_nav.grid(row=0, column=0, sticky="nswe")
        self.marco_nav.grid_rowconfigure(10, weight=1)
        
        # Título principal
        ctk.CTkLabel(self.marco_nav, text="MathPro", 
                    font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=12, pady=(15, 10), sticky="w")
        
        # Botón Regresar al Inicio
        self.btn_inicio = ctk.CTkButton(self.marco_nav, text="🏠 Regresar al Inicio", anchor="w",
                                      fg_color=COLOR_BOTON_SECUNDARIO, 
                                      hover_color=COLOR_BOTON_SECUNDARIO_HOVER,
                                      command=lambda: self.mostrar_pagina("inicio"))
        self.btn_inicio.grid(row=1, column=0, sticky="ew", padx=12, pady=5)
        self.btn_inicio.grid_remove()
        
        # Separador
        ctk.CTkFrame(self.marco_nav, height=2).grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        # Algebra Lineal
        ctk.CTkLabel(self.marco_nav, text="ALGEBRA LINEAL", 
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
        
        # Metodos Numericos
        ctk.CTkLabel(self.marco_nav, text="METODOS NUMERICOS", 
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=COLOR_NUMERICOS).grid(row=7, column=0, sticky="w", padx=15, pady=(15, 5))
        
        ctk.CTkButton(self.marco_nav, text="   Ecuaciones No Lineales", anchor="w",
                      fg_color=COLOR_NUMERICOS, hover_color=COLOR_HOVER,
                      command=lambda: self.mostrar_pagina("metodos_numericos")).grid(row=8, column=0, sticky="ew", padx=12, pady=3)

        # Espacio flexible
        ctk.CTkLabel(self.marco_nav, text="").grid(row=9, column=0, sticky="nswe")

        # Configuracion
        marco_config = ctk.CTkFrame(self.marco_nav, fg_color="transparent")
        marco_config.grid(row=10, column=0, sticky="ew", padx=12, pady=15)
        
        self.btn_ayuda = ctk.CTkButton(marco_config, text="📚 Ayuda SymPy",
                                     command=self.mostrar_ayuda_sympy,
                                     fg_color=COLOR_BOTON_SECUNDARIO,
                                     hover_color=COLOR_BOTON_SECUNDARIO_HOVER)
        self.btn_ayuda.pack(side="left", padx=(0, 10))
        
        self.theme_switch = ctk.CTkSwitch(marco_config, text="Modo Oscuro", command=self.toggle_theme,
                                          progress_color=COLOR_ACENTO)
        self.theme_switch.pack(side="right")
        
        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def mostrar_ayuda_sympy(self):
        VentanaAyudaSymPy(self)

    def crear_panel_principal(self):
        # Panel principal SIN padding para que ocupe todo el espacio
        self.marco_principal = ctk.CTkFrame(self, corner_radius=0)
        self.marco_principal.grid(row=0, column=1, sticky="nswe", padx=0, pady=0)
        self.marco_principal.grid_rowconfigure(0, weight=1)
        self.marco_principal.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = AplicacionPrincipal()
    app.mainloop()