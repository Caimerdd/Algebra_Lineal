import customtkinter as ctk
import sympy as sp
from paginas.pagina_base import PaginaBase
from app_config import (COLOR_FONDO_SECUNDARIO, COLOR_ALGEBRA, COLOR_HOVER, 
                        COLOR_BOTON_SECUNDARIO, COLOR_BOTON_SECUNDARIO_HOVER)
from app_config import fmt, parse_valor
from typing import List, Dict, Any

class PaginaOperacionesMatriciales(PaginaBase):
    def crear_widgets(self):
        self.configurar_grid()
        self.crear_barra_navegacion()
        self.crear_interfaz()
        self.after(100, self.generar_cuadriculas_operaciones)
    
    def configurar_grid(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0) 
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def crear_barra_navegacion(self):
        marco_nav = ctk.CTkFrame(self, fg_color="transparent", height=40)
        marco_nav.grid(row=0, column=0, sticky="ew", padx=12, pady=(8,0))
        
        btn_sistemas = ctk.CTkButton(marco_nav, text="Sistemas de Ecuaciones", 
                                     fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, height=30,
                                     command=lambda: self.app.mostrar_pagina("sistemas_ecuaciones"))
        btn_sistemas.pack(side="left", padx=(0, 5), expand=True, fill="x")
        
        btn_ops = ctk.CTkButton(marco_nav, text="Operaciones Matriciales", 
                                fg_color=COLOR_ALGEBRA, state="disabled", text_color_disabled=("white", "white"), height=30)
        btn_ops.pack(side="left", padx=5, expand=True, fill="x")
        
        btn_props = ctk.CTkButton(marco_nav, text="Propiedades", 
                                  fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, height=30,
                                  command=lambda: self.app.mostrar_pagina("propiedades_matrices"))
        btn_props.pack(side="left", padx=(5, 0), expand=True, fill="x")
    
    def crear_interfaz(self):
        # --- Selector de Operacion ---
        marco_operacion = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_operacion.grid(row=1, column=0, sticky="ew", padx=12, pady=8)
        
        ctk.CTkLabel(marco_operacion, text="Operación:", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=(12, 8), pady=12)
        
        self.operacion_matricial_var = ctk.StringVar(value="Multiplicacion")
        
        operaciones = [
            "Suma", "Resta", "Multiplicacion", 
            "Transpuesta (A)", "Inversa (A)", "Personalizada"
        ]
        
        frame_radios = ctk.CTkFrame(marco_operacion, fg_color="transparent")
        frame_radios.grid(row=0, column=1, padx=10, pady=5)
        
        for i, operacion in enumerate(operaciones):
            rb = ctk.CTkRadioButton(frame_radios, text=operacion, variable=self.operacion_matricial_var, 
                                   value=operacion, font=ctk.CTkFont(size=13),
                                   command=self._actualizar_ui_operacion)
            fila = 0 if i < 3 else 1
            col = i if i < 3 else i - 3
            rb.grid(row=fila, column=col, padx=8, pady=5, sticky="w")

        # --- ETIQUETA DINÁMICA DE AYUDA ---
        self.lbl_info_op = ctk.CTkLabel(marco_operacion, text="", 
                                       font=ctk.CTkFont(size=12, slant="italic"),
                                       text_color="gray70")
        self.lbl_info_op.grid(row=1, column=0, columnspan=2, pady=(0, 8), sticky="ew")

        # --- Entrada de Operación Personalizada ---
        self.marco_custom = ctk.CTkFrame(self, fg_color="transparent")
        self.marco_custom.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 8))
        self.marco_custom.grid_remove() 
        
        ctk.CTkLabel(self.marco_custom, text="Fórmula:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
        self.ent_expresion_custom = ctk.CTkEntry(self.marco_custom, placeholder_text="Ej: A + eye(3)  o  A.T * B", width=400)
        self.ent_expresion_custom.pack(side="left", padx=5, expand=True, fill="x")
        
        ctk.CTkButton(self.marco_custom, text="?", width=30, 
                     command=lambda: self.resultado_caja.configure(state="normal") or self.resultado_caja.delete('0.0','end') or self.resultado_caja.insert('0.0', "Sintaxis:\n- A, B: Matrices\n- A.T: Transpuesta\n- A.inv(): Inversa\n- eye(n): Identidad\n- ones(n): Matriz de 1s\nEj: A + eye(3)") or self.resultado_caja.configure(state="disabled"),
                     fg_color=COLOR_BOTON_SECUNDARIO).pack(side="left", padx=2)

        # --- Marco para matrices ---
        self.marco_matrices = ctk.CTkFrame(self)
        self.marco_matrices.grid(row=3, column=0, sticky="nsew", padx=12, pady=8)
        self.marco_matrices.grid_columnconfigure(0, weight=1)
        self.marco_matrices.grid_columnconfigure(1, weight=1)
        self.marco_matrices.grid_rowconfigure(0, weight=1)
        
        # --- Matriz A ---
        self.marco_a = ctk.CTkFrame(self.marco_matrices, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_a.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=4)
        self.marco_a.grid_rowconfigure(3, weight=1)
        
        header_a = ctk.CTkFrame(self.marco_a, fg_color="transparent")
        header_a.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        header_a.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header_a, text="Matriz A", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky="w")
        self.btn_expandir_a = ctk.CTkButton(header_a, text="−", width=30, height=30, command=lambda: self.toggle_matriz_visibility('a'), fg_color=COLOR_BOTON_SECUNDARIO)
        self.btn_expandir_a.grid(row=0, column=1, sticky="e")
        
        marco_dims_a = ctk.CTkFrame(self.marco_a, fg_color="transparent")
        marco_dims_a.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        ctk.CTkLabel(marco_dims_a, text="Filas:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=(0, 4))
        self.var_filas_a = ctk.StringVar(value="3")
        self.ent_filas_a = ctk.CTkEntry(marco_dims_a, width=60, textvariable=self.var_filas_a)
        self.ent_filas_a.grid(row=0, column=1, padx=(0, 12))
        ctk.CTkLabel(marco_dims_a, text="Cols:", font=ctk.CTkFont(size=13)).grid(row=0, column=2, padx=(0, 4))
        self.var_columnas_a = ctk.StringVar(value="3")
        self.ent_columnas_a = ctk.CTkEntry(marco_dims_a, width=60, textvariable=self.var_columnas_a)
        self.ent_columnas_a.grid(row=0, column=3)
        
        self.marco_escalar_a = ctk.CTkFrame(self.marco_a, fg_color="transparent")
        self.marco_escalar_a.grid(row=2, column=0, sticky="ew", padx=8, pady=(4, 8))
        ctk.CTkLabel(self.marco_escalar_a, text="Escalar α:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=(0, 4))
        self.ent_coef_a = ctk.CTkEntry(self.marco_escalar_a, width=80)
        self.ent_coef_a.insert(0, "1")
        self.ent_coef_a.grid(row=0, column=1)
        
        self.marco_grilla_a = ctk.CTkFrame(self.marco_a)
        self.marco_grilla_a.grid(row=3, column=0, sticky="nsew", padx=8, pady=(0, 8))

        # --- Matriz B ---
        self.marco_b = ctk.CTkFrame(self.marco_matrices, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_b.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=4)
        self.marco_b.grid_rowconfigure(3, weight=1)
        
        header_b = ctk.CTkFrame(self.marco_b, fg_color="transparent")
        header_b.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        header_b.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header_b, text="Matriz B", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky="w")
        self.btn_expandir_b = ctk.CTkButton(header_b, text="−", width=30, height=30, command=lambda: self.toggle_matriz_visibility('b'), fg_color=COLOR_BOTON_SECUNDARIO)
        self.btn_expandir_b.grid(row=0, column=1, sticky="e")
        
        marco_dims_b = ctk.CTkFrame(self.marco_b, fg_color="transparent")
        marco_dims_b.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        ctk.CTkLabel(marco_dims_b, text="Filas:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=(0, 4))
        self.var_filas_b = ctk.StringVar(value="3")
        self.ent_filas_b = ctk.CTkEntry(marco_dims_b, width=60, textvariable=self.var_filas_b)
        self.ent_filas_b.grid(row=0, column=1, padx=(0, 12))
        ctk.CTkLabel(marco_dims_b, text="Cols:", font=ctk.CTkFont(size=13)).grid(row=0, column=2, padx=(0, 4))
        self.var_columnas_b = ctk.StringVar(value="3")
        self.ent_columnas_b = ctk.CTkEntry(marco_dims_b, width=60, textvariable=self.var_columnas_b)
        self.ent_columnas_b.grid(row=0, column=3)
        
        self.marco_escalar_b = ctk.CTkFrame(self.marco_b, fg_color="transparent")
        self.marco_escalar_b.grid(row=2, column=0, sticky="ew", padx=8, pady=(4, 8))
        ctk.CTkLabel(self.marco_escalar_b, text="Escalar β:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=(0, 4))
        self.ent_coef_b = ctk.CTkEntry(self.marco_escalar_b, width=80)
        self.ent_coef_b.insert(0, "1")
        self.ent_coef_b.grid(row=0, column=1)
        
        self.marco_grilla_b = ctk.CTkFrame(self.marco_b)
        self.marco_grilla_b.grid(row=3, column=0, sticky="nsew", padx=8, pady=(0, 8))

        self.entradas_a = []; self.entradas_b = []
        self.grilla_a = []; self.grilla_b = []
        self.matriz_a_visible = True; self.matriz_b_visible = True

        # --- Controles ---
        marco_controles = ctk.CTkFrame(self)
        marco_controles.grid(row=4, column=0, sticky="ew", padx=12, pady=8)
        ctk.CTkButton(marco_controles, text="Generar Cuadrículas", command=self.generar_cuadriculas_operaciones, fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        ctk.CTkButton(marco_controles, text="Calcular", command=self.calcular_operacion_matricial, fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=1, padx=6)
        ctk.CTkButton(marco_controles, text="Limpiar", command=self.limpiar_operaciones, fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=2, padx=6)
        ctk.CTkButton(marco_controles, text="Ayuda ❓", command=lambda: self.app.mostrar_ayuda_sympy(), fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, width=80).grid(row=0, column=3, padx=6)

        # --- Resultados ---
        marco_resultados = ctk.CTkFrame(self)
        marco_resultados.grid(row=5, column=0, sticky="nsew", padx=12, pady=(0, 12))
        marco_resultados.grid_rowconfigure(0, weight=1)
        marco_resultados.grid_columnconfigure(0, weight=2)
        marco_resultados.grid_columnconfigure(1, weight=1)

        marco_pasos = ctk.CTkFrame(marco_resultados)
        marco_pasos.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=8)
        marco_pasos.grid_columnconfigure(0, weight=1)
        marco_pasos.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(marco_pasos, text="Bitácora Paso a Paso", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        self.pasos_scroll_frame = ctk.CTkScrollableFrame(marco_pasos, fg_color=COLOR_FONDO_SECUNDARIO)
        self.pasos_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.pasos_scroll_frame.grid_columnconfigure(0, weight=1)

        marco_resultado = ctk.CTkFrame(marco_resultados)
        marco_resultado.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=8)
        marco_resultado.grid_columnconfigure(0, weight=1)
        marco_resultado.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(marco_resultado, text="Resultado Final", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        self.resultado_caja = ctk.CTkTextbox(marco_resultado, 
                                             font=ctk.CTkFont(family="monospace", size=14, weight="bold"),
                                             border_color=COLOR_ALGEBRA[1],
                                             border_width=2,
                                             wrap="word")
        self.resultado_caja.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.resultado_caja.configure(state="disabled")
        
        # Iniciar texto
        self._actualizar_ui_operacion()

    # --- UI Helpers ---
    def _limpiar_pasos_scroll(self):
        for widget in self.pasos_scroll_frame.winfo_children(): widget.destroy()
            
    def _crear_bloque_texto(self, titulo: str, math: str):
        paso_frame = ctk.CTkFrame(self.pasos_scroll_frame, fg_color="transparent")
        paso_frame.pack(fill="x", pady=(0, 10))
        lbl_titulo = ctk.CTkLabel(paso_frame, text=titulo.upper(), font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_ALGEBRA[0])
        lbl_titulo.pack(anchor="w", padx=5)
        lbl_math = ctk.CTkLabel(paso_frame, text=math, font=ctk.CTkFont(family="monospace", size=13), justify="left")
        lbl_math.pack(anchor="w", padx=20, pady=2)
        
    def _matriz_a_pretty(self, M):
        try: return sp.pretty(sp.Matrix(M), use_unicode=False)
        except Exception: return str(M)

    def _renderizar_pasos(self, pasos_lista: List[Dict[str, str]]):
        self._limpiar_pasos_scroll()
        for paso in pasos_lista:
            self._crear_bloque_texto(titulo=paso['titulo'], math=paso['math'])
            
    # --- Lógica de Visibilidad, Estado y Ayuda Dinámica ---
    
    def _actualizar_ui_operacion(self):
        op = self.operacion_matricial_var.get()
        texto_ayuda = ""
        
        # Configurar visibilidad y texto
        if op == "Suma":
            texto_ayuda = "Suma elemento a elemento: Cij = αAij + βBij. (Requiere mismas dimensiones)."
            self._set_visibilidad_estandar()
        elif op == "Resta":
            texto_ayuda = "Resta elemento a elemento: Cij = αAij - βBij. (Requiere mismas dimensiones)."
            self._set_visibilidad_estandar()
        elif op == "Multiplicacion":
            texto_ayuda = "Producto Matricial: C = A · B. (Columnas de A deben igualar Filas de B)."
            self._set_visibilidad_estandar()
        elif op == "Transpuesta (A)":
            texto_ayuda = "Intercambia filas por columnas (Aᵀ). B se ignora."
            self.marco_b.grid_remove(); self.marco_custom.grid_remove(); self.marco_escalar_a.grid()
        elif op == "Inversa (A)":
            texto_ayuda = "Calcula la matriz A⁻¹ tal que A · A⁻¹ = I. (A debe ser cuadrada y Det ≠ 0)."
            self.marco_b.grid_remove(); self.marco_custom.grid_remove(); self.marco_escalar_a.grid()
        elif op == "Personalizada":
            texto_ayuda = "Escriba su propia fórmula usando A, B, inv(), eye(), etc."
            self.marco_b.grid(); self.marco_custom.grid(); self.marco_escalar_a.grid_remove(); self.marco_escalar_b.grid_remove()
            
        self.lbl_info_op.configure(text=texto_ayuda)

    def _set_visibilidad_estandar(self):
        self.marco_b.grid()
        self.marco_custom.grid_remove()
        self.marco_escalar_a.grid()
        self.marco_escalar_b.grid()

    def toggle_matriz_visibility(self, matriz: str):
        if matriz == 'a':
            self.matriz_a_visible = not self.matriz_a_visible
            if self.matriz_a_visible:
                self.marco_grilla_a.grid()
                self.btn_expandir_a.configure(text="−")
            else:
                self.marco_grilla_a.grid_remove()
                self.btn_expandir_a.configure(text="+")
        elif matriz == 'b':
            self.matriz_b_visible = not self.matriz_b_visible
            if self.matriz_b_visible:
                self.marco_grilla_b.grid()
                self.btn_expandir_b.configure(text="−")
            else:
                self.marco_grilla_b.grid_remove()
                self.btn_expandir_b.configure(text="+")

    def generar_cuadriculas_operaciones(self):
        try:
            filas_a = int(self.ent_filas_a.get())
            cols_a = int(self.ent_columnas_a.get())
            filas_b = int(self.ent_filas_b.get())
            cols_b = int(self.ent_columnas_b.get())
            if filas_a <= 0 or cols_a <= 0 or filas_b <= 0 or cols_b <= 0:
                raise ValueError("Dimensiones deben ser enteros positivos")

            for widget in self.marco_grilla_a.winfo_children(): widget.destroy()
            for widget in self.marco_grilla_b.winfo_children(): widget.destroy()
            self.entradas_a = [[None for _ in range(cols_a)] for _ in range(filas_a)]
            self.entradas_b = [[None for _ in range(cols_b)] for _ in range(filas_b)]
            self.grilla_a, self.grilla_b = [], []

            for i in range(filas_a):
                for j in range(cols_a):
                    e = ctk.CTkEntry(self.marco_grilla_a, width=60)
                    e.grid(row=i, column=j, padx=2, pady=2)
                    self.grilla_a.append(e)
                    self.entradas_a[i][j] = e
            for i in range(filas_b):
                for j in range(cols_b):
                    e2 = ctk.CTkEntry(self.marco_grilla_b, width=60)
                    e2.grid(row=i, column=j, padx=2, pady=2)
                    self.grilla_b.append(e2)
                    self.entradas_b[i][j] = e2
            self.limpiar_operaciones(borrar_entradas=False)
            self._actualizar_ui_operacion()
            
        except ValueError as e:
            self.resultado_caja.configure(state="normal")
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f'Error: {e}')
            self.resultado_caja.configure(state="disabled")

    def leer_entradas_cuadricula(self, entradas):
        if not entradas or len(entradas) == 0: return None
        filas = len(entradas); cols = len(entradas[0]) if filas > 0 else 0
        matriz = [[0.0 for _ in range(cols)] for _ in range(filas)]
        celdas_no_vacias = 0
        for i in range(filas):
            for j in range(cols):
                if entradas[i][j] is not None:
                    texto = entradas[i][j].get().strip()
                    if texto:
                        celdas_no_vacias += 1
                        try: matriz[i][j] = parse_valor(texto)
                        except ValueError: raise ValueError(f'Valor inválido en ({i+1},{j+1})')
        if celdas_no_vacias == 0: return None
        return matriz

    def leer_escalar(self, e):
        t = e.get().strip() if e else ''
        if t in ('','+'): return 1.0
        if t == '-': return -1.0
        try: return parse_valor(t)
        except ValueError as err: raise ValueError(f"Escalar inválido: {err}")

    def calcular_operacion_matricial(self):
        self._limpiar_pasos_scroll()
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete('0.0','end')
        
        pasos: List[Dict[str, str]] = []
        operacion = self.operacion_matricial_var.get()
        
        try:
            A_raw = self.leer_entradas_cuadricula(self.entradas_a) if self.matriz_a_visible else None
            B_raw = self.leer_entradas_cuadricula(self.entradas_b) if self.matriz_b_visible else None
            
            if operacion in ["Transpuesta (A)", "Inversa (A)"]: B_raw = None

            texto_entrada = ""
            if A_raw: texto_entrada += f"Matriz A ({len(A_raw)}x{len(A_raw[0])}):\n{self._matriz_a_pretty(A_raw)}\n\n"
            if B_raw: texto_entrada += f"Matriz B ({len(B_raw)}x{len(B_raw[0])}):\n{self._matriz_a_pretty(B_raw)}"
            
            if not A_raw and not B_raw: raise ValueError("No hay matrices activas.")
            pasos.append({'titulo': "Matrices de Entrada:", 'math': texto_entrada})

            if operacion == "Personalizada":
                expr_str = self.ent_expresion_custom.get().strip()
                if not expr_str: raise ValueError("Escriba una expresión.")
                sym_A = sp.Matrix(A_raw) if A_raw else sp.zeros(1)
                sym_B = sp.Matrix(B_raw) if B_raw else sp.zeros(1)
                
                local_dict = {'A': sym_A, 'B': sym_B, 'sp': sp, 'inv': lambda m: m.inv(), 'det': lambda m: m.det(), 'T': lambda m: m.T, 'eye': sp.eye, 'ones': sp.ones, 'zeros': sp.zeros}
                try:
                    res_sym = sp.sympify(expr_str, locals=local_dict)
                    if isinstance(res_sym, sp.Matrix):
                        res_final = res_sym.tolist()
                        pasos.append({'titulo': f"Evaluando: {expr_str}", 'math': self._matriz_a_pretty(res_final)})
                        self.resultado_caja.insert('0.0', self._matriz_a_pretty(res_final))
                    else:
                        self.resultado_caja.insert('0.0', str(res_sym))
                except Exception as e: raise ValueError(f"Error en fórmula: {e}")

            elif operacion == "Transpuesta (A)":
                if not A_raw: raise ValueError("Matriz A requerida.")
                res = sp.Matrix(A_raw).T.tolist()
                alpha = self.leer_escalar(self.ent_coef_a)
                if alpha != 1: res = [[alpha * c for c in r] for r in res]
                pasos.append({'titulo': "Resultado:", 'math': self._matriz_a_pretty(res)})
                self.resultado_caja.insert('0.0', self._matriz_a_pretty(res))

            elif operacion == "Inversa (A)":
                if not A_raw: raise ValueError("Matriz A requerida.")
                try:
                    res = sp.Matrix(A_raw).inv().tolist()
                    pasos.append({'titulo': "Inversa A⁻¹:", 'math': self._matriz_a_pretty(res)})
                    self.resultado_caja.insert('0.0', self._matriz_a_pretty(res))
                except Exception: raise ValueError("La matriz A no es invertible.")

            else:
                R = []
                alpha = self.leer_escalar(self.ent_coef_a)
                beta = self.leer_escalar(self.ent_coef_b)
                sgn = 1.0 if operacion=='Suma' else -1.0

                if A_raw and not B_raw:
                    R = [[alpha*A_raw[i][j] for j in range(len(A_raw[0]))] for i in range(len(A_raw))]
                    pasos.append({'titulo': f"Operación (Solo A): α·A", 'math': self._matriz_a_pretty(R)})
                elif B_raw and not A_raw:
                    factor = sgn * beta
                    R = [[factor*B_raw[i][j] for j in range(len(B_raw[0]))] for i in range(len(B_raw))]
                    pasos.append({'titulo': f"Operación (Solo B): ±β·B", 'math': self._matriz_a_pretty(R)})
                else:
                    if operacion in ('Suma','Resta'):
                        fa, ca = len(A_raw), len(A_raw[0])
                        fb, cb = len(B_raw), len(B_raw[0])
                        if fa != fb or ca != cb: raise ValueError(f"Dimensiones incompatibles.")
                        Aesc = [[alpha*A_raw[i][j] for j in range(ca)] for i in range(fa)]
                        Besc = [[sgn*beta*B_raw[i][j] for j in range(cb)] for i in range(fb)]
                        R = [[Aesc[i][j]+Besc[i][j] for j in range(ca)] for i in range(fa)]
                        pasos.append({'titulo': f"Resultado:", 'math': self._matriz_a_pretty(R)})
                    elif operacion == 'Multiplicacion':
                        fa, ca = len(A_raw), len(A_raw[0])
                        fb, cb = len(B_raw), len(B_raw[0])
                        if ca != fb: raise ValueError(f"Error mult: cols(A)={ca} != filas(B)={fb}")
                        R = [[sum(A_raw[i][k]*B_raw[k][j] for k in range(ca)) for j in range(cb)] for i in range(fa)]
                        if alpha != 1 or beta != 1:
                            ft = alpha * beta
                            R = [[ft * c for c in r] for r in R]
                        pasos.append({'titulo': "Resultado (A · B):", 'math': self._matriz_a_pretty(R)})

                self.resultado_caja.insert('0.0', self._matriz_a_pretty(R))

        except ValueError as e:
            self.resultado_caja.insert('0.0', f'Error: {e}')
        except Exception as e:
            self.resultado_caja.insert('0.0', f'Error inesperado: {e}')
            
        self.resultado_caja.configure(state="disabled")
        if pasos: self._renderizar_pasos(pasos)

    def limpiar_operaciones(self, borrar_entradas=True):
        if borrar_entradas:
            for fila in self.entradas_a:
                for entrada in fila:
                    if entrada: entrada.delete(0,'end')
            for fila in self.entradas_b:
                for entrada in fila:
                    if entrada: entrada.delete(0,'end')
        
        self._limpiar_pasos_scroll()
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete('0.0','end')
        self.resultado_caja.configure(state="disabled")
        self.ent_coef_a.delete(0, 'end'); self.ent_coef_a.insert(0, "1")
        self.ent_coef_b.delete(0, 'end'); self.ent_coef_b.insert(0, "1")
        self.ent_expresion_custom.delete(0, 'end')

    def mostrar(self):
        self.grid(row=0, column=0, sticky="nsew")
        self.after(100, self.generar_cuadriculas_operaciones)