import customtkinter as ctk
import sys
import os

# --- IMPORTACIONES ---
try:
    from app_config import *
    print("✅ Configuración cargada.")
except ImportError as e:
    print(f"❌ Error config: {e}")
    COLOR_FONDO_SECUNDARIO = ("gray90", "gray16")
    COLOR_FONDO_PRINCIPAL = ("white", "black")
    COLOR_TEXTO_PRINCIPAL = ("black", "white")
    COLOR_BOTON_SECUNDARIO = "gray"
    COLOR_BOTON_SECUNDARIO_HOVER = "gray"

try: from paginas.pagina_inicio import PaginaInicio
except ImportError: PaginaInicio = None

class DummyPage:
    def __init__(self, parent, app): pass
    def crear_widgets(self): pass
    def mostrar(self): pass
    def grid_remove(self): pass

# Importaciones Lazy
try: from paginas.pagina_sistemas_ecuaciones import PaginaSistemasEcuaciones
except: PaginaSistemasEcuaciones = DummyPage
try: from paginas.pagina_operaciones_matriciales import PaginaOperacionesMatriciales
except: PaginaOperacionesMatriciales = DummyPage
try: from paginas.pagina_propiedades_matrices import PaginaPropiedadesMatrices
except: PaginaPropiedadesMatrices = DummyPage
try: from paginas.pagina_metodos_numericos import PaginaMetodosNumericos
except: PaginaMetodosNumericos = DummyPage
try: from paginas.pagina_fundamentos import PaginaFundamentos
except: PaginaFundamentos = DummyPage
try: from paginas.pagina_diferencial import PaginaDiferencial
except: PaginaDiferencial = DummyPage
try: from paginas.pagina_integral import PaginaIntegral
except: PaginaIntegral = DummyPage
try: from ui_components.ventana_ayuda import VentanaAyudaSymPy
except: 
    class VentanaAyudaSymPy: 
        def __init__(self,p): pass

class AplicacionPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("MathPro")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        self.configure(fg_color=COLOR_FONDO_PRINCIPAL)
        
        # Grid Principal: Columna 0 (Menú), Columna 1 (Contenido)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0) # Menú: Ancho fijo/dinámico
        self.grid_columnconfigure(1, weight=1) # Contenido: Se expande
        
        self.menu_visible = True 
        self.ancho_menu = 280 
        self.pantalla_actual = "inicio"
        
        self.crear_panel_nav()
        self.crear_panel_principal()
        self.inicializar_paginas()
        
        self.mostrar_pagina("inicio")
        
        # Iniciar con menú oculto para probar (opcional, puedes quitar esta línea)
        self.toggle_menu() 

    def inicializar_paginas(self):
        self.paginas = {}
        self.paginas["inicio"] = PaginaInicio(self.area_contenido, self) if PaginaInicio else DummyPage(self.area_contenido, self)
        self.paginas["sistemas_ecuaciones"] = PaginaSistemasEcuaciones(self.area_contenido, self)
        self.paginas["operaciones_matriciales"] = PaginaOperacionesMatriciales(self.area_contenido, self)
        self.paginas["propiedades_matrices"] = PaginaPropiedadesMatrices(self.area_contenido, self)
        self.paginas["metodos_numericos"] = PaginaMetodosNumericos(self.area_contenido, self)
        self.paginas["fundamentos"] = PaginaFundamentos(self.area_contenido, self)
        self.paginas["diferencial"] = PaginaDiferencial(self.area_contenido, self)
        self.paginas["integral"] = PaginaIntegral(self.area_contenido, self)
        
        for pagina in self.paginas.values():
            pagina.configure(fg_color=COLOR_FONDO_PRINCIPAL)
            if hasattr(pagina, 'grid_remove'):
                pagina.grid_remove()

    def mostrar_pagina(self, nombre_pagina, subseccion=None):
        if self.pantalla_actual in self.paginas:
            if hasattr(self.paginas[self.pantalla_actual], 'grid_remove'):
                self.paginas[self.pantalla_actual].grid_remove()
        
        self.pantalla_actual = nombre_pagina
        pagina = self.paginas[nombre_pagina]
        
        if hasattr(pagina, 'grid'):
            pagina.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        if hasattr(pagina, 'mostrar'):
            pagina.mostrar()
        
        if subseccion:
            if nombre_pagina == "integral" and hasattr(pagina, 'mostrar_seccion'):
                pagina.mostrar_seccion(subseccion)
            elif nombre_pagina == "fundamentos":
                if hasattr(pagina, 'cambiar_seccion'):
                    pagina.cambiar_seccion(subseccion)
                elif hasattr(pagina, 'operacion_var'): 
                    if subseccion == "basico": pagina.operacion_var.set("Suma")
                    elif subseccion == "avanzado": pagina.operacion_var.set("Factorizar")
                    if hasattr(pagina, '_actualizar_ui_operacion'): pagina._actualizar_ui_operacion()

        if nombre_pagina == "inicio":
            self.btn_inicio.pack_forget()
        else:
            self.btn_inicio.pack(fill="x", padx=20, pady=(0, 10), after=self.lbl_titulo_menu)

    def crear_panel_nav(self):
        self.marco_nav = ctk.CTkFrame(self, width=self.ancho_menu, corner_radius=0, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_nav.grid(row=0, column=0, sticky="nsew")
        self.marco_nav.grid_propagate(False) 
        
        self.scroll_menu = ctk.CTkScrollableFrame(self.marco_nav, fg_color="transparent", corner_radius=0)
        self.scroll_menu.pack(fill="both", expand=True)

        # -- Título --
        self.lbl_titulo_menu = ctk.CTkLabel(self.scroll_menu, text="MathPro", 
                                           font=ctk.CTkFont(size=26, weight="bold"),
                                           text_color=COLOR_TEXTO_PRINCIPAL)
        self.lbl_titulo_menu.pack(pady=(30, 15), padx=20, anchor="w")
        
        # Botón Inicio
        self.btn_inicio = ctk.CTkButton(self.scroll_menu, text="🏠  Inicio", anchor="w",
                                      fg_color=COLOR_BOTON_SECUNDARIO, 
                                      text_color=COLOR_TEXTO_PRINCIPAL,
                                      hover_color=COLOR_BOTON_SECUNDARIO_HOVER,
                                      height=35, corner_radius=8,
                                      command=lambda: self.mostrar_pagina("inicio"))
        
        # --- MENU ---
        self._crear_seccion_menu("FUNDAMENTOS", COLOR_FUNDAMENTOS)
        self._crear_boton_menu("Operaciones Básicas", "fundamentos", "basico")
        self._crear_boton_menu("Factorización y Raíces", "fundamentos", "avanzado")

        self._crear_seccion_menu("CÁLCULO DIFERENCIAL", COLOR_DIFERENCIAL)
        self._crear_boton_menu("Límites y Derivadas", "diferencial")

        self._crear_seccion_menu("CÁLCULO INTEGRAL", COLOR_INTEGRAL)
        self._crear_boton_menu("Técnicas e Integrales", "integral", "basicas")
        self._crear_boton_menu("Área y Volúmenes", "integral", "areas")

        self._crear_seccion_menu("ÁLGEBRA LINEAL", COLOR_ALGEBRA)
        self._crear_boton_menu("Sistemas y Matrices", "sistemas_ecuaciones")
        self._crear_boton_menu("Operaciones y Propiedades", "operaciones_matriciales")

        self._crear_seccion_menu("MÉTODOS NUMÉRICOS", COLOR_NUMERICOS)
        self._crear_boton_menu("Raíces de Ecuaciones", "metodos_numericos")

        # Espacio
        ctk.CTkLabel(self.scroll_menu, text="").pack(pady=5)
        
        # Ayuda
        self.btn_ayuda = ctk.CTkButton(self.scroll_menu, text="❓ Ayuda / Documentación",
                                     command=self.mostrar_ayuda_sympy,
                                     text_color=COLOR_TEXTO_SECUNDARIO,
                                     fg_color="transparent", border_width=1, border_color=COLOR_BOTON_SECUNDARIO_HOVER,
                                     hover_color=COLOR_BOTON_SECUNDARIO_HOVER, height=32)
        self.btn_ayuda.pack(fill="x", padx=20, pady=(10, 10))

        # Switch Tema
        self.switch_tema = ctk.CTkSwitch(self.scroll_menu, text="Modo Oscuro", 
                                       command=self.toggle_theme, 
                                       text_color=COLOR_TEXTO_PRINCIPAL,
                                       progress_color=COLOR_ACENTO)
        self.switch_tema.pack(padx=20, pady=(0, 30), anchor="w")
        
        if ctk.get_appearance_mode() == "Dark":
            self.switch_tema.select()

    def _crear_seccion_menu(self, texto, color):
        ctk.CTkLabel(self.scroll_menu, text=texto, 
                    font=ctk.CTkFont(size=11, weight="bold"), 
                    text_color=color).pack(anchor="w", padx=25, pady=(15, 2))

    def _crear_boton_menu(self, texto, pagina, subseccion=None):
        cmd = lambda p=pagina, s=subseccion: self.mostrar_pagina(p, s)
        
        # CORRECCIÓN 1: Botones Sólidos (Ya no transparentes)
        btn = ctk.CTkButton(self.scroll_menu, text=texto, anchor="w",
                      fg_color=COLOR_BOTON_SECUNDARIO, # Color sólido para que se vea el botón
                      text_color=COLOR_TEXTO_PRINCIPAL, 
                      hover_color=COLOR_BOTON_SECUNDARIO_HOVER,
                      height=30, # Un poco más altos
                      corner_radius=6,
                      font=ctk.CTkFont(size=13),
                      command=cmd)
        btn.pack(fill="x", padx=20, pady=3) # Margen vertical para separar botones

    def crear_panel_principal(self):
        self.marco_derecho = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.marco_derecho.grid(row=0, column=1, sticky="nswe", padx=0, pady=0)
        self.marco_derecho.grid_rowconfigure(1, weight=1)
        self.marco_derecho.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkFrame(self.marco_derecho, height=50, corner_radius=0, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        self.btn_menu = ctk.CTkButton(self.header, text="☰", width=40, height=40,
                                    font=ctk.CTkFont(size=20),
                                    fg_color="transparent",
                                    text_color=COLOR_TEXTO_PRINCIPAL,
                                    hover_color=COLOR_BOTON_SECUNDARIO_HOVER,
                                    command=self.toggle_menu)
        self.btn_menu.pack(side="left", padx=10, pady=5)

        self.area_contenido = ctk.CTkFrame(self.marco_derecho, corner_radius=0, fg_color="transparent")
        self.area_contenido.grid(row=1, column=0, sticky="nswe", padx=0, pady=0)
        self.area_contenido.grid_rowconfigure(0, weight=1)
        self.area_contenido.grid_columnconfigure(0, weight=1)

    def toggle_menu(self):
        # CORRECCIÓN 2: Animación y Ajuste correcto del Grid
        if self.menu_visible:
            # Ocultar: Forzamos el ancho a 0 y quitamos el widget del grid
            self.marco_nav.grid_remove()
            self.grid_columnconfigure(0, weight=0, minsize=0) # Columna 0 colapsada
            self.menu_visible = False
        else:
            # Mostrar: Restauramos el widget y el ancho mínimo
            self.grid_columnconfigure(0, weight=0, minsize=self.ancho_menu) # Columna 0 fija
            self.marco_nav.grid()
            self.menu_visible = True

    def toggle_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")

    def mostrar_ayuda_sympy(self):
        VentanaAyudaSymPy(self)

if __name__ == "__main__":
    print("🚀 Iniciando MathPro...")
    try:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        app = AplicacionPrincipal()
        app.mainloop()
    except Exception as e:
        print(f"❌ ERROR: {e}")
        input("Presiona ENTER...")