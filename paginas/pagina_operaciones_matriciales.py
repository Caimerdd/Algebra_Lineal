import customtkinter as ctk
from paginas.pagina_base import PaginaBase
from app_config import COLOR_FONDO_SECUNDARIO, COLOR_ALGEBRA, COLOR_HOVER, COLOR_BOTON_SECUNDARIO, COLOR_BOTON_SECUNDARIO_HOVER
from app_config import fmt, parse_valor

class PaginaOperacionesMatriciales(PaginaBase):
    def crear_widgets(self):
        self.configurar_grid()
        self.crear_interfaz()
        # Generar cuadrículas iniciales automáticamente
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
        operaciones = ["Suma", "Resta", "Multiplicacion", "Multiplicacion por Escalar"]
        
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
        
        # Matriz A
        self.marco_a = ctk.CTkFrame(marco_matrices, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_a.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=4)
        self.marco_a.grid_rowconfigure(2, weight=1)
        
        header_a = ctk.CTkFrame(self.marco_a, fg_color="transparent")
        header_a.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        header_a.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(header_a, text="Matriz A", 
                    font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky="w")
        
        # Botón expandir A
        self.btn_expandir_a = ctk.CTkButton(header_a, text="−", width=30, height=30,
                                          command=lambda: self.toggle_matriz_visibility('a'),
                                          fg_color=COLOR_BOTON_SECUNDARIO)
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

        # Escalar para A
        marco_escalar_a = ctk.CTkFrame(self.marco_a, fg_color="transparent")
        marco_escalar_a.grid(row=2, column=0, sticky="ew", padx=8, pady=(4, 8))
        ctk.CTkLabel(marco_escalar_a, text="Escalar α:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=(0, 4))
        self.ent_coef_a = ctk.CTkEntry(marco_escalar_a, width=80)
        self.ent_coef_a.insert(0, "1")
        self.ent_coef_a.grid(row=0, column=1)

        # Marco para la cuadrícula de A
        self.marco_grilla_a = ctk.CTkFrame(self.marco_a)
        self.marco_grilla_a.grid(row=3, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.marco_grilla_a.grid_rowconfigure(0, weight=1)
        self.marco_grilla_a.grid_columnconfigure(0, weight=1)

        # Matriz B
        self.marco_b = ctk.CTkFrame(marco_matrices, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_b.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=4)
        self.marco_b.grid_rowconfigure(2, weight=1)
        
        header_b = ctk.CTkFrame(self.marco_b, fg_color="transparent")
        header_b.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        header_b.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(header_b, text="Matriz B", 
                    font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky="w")
        
        # Botón expandir B
        self.btn_expandir_b = ctk.CTkButton(header_b, text="−", width=30, height=30,
                                          command=lambda: self.toggle_matriz_visibility('b'),
                                          fg_color=COLOR_BOTON_SECUNDARIO)
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

        # Escalar para B
        marco_escalar_b = ctk.CTkFrame(self.marco_b, fg_color="transparent")
        marco_escalar_b.grid(row=2, column=0, sticky="ew", padx=8, pady=(4, 8))
        ctk.CTkLabel(marco_escalar_b, text="Escalar β:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=(0, 4))
        self.ent_coef_b = ctk.CTkEntry(marco_escalar_b, width=80)
        self.ent_coef_b.insert(0, "1")
        self.ent_coef_b.grid(row=0, column=1)

        # Marco para la cuadrícula de B
        self.marco_grilla_b = ctk.CTkFrame(self.marco_b)
        self.marco_grilla_b.grid(row=3, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.marco_grilla_b.grid_rowconfigure(0, weight=1)
        self.marco_grilla_b.grid_columnconfigure(0, weight=1)

        # Listas para entradas
        self.entradas_a = []
        self.entradas_b = []
        self.grilla_a = []
        self.grilla_b = []
        
        # Variables de visibilidad
        self.matriz_a_visible = True
        self.matriz_b_visible = True

        # Controles
        marco_controles = ctk.CTkFrame(self)
        marco_controles.grid(row=2, column=0, sticky="ew", padx=12, pady=8)
        
        ctk.CTkButton(marco_controles, text="Generar Cuadriculas", 
                     command=self.generar_cuadriculas_operaciones,
                     fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        
        ctk.CTkButton(marco_controles, text="Calcular Operacion", 
                     command=self.calcular_operacion_matricial,
                     fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=1, padx=6)
        
        ctk.CTkButton(marco_controles, text="Limpiar", 
                     command=self.limpiar_operaciones,
                     fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=2, padx=6)

        # Resultados
        marco_resultados = ctk.CTkFrame(self)
        marco_resultados.grid(row=3, column=0, sticky="nsew", padx=12, pady=(0, 12))
        marco_resultados.grid_rowconfigure(0, weight=1)
        marco_resultados.grid_columnconfigure(0, weight=1)
        marco_resultados.grid_columnconfigure(1, weight=1)

        # Pasos
        marco_pasos = ctk.CTkFrame(marco_resultados)
        marco_pasos.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=8)
        marco_pasos.grid_columnconfigure(0, weight=1)
        marco_pasos.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_pasos, text="Bitacora Paso a Paso", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        
        self.pasos_caja = ctk.CTkTextbox(marco_pasos, font=ctk.CTkFont(family="monospace", size=12))
        self.pasos_caja.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))

        # Resultado
        marco_resultado = ctk.CTkFrame(marco_resultados)
        marco_resultado.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=8)
        marco_resultado.grid_columnconfigure(0, weight=1)
        marco_resultado.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_resultado, text="Resultado Final", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        
        self.resultado_caja = ctk.CTkTextbox(marco_resultado, font=ctk.CTkFont(family="monospace", size=12))
        self.resultado_caja.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))

    def toggle_matriz_visibility(self, matriz: str):
        """Alterna la visibilidad de las matrices."""
        if matriz == 'a':
            if self.matriz_a_visible:
                self.marco_grilla_a.grid_remove()
                self.btn_expandir_a.configure(text="+")
                self.matriz_a_visible = False
            else:
                self.marco_grilla_a.grid()
                self.btn_expandir_a.configure(text="−")
                self.matriz_a_visible = True
        elif matriz == 'b':
            if self.matriz_b_visible:
                self.marco_grilla_b.grid_remove()
                self.btn_expandir_b.configure(text="+")
                self.matriz_b_visible = False
            else:
                self.marco_grilla_b.grid()
                self.btn_expandir_b.configure(text="−")
                self.matriz_b_visible = True

    def generar_cuadriculas_operaciones(self):
        try:
            filas_a = int(self.ent_filas_a.get())
            cols_a = int(self.ent_columnas_a.get())
            filas_b = int(self.ent_filas_b.get())
            cols_b = int(self.ent_columnas_b.get())
            
            if filas_a <= 0 or cols_a <= 0 or filas_b <= 0 or cols_b <= 0:
                raise ValueError("Las dimensiones deben ser numeros enteros positivos")

            print(f"Generando cuadriculas: A({filas_a}x{cols_a}), B({filas_b}x{cols_b})")  # Debug

            # Limpiar cuadriculas existentes
            for widget in self.marco_grilla_a.winfo_children():
                widget.destroy()
            for widget in self.marco_grilla_b.winfo_children():
                widget.destroy()
                
            self.entradas_a = []
            self.entradas_b = []
            self.grilla_a = []
            self.grilla_b = []

            # Inicializar listas
            self.entradas_a = [[None for _ in range(cols_a)] for _ in range(filas_a)]
            self.entradas_b = [[None for _ in range(cols_b)] for _ in range(filas_b)]

            # Crear cuadricula para A
            for i in range(filas_a):
                for j in range(cols_a):
                    e = ctk.CTkEntry(self.marco_grilla_a, width=60)
                    e.grid(row=i, column=j, padx=2, pady=2)
                    self.grilla_a.append(e)
                    self.entradas_a[i][j] = e
                    # Poner valores de ejemplo
                    e.insert(0, f"{i+1}{j+1}")

            # Crear cuadricula para B
            for i in range(filas_b):
                for j in range(cols_b):
                    e2 = ctk.CTkEntry(self.marco_grilla_b, width=60)
                    e2.grid(row=i, column=j, padx=2, pady=2)
                    self.grilla_b.append(e2)
                    self.entradas_b[i][j] = e2
                    # Poner valores de ejemplo
                    e2.insert(0, f"{i+1}{j+1}")

            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f'Matrices generadas: A({filas_a}x{cols_a}), B({filas_b}x{cols_b})')

        except ValueError as e:
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f'Error: {e}')

    def leer_entradas_cuadricula(self, entradas):
        if not entradas or len(entradas) == 0:
            raise ValueError("Primero debe generar la matriz")

        filas = len(entradas)
        cols = len(entradas[0]) if filas > 0 else 0

        matriz = [[0.0 for _ in range(cols)] for _ in range(filas)]
        celdas_no_vacias = 0
        
        for i in range(filas):
            for j in range(cols):
                if entradas[i][j] is not None:
                    texto = entradas[i][j].get().strip()
                    if texto:
                        celdas_no_vacias += 1
                        try:
                            matriz[i][j] = parse_valor(texto)
                        except ValueError as e:
                            raise ValueError(f'Valor invalido en ({i+1},{j+1}): {e}')

        if celdas_no_vacias == 0 and filas * cols > 0:
            raise ValueError("La matriz no puede estar vacia, ingrese al menos un valor.")

        return matriz

    def leer_escalar(self, e):
        t = e.get().strip() if e else ''
        if t in ('','+'): return 1.0
        if t == '-': return -1.0
        try: return parse_valor(t)
        except ValueError as err: raise ValueError(f"Valor de escalar invalido: {err}")

    def append_matriz(self, M, titulo=None):
        if titulo: 
            self.pasos_caja.insert('end', f'{titulo}\n')
        for f in M: 
            self.pasos_caja.insert('end', '  '.join(fmt(v) for v in f) + '\n')
        self.pasos_caja.insert('end', '\n')

    def calcular_operacion_matricial(self):
        try:
            print("Leyendo matriz A...")  # Debug
            A = self.leer_entradas_cuadricula(self.entradas_a)
            print("Leyendo matriz B...")  # Debug
            B = self.leer_entradas_cuadricula(self.entradas_b)
                 
        except ValueError as e:
            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', f'Error de entrada: {e}')
            self.pasos_caja.delete('0.0', 'end')
            return
        except Exception as e:
            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', f'Error inesperado al leer matrices: {e}')
            self.pasos_caja.delete('0.0', 'end')
            return

        operacion = self.operacion_matricial_var.get()
        fa, ca = len(A), len(A[0]) if A else 0
        fb, cb = len(B), len(B[0]) if B else 0
        
        print(f"Calculando {operacion} con A({fa}x{ca}), B({fb}x{cb})")  # Debug
        
        self.pasos_caja.delete('0.0','end')
        try:
            if operacion in ('Suma','Resta'):
                alpha = self.leer_escalar(self.ent_coef_a)
                beta = self.leer_escalar(self.ent_coef_b)
                sgn = 1.0 if operacion=='Suma' else -1.0
                
                if fa != fb or ca != cb:
                    raise ValueError(f"Para {operacion.lower()}: dims(A)={fa}x{ca} != dims(B)={fb}x{cb}")

                Aesc = [[alpha*A[i][j] for j in range(ca)] for i in range(fa)]
                Besc = [[sgn*beta*B[i][j] for j in range(cb)] for i in range(fb)]
                C = [[Aesc[i][j]+Besc[i][j] for j in range(ca)] for i in range(fa)]
                R = C
                
                self.append_matriz(A,'Matriz A:')
                self.append_matriz(B,'Matriz B:')
                self.append_matriz(Aesc, f'α·A (α={fmt(alpha)}):')
                self.append_matriz(Besc, f'{"+" if sgn>0 else "-"} β·B (β={fmt(beta)}):')
                
                for i in range(fa):
                    for j in range(ca):
                        self.pasos_caja.insert('end', f'C[{i+1},{j+1}] = {fmt(alpha)}·{fmt(A[i][j])} {"+" if sgn>0 else "-"} {fmt(beta)}·{fmt(B[i][j])} = {fmt(C[i][j])}\n')
                self.append_matriz(C, 'Resultado C = αA ' + ('+' if sgn>0 else '−') + ' βB:')

            elif operacion == 'Multiplicacion':
                if ca != fb:
                    raise ValueError(f"Para multiplicacion: cols(A)={ca} != filas(B)={fb}")

                C = [[sum(A[i][k]*B[k][j] for k in range(ca)) for j in range(cb)] for i in range(fa)]
                R = C
                
                self.append_matriz(A,'Matriz A:')
                self.append_matriz(B,'Matriz B:')
                
                for i in range(fa):
                    for j in range(cb):
                        terms = [f'{fmt(A[i][k])}·{fmt(B[k][j])}' for k in range(ca)]
                        self.pasos_caja.insert('end', f'C[{i+1},{j+1}] = ' + ' + '.join(terms) + f' = {fmt(C[i][j])}\n')
                self.append_matriz(C,'Resultado C = A·B:')

            elif operacion == 'Multiplicacion por Escalar':
                alpha = self.leer_escalar(self.ent_coef_a)
                C = [[alpha*A[i][j] for j in range(ca)] for i in range(fa)]
                R = C
                
                self.append_matriz(A,'Matriz A:')
                
                for i in range(fa):
                    for j in range(ca):
                        self.pasos_caja.insert('end', f'C[{i+1},{j+1}] = {fmt(alpha)}·{fmt(A[i][j])} = {fmt(C[i][j])}\n')
                self.append_matriz(C, f'Resultado C = {fmt(alpha)}·A:')

            else:
                raise ValueError('Operacion desconocida')

            self.resultado_caja.delete('0.0','end')
            resultado_texto = '\n'.join('  '.join(fmt(v) for v in fila) for fila in R)
            self.resultado_caja.insert('0.0', f"Resultado ({operacion}):\n{resultado_texto}")

        except ValueError as e:
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f'Error: {e}')
        except Exception as e:
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f'Error inesperado al calcular: {e}')

    def limpiar_operaciones(self):
        # Limpiar entradas de matriz A
        for i in range(len(self.entradas_a)):
            for j in range(len(self.entradas_a[i])):
                if self.entradas_a[i][j]:
                    self.entradas_a[i][j].delete(0, 'end')
                    self.entradas_a[i][j].insert(0, f"{i+1}{j+1}")
        
        # Limpiar entradas de matriz B
        for i in range(len(self.entradas_b)):
            for j in range(len(self.entradas_b[i])):
                if self.entradas_b[i][j]:
                    self.entradas_b[i][j].delete(0, 'end')
                    self.entradas_b[i][j].insert(0, f"{i+1}{j+1}")
        
        self.resultado_caja.delete('0.0','end')
        self.pasos_caja.delete('0.0','end')
        self.ent_coef_a.delete(0, 'end')
        self.ent_coef_a.insert(0, "1")
        self.ent_coef_b.delete(0, 'end')
        self.ent_coef_b.insert(0, "1")

    def mostrar(self):
        self.grid(row=0, column=0, sticky="nsew")
        # Regenerar cuadrículas cuando se muestra la página
        self.after(100, self.generar_cuadriculas_operaciones)