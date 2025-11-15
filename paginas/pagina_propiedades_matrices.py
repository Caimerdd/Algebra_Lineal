import customtkinter as ctk
import sympy as sp # Para formatear matrices
from paginas.pagina_base import PaginaBase
from app_config import (COLOR_FONDO_SECUNDARIO, COLOR_ALGEBRA, COLOR_HOVER, 
                        COLOR_BOTON_SECUNDARIO, COLOR_BOTON_SECUNDARIO_HOVER)
from app_config import fmt, parse_valor

# Intentamos importar la lógica
try:
    from Complement import (
        pasos_determinante, independenciaVectores
    )
    LOGICA_DISPONIBLE = True
except ImportError:
    LOGICA_DISPONIBLE = False
    print("ADVERTENCIA: No se pudo cargar Complement.py")

class PaginaPropiedadesMatrices(PaginaBase):
    def crear_widgets(self):
        self.configurar_grid()
        self.crear_interfaz()
        self.generar_cuadriculas_propiedades()
    
    def configurar_grid(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def crear_interfaz(self):
        # Selector de Propiedad
        marco_propiedad = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_propiedad.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        
        ctk.CTkLabel(marco_propiedad, text="Propiedad a Calcular:", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=(12, 8), pady=12)
        
        self.propiedad_matricial_var = ctk.StringVar(value="Determinante")
        propiedades = ["Determinante", "Independencia Lineal", "Rango"]
        
        for i, propiedad in enumerate(propiedades):
            rb = ctk.CTkRadioButton(marco_propiedad, text=propiedad, variable=self.propiedad_matricial_var, 
                                   value=propiedad, font=ctk.CTkFont(size=13))
            rb.grid(row=0, column=i+1, padx=8, pady=12)

        # Marco para matriz
        marco_matriz = ctk.CTkFrame(self)
        marco_matriz.grid(row=1, column=0, sticky="nsew", padx=12, pady=8)
        
        # Matriz A
        self.marco_a = ctk.CTkFrame(marco_matriz, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_a.grid(row=0, column=0, sticky="nsew", padx=(0, 0), pady=4)
        self.marco_a.grid_rowconfigure(2, weight=1)
        
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

        self.marco_grilla_a = ctk.CTkFrame(self.marco_a)
        self.marco_grilla_a.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))

        self.entradas_a = []
        self.grilla_a = []
        self.matriz_a_visible = True

        # Controles
        marco_controles = ctk.CTkFrame(self)
        marco_controles.grid(row=2, column=0, sticky="ew", padx=12, pady=8)
        ctk.CTkButton(marco_controles, text="Generar Cuadricula", command=self.generar_cuadriculas_propiedades, fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        ctk.CTkButton(marco_controles, text="Calcular Propiedad", command=self.calcular_propiedad_matricial, fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=1, padx=6)
        ctk.CTkButton(marco_controles, text="Limpiar", command=self.limpiar_propiedades, fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=2, padx=6)

        # Resultados
        marco_resultados = ctk.CTkFrame(self)
        marco_resultados.grid(row=3, column=0, sticky="nsew", padx=12, pady=(0, 12))
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
        try: return sp.pretty(sp.Matrix(M), use_unicode=False) # CORRECCIÓN: use_unicode=False
        except Exception: return str(M)

    def _renderizar_pasos_texto(self, pasos_lista: list):
        self._limpiar_pasos_scroll()
        titulo_actual = "INICIO"
        math_actual = []
        for linea in pasos_lista:
            linea = linea.strip()
            if not linea: continue
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

    def generar_cuadriculas_propiedades(self):
        try:
            filas_a = int(self.ent_filas_a.get())
            cols_a = int(self.ent_columnas_a.get())
            if filas_a <= 0 or cols_a <= 0:
                raise ValueError("Las dimensiones deben ser numeros enteros positivos")

            for widget in self.grilla_a: widget.destroy()
            self.grilla_a = []
            self.entradas_a = [[None]*cols_a for _ in range(filas_a)]

            for i in range(filas_a):
                for j in range(cols_a):
                    e = ctk.CTkEntry(self.marco_grilla_a, width=60)
                    e.grid(row=i, column=j, padx=2, pady=2)
                    self.grilla_a.append(e)
                    self.entradas_a[i][j] = e

            self.limpiar_propiedades()
            self.resultado_caja.configure(state="normal")
            self.resultado_caja.insert('0.0','Matriz lista para ingresar datos')
            self.resultado_caja.configure(state="disabled")

        except ValueError as e:
            self.resultado_caja.configure(state="normal")
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f'Error: {e}')
            self.resultado_caja.configure(state="disabled")

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

    def calcular_propiedad_matricial(self):
        self._limpiar_pasos_scroll()
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete('0.0','end')

        if not LOGICA_DISPONIBLE:
            self.resultado_caja.insert('0.0', "ERROR: No se pudo cargar Complement.py")
            self.resultado_caja.configure(state="disabled")
            return

        try:
            A = self.leer_entradas_cuadricula(self.entradas_a)
        except ValueError as e:
            self.resultado_caja.insert('0.0', f'Error de entrada: {e}')
            self.resultado_caja.configure(state="disabled")
            return
        
        propiedad = self.propiedad_matricial_var.get()
        resultado_texto = ""
        
        try:
            if propiedad == 'Determinante':
                if len(A) != len(A[0]):
                    raise ValueError("El determinante solo existe para matrices cuadradas")
                
                res = pasos_determinante(A) 
                
                if res.get('pasos'):
                    self._renderizar_pasos_texto(res['pasos'])
                    
                if res['estado'] == 'exito':
                    resultado_texto = f"El determinante es:\n\n{fmt(res['determinante'])}"
                else:
                    resultado_texto = f"Error: {res['mensaje']}"

            elif propiedad == 'Independencia Lineal':
                self._crear_bloque_texto("MATRIZ A (VECTORES COLUMNA)", self._matriz_a_pretty(A))
                ver = independenciaVectores(A)
                
                if ver.get('num_vectors',0) == 0: 
                    resultado_texto = 'No hay vectores (matriz vacia)'
                else:
                    r, k = ver.get('rank'), ver.get('num_vectors')
                    self._crear_bloque_texto("RESULTADO", f"Rango = {r}\nNúmero de Vectores = {k}")
                    resultado_texto = f"Rango = {r} / {k} vectores\n"
                    resultado_texto += ('Linealmente Independiente' if ver.get('independent') else 'Linealmente Dependiente')

            elif propiedad == 'Rango':
                self._crear_bloque_texto("MATRIZ A", self._matriz_a_pretty(A))
                ver = independenciaVectores(A)
                rango = ver.get('rank', 0)
                resultado_texto = f"El rango de la matriz es: {rango}"

            self.resultado_caja.insert('0.0', resultado_texto)

        except ValueError as e:
            self.resultado_caja.insert('0.0', f'Error: {e}')
        except Exception as e:
            self.resultado_caja.insert('0.0', f'Error inesperado al calcular: {e}')
            
        self.resultado_caja.configure(state="disabled")

    def limpiar_propiedades(self):
        for fila_entradas in self.entradas_a:
            for entrada in fila_entradas:
                if entrada: entrada.delete(0,'end')
        
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete('0.0','end')
        self.resultado_caja.configure(state="disabled")
        
        self._limpiar_pasos_scroll()

    def mostrar(self):
        self.grid(row=0, column=0, sticky="nsew")