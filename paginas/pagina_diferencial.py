import customtkinter as ctk
from paginas.pagina_base import PaginaBase
from app_config import (COLOR_FONDO_SECUNDARIO, COLOR_DIFERENCIAL, 
                        COLOR_HOVER, COLOR_BOTON_SECUNDARIO, 
                        COLOR_BOTON_SECUNDARIO_HOVER)

# Importación de Logica
try:
    from LogicaDiferencial import calcular_limite, calcular_derivada
    LOGICA_DISPONIBLE = True
except ImportError:
    LOGICA_DISPONIBLE = False
    def calcular_limite(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}
    def calcular_derivada(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}

class PaginaDiferencial(PaginaBase):
    def crear_widgets(self):
        self.configurar_grid()
        self.crear_barra_navegacion()
        self.crear_interfaz()
        self._actualizar_ui_operacion()
    
    def configurar_grid(self):
        self.grid_rowconfigure(0, weight=0) # Nav
        self.grid_rowconfigure(1, weight=0) # Selector
        self.grid_rowconfigure(2, weight=0) # Inputs
        self.grid_rowconfigure(3, weight=0) # Controles
        self.grid_rowconfigure(4, weight=1) # Resultados
        self.grid_columnconfigure(0, weight=1)

    def crear_barra_navegacion(self):
        marco_nav = ctk.CTkFrame(self, fg_color="transparent", height=40)
        marco_nav.grid(row=0, column=0, sticky="ew", padx=12, pady=(8,0))
        
        btn_calc1 = ctk.CTkButton(marco_nav, text="Cálculo Diferencial (I)", 
                                  fg_color=COLOR_DIFERENCIAL, state="disabled", 
                                  text_color_disabled=("white", "white"), height=30)
        btn_calc1.pack(side="left", padx=(0, 5), expand=True, fill="x")

    def crear_interfaz(self):
        # --- Selector ---
        marco_metodo = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_metodo.grid(row=1, column=0, sticky="ew", padx=12, pady=8)
        
        ctk.CTkLabel(marco_metodo, text="Operación:", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=(12, 8), pady=12)
        
        self.operacion_var = ctk.StringVar(value="Derivada")
        
        rb1 = ctk.CTkRadioButton(marco_metodo, text="Derivada", variable=self.operacion_var, 
                                value="Derivada", command=self._actualizar_ui_operacion)
        rb1.grid(row=0, column=1, padx=10)
        
        rb2 = ctk.CTkRadioButton(marco_metodo, text="Límite", variable=self.operacion_var, 
                                value="Límite", command=self._actualizar_ui_operacion)
        rb2.grid(row=0, column=2, padx=10)

        # --- Entradas ---
        marco_entradas = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_entradas.grid(row=2, column=0, sticky="ew", padx=12, pady=(4, 8))
        
        # Fila 0: Función
        ctk.CTkLabel(marco_entradas, text="Función f(x) =", font=ctk.CTkFont(size=13)).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.ent_funcion = ctk.CTkEntry(marco_entradas, placeholder_text="Ej: x^2 * sin(x)", width=300)
        self.ent_funcion.grid(row=0, column=1, columnspan=3, sticky="ew", padx=8, pady=6)
        
        # Fila 1: Opciones Dinámicas
        self.lbl_param = ctk.CTkLabel(marco_entradas, text="Orden:", font=ctk.CTkFont(size=13))
        self.lbl_param.grid(row=1, column=0, sticky="w", padx=8, pady=6)
        
        self.ent_param = ctk.CTkEntry(marco_entradas, width=100)
        self.ent_param.grid(row=1, column=1, sticky="w", padx=8, pady=6)
        
        # Selector de Dirección (Solo para límites)
        self.lbl_dir = ctk.CTkLabel(marco_entradas, text="Dirección:", font=ctk.CTkFont(size=13))
        self.opt_dir = ctk.CTkOptionMenu(marco_entradas, values=["Ambos lados", "Derecha (+)", "Izquierda (-)"], width=120)
        
        # --- Controles ---
        marco_controles = ctk.CTkFrame(self)
        marco_controles.grid(row=3, column=0, sticky="ew", padx=12, pady=(6,12))
        
        ctk.CTkButton(marco_controles, text="Calcular", command=self.calcular,
                      fg_color=COLOR_DIFERENCIAL, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        
        ctk.CTkButton(marco_controles, text="Limpiar", command=self.limpiar,
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=1, padx=6)

        ctk.CTkButton(marco_controles, text="Ayuda ❓", command=lambda: self.app.mostrar_ayuda_sympy(),
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, width=80).grid(row=0, column=2, padx=6)

        # --- Resultados ---
        marco_resultados = ctk.CTkFrame(self)
        marco_resultados.grid(row=4, column=0, sticky="nsew", padx=12, pady=(6,12))
        marco_resultados.grid_rowconfigure(0, weight=1)
        marco_resultados.grid_columnconfigure(0, weight=2)
        marco_resultados.grid_columnconfigure(1, weight=1)
        
        # Bitácora
        marco_pasos = ctk.CTkFrame(marco_resultados)
        marco_pasos.grid(row=0, column=0, sticky="nswe", padx=(0,6))
        marco_pasos.grid_columnconfigure(0, weight=1)
        marco_pasos.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(marco_pasos, text="Bitácora y Procedimiento", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.pasos_scroll_frame = ctk.CTkScrollableFrame(marco_pasos, fg_color=COLOR_FONDO_SECUNDARIO)
        self.pasos_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))
        self.pasos_scroll_frame.grid_columnconfigure(0, weight=1)

        # Resultado
        marco_resultado = ctk.CTkFrame(marco_resultados)
        marco_resultado.grid(row=0, column=1, sticky="nswe", padx=(6,0))
        marco_resultado.grid_columnconfigure(0, weight=1)
        marco_resultado.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(marco_resultado, text="Resultado Final", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.resultado_caja = ctk.CTkTextbox(marco_resultado, height=220, 
                                             font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
                                             border_color=COLOR_DIFERENCIAL[1], border_width=2, wrap="none")
        self.resultado_caja.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))
        self.resultado_caja.configure(state="disabled")

    def _actualizar_ui_operacion(self):
        op = self.operacion_var.get()
        if op == "Derivada":
            self.lbl_param.configure(text="Orden (n):")
            self.ent_param.delete(0, 'end'); self.ent_param.insert(0, "1") # Default 1ra derivada
            self.lbl_dir.grid_remove()
            self.opt_dir.grid_remove()
        else: # Límite
            self.lbl_param.configure(text="Cuando x tiende a:")
            self.ent_param.delete(0, 'end'); self.ent_param.insert(0, "0")
            self.lbl_dir.grid(row=1, column=2, padx=8, sticky="e")
            self.opt_dir.grid(row=1, column=3, padx=8, sticky="w")

    # --- UI Helpers ---
    def _limpiar_pasos_scroll(self):
        for widget in self.pasos_scroll_frame.winfo_children(): widget.destroy()

    def _crear_bloque_paso(self, titulo: str, math: str):
        paso_frame = ctk.CTkFrame(self.pasos_scroll_frame, fg_color="transparent")
        paso_frame.pack(fill="x", pady=(0, 15))
        lbl_titulo = ctk.CTkLabel(paso_frame, text=titulo.upper(), font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_DIFERENCIAL[0])
        lbl_titulo.pack(anchor="w", padx=5)
        lbl_math = ctk.CTkLabel(paso_frame, text=math, font=ctk.CTkFont(family="Consolas", size=14), justify="left")
        lbl_math.pack(anchor="w", padx=20, pady=5)

    def limpiar(self):
        self.ent_funcion.delete(0, 'end')
        self._actualizar_ui_operacion() # Reset defaults
        self._limpiar_pasos_scroll()
        self.resultado_caja.configure(state="normal"); self.resultado_caja.delete('0.0', 'end'); self.resultado_caja.configure(state="disabled")

    def calcular(self):
        self._limpiar_pasos_scroll()
        self.resultado_caja.configure(state="normal"); self.resultado_caja.delete('0.0', 'end')
        
        if not LOGICA_DISPONIBLE:
            self.resultado_caja.insert('0.0', "Error: Lógica no disponible.")
            self.resultado_caja.configure(state="disabled")
            return

        op = self.operacion_var.get()
        func_str = self.ent_funcion.get()
        param_str = self.ent_param.get()
        
        try:
            if not func_str: raise ValueError("Ingrese una función.")
            
            if op == "Derivada":
                res = calcular_derivada(func_str, orden=param_str)
            else: # Límite
                d_map = {"Ambos lados": "both", "Derecha (+)": "+", "Izquierda (-)": "-"}
                res = calcular_limite(func_str, param_str, direccion=d_map[self.opt_dir.get()])
            
            if res.get('pasos'):
                for paso in res['pasos']:
                    self._crear_bloque_paso(paso['titulo'], paso['math'])
            
            if res['estado'] == 'exito':
                self.resultado_caja.insert('0.0', res['resultado_math'])
            else:
                self.resultado_caja.insert('0.0', f"Error:\n{res['mensaje']}")

        except ValueError as e: self.resultado_caja.insert('0.0', f"Entrada inválida: {e}")
        except Exception as e: self.resultado_caja.insert('0.0', f"Error: {e}")
            
        self.resultado_caja.configure(state="disabled")