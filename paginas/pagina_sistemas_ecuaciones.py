import customtkinter as ctk
import re
import sympy as sp # Para formatear matrices
from paginas.pagina_base import PaginaBase
from app_config import (COLOR_FONDO_SECUNDARIO, COLOR_ALGEBRA, COLOR_HOVER, 
                        COLOR_BOTON_SECUNDARIO, COLOR_BOTON_SECUNDARIO_HOVER)
from app_config import fmt, parse_valor

# Intentamos importar la lógica de tu archivo
try:
    from Complement import (
        gauss_steps, gauss_jordan_steps, inverse_steps, 
        resolver_por_cramer
    )
    LOGICA_DISPONIBLE = True
except ImportError:
    LOGICA_DISPONIBLE = False
    print("ADVERTENCIA: No se pudo cargar Complement.py")

class PaginaSistemasEcuaciones(PaginaBase):
    def crear_widgets(self):
        self.configurar_grid()
        self.crear_interfaz()
        self.generar_cuadriculas_matriz()
    
    def configurar_grid(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=1) # Fila de resultados se expande
        self.grid_columnconfigure(0, weight=1)
    
    def crear_interfaz(self):
        # Selector de Metodo
        marco_metodo = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_metodo.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        
        ctk.CTkLabel(marco_metodo, text="Metodo de Solucion:", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=(12, 8), pady=12)
        
        self.metodo_sistema_var = ctk.StringVar(value="Gauss-Jordan")
        metodos = ["Gauss-Jordan", "Eliminacion Gaussiana", "Regla de Cramer", "Matriz Inversa"]
        
        for i, metodo in enumerate(metodos):
            rb = ctk.CTkRadioButton(marco_metodo, text=metodo, variable=self.metodo_sistema_var, 
                                   value=metodo, font=ctk.CTkFont(size=13))
            rb.grid(row=0, column=i+1, padx=8, pady=12)
        
        # Entrada de Ecuaciones
        marco_ecuaciones = ctk.CTkFrame(self)
        marco_ecuaciones.grid(row=1, column=0, sticky="ew", padx=12, pady=(4, 8))
        marco_ecuaciones.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(marco_ecuaciones, text="Ingrese el sistema de ecuaciones:", 
                    font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=(8, 4))
        
        self.caja_ecuaciones = ctk.CTkTextbox(marco_ecuaciones, height=120, font=ctk.CTkFont(size=13))
        self.caja_ecuaciones.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        self.caja_ecuaciones.insert("0.0", "2x + 3y - z = 5\nx - y + 2z = 10\n3x + 2y = 0")
        
        ctk.CTkButton(marco_ecuaciones, text="Generar Matriz Aumentada", 
                     command=self.parsear_y_poblar_ecuaciones,
                     fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=1, column=1, sticky="ns", padx=(0, 8), pady=(0, 8))

        # Marco para matrices
        marco_matrices = ctk.CTkFrame(self)
        marco_matrices.grid(row=2, column=0, sticky="nsew", padx=12, pady=8)
        marco_matrices.grid_columnconfigure(0, weight=1)
        marco_matrices.grid_columnconfigure(1, weight=1)
        
        # Matriz A
        self.marco_a = ctk.CTkFrame(marco_matrices, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_a.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=4)
        self.marco_a.grid_rowconfigure(2, weight=1)
        header_a = ctk.CTkFrame(self.marco_a, fg_color="transparent")
        header_a.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        header_a.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header_a, text="Matriz de Coeficientes (A)", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky="w")
        self.btn_expandir_a = ctk.CTkButton(header_a, text="−", width=30, height=30, command=lambda: self.toggle_matriz_visibility('a'), fg_color=COLOR_BOTON_SECUNDARIO)
        self.btn_expandir_a.grid(row=0, column=1, sticky="e")
        marco_dims_a = ctk.CTkFrame(self.marco_a, fg_color="transparent")
        marco_dims_a.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        ctk.CTkLabel(marco_dims_a, text="Filas:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=(0, 4))
        self.var_filas_a = ctk.StringVar(value="3")
        self.ent_filas_a = ctk.CTkEntry(marco_dims_a, width=60, textvariable=self.var_filas_a)
        self.ent_filas_a.grid(row=0, column=1, padx=(0, 12))
        ctk.CTkLabel(marco_dims_a, text="Columnas:", font=ctk.CTkFont(size=13)).grid(row=0, column=2, padx=(0, 4))
        self.var_columnas_a = ctk.StringVar(value="3")
        self.ent_columnas_a = ctk.CTkEntry(marco_dims_a, width=60, textvariable=self.var_columnas_a)
        self.ent_columnas_a.grid(row=0, column=3)
        self.marco_grilla_a = ctk.CTkFrame(self.marco_a)
        self.marco_grilla_a.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))

        # Matriz B
        self.marco_b = ctk.CTkFrame(marco_matrices, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_b.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=4)
        self.marco_b.grid_rowconfigure(2, weight=1)
        header_b = ctk.CTkFrame(self.marco_b, fg_color="transparent")
        header_b.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        header_b.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header_b, text="Vector de Terminos (B)", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky="w")
        self.btn_expandir_b = ctk.CTkButton(header_b, text="−", width=30, height=30, command=lambda: self.toggle_matriz_visibility('b'), fg_color=COLOR_BOTON_SECUNDARIO)
        self.btn_expandir_b.grid(row=0, column=1, sticky="e")
        marco_dims_b = ctk.CTkFrame(self.marco_b, fg_color="transparent")
        marco_dims_b.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        ctk.CTkLabel(marco_dims_b, text="Filas:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=(0, 4))
        self.var_filas_b = ctk.StringVar(value="3")
        self.ent_filas_b = ctk.CTkEntry(marco_dims_b, width=60, textvariable=self.var_filas_b)
        self.ent_filas_b.grid(row=0, column=1)
        ctk.CTkLabel(marco_dims_b, text="Columnas:", font=ctk.CTkFont(size=13)).grid(row=0, column=2, padx=(0, 4))
        self.var_columnas_b = ctk.StringVar(value="1")
        self.ent_columnas_b = ctk.CTkEntry(marco_dims_b, width=60, textvariable=self.var_columnas_b)
        self.ent_columnas_b.grid(row=0, column=3)
        self.marco_grilla_b = ctk.CTkFrame(self.marco_b)
        self.marco_grilla_b.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))

        self.entradas_a = []
        self.entradas_b = []
        self.grilla_a = []
        self.grilla_b = []
        self.matriz_a_visible = True
        self.matriz_b_visible = True

        # Controles
        marco_controles = ctk.CTkFrame(self)
        marco_controles.grid(row=3, column=0, sticky="ew", padx=12, pady=8)
        ctk.CTkButton(marco_controles, text="Generar Cuadriculas", command=self.generar_cuadriculas_matriz, fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        ctk.CTkButton(marco_controles, text="Resolver Sistema", command=self.calcular_sistema_ecuaciones, fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=1, padx=6)
        ctk.CTkButton(marco_controles, text="Limpiar", command=self.limpiar_matrices, fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=2, padx=6)

        # Resultados
        marco_resultados = ctk.CTkFrame(self)
        marco_resultados.grid(row=4, column=0, sticky="nsew", padx=12, pady=(0, 12))
        marco_resultados.grid_rowconfigure(0, weight=1)
        marco_resultados.grid_columnconfigure(0, weight=2)
        marco_resultados.grid_columnconfigure(1, weight=1)

        # --- Bitácora (ScrollableFrame) ---
        marco_pasos = ctk.CTkFrame(marco_resultados)
        marco_pasos.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=8)
        marco_pasos.grid_columnconfigure(0, weight=1)
        marco_pasos.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(marco_pasos, text="Bitacora Paso a Paso", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        self.pasos_scroll_frame = ctk.CTkScrollableFrame(marco_pasos, fg_color=COLOR_FONDO_SECUNDARIO)
        self.pasos_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.pasos_scroll_frame.grid_columnconfigure(0, weight=1)

        # --- Resultado (Resaltado) ---
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
        """Formatea una matriz (lista de listas) usando SymPy SIN Unicode."""
        try:
            # CORRECCIÓN: use_unicode=False para evitar '?'
            return sp.pretty(sp.Matrix(M), use_unicode=False) 
        except Exception:
            # Fallback por si SymPy falla
            return '\n'.join(['[' + ' '.join([fmt(val) for val in fila]) + ']' for fila in M])

    def _renderizar_pasos_gauss(self, pasos_lista: list, ops_lista: list):
        """Dibuja los pasos de Gauss/Inversa en el scroll frame."""
        self._limpiar_pasos_scroll()
        MAX_PASOS_VISUALES = 40
        pasos_a_mostrar = pasos_lista[:MAX_PASOS_VISUALES]
        ops_a_mostrar = ops_lista[:MAX_PASOS_VISUALES]
        
        for i, (matriz, op) in enumerate(zip(pasos_a_mostrar, ops_a_mostrar)):
            titulo = f"PASO {i}: {op}"
            math_str = self._matriz_a_pretty(matriz)
            self._crear_bloque_texto(titulo, math_str)
            
        if len(pasos_lista) > MAX_PASOS_VISUALES:
            self._crear_bloque_texto("...", f"({len(pasos_lista) - MAX_PASOS_VISUALES} pasos más omitidos)")
            self._crear_bloque_texto("PASO FINAL", self._matriz_a_pretty(pasos_lista[-1]))

    def _renderizar_pasos_cramer(self, pasos_lista: list):
        """Dibuja los pasos de Cramer (texto simple) en el scroll frame."""
        self._limpiar_pasos_scroll()
        titulo_actual = "INICIO"
        math_actual = []
        
        for linea in pasos_lista:
            linea = linea.strip()
            if not linea: continue
            
            # Detectar si la línea es un título (no empieza con espacio)
            if not linea.startswith(" ") and ":" in linea:
                if math_actual:
                    self._crear_bloque_texto(titulo_actual, "\n".join(math_actual))
                titulo_actual = linea
                math_actual = []
            else:
                math_actual.append(linea)
        
        if math_actual:
            self._crear_bloque_texto(titulo_actual, "\n".join(math_actual))

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

    def generar_cuadriculas_matriz(self):
        try:
            filas_a = int(self.ent_filas_a.get())
            cols_a = int(self.ent_columnas_a.get())
            filas_b = int(self.ent_filas_b.get())
            if filas_a <= 0 or cols_a <= 0 or filas_b <= 0:
                raise ValueError("Las dimensiones deben ser numeros enteros positivos")

            for widget in self.grilla_a: widget.destroy()
            for widget in self.grilla_b: widget.destroy()
            self.grilla_a, self.grilla_b = [], []
            self.entradas_a = [[None]*cols_a for _ in range(filas_a)]
            self.entradas_b = [[None]*1 for _ in range(filas_b)]

            for i in range(filas_a):
                for j in range(cols_a):
                    e = ctk.CTkEntry(self.marco_grilla_a, width=60)
                    e.grid(row=i, column=j, padx=2, pady=2)
                    self.grilla_a.append(e)
                    self.entradas_a[i][j] = e
            for i in range(filas_b):
                e2 = ctk.CTkEntry(self.marco_grilla_b, width=60)
                e2.grid(row=i, column=0, padx=2, pady=2)
                self.grilla_b.append(e2)
                self.entradas_b[i][0] = e2

            self.limpiar_matrices()
        except ValueError as e:
            self.resultado_caja.configure(state="normal")
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f'Error: {e}')
            self.resultado_caja.configure(state="disabled")

    def parsear_y_poblar_ecuaciones(self):
        try:
            texto_completo = self.caja_ecuaciones.get('1.0', 'end')
            lineas = [linea.strip() for linea in texto_completo.split('\n') if linea.strip() and '=' in linea]
            if not lineas:
                raise ValueError("No se encontraron ecuaciones validas (deben contener '=')")

            var_map, var_ordenadas = {}, []
            matriz_coef_dict, vector_const = [], []
            regex_termino = re.compile(r'([+-]?)(\d*\.?\d*)\s*\*?\s*([a-zA-Z]\w*)')

            for linea in lineas:
                partes = linea.split('=', 1)
                if len(partes) != 2: continue
                lhs, rhs = partes[0].strip(), partes[1].strip()
                vector_const.append(parse_valor(rhs))
                fila_coef = {}
                lhs_limpio = lhs.replace(' ', '').replace('−', '-')
                if lhs_limpio and lhs_limpio[0] not in ('+', '-'): lhs_limpio = '+' + lhs_limpio
                
                for match in regex_termino.finditer(lhs_limpio):
                    signo, coeff_str, var_str = match.groups()
                    if var_str not in var_map:
                        var_map[var_str] = len(var_ordenadas)
                        var_ordenadas.append(var_str)
                    coeff_val = 1.0
                    if coeff_str: coeff_val = parse_valor(coeff_str)
                    if signo == '-': coeff_val = -coeff_val
                    fila_coef[var_str] = fila_coef.get(var_str, 0.0) + coeff_val
                matriz_coef_dict.append(fila_coef)

            num_filas, num_vars = len(lineas), len(var_ordenadas)
            matriz_a = [[0.0] * num_vars for _ in range(num_filas)]
            for i, fila_coef in enumerate(matriz_coef_dict):
                for var_str, coeff_val in fila_coef.items():
                    j = var_map[var_str]
                    matriz_a[i][j] = coeff_val
            matriz_b = [[val] for val in vector_const]

            self.var_filas_a.set(str(num_filas))
            self.ent_columnas_a.delete(0, 'end'); self.ent_columnas_a.insert(0, str(num_vars))
            self.ent_filas_b.delete(0, 'end'); self.ent_filas_b.insert(0, str(num_filas))

            self.generar_cuadriculas_matriz()
            self.poblar_cuadricula(self.entradas_a, matriz_a)
            self.poblar_cuadricula(self.entradas_b, matriz_b)
            
            self.resultado_caja.configure(state="normal")
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f"Sistema de {num_filas}x{num_vars} cargado.\nVariables: {', '.join(var_ordenadas)}")
            self.resultado_caja.configure(state="disabled")
                
        except ValueError as e:
            self.resultado_caja.configure(state="normal")
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f"Error al analizar ecuaciones: {e}")
            self.resultado_caja.configure(state="disabled")

    def poblar_cuadricula(self, entradas_grid, datos):
        filas_grid, cols_grid = len(entradas_grid), len(entradas_grid[0]) if entradas_grid else 0
        filas_datos, cols_datos = len(datos), len(datos[0]) if datos else 0
        for i in range(min(filas_grid, filas_datos)):
            for j in range(min(cols_grid, cols_datos)):
                if entradas_grid[i][j]:
                    entradas_grid[i][j].delete(0, 'end')
                    entradas_grid[i][j].insert(0, fmt(datos[i][j]))

    def leer_entradas_cuadricula(self, entradas):
        if not entradas or len(entradas) == 0: raise ValueError("Primero debe generar la matriz")
        filas = len(entradas); cols = len(entradas[0]) if filas > 0 else 0
        matriz = [[0.0]*cols for _ in range(filas)]
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

    def calcular_sistema_ecuaciones(self):
        self._limpiar_pasos_scroll()
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete('0.0', 'end')
        
        if not LOGICA_DISPONIBLE:
            self.resultado_caja.insert('0.0', "ERROR: No se pudo cargar Complement.py")
            self.resultado_caja.configure(state="disabled")
            return

        try:
            A = self.leer_entradas_cuadricula(self.entradas_a)
            B = self.leer_entradas_cuadricula(self.entradas_b)
        except ValueError as e:
            self.resultado_caja.insert('0.0', f'Error de entrada: {e}')
            self.resultado_caja.configure(state="disabled")
            return
        
        metodo = self.metodo_sistema_var.get()
        res = None
        resultado_texto = ""
        
        try:
            if metodo == 'Regla de Cramer':
                if not A or not B: raise ValueError("Matrices A y B no pueden estar vacías")
                if len(A) != len(B): raise ValueError(f"Las filas de A ({len(A)}) y B ({len(B)}) no coinciden")
                if not A[0]: raise ValueError("La matriz A no tiene columnas")
                if len(A) != len(A[0]): raise ValueError("La matriz A debe ser cuadrada (n x n)")
                if not B[0] or len(B[0]) != 1: raise ValueError("B debe ser un vector columna (n x 1)")
                
                matriz_aumentada = [A[i] + [B[i][0]] for i in range(len(A))]
                res = resolver_por_cramer(matriz_aumentada)
                
                if res.get('pasos'):
                    self._renderizar_pasos_cramer(res['pasos'])
                
                if res['estado'] == 'exito':
                    sol_texto = '\n'.join(f'x{i+1} = {fmt(v)}' for i,v in enumerate(res['solucion']))
                    resultado_texto = f"Solucion unica encontrada:\n{sol_texto}"
                else:
                    resultado_texto = f"Error: {res['mensaje']}"

            elif metodo == 'Matriz Inversa':
                res = inverse_steps(A)
                
                if res.get('steps') and res.get('ops'):
                    self._renderizar_pasos_gauss(res['steps'], res['ops'])
                
                if res.get('status') == 'invertible':
                    inv = res['inverse']
                    solucion = [sum(inv[i][j] * B[j][0] for j in range(len(inv[0]))) for i in range(len(inv))]
                    sol_texto = '\n'.join(f'x{i+1} = {fmt(v)}' for i,v in enumerate(solucion))
                    resultado_texto = f"A es invertible.\nSolucion (x = A⁻¹ * b):\n{sol_texto}"
                else:
                    resultado_texto = f"Error: {res.get('mensaje','A es singular (no tiene inversa)')}"
            
            else:  # Gauss o Gauss-Jordan
                matriz_aumentada = [A[i] + [B[i][0]] for i in range(len(A))]
                res = gauss_jordan_steps(matriz_aumentada) if metodo == 'Gauss-Jordan' else gauss_steps(matriz_aumentada)
                
                if res.get('steps') and res.get('ops'):
                    self._renderizar_pasos_gauss(res['steps'], res['ops'])
                
                status = res.get('status'); sol = res.get('solution')
                if status=='unique' and sol is not None:
                    resultado_texto = 'Solucion unica:\n' + '\n'.join(f'x{i+1} = {v:.6g}' for i,v in enumerate(sol))
                elif status=='inconsistent': 
                    resultado_texto = 'El sistema es inconsistente (sin solucion)'
                elif status=='infinite':
                    libres = res.get('free_vars', []); base = res.get('basic_solution', {})
                    lineas = [f'x{i+1} = variable libre' if i in libres else f'x{i+1} = {base.get(i,0.0):.6g}  (con libres = 0)' for i in range(len(A[0]))]
                    resultado_texto = 'Soluciones infinitas:\n' + '\n'.join(lineas)
                else: 
                    resultado_texto = f"Estado: {status}"

            self.resultado_caja.insert('0.0', resultado_texto)

        except ValueError as e:
            self.resultado_caja.insert('0.0', f'Error: {e}')
        except Exception as e:
            self.resultado_caja.insert('0.0', f'Error inesperado al calcular: {e}')
        
        self.resultado_caja.configure(state="disabled")


    def limpiar_matrices(self):
        for fila_entradas in self.entradas_a:
            for entrada in fila_entradas:
                if entrada: entrada.delete(0,'end')
        for fila_entradas in self.entradas_b:
            for entrada in fila_entradas:
                if entrada: entrada.delete(0,'end')
        
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete('0.0','end')
        self.resultado_caja.configure(state="disabled")
        
        self._limpiar_pasos_scroll()
        
        self.caja_ecuaciones.delete('1.0', 'end')
        self.caja_ecuaciones.insert("0.0", "2x + 3y - z = 5\nx - y + 2z = 10\n3x + 2y = 0")

    def mostrar(self):
        self.grid(row=0, column=0, sticky="nsew")