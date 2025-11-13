import customtkinter as ctk
from paginas.pagina_base import PaginaBase
from app_config import COLOR_TARJETA, COLOR_TEXTO_TARJETA, COLOR_ALGEBRA, COLOR_NUMERICOS, COLOR_HOVER

class PaginaInicio(PaginaBase):
    def crear_widgets(self):
        self.configurar_grid()
        self.crear_interfaz()
    
    def configurar_grid(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def crear_interfaz(self):
        # Espacio superior
        ctk.CTkLabel(self, text="").grid(row=0, column=0)
        
        # Marco principal de bienvenida
        marco_bienvenida = ctk.CTkFrame(self, corner_radius=12)
        marco_bienvenida.grid(row=1, column=0, sticky="nsew", padx=50, pady=20)
        marco_bienvenida.grid_columnconfigure(0, weight=1)
        
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
        self.crear_tarjeta_algebra(marco_tarjetas)
        
        # Tarjeta Métodos Numéricos
        self.crear_tarjeta_numericos(marco_tarjetas)
        
        # Espacio inferior
        ctk.CTkLabel(self, text="").grid(row=2, column=0)
    
    def crear_tarjeta_algebra(self, parent):
        tarjeta_algebra = ctk.CTkFrame(parent, corner_radius=12, 
                                     fg_color=COLOR_TARJETA, 
                                     border_width=2,
                                     border_color=COLOR_ALGEBRA[1] if ctk.get_appearance_mode() == "Dark" else COLOR_ALGEBRA[0])
        tarjeta_algebra.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        tarjeta_algebra.grid_columnconfigure(0, weight=1)
        
        # Contenido de la tarjeta álgebra
        ctk.CTkLabel(tarjeta_algebra, text="📐", 
                    font=ctk.CTkFont(size=40)).grid(row=0, column=0, pady=(20, 10))
        
        ctk.CTkLabel(tarjeta_algebra, text="Algebra Lineal", 
                    font=ctk.CTkFont(size=20, weight="bold"),
                    text_color=COLOR_TEXTO_TARJETA).grid(row=1, column=0, pady=(0, 10))
        
        desc_algebra = "Sistemas de ecuaciones\nOperaciones matriciales\nDeterminantes\nValores y vectores propios"
        ctk.CTkLabel(tarjeta_algebra, text=desc_algebra,
                    font=ctk.CTkFont(size=12),
                    text_color=COLOR_TEXTO_TARJETA,
                    justify="center").grid(row=2, column=0, pady=(0, 20))
        
        btn_algebra = ctk.CTkButton(tarjeta_algebra, text="Explorar Algebra Lineal",
                                  fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER,
                                  command=lambda: self.app.mostrar_pagina("sistemas_ecuaciones"))
        btn_algebra.grid(row=3, column=0, sticky="s", padx=20, pady=20)
    
    def crear_tarjeta_numericos(self, parent):
        tarjeta_numericos = ctk.CTkFrame(parent, corner_radius=12,
                                       fg_color=COLOR_TARJETA,
                                       border_width=2,
                                       border_color=COLOR_NUMERICOS[1] if ctk.get_appearance_mode() == "Dark" else COLOR_NUMERICOS[0])
        tarjeta_numericos.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        tarjeta_numericos.grid_columnconfigure(0, weight=1)
        
        # Contenido de la tarjeta numéricos
        ctk.CTkLabel(tarjeta_numericos, text="🔢", 
                    font=ctk.CTkFont(size=40)).grid(row=0, column=0, pady=(20, 10))
        
        ctk.CTkLabel(tarjeta_numericos, text="Metodos Numericos", 
                    font=ctk.CTkFont(size=20, weight="bold"),
                    text_color=COLOR_TEXTO_TARJETA).grid(row=1, column=0, pady=(0, 10))
        
        desc_numericos = "Ecuaciones no lineales\nInterpolacion\nDiferenciacion numerica\nEcuaciones diferenciales"
        ctk.CTkLabel(tarjeta_numericos, text=desc_numericos,
                    font=ctk.CTkFont(size=12),
                    text_color=COLOR_TEXTO_TARJETA,
                    justify="center").grid(row=2, column=0, pady=(0, 20))
        
        btn_numericos = ctk.CTkButton(tarjeta_numericos, text="Explorar Metodos Numericos",
                                    fg_color=COLOR_NUMERICOS, hover_color=COLOR_HOVER,
                                    command=lambda: self.app.mostrar_pagina("metodos_numericos"))
        btn_numericos.grid(row=3, column=0, sticky="s", padx=20, pady=20)