import customtkinter as ctk
from paginas.pagina_base import PaginaBase
from app_config import (COLOR_INTEGRAL, COLOR_FONDO_SECUNDARIO, 
                        COLOR_BOTON_SECUNDARIO, COLOR_BOTON_SECUNDARIO_HOVER)

class PaginaIntegral(PaginaBase):
    def crear_widgets(self):
        self.configurar_grid()
        
        # Título y estado
        marco_info = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_info.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        ctk.CTkLabel(marco_info, text="Cálculo Integral", 
                    font=ctk.CTkFont(size=24, weight="bold"),
                    text_color=COLOR_INTEGRAL[1]).pack(pady=(20, 10))
                    
        ctk.CTkLabel(marco_info, text="🚧 Módulo en Construcción 🚧", 
                    font=ctk.CTkFont(size=16)).pack(pady=(0, 20))

        # Espacio reservado
        marco_placeholder = ctk.CTkFrame(self, fg_color="transparent")
        marco_placeholder.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        ctk.CTkButton(marco_placeholder, text="Próximamente: Integrales Indefinidas", 
                     state="disabled", fg_color=COLOR_BOTON_SECUNDARIO).pack(pady=10)
        
        ctk.CTkButton(marco_placeholder, text="Próximamente: Área bajo la curva", 
                     state="disabled", fg_color=COLOR_BOTON_SECUNDARIO).pack(pady=10)

    def configurar_grid(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)