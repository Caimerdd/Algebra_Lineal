import customtkinter as ctk
import re
import sympy as sp
from paginas.pagina_base import PaginaBase
from app_config import (COLOR_FONDO_SECUNDARIO, COLOR_ALGEBRA, COLOR_HOVER, 
                        COLOR_BOTON_SECUNDARIO, COLOR_BOTON_SECUNDARIO_HOVER)
from app_config import fmt, parse_valor

# Importación de Complement
try:
    from Complement import (
        gauss_steps, gauss_jordan_steps, inverse_steps, 
        resolver_por_cramer
    )
    LOGICA_DISPONIBLE = True
except ImportError:
    LOGICA_DISPONIBLE = False
    def gauss_steps(M): return {}
    def gauss_jordan_steps(M): return {}
    def inverse_steps(A): return {}
    def resolver_por_cramer(M): return {}

class PaginaSistemasEcuaciones(PaginaBase):
    def crear_widgets(self):
        self.configurar_grid()
        self.crear_barra_navegacion()
        self.crear_interfaz()
        self.after(100, self.generar_cuadriculas_matriz)
    
    def configurar_grid(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def crear_barra_navegacion(self):
        marco_nav = ctk.CTkFrame(self, fg_color="transparent", height=40)
        marco_nav.grid(row=0, column=0, sticky="ew", padx=12, pady=(8,0))
        
        btn_sistemas = ctk.CTkButton(marco_nav, text="Sistemas de Ecuaciones", 
                                     fg_color=COLOR_ALGEBRA, state="disabled",
                                     text_color_disabled=("white", "white"), height=30)
        btn_sistemas.pack(side="left", padx=(0, 5), expand=True, fill="x")
        
        btn_ops = ctk.CTkButton(marco_nav, text="Operaciones Matriciales", 
                                fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER,
                                height=30, command=lambda: self.app.mostrar_pagina("operaciones_matriciales"))
        btn_ops.pack(side="left", padx=5, expand=True, fill="x")
        
        btn_props = ctk.CTkButton(marco_nav, text="Propiedades", 
                                  fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER,
                                  height=30, command=lambda: self.app.mostrar_pagina("propiedades_matrices"))
        btn_props.pack(side="left", padx=(5, 0), expand=True, fill="x")
    
    def crear_interfaz(self):
        # Selector de Metodo
        marco_metodo = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_metodo.grid(row=1, column=0, sticky="ew", padx=12, pady=8)
        
        # Título y opciones
        ctk.CTkLabel(marco_metodo, text="Método de Solución:", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=(12, 8), pady=12)
        
        self.metodo_sistema_var = ctk.StringVar(value="Gauss-Jordan")
        metodos = ["Gauss-Jordan", "Eliminacion Gaussiana", "Regla de Cramer", "Matriz Inversa"]
        
        for i, metodo in enumerate(metodos):
            rb = ctk.CTkRadioButton(marco_metodo, text=metodo, variable=self.metodo_sistema_var, 
                                   value=metodo, font=ctk.CTkFont(size=13),
                                   command=self._actualizar_info_metodo) # CAMBIO DE NOMBRE DE LA FUNCION
            rb.grid(row=0, column=i+1, padx=8, pady=5)

        # --- AQUI ESTA EL TRUCO: ETIQUETA DINAMICA ---
        # Una etiqueta pequeña debajo de los botones que explica qué hace
        self.lbl_info_metodo = ctk.CTkLabel(marco_metodo, text="", 
                                           font=ctk.CTkFont(size=12, slant="italic"),
                                           text_color="gray70")
        self.lbl_info_metodo.grid(row=1, column=0, columnspan=5, pady=(0, 10), sticky="ew")
        
        # Entrada de Ecuaciones
        marco_ecuaciones = ctk.CTkFrame(self)
        marco_ecuaciones.grid(row=2, column=0, sticky="ew", padx=12, pady=(4, 8))
        marco_ecuaciones.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(marco_ecuaciones, text="Ingrese el sistema (ej: 3x1 + x2 = 10):", 
                    font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=(8, 4))
        
        self.caja_ecuaciones = ctk.CTkTextbox(marco_ecuaciones, height=100, font=ctk.CTkFont(size=13))
        self.caja_ecuaciones.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        
        ctk.CTkButton(marco_ecuaciones, text="Generar Matriz Aumentada ↓", 
                     command=self.parsear_y_poblar_ecuaciones,
                     fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=1, column=1, sticky="ns", padx=(0, 8), pady=(0, 8))

        # Marco para matrices
        self.marco_matrices = ctk.CTkFrame(self)
        self.marco_matrices.grid(row=3, column=0, sticky="nsew", padx=12, pady=8)
        self.marco_matrices.grid_columnconfigure(0, weight=1)
        self.marco_matrices.grid_columnconfigure(1, weight=1)
        
        # Matriz A
        self.marco_a = ctk.CTkFrame(self.marco_matrices, fg_color=COLOR_FONDO_SECUNDARIO)
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
        
        ctk.CTkLabel(marco_dims_a, text="N° Ecuaciones:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=(0, 4))
        self.var_filas_a = ctk.StringVar(value="3")
        self.ent_filas_a = ctk.CTkEntry(marco_dims_a, width=50, textvariable=self.var_filas_a)
        self.ent_filas_a.grid(row=0, column=1, padx=(0, 12))
        
        ctk.CTkLabel(marco_dims_a, text="N° Variables:", font=ctk.CTkFont(size=13)).grid(row=0, column=2, padx=(0, 4))
        self.var_columnas_a = ctk.StringVar(value="3")
        self.ent_columnas_a = ctk.CTkEntry(marco_dims_a, width=50, textvariable=self.var_columnas_a)
        self.ent_columnas_a.grid(row=0, column=3)
        
        self.marco_grilla_a = ctk.CTkFrame(self.marco_a)
        self.marco_grilla_a.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))

        # Matriz B
        self.marco_b = ctk.CTkFrame(self.marco_matrices, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_b.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=4)
        self.marco_b.grid_rowconfigure(2, weight=1)
        
        header_b = ctk.CTkFrame(self.marco_b, fg_color="transparent")
        header_b.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        header_b.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header_b, text="Constantes (Vector B)", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky="w")
        self.btn_expandir_b = ctk.CTkButton(header_b, text="−", width=30, height=30, command=lambda: self.toggle_matriz_visibility('b'), fg_color=COLOR_BOTON_SECUNDARIO)
        self.btn_expandir_b.grid(row=0, column=1, sticky="e")
        
        marco_dims_b = ctk.CTkFrame(self.marco_b, fg_color="transparent")
        marco_dims_b.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        ctk.CTkLabel(marco_dims_b, text="Se ajusta a N° Ecuaciones automáticamente.", font=ctk.CTkFont(size=12, slant="italic"), text_color="gray").grid(row=0, column=0, sticky="w")
        
        self.var_filas_b = ctk.StringVar(value="3")
        self.marco_grilla_b = ctk.CTkFrame(self.marco_b)
        self.marco_grilla_b.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))

        self.entradas_a = []; self.entradas_b = []
        self.grilla_a = []; self.grilla_b = []
        self.matriz_a_visible = True; self.matriz_b_visible = True

        # Controles
        marco_controles = ctk.CTkFrame(self)
        marco_controles.grid(row=4, column=0, sticky="ew", padx=12, pady=8)
        ctk.CTkButton(marco_controles, text="Generar Cuadrículas", command=self.generar_cuadriculas_matriz, fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        ctk.CTkButton(marco_controles, text="Resolver Sistema", command=self.calcular_sistema_ecuaciones, fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=1, padx=6)
        ctk.CTkButton(marco_controles, text="Limpiar", command=self.limpiar_matrices, fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=2, padx=6)
        ctk.CTkButton(marco_controles, text="Ayuda ❓", command=lambda: self.app.mostrar_ayuda_sympy(), fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, width=80).grid(row=0, column=3, padx=6)

        # Resultados
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
        
        # Inicializar el texto de ayuda
        self._actualizar_info_metodo()

    # --- Lógica de Información Dinámica ---
    def _actualizar_info_metodo(self):
        metodo = self.metodo_sistema_var.get()
        texto = ""
        
        if metodo == "Gauss-Jordan":
            texto = "Reduce la matriz a su forma escalonada reducida para hallar la solución."
        elif metodo == "Eliminacion Gaussiana":
            texto = "Reduce la matriz a su forma triangular superior y resuelve por sustitución."
        elif metodo == "Regla de Cramer":
            texto = "Usa determinantes para hallar cada incógnita (Solo para sistemas con solución única)."
        elif metodo == "Matriz Inversa":
            texto = "Calcula la inversa de A y la multiplica por B (X = A⁻¹ · B). Requiere que A sea invertible."
            
        self.lbl_info_metodo.configure(text=texto)

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

    def _renderizar_pasos_gauss(self, pasos_lista: list, ops_lista: list):
        self._limpiar_pasos_scroll()
        MAX_PASOS = 40
        if not pasos_lista: return
        pasos_ver = pasos_lista[:MAX_PASOS]
        ops_ver = ops_lista[:len(pasos_ver)]
        for i, (mat, op) in enumerate(zip(pasos_ver, ops_ver)):
            self._crear_bloque_texto(f"PASO {i}: {op}", self._matriz_a_pretty(mat))
        if len(pasos_lista) > MAX_PASOS:
            self._crear_bloque_texto("...", f"({len(pasos_lista)-MAX_PASOS} pasos ocultos)")
            self._crear_bloque_texto("MATRIZ FINAL", self._matriz_a_pretty(pasos_lista[-1]))

    def _renderizar_pasos_cramer(self, pasos_lista: list):
        self._limpiar_pasos_scroll()
        titulo = "INICIO"; buffer = []
        for linea in pasos_lista:
            linea = str(linea).strip()
            if not linea: continue
            if ":" in linea and not linea.startswith("[") and len(linea) < 50:
                if buffer: self._crear_bloque_texto(titulo, "\n".join(buffer))
                titulo = linea; buffer = []
            else: buffer.append(linea)
        if buffer: self._crear_bloque_texto(titulo, "\n".join(buffer))

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
            filas_b = filas_a 
            self.var_filas_b.set(str(filas_b))

            if filas_a <= 0 or cols_a <= 0: raise ValueError("Ingrese valores positivos.")

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

            self.limpiar_matrices(borrar_grid=False)
            
        except ValueError as e:
            self.resultado_caja.configure(state="normal")
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f'Error: {e}')
            self.resultado_caja.configure(state="disabled")

    def parsear_y_poblar_ecuaciones(self):
        try:
            texto = self.caja_ecuaciones.get('1.0', 'end')
            lineas = [l.strip() for l in texto.split('\n') if l.strip() and '=' in l]
            if not lineas: raise ValueError("No hay ecuaciones válidas.")

            var_map, var_ord = {}, []
            mat_coef, vec_const = [], []
            regex = re.compile(r'([+-]?)(\d*\.?\d*)\s*\*?\s*([a-zA-Z]\w*)')

            for l in lineas:
                lhs, rhs = l.split('=', 1)
                vec_const.append(parse_valor(rhs))
                fila_coef = {}
                lhs = lhs.replace(' ', '').replace('−', '-')
                if lhs and lhs[0] not in ('+', '-'): lhs = '+' + lhs
                for m in regex.finditer(lhs):
                    sgn, cf_str, v_str = m.groups()
                    if v_str not in var_map:
                        var_map[v_str] = len(var_ord)
                        var_ord.append(v_str)
                    val = parse_valor(cf_str) if cf_str else 1.0
                    if sgn == '-': val = -val
                    fila_coef[v_str] = fila_coef.get(v_str, 0.0) + val
                mat_coef.append(fila_coef)

            if not var_ord: raise ValueError("No se detectaron variables.")
            def natural_keys(text):
                return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]
            var_ord = sorted(list(set(var_ord)), key=natural_keys)
            var_map = {v: i for i, v in enumerate(var_ord)}

            n_filas, n_vars = len(lineas), len(var_ord)
            mat_a = [[0.0]*n_vars for _ in range(n_filas)]
            mat_b = [[v] for v in vec_const] 

            for i, fc in enumerate(mat_coef):
                for v, val in fc.items():
                    if v in var_map: mat_a[i][var_map[v]] += val

            self.var_filas_a.set(str(n_filas))
            self.ent_columnas_a.delete(0, 'end'); self.ent_columnas_a.insert(0, str(n_vars))
            
            self.generar_cuadriculas_matriz()
            self.poblar_cuadricula(self.entradas_a, mat_a)
            self.poblar_cuadricula(self.entradas_b, mat_b)
            
            self.resultado_caja.configure(state="normal")
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f"Sistema cargado.\nVariables ordenadas: {', '.join(var_ord)}")
            self.resultado_caja.configure(state="disabled")
        except ValueError as e:
            self.resultado_caja.configure(state="normal")
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f"Error: {e}")
            self.resultado_caja.configure(state="disabled")

    def poblar_cuadricula(self, grid, data):
        nr, nc = len(grid), len(grid[0]) if grid else 0
        dr, dc = len(data), len(data[0]) if data else 0
        for i in range(min(nr, dr)):
            for j in range(min(nc, dc)):
                if grid[i][j]:
                    grid[i][j].delete(0, 'end')
                    grid[i][j].insert(0, fmt(data[i][j]))

    def leer_entradas_cuadricula(self, entradas):
        if not entradas: raise ValueError("Genere la matriz primero.")
        nr, nc = len(entradas), len(entradas[0])
        mat = [[0.0]*nc for _ in range(nr)]
        llenos = 0
        for i in range(nr):
            for j in range(nc):
                txt = entradas[i][j].get().strip()
                if txt:
                    llenos += 1
                    try: mat[i][j] = parse_valor(txt)
                    except: raise ValueError(f"Valor inválido en ({i+1},{j+1})")
        if llenos == 0: raise ValueError("Matriz vacía.")
        return mat

    def calcular_sistema_ecuaciones(self):
        self._limpiar_pasos_scroll()
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete('0.0', 'end')
        
        if not LOGICA_DISPONIBLE:
            self.resultado_caja.insert('0.0', "ERROR: Complement.py no cargado.")
            self.resultado_caja.configure(state="disabled")
            return

        metodo = self.metodo_sistema_var.get()
        
        try:
            A = self.leer_entradas_cuadricula(self.entradas_a)
            # SIEMPRE leemos B porque es un sistema Ax=b
            B = self.leer_entradas_cuadricula(self.entradas_b)

            txt_res = ""
            
            if metodo == 'Regla de Cramer':
                if len(A) != len(A[0]): raise ValueError("Para Cramer, N° Ecuaciones debe ser igual a N° Variables.")
                mat_aum = [A[i] + [B[i][0]] for i in range(len(A))]
                res = resolver_por_cramer(mat_aum)
                if res.get('pasos'): self._renderizar_pasos_cramer(res['pasos'])
                if res['estado'] == 'exito':
                    sol = '\n'.join(f'x{i+1} = {fmt(v)}' for i,v in enumerate(res['solucion']))
                    txt_res = f"Solución única:\n{sol}"
                else: txt_res = f"Error: {res['mensaje']}"

            elif metodo == 'Matriz Inversa':
                res = inverse_steps(A)
                if res.get('steps'): self._renderizar_pasos_gauss(res['steps'], res['ops'])
                
                if res.get('status') == 'invertible':
                    inv = res['inverse']
                    txt_res = "La Matriz A es Invertible.\n\nInversa (A⁻¹):\n" + self._matriz_a_pretty(inv)
                    # Calculamos X = Inv * B
                    if B and len(B) == len(A):
                        sol = [sum(inv[i][j]*B[j][0] for j in range(len(inv))) for i in range(len(inv))]
                        s_txt = '\n'.join(f'x{i+1} = {fmt(v)}' for i,v in enumerate(sol))
                        txt_res += f"\n\nSolución del sistema (x = A⁻¹·b):\n{s_txt}"
                else: txt_res = f"Error: {res.get('mensaje','Singular')}"
            
            else: 
                mat_aum = [A[i] + [B[i][0]] for i in range(len(A))]
                res = gauss_jordan_steps(mat_aum) if metodo == 'Gauss-Jordan' else gauss_steps(mat_aum)
                if res.get('steps'): self._renderizar_pasos_gauss(res['steps'], res['ops'])
                st = res.get('status')
                if st == 'unique':
                    sol = res['solution']
                    txt_res = 'Solución única:\n' + '\n'.join(f'x{i+1} = {fmt(v)}' for i,v in enumerate(sol))
                elif st == 'inconsistent': txt_res = 'Sistema Inconsistente (Sin solución)'
                elif st == 'infinite': txt_res = 'Infinitas Soluciones'
                else: txt_res = f"Estado: {st}"

            self.resultado_caja.insert('0.0', txt_res)

        except ValueError as e: self.resultado_caja.insert('0.0', f'Error: {e}')
        except Exception as e: self.resultado_caja.insert('0.0', f'Error: {e}')
        
        self.resultado_caja.configure(state="disabled")

    def limpiar_matrices(self, borrar_grid=True):
        if borrar_grid:
            for r in self.entradas_a:
                for e in r: e.delete(0,'end') if e else None
            for r in self.entradas_b:
                for e in r: e.delete(0,'end') if e else None
            self.caja_ecuaciones.delete('1.0', 'end')
        
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete('0.0','end')
        self.resultado_caja.configure(state="disabled")
        self._limpiar_pasos_scroll()