import customtkinter as ctk
import os
import subprocess
import tkinter.messagebox # Importante para mostrar alertas si algo falla

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
        
        # --- VARIABLES DE ESTADO ---
        self.menu_visible = False # Inicia oculto
        self.ancho_menu = 280

        # Configurar grid principal
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
        self.marco_nav = ctk.CTkFrame(self, width=0, corner_radius=0)
        self.marco_nav.grid(row=0, column=0, sticky="nswe")
        self.marco_nav.grid_propagate(False)
        
        # Configuración de filas
        self.marco_nav.grid_rowconfigure(9, weight=1)  # Espaciador
        self.marco_nav.grid_rowconfigure(10, weight=0) # Botón Rojo
        self.marco_nav.grid_rowconfigure(11, weight=0) # Configuración
        self.marco_nav.grid_columnconfigure(0, weight=1)
        
        # -- Contenido del Menú --
        ctk.CTkLabel(self.marco_nav, text="MathPro", 
                    font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=20, pady=(25, 15), sticky="w")
        
        self.btn_inicio = ctk.CTkButton(self.marco_nav, text="🏠 Regresar al Inicio", anchor="w",
                                      fg_color=COLOR_BOTON_SECUNDARIO, 
                                      hover_color=COLOR_BOTON_SECUNDARIO_HOVER,
                                      command=lambda: self.mostrar_pagina("inicio"))
        self.btn_inicio.grid(row=1, column=0, sticky="ew", padx=12, pady=5)
        self.btn_inicio.grid_remove()
        
        ctk.CTkFrame(self.marco_nav, height=2).grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        # Algebra
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
        
        # Numericos
        ctk.CTkLabel(self.marco_nav, text="METODOS NUMERICOS", 
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=COLOR_NUMERICOS).grid(row=7, column=0, sticky="w", padx=15, pady=(15, 5))
        
        ctk.CTkButton(self.marco_nav, text="   Ecuaciones No Lineales", anchor="w",
                      fg_color=COLOR_NUMERICOS, hover_color=COLOR_HOVER,
                      command=lambda: self.mostrar_pagina("metodos_numericos")).grid(row=8, column=0, sticky="ew", padx=12, pady=3)

        # Espaciador (Fila 9)
        ctk.CTkFrame(self.marco_nav, fg_color="transparent").grid(row=9, column=0, sticky="nsew")

        # BOTÓN SECRETO (Fila 10)
        self.btn_secreto = ctk.CTkButton(self.marco_nav, text="🚫 NO TOCAR ❯",
                      font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color="#E53935", hover_color="#B71C1C",
                      height=40,
                      command=self.abrir_secreto_video)
        self.btn_secreto.grid(row=10, column=0, sticky="ew", padx=12, pady=(10, 0))

        # Configuración (Fila 11)
        marco_config = ctk.CTkFrame(self.marco_nav, fg_color="transparent")
        marco_config.grid(row=11, column=0, sticky="ews", padx=12, pady=20)
        
        self.btn_ayuda = ctk.CTkButton(marco_config, text="📚 Ayuda",
                                     command=self.mostrar_ayuda_sympy,
                                     width=80,
                                     fg_color=COLOR_BOTON_SECUNDARIO,
                                     hover_color=COLOR_BOTON_SECUNDARIO_HOVER)
        self.btn_ayuda.pack(side="left", padx=(0, 5))
        
        self.theme_switch = ctk.CTkSwitch(marco_config, text="Oscuro", command=self.toggle_theme,
                                          width=80, progress_color=COLOR_ACENTO)
        self.theme_switch.pack(side="right")
        
        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()

    def crear_panel_principal(self):
        self.marco_derecho = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.marco_derecho.grid(row=0, column=1, sticky="nswe", padx=0, pady=0)
        self.marco_derecho.grid_rowconfigure(1, weight=1)
        self.marco_derecho.grid_columnconfigure(0, weight=1)

        # Header
        self.header = ctk.CTkFrame(self.marco_derecho, height=50, corner_radius=0, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        # Botón Menú
        self.btn_menu = ctk.CTkButton(self.header, text="☰", width=40, height=40,
                                    font=ctk.CTkFont(size=20),
                                    fg_color="transparent",
                                    text_color=("black", "white"),
                                    hover_color=("gray80", "gray30"),
                                    command=self.toggle_menu)
        self.btn_menu.pack(side="left", padx=10, pady=5)

        # Área de Contenido
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

    def abrir_secreto_video(self):
        """
        Abre el archivo de video con verificación de errores y doble extensión.
        """
        # Obtiene la carpeta base
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Ruta ideal
        video_path = os.path.join(base_path, "secreto", "himno.mp4")
        
        # Verificación robusta
        if not os.path.exists(video_path):
            # Intento de corrección de doble extensión (himno.mp4.mp4)
            ruta_alternativa = os.path.join(base_path, "secreto", "himno.mp4.mp4")
            if os.path.exists(ruta_alternativa):
                video_path = ruta_alternativa
            else:
                tkinter.messagebox.showerror("Error de Archivo", 
                    f"No encuentro el video.\n\nBuscando en:\n{video_path}\n\n"
                    "Asegúrate de:\n1. Crear la carpeta 'secreto'\n2. Poner el archivo 'himno.mp4' dentro.")
                return

        try:
            # Abrir según el sistema operativo
            if os.name == 'nt': # Windows
                os.startfile(video_path)
            elif os.name == 'posix': # macOS o Linux
                if os.system(f'open "{video_path}"') != 0:
                    # Si falla 'open', intenta 'xdg-open' (Linux)
                    os.system(f'xdg-open "{video_path}"')
        except Exception as e:
            tkinter.messagebox.showerror("Error al abrir", f"No se pudo reproducir el video.\nError: {e}")

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