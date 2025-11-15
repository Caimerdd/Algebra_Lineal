import customtkinter as ctk
from paginas.pagina_base import PaginaBase
from app_config import COLOR_INTEGRAL, COLOR_FONDO_SECUNDARIO

class PaginaIntegral(PaginaBase):
    def crear_widgets(self):
        self.configurar_grid()
        
        # --- Selector (Placeholder) ---
        marco_metodo = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_metodo.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        ctk.CTkLabel(marco_metodo, text="Operación:", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=(12, 8), pady=12)
        ctk.CTkRadioButton(marco_metodo, text="Integral Indefinida", state="disabled").grid(row=0, column=1, padx=8)
        ctk.CTkRadioButton(marco_metodo, text="Integral Definida", state="disabled").grid(row=0, column=2, padx=8)
        
        # --- Entradas (Placeholder) ---
        marco_entradas = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_entradas.grid(row=1, column=0, sticky="ew", padx=12, pady=(4, 8))
        marco_entradas.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(marco_entradas, text="f(x) dx =", font=ctk.CTkFont(size=13)).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        ctk.CTkEntry(marco_entradas, placeholder_text="Ej: x^3 / (x-1)", state="disabled").grid(row=0, column=1, sticky="ew", padx=8, pady=6)
        
        # --- Resultados (Layout de UI) ---
        marco_resultados = ctk.CTkFrame(self)
        marco_resultados.grid(row=3, column=0, sticky="nsew", padx=12, pady=(6,12))
        marco_resultados.grid_rowconfigure(0, weight=1)
        marco_resultados.grid_columnconfigure(0, weight=2)
        marco_resultados.grid_columnconfigure(1, weight=1)
        
        # Bitácora (ScrollableFrame)
        marco_pasos = ctk.CTkFrame(marco_resultados)
        marco_pasos.grid(row=0, column=0, sticky="nswe", padx=(0,6))
        marco_pasos.grid_columnconfigure(0, weight=1)
        marco_pasos.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(marco_pasos, text="Bitacora Paso a Paso", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.pasos_scroll_frame = ctk.CTkScrollableFrame(marco_pasos, fg_color=COLOR_FONDO_SECUNDARIO)
        self.pasos_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))
        self.pasos_scroll_frame.grid_columnconfigure(0, weight=1)

        # Mensaje "En Construcción"
        lbl_info = ctk.CTkLabel(self.pasos_scroll_frame, 
                                text="🚧 En construcción... 🚧\n\nAquí irán las herramientas de integrales y series.",
                                font=ctk.CTkFont(size=16),
                                text_color="gray")
        lbl_info.pack(pady=50, padx=10)

        # Resultado (Resaltado)
        marco_resultado = ctk.CTkFrame(marco_resultados)
        marco_resultado.grid(row=0, column=1, sticky="nswe", padx=(6,0))
        marco_resultado.grid_columnconfigure(0, weight=1)
        marco_resultado.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(marco_resultado, text="Resultado Final", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.resultado_caja = ctk.CTkTextbox(marco_resultado, height=220, 
                                             font=ctk.CTkFont(family="monospace", size=14, weight="bold"),
                                             border_color=COLOR_INTEGRAL[1],
                                             border_width=2,
                                             wrap="none")
        self.resultado_caja.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))
        self.resultado_caja.configure(state="disabled")

    def configurar_grid(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)