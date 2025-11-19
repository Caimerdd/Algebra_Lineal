import customtkinter as ctk
from paginas.pagina_base import PaginaBase
# --- IMPORTACIONES MODIFICADAS ---
from app_config import (COLOR_TARJETA, COLOR_TEXTO_TARJETA, 
                        COLOR_ALGEBRA, COLOR_NUMERICOS, COLOR_HOVER,
                        COLOR_FUNDAMENTOS, COLOR_DIFERENCIAL, COLOR_INTEGRAL)
# ---------------------------------

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
        ctk.CTkLabel(self, text="").grid(row=0, column=0)
        
        marco_bienvenida = ctk.CTkFrame(self, corner_radius=12)
        marco_bienvenida.grid(row=1, column=0, sticky="nsew", padx=50, pady=20)
        marco_bienvenida.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(marco_bienvenida, 
                    text="MathPro",
                    font=ctk.CTkFont(size=32, weight="bold")).grid(row=0, column=0, pady=(40, 10))
        
        ctk.CTkLabel(marco_bienvenida, 
                    text="Herramientas Matemáticas Avanzadas",
                    font=ctk.CTkFont(size=16),
                    text_color="gray70").grid(row=1, column=0, pady=(0, 40))
        
        # --- LAYOUT DE TARJETAS MODIFICADO (3 Columnas, 2 Filas) ---
        marco_tarjetas = ctk.CTkFrame(marco_bienvenida, fg_color="transparent")
        marco_tarjetas.grid(row=2, column=0, sticky="nsew", padx=40, pady=20)
        marco_tarjetas.grid_columnconfigure(0, weight=1)
        marco_tarjetas.grid_columnconfigure(1, weight=1)
        marco_tarjetas.grid_columnconfigure(2, weight=1) # Nueva columna
        marco_tarjetas.grid_rowconfigure(0, weight=1)
        marco_tarjetas.grid_rowconfigure(1, weight=1) # Nueva fila
        
        # --- Fila 1 ---
        self.crear_tarjeta(marco_tarjetas, 
                           titulo="Fundamentos de Álgebra", 
                           emoji="🧮",
                           descripcion="Polinomios, funciones\ny gráficas.\n(En construcción...)",
                           color=COLOR_FUNDAMENTOS,
                           pagina="fundamentos").grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.crear_tarjeta(marco_tarjetas, 
                           titulo="Cálculo Diferencial", 
                           emoji="📈",
                           descripcion="Límites, reglas de\nderivación y aplicaciones.\n(En construcción...)",
                           color=COLOR_DIFERENCIAL,
                           pagina="diferencial").grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.crear_tarjeta(marco_tarjetas, 
                           titulo="Cálculo Integral", 
                           emoji="📉",
                           descripcion="Integrales indefinidas,\ndefinidas y series.\n(En construcción...)",
                           color=COLOR_INTEGRAL,
                           pagina="integral").grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        
        # --- Fila 2 ---
        self.crear_tarjeta(marco_tarjetas, 
                           titulo="Álgebra Lineal", 
                           emoji="📐",
                           descripcion="Sistemas de ecuaciones,\nmatrices y propiedades.",
                           color=COLOR_ALGEBRA,
                           pagina="sistemas_ecuaciones").grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        self.crear_tarjeta(marco_tarjetas, 
                           titulo="Métodos Numéricos", 
                           emoji="🔢",
                           descripcion="Ecuaciones no lineales,\nBisección, Newton...",
                           color=COLOR_NUMERICOS,
                           pagina="metodos_numericos").grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        # Dejamos la (Fila 1, Columna 2) vacía a propósito
        
        ctk.CTkLabel(self, text="").grid(row=2, column=0)
    
    def crear_tarjeta(self, parent, titulo, emoji, descripcion, color, pagina):
        """Función genérica para crear tarjetas."""
        
        tarjeta = ctk.CTkFrame(parent, corner_radius=12, 
                                     fg_color=COLOR_TARJETA, 
                                     border_width=2,
                                     border_color=color[1] if ctk.get_appearance_mode() == "Dark" else color[0])
        tarjeta.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(tarjeta, text=emoji, 
                    font=ctk.CTkFont(size=40)).grid(row=0, column=0, pady=(20, 10))
        
        ctk.CTkLabel(tarjeta, text=titulo, 
                    font=ctk.CTkFont(size=20, weight="bold"),
                    text_color=COLOR_TEXTO_TARJETA).grid(row=1, column=0, pady=(0, 10))
        
        ctk.CTkLabel(tarjeta, text=descripcion,
                    font=ctk.CTkFont(size=12),
                    text_color=COLOR_TEXTO_TARJETA,
                    justify="center").grid(row=2, column=0, pady=(0, 20), padx=10)
        
        # Extrae la primera palabra del título para el botón
        txt_btn = titulo.split(' ')[0]
        if txt_btn == "Fundamentos": txt_btn = "Álgebra"
        
        btn = ctk.CTkButton(tarjeta, text=f"Explorar {txt_btn}",
                                  fg_color=color, hover_color=COLOR_HOVER,
                                  command=lambda: self.app.mostrar_pagina(pagina))
        btn.grid(row=3, column=0, sticky="s", padx=20, pady=20)
        
        return tarjeta