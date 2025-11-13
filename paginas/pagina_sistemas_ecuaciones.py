import customtkinter as ctk
import re
from paginas.pagina_base import PaginaBase
from app_config import COLOR_FONDO_SECUNDARIO, COLOR_ALGEBRA, COLOR_HOVER, COLOR_BOTON_SECUNDARIO, COLOR_BOTON_SECUNDARIO_HOVER
from app_config import fmt, parse_valor

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
        self.grid_rowconfigure(4, weight=1)
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
        
        ctk.CTkLabel(header_a, text="Matriz de Coeficientes (A)", 
                    font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky="w")
        
        # Botón expandir A
        self.btn_expandir_a = ctk.CTkButton(header_a, text="−", width=30, height=30,
                                          command=lambda: self.toggle_matriz_visibility('a'),
                                          fg_color=COLOR_BOTON_SECUNDARIO)
        self.btn_expandir_a.grid(row=0, column=1, sticky="e")
        
        marco_dims_a = ctk.CTkFrame(self.marco_a, fg_color="transparent")
        marco_dims_a.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        ctk.CTkLabel(marco_dims_a, text="Filas:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=(0, 4))
        self.var_filas_a = ctk.StringVar(value="3")
        self.ent_filas_a = ctk.CTkEntry(marco_dims_a, width=60, textvariable=self.var_filas_a)
        self.ent_filas_a.grid(row=0, column=1, padx=(0, 12))
        ctk.CTkLabel(marco_dims_a, text="Columnas:", font=ctk.CTkFont(size=13)).grid(row=0, column=2, padx=(0, 4))
        self.ent_columnas_a = ctk.CTkEntry(marco_dims_a, width=60)
        self.ent_columnas_a.insert(0, "3")
        self.ent_columnas_a.grid(row=0, column=3)

        # Marco para la cuadrícula de A
        self.marco_grilla_a = ctk.CTkFrame(self.marco_a)
        self.marco_grilla_a.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))

        # Matriz B
        self.marco_b = ctk.CTkFrame(marco_matrices, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_b.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=4)
        self.marco_b.grid_rowconfigure(2, weight=1)
        
        header_b = ctk.CTkFrame(self.marco_b, fg_color="transparent")
        header_b.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        header_b.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(header_b, text="Vector de Terminos Independientes (B)", 
                    font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky="w")
        
        # Botón expandir B
        self.btn_expandir_b = ctk.CTkButton(header_b, text="−", width=30, height=30,
                                          command=lambda: self.toggle_matriz_visibility('b'),
                                          fg_color=COLOR_BOTON_SECUNDARIO)
        self.btn_expandir_b.grid(row=0, column=1, sticky="e")
        
        marco_dims_b = ctk.CTkFrame(self.marco_b, fg_color="transparent")
        marco_dims_b.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        ctk.CTkLabel(marco_dims_b, text="Filas:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=(0, 4))
        self.ent_filas_b = ctk.CTkEntry(marco_dims_b, width=60)
        self.ent_filas_b.insert(0, "3")
        self.ent_filas_b.grid(row=0, column=1)

        # Marco para la cuadrícula de B
        self.marco_grilla_b = ctk.CTkFrame(self.marco_b)
        self.marco_grilla_b.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))

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
        marco_controles.grid(row=3, column=0, sticky="ew", padx=12, pady=8)
        
        ctk.CTkButton(marco_controles, text="Generar Cuadriculas", 
                     command=self.generar_cuadriculas_matriz,
                     fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        
        ctk.CTkButton(marco_controles, text="Resolver Sistema", 
                     command=self.calcular_sistema_ecuaciones,
                     fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=1, padx=6)
        
        ctk.CTkButton(marco_controles, text="Limpiar", 
                     command=self.limpiar_matrices,
                     fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=2, padx=6)

        # Resultados
        marco_resultados = ctk.CTkFrame(self)
        marco_resultados.grid(row=4, column=0, sticky="nsew", padx=12, pady=(0, 12))
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

    def generar_cuadriculas_matriz(self):
        try:
            filas_a = int(self.ent_filas_a.get())
            cols_a = int(self.ent_columnas_a.get())
            filas_b = int(self.ent_filas_b.get())
            
            if filas_a <= 0 or cols_a <= 0 or filas_b <= 0:
                raise ValueError("Las dimensiones deben ser numeros enteros positivos")

            # Limpiar cuadriculas existentes
            for widget in self.grilla_a: 
                widget.destroy()
            for widget in self.grilla_b: 
                widget.destroy()
            self.grilla_a = []
            self.grilla_b = []

            # Inicializar listas
            self.entradas_a = [[None]*cols_a for _ in range(filas_a)]
            self.entradas_b = [[None]*1 for _ in range(filas_b)]

            # Crear cuadricula para A
            for i in range(filas_a):
                for j in range(cols_a):
                    e = ctk.CTkEntry(self.marco_grilla_a, width=60)
                    e.grid(row=i, column=j, padx=2, pady=2)
                    self.grilla_a.append(e)
                    self.entradas_a[i][j] = e

            # Crear cuadricula para B
            for i in range(filas_b):
                e2 = ctk.CTkEntry(self.marco_grilla_b, width=60)
                e2.grid(row=i, column=0, padx=2, pady=2)
                self.grilla_b.append(e2)
                self.entradas_b[i][0] = e2

            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0','Matrices listas para ingresar datos')

        except ValueError as e:
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f'Error: {e}')

    def parsear_y_poblar_ecuaciones(self):
        try:
            texto_completo = self.caja_ecuaciones.get('1.0', 'end')
            lineas = [linea.strip() for linea in texto_completo.split('\n') if linea.strip() and '=' in linea]
            if not lineas:
                raise ValueError("No se encontraron ecuaciones validas (deben contener '=')")

            var_map = {}
            var_ordenadas = []
            matriz_coef_dict = []
            vector_const = []

            regex_termino = re.compile(r'([+-]?)(\d*\.?\d*)\s*\*?\s*([a-zA-Z]\w*)')

            for linea in lineas:
                partes = linea.split('=', 1)
                if len(partes) != 2: continue
                lhs, rhs = partes[0].strip(), partes[1].strip()

                constante = parse_valor(rhs)
                vector_const.append(constante)
                
                fila_coef = {}
                lhs_limpio = lhs.replace(' ', '').replace('−', '-')
                
                if lhs_limpio and lhs_limpio[0] not in ('+', '-'):
                    lhs_limpio = '+' + lhs_limpio
                
                for match in regex_termino.finditer(lhs_limpio):
                    signo, coeff_str, var_str = match.groups()
                    
                    if var_str not in var_map:
                        var_map[var_str] = len(var_ordenadas)
                        var_ordenadas.append(var_str)
                    
                    coeff_val = 1.0
                    if coeff_str:
                        coeff_val = parse_valor(coeff_str)
                    
                    if signo == '-':
                        coeff_val = -coeff_val
                    
                    fila_coef[var_str] = fila_coef.get(var_str, 0.0) + coeff_val

                matriz_coef_dict.append(fila_coef)

            num_filas = len(lineas)
            num_vars = len(var_ordenadas)
            
            # Construye las matrices finales
            matriz_a = [[0.0] * num_vars for _ in range(num_filas)]
            for i, fila_coef in enumerate(matriz_coef_dict):
                for var_str, coeff_val in fila_coef.items():
                    j = var_map[var_str]
                    matriz_a[i][j] = coeff_val
            
            matriz_b = [[val] for val in vector_const]

            # Actualiza la UI
            self.var_filas_a.set(str(num_filas))
            self.ent_columnas_a.delete(0, 'end')
            self.ent_columnas_a.insert(0, str(num_vars))
            
            self.ent_filas_b.delete(0, 'end')
            self.ent_filas_b.insert(0, str(num_filas))

            # Regenerar cuadriculas y poblar
            self.generar_cuadriculas_matriz()
            self.poblar_cuadricula(self.entradas_a, matriz_a)
            self.poblar_cuadricula(self.entradas_b, matriz_b)
            
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f"Sistema de {num_filas} ecuaciones con {num_vars} variables cargado.\nVariables: {', '.join(var_ordenadas)}")
                
        except ValueError as e:
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f"Error al analizar ecuaciones: {e}")
        except Exception as e:
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f"Error inesperado: {e}")

    def poblar_cuadricula(self, entradas_grid, datos):
        filas_grid = len(entradas_grid)
        cols_grid = len(entradas_grid[0]) if filas_grid > 0 else 0
        filas_datos = len(datos)
        cols_datos = len(datos[0]) if filas_datos > 0 else 0

        for i in range(min(filas_grid, filas_datos)):
            for j in range(min(cols_grid, cols_datos)):
                if entradas_grid[i][j]:
                    entradas_grid[i][j].delete(0, 'end')
                    entradas_grid[i][j].insert(0, fmt(datos[i][j]))

    def leer_entradas_cuadricula(self, entradas):
        if not entradas:
            return []
            
        if not entradas[0] and len(entradas) > 0:
            raise ValueError("Primero debe generar la matriz")

        filas = len(entradas)
        cols = len(entradas[0]) if filas > 0 else 0

        matriz = [[0.0]*cols for _ in range(filas)]
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

    def append_matriz(self, M, titulo=None):
        if titulo: 
            self.pasos_caja.insert('end', f'{titulo}\n')
        for f in M: 
            self.pasos_caja.insert('end', '  '.join(fmt(v) for v in f) + '\n')
        self.pasos_caja.insert('end', '\n')

    def calcular_sistema_ecuaciones(self):
        try:
            # Importar los modulos de calculo
            try:
                from Complement import (
                    gauss_steps, gauss_jordan_steps, inverse_steps, 
                    resolver_por_cramer
                )
            except ImportError:
                self.resultado_caja.delete('0.0', 'end')
                self.resultado_caja.insert('0.0', "ERROR: No se pudo cargar Complement.py")
                return

            A = self.leer_entradas_cuadricula(self.entradas_a)
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

        metodo = self.metodo_sistema_var.get()
        
        if metodo == 'Regla de Cramer':
            try:
                if not A: raise ValueError("La matriz A no puede estar vacia")
                if not B: raise ValueError("El vector B no puede estar vacio")
                if len(A) != len(B): raise ValueError(f"Las filas de A ({len(A)}) y B ({len(B)}) no coinciden")
                if not A[0]: raise ValueError("La matriz A no tiene columnas")
                if len(A) != len(A[0]): raise ValueError("La matriz A debe ser cuadrada (n x n)")
                if not B[0] or len(B[0]) != 1: raise ValueError("B debe ser un vector columna (n x 1)")

                matriz_aumentada = [A[i] + [B[i][0]] for i in range(len(A))]
            except Exception as e:
                 self.resultado_caja.delete('0.0', 'end')
                 self.resultado_caja.insert('0.0', f'Error al preparar Cramer: {e}')
                 self.pasos_caja.delete('0.0', 'end')
                 return

            res = resolver_por_cramer(matriz_aumentada)
            
            self.pasos_caja.delete('0.0', 'end')
            if res.get('pasos'):
                 self.pasos_caja.insert('0.0', '\n'.join(res['pasos']))

            if res['estado'] == 'exito':
                 sol_texto = '\n'.join(f'x{i+1} = {fmt(v)}' for i,v in enumerate(res['solucion']))
                 self.resultado_caja.delete('0.0', 'end')
                 self.resultado_caja.insert('0.0', f"Solucion unica encontrada:\n{sol_texto}")
            elif res['estado'] == 'sin_solucion_unica':
                 self.resultado_caja.delete('0.0', 'end')
                 self.resultado_caja.insert('0.0', res['mensaje'])
            else:
                 self.resultado_caja.delete('0.0', 'end')
                 self.resultado_caja.insert('0.0', f"Error: {res['mensaje']}")

        elif metodo == 'Matriz Inversa':
            res = inverse_steps(A) 
            
            self.pasos_caja.delete('0.0','end')
            steps, ops = res.get('steps',[]), res.get('ops',[])
            total = len(steps); shown = 0
            
            # Mostrar pasos (simplificado para el ejemplo)
            for i, M in enumerate(steps):
                if i < 10:  # Mostrar solo primeros 10 pasos
                    if i < len(ops) and ops[i]: 
                        self.pasos_caja.insert('end', f'Op: {ops[i]}\n')
                    self.append_matriz(M, f'Paso {i}:')
                    shown += 1
            
            if res.get('status') == 'invertible':
                inv = res['inverse']
                # Calcular solucion: x = A⁻¹ * b
                solucion = []
                for i in range(len(inv)):
                    suma = 0.0
                    for j in range(len(inv[0])):
                        suma += inv[i][j] * B[j][0]
                    solucion.append(suma)
                
                sol_texto = '\n'.join(f'x{i+1} = {fmt(v)}' for i,v in enumerate(solucion))
                self.resultado_caja.delete('0.0', 'end')
                self.resultado_caja.insert('0.0', f"A es invertible. Solucion:\n{sol_texto}")
            elif res.get('status') == 'singular':
                 self.resultado_caja.delete('0.0', 'end')
                 self.resultado_caja.insert('0.0', 'A es singular (no tiene inversa)')
            else:
                 self.resultado_caja.delete('0.0', 'end')
                 self.resultado_caja.insert('0.0', f"Error: {res.get('mensaje','error desconocido en inversa')}")

        else:  # Gauss o Gauss-Jordan
            matriz_aumentada = [A[i] + B[i] for i in range(len(A))]
            
            if metodo == 'Gauss-Jordan':
                res = gauss_jordan_steps(matriz_aumentada)
            else:  # Eliminacion Gaussiana
                res = gauss_steps(matriz_aumentada)
            
            self.pasos_caja.delete('0.0','end')
            steps, ops = res.get('steps',[]), res.get('ops',[])
            total = len(steps); shown = 0
            
            # Mostrar pasos
            for i, paso in enumerate(steps):
                if i < 10:  # Mostrar solo primeros 10 pasos
                    if i < len(ops) and ops[i]: 
                        self.pasos_caja.insert('end', f'Op: {ops[i]}\n')
                    self.append_matriz(paso, f'Paso {i}:')
                    shown += 1
            
            status = res.get('status'); sol = res.get('solution')
            self.resultado_caja.delete('0.0', 'end')
            if status=='unique' and sol is not None:
                txt = 'Solucion unica:\n' + '\n'.join(f'x{i+1} = {v:.6g}' for i,v in enumerate(sol))
            elif status=='inconsistent': 
                txt = 'El sistema es inconsistente (sin solucion)'
            elif status=='infinite':
                libres = res.get('free_vars', []); base = res.get('basic_solution', {})
                m = len(A[0])
                lineas=[]
                for i in range(m):
                    if i in libres: lineas.append(f'x{i+1} = variable libre')
                    else: lineas.append(f'x{i+1} = {base.get(i,0.0):.6g}  (con libres = 0)')
                txt = 'Soluciones infinitas:\n' + '\n'.join(lineas)
            elif status=='empty': 
                txt = 'Matriz vacia'
            else: 
                txt = f"Estado: {status}"
            self.resultado_caja.insert('0.0', txt)

    def limpiar_matrices(self):
        for fila_entradas in self.entradas_a:
            for entrada in fila_entradas:
                if entrada: entrada.delete(0,'end')
        for fila_entradas in self.entradas_b:
            for entrada in fila_entradas:
                if entrada: entrada.delete(0,'end')
        
        self.resultado_caja.delete('0.0','end')
        self.pasos_caja.delete('0.0','end')
        self.caja_ecuaciones.delete('1.0', 'end')
        self.caja_ecuaciones.insert("0.0", "2x + 3y - z = 5\nx - y + 2z = 10\n3x + 2y = 0")

    def mostrar(self):
        self.grid(row=0, column=0, sticky="nsew")