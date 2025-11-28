import customtkinter as ctk
from paginas.pagina_base import PaginaBase
from app_config import (COLOR_FONDO_SECUNDARIO, COLOR_FUNDAMENTOS, 
                        COLOR_HOVER, COLOR_BOTON_SECUNDARIO, 
                        COLOR_BOTON_SECUNDARIO_HOVER)

# Importación de LogicaFundamentos con manejo de errores
try:
    from LogicaFundamentos import (
        operar_polinomios, resolver_polinomio, 
        factorizar_expresion, simplificar_expresion
    )
    LOGICA_DISPONIBLE = True
except ImportError:
    LOGICA_DISPONIBLE = False
    def operar_polinomios(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}
    def resolver_polinomio(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}
    def factorizar_expresion(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}
    def simplificar_expresion(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}

class PaginaFundamentos(PaginaBase):
    
    def crear_widgets(self):
        self.configurar_grid()
        self.crear_barra_navegacion()
        self.crear_interfaz()
        self.mostrar_seccion("basico") # Default
        
    def configurar_grid(self):
        self.grid_rowconfigure(0, weight=0) # Nav
        self.grid_rowconfigure(1, weight=0) # Selector
        self.grid_rowconfigure(2, weight=0) # Entradas
        self.grid_rowconfigure(3, weight=0) # Controles
        self.grid_rowconfigure(4, weight=1) # Resultados
        self.grid_columnconfigure(0, weight=1)

    def crear_barra_navegacion(self):
        """Barra superior para dividir temas."""
        marco_nav = ctk.CTkFrame(self, fg_color="transparent", height=40)
        marco_nav.grid(row=0, column=0, sticky="ew", padx=12, pady=(8,0))
        
        self.btn_basico = ctk.CTkButton(marco_nav, text="Operaciones Básicas", 
                                   fg_color=COLOR_FUNDAMENTOS, height=30,
                                   command=lambda: self.mostrar_seccion("basico"))
        self.btn_basico.pack(side="left", padx=(0, 5), expand=True, fill="x")
        
        self.btn_avanzado = ctk.CTkButton(marco_nav, text="Factorización y Raíces", 
                                   fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, height=30,
                                   command=lambda: self.mostrar_seccion("avanzado"))
        self.btn_avanzado.pack(side="left", padx=5, expand=True, fill="x")

    def crear_interfaz(self):
        # --- Selector de Operación ---
        self.marco_metodo = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_metodo.grid(row=1, column=0, sticky="ew", padx=12, pady=8)
        
        ctk.CTkLabel(self.marco_metodo, text="Operación:", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=(12, 8), pady=12)
        
        self.operacion_var = ctk.StringVar(value="Suma")
        self.marco_radios = ctk.CTkFrame(self.marco_metodo, fg_color="transparent")
        self.marco_radios.grid(row=0, column=1, padx=10)

        # --- Entradas de Polinomios ---
        marco_entradas = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_entradas.grid(row=2, column=0, sticky="ew", padx=12, pady=(4, 8))
        marco_entradas.grid_columnconfigure(1, weight=1)

        self.lbl_p1 = ctk.CTkLabel(marco_entradas, text="P(x) =", font=ctk.CTkFont(size=13))
        self.lbl_p1.grid(row=0, column=0, sticky="w", padx=8, pady=6)
        
        self.ent_p1 = ctk.CTkEntry(marco_entradas, placeholder_text="Ej: 2x^2 + 5x + 6")
        self.ent_p1.grid(row=0, column=1, sticky="ew", padx=8, pady=6)
        
        self.lbl_p2 = ctk.CTkLabel(marco_entradas, text="Q(x) =", font=ctk.CTkFont(size=13))
        self.lbl_p2.grid(row=1, column=0, sticky="w", padx=8, pady=6)
        
        self.ent_p2 = ctk.CTkEntry(marco_entradas, placeholder_text="Ej: x + 2")
        self.ent_p2.grid(row=1, column=1, sticky="ew", padx=8, pady=6)

        # --- Controles ---
        marco_controles = ctk.CTkFrame(self)
        marco_controles.grid(row=3, column=0, sticky="ew", padx=12, pady=(6,12))
        
        ctk.CTkButton(marco_controles, text="Calcular", command=self.calcular,
                      fg_color=COLOR_FUNDAMENTOS, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        
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
        
        # --- Bitácora ---
        marco_pasos = ctk.CTkFrame(marco_resultados)
        marco_pasos.grid(row=0, column=0, sticky="nswe", padx=(0,6))
        marco_pasos.grid_columnconfigure(0, weight=1)
        marco_pasos.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_pasos, text="Bitácora y Procedimiento", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        
        self.pasos_scroll_frame = ctk.CTkScrollableFrame(marco_pasos, fg_color=COLOR_FONDO_SECUNDARIO)
        self.pasos_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))
        self.pasos_scroll_frame.grid_columnconfigure(0, weight=1)

        # --- Resultado Final ---
        marco_resultado = ctk.CTkFrame(marco_resultados)
        marco_resultado.grid(row=0, column=1, sticky="nswe", padx=(6,0))
        marco_resultado.grid_columnconfigure(0, weight=1)
        marco_resultado.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_resultado, text="Resultado Final", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        
        self.resultado_caja = ctk.CTkTextbox(marco_resultado, height=220, 
                                             font=ctk.CTkFont(family="Consolas", size=14, weight="bold"), 
                                             border_color=COLOR_FUNDAMENTOS[1],
                                             border_width=2,
                                             wrap="none") 
        self.resultado_caja.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))
        self.resultado_caja.configure(state="disabled")
        
        self.seccion_actual = "basico"

    # --- LÓGICA DE NAVEGACIÓN ---
    def cambiar_seccion(self, seccion):
        """Método llamado desde main.py."""
        self.mostrar_seccion(seccion)

    def mostrar_seccion(self, seccion):
        self.seccion_actual = seccion
        
        # Actualizar colores de botones
        self.btn_basico.configure(fg_color=COLOR_FUNDAMENTOS if seccion=="basico" else COLOR_BOTON_SECUNDARIO)
        self.btn_avanzado.configure(fg_color=COLOR_FUNDAMENTOS if seccion=="avanzado" else COLOR_BOTON_SECUNDARIO)

        # Limpiar radiobuttons viejos
        for w in self.marco_radios.winfo_children(): w.destroy()
        
        # Crear nuevos radiobuttons según la sección
        operaciones = []
        if seccion == "basico":
            operaciones = ["Suma", "Resta", "Multiplicación", "División"]
            self.operacion_var.set("Suma")
        else: # avanzado
            operaciones = ["Factorizar", "Simplificar", "Encontrar Raíces"]
            self.operacion_var.set("Factorizar")
            
        for i, op in enumerate(operaciones):
            rb = ctk.CTkRadioButton(self.marco_radios, text=op, variable=self.operacion_var, 
                                   value=op, font=ctk.CTkFont(size=13),
                                   command=self._actualizar_ui_operacion)
            rb.grid(row=0, column=i, padx=8, pady=5, sticky="w")
            
        self._actualizar_ui_operacion()

    def _actualizar_ui_operacion(self):
        operacion = self.operacion_var.get()
        # Operaciones unarias (solo necesitan un polinomio)
        if operacion in ["Encontrar Raíces", "Factorizar", "Simplificar"]:
            self.lbl_p2.grid_remove()
            self.ent_p2.grid_remove()
            self.lbl_p1.configure(text="Expresión:")
        else:
            self.lbl_p2.grid()
            self.ent_p2.grid()
            self.lbl_p1.configure(text="P(x) =")

    # --- Funciones de UI ---
    def _limpiar_pasos_scroll(self):
        for widget in self.pasos_scroll_frame.winfo_children(): widget.destroy()

    def _crear_bloque_paso(self, titulo: str, math: str):
        paso_frame = ctk.CTkFrame(self.pasos_scroll_frame, fg_color="transparent")
        paso_frame.pack(fill="x", pady=(0, 15))
        
        lbl_titulo = ctk.CTkLabel(paso_frame, text=titulo.upper(), 
                                  font=ctk.CTkFont(size=12, weight="bold"),
                                  text_color=COLOR_FUNDAMENTOS[0])
        lbl_titulo.pack(anchor="w", padx=5)
        
        lbl_math = ctk.CTkLabel(paso_frame, text=math, 
                                font=ctk.CTkFont(family="Consolas", size=14), 
                                justify="left")
        lbl_math.pack(anchor="w", padx=20, pady=5)
        
    def _renderizar_pasos(self, pasos_lista: list):
        self._limpiar_pasos_scroll()
        if not pasos_lista: return
        for paso in pasos_lista:
            contenido = paso.get('math', '...')
            self._crear_bloque_paso(titulo=paso.get('titulo', 'PASO'), math=contenido)

    def limpiar(self):
        self.ent_p1.delete(0, 'end')
        self.ent_p2.delete(0, 'end')
        self._limpiar_pasos_scroll()
        
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete('0.0', 'end')
        self.resultado_caja.configure(state="disabled")

    def calcular(self):
        if not LOGICA_DISPONIBLE:
            self.resultado_caja.configure(state="normal")
            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', "Error: Lógica no disponible.")
            self.resultado_caja.configure(state="disabled")
            return
        
        self._limpiar_pasos_scroll()
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete('0.0', 'end')
        
        operacion = self.operacion_var.get()
        p1_str = self.ent_p1.get()
        
        try:
            if not p1_str: raise ValueError("Ingrese al menos la primera expresión.")

            if operacion == "Encontrar Raíces":
                res = resolver_polinomio(p1_str)
            elif operacion == "Factorizar":
                res = factorizar_expresion(p1_str)
            elif operacion == "Simplificar":
                res = simplificar_expresion(p1_str)
            else:
                p2_str = self.ent_p2.get()
                if not p2_str: raise ValueError("Se requieren dos expresiones para esta operación.")
                res = operar_polinomios(p1_str, p2_str, operacion)
            
            if res.get('pasos'): self._renderizar_pasos(res['pasos'])
            
            if res['estado'] == 'exito':
                self.resultado_caja.insert('0.0', res.get('resultado_math', 'Éxito'))
            else:
                self.resultado_caja.insert('0.0', f"Error:\n{res['mensaje']}")
                
        except ValueError as e:
            self.resultado_caja.insert('0.0', f"Error de entrada: {e}")
        except Exception as e:
            self.resultado_caja.insert('0.0', f"Error inesperado: {e}")
            
        self.resultado_caja.configure(state="disabled")