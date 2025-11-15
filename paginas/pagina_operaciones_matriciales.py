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
        self.crear_interfaz()
        self.after(100, self.generar_cuadriculas_operaciones)
    
    def configurar_grid(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1) 
        self.grid_columnconfigure(0, weight=1)
    
    def crear_interfaz(self):
        # Selector de Operacion
        marco_operacion = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_operacion.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        
        ctk.CTkLabel(marco_operacion, text="Operacion:", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=(12, 8), pady=12)
        
        self.operacion_matricial_var = ctk.StringVar(value="Suma")
        operaciones = ["Suma", "Resta", "Multiplicacion"]
        
        for i, operacion in enumerate(operaciones):
            rb = ctk.CTkRadioButton(marco_operacion, text=operacion, variable=self.operacion_matricial_var, 
                                   value=operacion, font=ctk.CTkFont(size=13))
            rb.grid(row=0, column=i+1, padx=8, pady=12)

        # Marco para matrices
        marco_matrices = ctk.CTkFrame(self)
        marco_matrices.grid(row=1, column=0, sticky="nsew", padx=12, pady=8)
        marco_matrices.grid_columnconfigure(0, weight=1)
        marco_matrices.grid_columnconfigure(1, weight=1)
        marco_matrices.grid_rowconfigure(0, weight=1)
        
        # --- Matriz A ---
        self.marco_a = ctk.CTkFrame(marco_matrices, fg_color=COLOR_FONDO_SECUNDARIO)
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
        self.var_filas_a = ctk.StringVar(value="2")
        self.ent_filas_a = ctk.CTkEntry(marco_dims_a, width=60, textvariable=self.var_filas_a)
        self.ent_filas_a.grid(row=0, column=1, padx=(0, 12))
        ctk.CTkLabel(marco_dims_a, text="Columnas:", font=ctk.CTkFont(size=13)).grid(row=0, column=2, padx=(0, 4))
        self.var_columnas_a = ctk.StringVar(value="2")
        self.ent_columnas_a = ctk.CTkEntry(marco_dims_a, width=60, textvariable=self.var_columnas_a)
        self.ent_columnas_a.grid(row=0, column=3)
        marco_escalar_a = ctk.CTkFrame(self.marco_a, fg_color="transparent")
        marco_escalar_a.grid(row=2, column=0, sticky="ew", padx=8, pady=(4, 8))
        ctk.CTkLabel(marco_escalar_a, text="Escalar α:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=(0, 4))
        self.ent_coef_a = ctk.CTkEntry(marco_escalar_a, width=80)
        self.ent_coef_a.insert(0, "1")
        self.ent_coef_a.grid(row=0, column=1)
        self.marco_grilla_a = ctk.CTkFrame(self.marco_a)
        self.marco_grilla_a.grid(row=3, column=0, sticky="nsew", padx=8, pady=(0, 8))

        # --- Matriz B ---
        self.marco_b = ctk.CTkFrame(marco_matrices, fg_color=COLOR_FONDO_SECUNDARIO)
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
        self.var_filas_b = ctk.StringVar(value="2")
        self.ent_filas_b = ctk.CTkEntry(marco_dims_b, width=60, textvariable=self.var_filas_b)
        self.ent_filas_b.grid(row=0, column=1, padx=(0, 12))
        ctk.CTkLabel(marco_dims_b, text="Columnas:", font=ctk.CTkFont(size=13)).grid(row=0, column=2, padx=(0, 4))
        self.var_columnas_b = ctk.StringVar(value="2")
        self.ent_columnas_b = ctk.CTkEntry(marco_dims_b, width=60, textvariable=self.var_columnas_b)
        self.ent_columnas_b.grid(row=0, column=3)
        marco_escalar_b = ctk.CTkFrame(self.marco_b, fg_color="transparent")
        marco_escalar_b.grid(row=2, column=0, sticky="ew", padx=8, pady=(4, 8))
        ctk.CTkLabel(marco_escalar_b, text="Escalar β:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=(0, 4))
        self.ent_coef_b = ctk.CTkEntry(marco_escalar_b, width=80)
        self.ent_coef_b.insert(0, "1")
        self.ent_coef_b.grid(row=0, column=1)
        self.marco_grilla_b = ctk.CTkFrame(self.marco_b)
        self.marco_grilla_b.grid(row=3, column=0, sticky="nsew", padx=8, pady=(0, 8))

        self.entradas_a = []; self.entradas_b = []
        self.grilla_a = []; self.grilla_b = []
        self.matriz_a_visible = True; self.matriz_b_visible = True

        # --- Controles ---
        marco_controles = ctk.CTkFrame(self)
        marco_controles.grid(row=2, column=0, sticky="ew", padx=12, pady=8)
        ctk.CTkButton(marco_controles, text="Generar Cuadriculas", command=self.generar_cuadriculas_operaciones, fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        ctk.CTkButton(marco_controles, text="Calcular Operacion", command=self.calcular_operacion_matricial, fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=1, padx=6)
        ctk.CTkButton(marco_controles, text="Limpiar", command=self.limpiar_operaciones, fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=2, padx=6)

        # --- Resultados ---
        marco_resultados = ctk.CTkFrame(self)
        marco_resultados.grid(row=3, column=0, sticky="nsew", padx=12, pady=(0, 12))
        marco_resultados.grid_rowconfigure(0, weight=1)
        marco_resultados.grid_columnconfigure(0, weight=2)
        marco_resultados.grid_columnconfigure(1, weight=1)

        # Bitácora (ScrollableFrame)
        marco_pasos = ctk.CTkFrame(marco_resultados)
        marco_pasos.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=8)
        marco_pasos.grid_columnconfigure(0, weight=1)
        marco_pasos.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(marco_pasos, text="Bitacora Paso a Paso", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        self.pasos_scroll_frame = ctk.CTkScrollableFrame(marco_pasos, fg_color=COLOR_FONDO_SECUNDARIO)
        self.pasos_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.pasos_scroll_frame.grid_columnconfigure(0, weight=1)

        # Resultado (Resaltado)
        marco_resultado = ctk.CTkFrame(marco_resultados)
        marco_resultado.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=8)
        marco_resultado.grid_columnconfigure(0, weight=1)
        marco_resultado.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(marco_resultado, text="Resultado Final", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        self.resultado_caja = ctk.CTkTextbox(marco_resultado, 
                                             font=ctk.CTkFont(family="monospace", size=14, weight="bold"),
                                             border_color=COLOR_ALGEBRA[1],
                                             border_width=2,
                                             wrap="none")
        self.resultado_caja.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.resultado_caja.configure(state="disabled")

    # --- Funciones de UI para "Paso a Paso" ---
    
    def _limpiar_pasos_scroll(self):
        for widget in self.pasos_scroll_frame.winfo_children():
            widget.destroy()
            
    def _crear_bloque_texto(self, titulo: str, math: str):
        paso_frame = ctk.CTkFrame(self.pasos_scroll_frame, fg_color="transparent")
        paso_frame.pack(fill="x", pady=(0, 10))
        lbl_titulo = ctk.CTkLabel(paso_frame, text=titulo.upper(), 
                                  font=ctk.CTkFont(size=12, weight="bold"),
                                  text_color=COLOR_ALGEBRA[0])
        lbl_titulo.pack(anchor="w", padx=5)
        lbl_math = ctk.CTkLabel(paso_frame, text=math, 
                                font=ctk.CTkFont(family="monospace", size=13), 
                                justify="left")
        lbl_math.pack(anchor="w", padx=20, pady=2)
        
    def _matriz_a_pretty(self, M):
        try: return sp.pretty(sp.Matrix(M), use_unicode=False) # CORRECCIÓN: use_unicode=False
        except Exception: return str(M)

    def _renderizar_pasos(self, pasos_lista: List[Dict[str, str]]):
        self._limpiar_pasos_scroll()
        for paso in pasos_lista:
            self._crear_bloque_texto(titulo=paso['titulo'], math=paso['math'])
            
    # --- Funciones de Lógica ---
    
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
                raise ValueError("Las dimensiones deben ser numeros enteros positivos")

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
                    e.insert(0, f"{i+1}{j+1}")
            for i in range(filas_b):
                for j in range(cols_b):
                    e2 = ctk.CTkEntry(self.marco_grilla_b, width=60)
                    e2.grid(row=i, column=j, padx=2, pady=2)
                    self.grilla_b.append(e2)
                    self.entradas_b[i][j] = e2
                    e2.insert(0, f"{i+1}{j+1}")
            self.limpiar_operaciones()
        except ValueError as e:
            self.resultado_caja.configure(state="normal")
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f'Error: {e}')
            self.resultado_caja.configure(state="disabled")

    def leer_entradas_cuadricula(self, entradas):
        if not entradas or len(entradas) == 0: raise ValueError("Primero debe generar la matriz")
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
                        except ValueError as e: raise ValueError(f'Valor invalido en ({i+1},{j+1}): {e}')
        if celdas_no_vacias == 0 and filas * cols > 0: raise ValueError("La matriz no puede estar vacia")
        return matriz

    def leer_escalar(self, e):
        t = e.get().strip() if e else ''
        if t in ('','+'): return 1.0
        if t == '-': return -1.0
        try: return parse_valor(t)
        except ValueError as err: raise ValueError(f"Valor de escalar invalido: {err}")

    def calcular_operacion_matricial(self):
        self._limpiar_pasos_scroll()
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete('0.0','end')
        
        pasos: List[Dict[str, str]] = []
        
        try:
            A = self.leer_entradas_cuadricula(self.entradas_a)
            B = self.leer_entradas_cuadricula(self.entradas_b)
            fa, ca = len(A), len(A[0]) if A else 0
            fb, cb = len(B), len(B[0]) if B else 0
            
            pasos.append({
                'titulo': "Matrices de Entrada:",
                'math': f"Matriz A ({fa}x{ca}):\n{self._matriz_a_pretty(A)}\n\nMatriz B ({fb}x{cb}):\n{self._matriz_a_pretty(B)}"
            })

            operacion = self.operacion_matricial_var.get()
            R = []
            
            if operacion in ('Suma','Resta'):
                alpha = self.leer_escalar(self.ent_coef_a)
                beta = self.leer_escalar(self.ent_coef_b)
                sgn = 1.0 if operacion=='Suma' else -1.0
                if fa != fb or ca != cb: raise ValueError(f"Para {operacion.lower()}: dims(A)={fa}x{ca} != dims(B)={fb}x{cb}")

                Aesc = [[alpha*A[i][j] for j in range(ca)] for i in range(fa)]
                Besc = [[sgn*beta*B[i][j] for j in range(cb)] for i in range(fb)]
                R = [[Aesc[i][j]+Besc[i][j] for j in range(ca)] for i in range(fa)]
                
                pasos.append({'titulo': f"Paso 1: Calcular α·A (α={fmt(alpha)})", 'math': self._matriz_a_pretty(Aesc)})
                op_str = '+' if sgn>0 else '-'
                pasos.append({'titulo': f"Paso 2: Calcular {op_str} β·B (β={fmt(beta)})", 'math': self._matriz_a_pretty(Besc)})
                pasos.append({'titulo': f"Paso 3: Resultado C = (α·A) {op_str} (β·B)", 'math': self._matriz_a_pretty(R)})

            elif operacion == 'Multiplicacion':
                if ca != fb: raise ValueError(f"Para multiplicacion: cols(A)={ca} != filas(B)={fb}")
                R = [[sum(A[i][k]*B[k][j] for k in range(ca)) for j in range(cb)] for i in range(fa)]
                
                terms = [f'({fmt(A[0][k])})·({fmt(B[k][0])})' for k in range(ca)]
                pasos.append({
                    'titulo': "Calculando C = A·B (ejemplo C[1,1]):",
                    'math': f"C[1,1] = {' + '.join(terms)} = {fmt(R[0][0])}"
                })
                pasos.append({'titulo': "Resultado Final (C = A·B):", 'math': self._matriz_a_pretty(R)})
            else:
                raise ValueError('Operacion desconocida')
            
            self._renderizar_pasos(pasos)
            self.resultado_caja.insert('0.0', self._matriz_a_pretty(R))

        except ValueError as e:
            self.resultado_caja.insert('0.0', f'Error: {e}')
        except Exception as e:
            self.resultado_caja.insert('0.0', f'Error inesperado al calcular: {e}')
            
        self.resultado_caja.configure(state="disabled")


    def limpiar_operaciones(self):
        for fila in self.entradas_a:
            for entrada in fila:
                if entrada: entrada.delete(0,'end')
        for fila in self.entradas_b:
            for entrada in fila:
                if entrada: entrada.delete(0,'end')
        
        for i in range(len(self.entradas_a)):
            for j in range(len(self.entradas_a[i])):
                self.entradas_a[i][j].insert(0, f"{i+1}{j+1}")
        for i in range(len(self.entradas_b)):
            for j in range(len(self.entradas_b[i])):
                self.entradas_b[i][j].insert(0, f"{i+1}{j+1}")
        
        self._limpiar_pasos_scroll()
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete('0.0','end')
        self.resultado_caja.configure(state="disabled")
        
        self.ent_coef_a.delete(0, 'end'); self.ent_coef_a.insert(0, "1")
        self.ent_coef_b.delete(0, 'end'); self.ent_coef_b.insert(0, "1")

    def mostrar(self):
        self.grid(row=0, column=0, sticky="nsew")
        self.after(100, self.generar_cuadriculas_operaciones)