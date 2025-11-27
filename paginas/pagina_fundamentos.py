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
    print("✅ LogicaFundamentos.py cargado exitosamente")
except ImportError as e:
    LOGICA_DISPONIBLE = False
    print(f"❌ Error cargando LogicaFundamentos.py: {e}")
    # Funciones dummy para evitar crash
    def operar_polinomios(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}
    def resolver_polinomio(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}
    def factorizar_expresion(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}
    def simplificar_expresion(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}

class PaginaFundamentos(PaginaBase):
    
    def crear_widgets(self):
        self.configurar_grid()
        
        # --- Selector de Operación ---
        marco_metodo = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_metodo.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        
        ctk.CTkLabel(marco_metodo, text="Operación:", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=(12, 8), pady=12)
        
        self.operacion_var = ctk.StringVar(value="Suma")
        # Lista ampliada con las nuevas funciones
        operaciones = ["Suma", "Resta", "Multiplicación", "División", 
                       "Factorizar", "Simplificar", "Encontrar Raíces"]
        
        # Usamos un frame interno para los radiobuttons si son muchos, 
        # o los distribuimos en columnas
        marco_radios = ctk.CTkFrame(marco_metodo, fg_color="transparent")
        marco_radios.grid(row=0, column=1, padx=8, pady=12)
        
        for i, op in enumerate(operaciones):
            rb = ctk.CTkRadioButton(marco_radios, text=op, variable=self.operacion_var, 
                                   value=op, font=ctk.CTkFont(size=13),
                                   command=self._actualizar_ui_operacion)
            # Organizamos en 2 filas para que no se vea amontonado
            fila = 0 if i < 4 else 1
            col = i if i < 4 else i - 4
            rb.grid(row=fila, column=col, padx=8, pady=5, sticky="w")

        # --- Entradas de Polinomios ---
        marco_entradas = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_entradas.grid(row=1, column=0, sticky="ew", padx=12, pady=(4, 8))
        marco_entradas.grid_columnconfigure(1, weight=1)

        self.lbl_p1 = ctk.CTkLabel(marco_entradas, text="P(x) =", font=ctk.CTkFont(size=13))
        self.lbl_p1.grid(row=0, column=0, sticky="w", padx=8, pady=6)
        
        # Placeholder genérico, sin texto insertado
        self.ent_p1 = ctk.CTkEntry(marco_entradas, placeholder_text="Ej: x^2 + 5*x + 6")
        self.ent_p1.grid(row=0, column=1, sticky="ew", padx=8, pady=6)
        
        self.lbl_p2 = ctk.CTkLabel(marco_entradas, text="Q(x) =", font=ctk.CTkFont(size=13))
        self.lbl_p2.grid(row=1, column=0, sticky="w", padx=8, pady=6)
        self.ent_p2 = ctk.CTkEntry(marco_entradas, placeholder_text="Ej: x + 2")
        self.ent_p2.grid(row=1, column=1, sticky="ew", padx=8, pady=6)

        # --- Controles ---
        marco_controles = ctk.CTkFrame(self)
        marco_controles.grid(row=2, column=0, sticky="ew", padx=12, pady=(6,12))
        
        ctk.CTkButton(marco_controles, text="Calcular", command=self.calcular,
                      fg_color=COLOR_FUNDAMENTOS, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        
        ctk.CTkButton(marco_controles, text="Limpiar", command=self.limpiar,
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=1, padx=6)

        # --- Resultados ---
        marco_resultados = ctk.CTkFrame(self)
        marco_resultados.grid(row=3, column=0, sticky="nsew", padx=12, pady=(6,12))
        marco_resultados.grid_rowconfigure(0, weight=1)
        marco_resultados.grid_columnconfigure(0, weight=2)
        marco_resultados.grid_columnconfigure(1, weight=1)
        
        # --- Bitácora (ScrollableFrame) ---
        marco_pasos = ctk.CTkFrame(marco_resultados)
        marco_pasos.grid(row=0, column=0, sticky="nswe", padx=(0,6))
        marco_pasos.grid_columnconfigure(0, weight=1)
        marco_pasos.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_pasos, text="Bitácora Paso a Paso", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        
        self.pasos_scroll_frame = ctk.CTkScrollableFrame(marco_pasos, fg_color=COLOR_FONDO_SECUNDARIO)
        self.pasos_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))
        self.pasos_scroll_frame.grid_columnconfigure(0, weight=1)

        # --- Resultado Final (Resaltado) ---
        marco_resultado = ctk.CTkFrame(marco_resultados)
        marco_resultado.grid(row=0, column=1, sticky="nswe", padx=(6,0))
        marco_resultado.grid_columnconfigure(0, weight=1)
        marco_resultado.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_resultado, text="Resultado Final", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        
        self.resultado_caja = ctk.CTkTextbox(marco_resultado, height=220, 
                                             font=ctk.CTkFont(family="monospace", size=14, weight="bold"),
                                             border_color=COLOR_FUNDAMENTOS[1],
                                             border_width=2,
                                             wrap="word") # 'word' para que expresiones largas bajen de línea
        self.resultado_caja.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))
        self.resultado_caja.configure(state="disabled")
        
        self._actualizar_ui_operacion()

    def configurar_grid(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def _actualizar_ui_operacion(self):
        operacion = self.operacion_var.get()
        # Operaciones unarias (solo necesitan un polinomio)
        if operacion in ["Encontrar Raíces", "Factorizar", "Simplificar"]:
            self.lbl_p2.grid_remove()
            self.ent_p2.grid_remove()
            self.lbl_p1.configure(text="Expresión / P(x) =")
        else:
            self.lbl_p2.grid()
            self.ent_p2.grid()
            self.lbl_p1.configure(text="P(x) =")

    # --- Funciones de UI para "Paso a Paso" ---
    def _limpiar_pasos_scroll(self):
        for widget in self.pasos_scroll_frame.winfo_children():
            widget.destroy()

    def _crear_bloque_paso(self, titulo: str, math: str):
        paso_frame = ctk.CTkFrame(self.pasos_scroll_frame, fg_color="transparent")
        paso_frame.pack(fill="x", pady=(0, 15))
        
        lbl_titulo = ctk.CTkLabel(paso_frame, text=titulo.upper(), 
                                  font=ctk.CTkFont(size=12, weight="bold"),
                                  text_color=COLOR_FUNDAMENTOS[0])
        lbl_titulo.pack(anchor="w", padx=5)
        
        # Usamos texto normal pero intentamos que SymPy nos de algo legible
        lbl_math = ctk.CTkLabel(paso_frame, text=math, 
                                font=ctk.CTkFont(family="monospace", size=14), 
                                justify="left")
        lbl_math.pack(anchor="w", padx=20, pady=5)
        
    def _renderizar_pasos(self, pasos_lista: list):
        self._limpiar_pasos_scroll()
        if not pasos_lista:
            self._crear_bloque_paso("SIN PASOS", "La lógica no devolvió pasos detallados.")
            return
            
        for paso in pasos_lista:
            # Preferimos mostrar 'resultado_math' o 'math'
            contenido = paso.get('math', paso.get('resultado_math', '...'))
            self._crear_bloque_paso(titulo=paso.get('titulo', 'PASO'), 
                                    math=contenido)

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
            self.resultado_caja.insert('0.0', "Error: No se pudo cargar 'LogicaFundamentos.py'.")
            self.resultado_caja.configure(state="disabled")
            return
        
        self._limpiar_pasos_scroll()
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete('0.0', 'end')
        
        operacion = self.operacion_var.get()
        p1_str = self.ent_p1.get()
        
        try:
            if not p1_str:
                raise ValueError("La primera expresión no puede estar vacía.")

            # Llamadas a la lógica según la operación
            if operacion == "Encontrar Raíces":
                res = resolver_polinomio(p1_str)
            
            elif operacion == "Factorizar":
                res = factorizar_expresion(p1_str)
                
            elif operacion == "Simplificar":
                res = simplificar_expresion(p1_str)
                
            else:
                # Operaciones binarias (Suma, Resta, Mult, Div)
                p2_str = self.ent_p2.get()
                if not p2_str: 
                    # Si está vacío, asumimos 0 para suma/resta o 1 para mult/div? 
                    # Mejor avisar al usuario
                    raise ValueError("Para esta operación necesitas la segunda expresión Q(x).")
                
                res = operar_polinomios(p1_str, p2_str, operacion)
            
            # Renderizar Pasos
            if res.get('pasos'):
                self._renderizar_pasos(res['pasos'])
            
            # Renderizar Resultado Final
            if res['estado'] == 'exito':
                # Preferimos mostrar el resultado matemático limpio
                texto_final = res.get('resultado_latex', res.get('resultado_math', 'Exito'))
                # Limpieza simple de notación LaTeX para visualización básica si no hay render
                texto_final = texto_final.replace('\\cdot', '*').replace('\\frac', 'Div').replace('{', '(').replace('}', ')')
                
                self.resultado_caja.insert('0.0', texto_final)
            else:
                self.resultado_caja.insert('0.0', f"Error:\n{res['mensaje']}")
                
        except ValueError as e:
            self.resultado_caja.insert('0.0', f"Error de entrada: {e}")
        except Exception as e:
            self.resultado_caja.insert('0.0', f"Error inesperado: {e}")
            
        self.resultado_caja.configure(state="disabled")