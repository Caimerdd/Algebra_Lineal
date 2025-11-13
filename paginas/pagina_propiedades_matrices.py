import customtkinter as ctk
from paginas.pagina_base import PaginaBase
from app_config import COLOR_FONDO_SECUNDARIO, COLOR_ALGEBRA, COLOR_HOVER, COLOR_BOTON_SECUNDARIO, COLOR_BOTON_SECUNDARIO_HOVER
from app_config import fmt, parse_valor

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
        self.ent_columnas_a = ctk.CTkEntry(marco_dims_a, width=60)
        self.ent_columnas_a.insert(0, "2")
        self.ent_columnas_a.grid(row=0, column=3)

        # Marco para la cuadrícula de A
        self.marco_grilla_a = ctk.CTkFrame(self.marco_a)
        self.marco_grilla_a.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))

        # Listas para entradas
        self.entradas_a = []
        self.grilla_a = []
        
        # Variable de visibilidad
        self.matriz_a_visible = True

        # Controles
        marco_controles = ctk.CTkFrame(self)
        marco_controles.grid(row=2, column=0, sticky="ew", padx=12, pady=8)
        
        ctk.CTkButton(marco_controles, text="Generar Cuadricula", 
                     command=self.generar_cuadriculas_propiedades,
                     fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        
        ctk.CTkButton(marco_controles, text="Calcular Propiedad", 
                     command=self.calcular_propiedad_matricial,
                     fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER).grid(row=0, column=1, padx=6)
        
        ctk.CTkButton(marco_controles, text="Limpiar", 
                     command=self.limpiar_propiedades,
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
        """Alterna la visibilidad de la matriz."""
        if matriz == 'a':
            if self.matriz_a_visible:
                self.marco_grilla_a.grid_remove()
                self.btn_expandir_a.configure(text="+")
                self.matriz_a_visible = False
            else:
                self.marco_grilla_a.grid()
                self.btn_expandir_a.configure(text="−")
                self.matriz_a_visible = True

    def generar_cuadriculas_propiedades(self):
        try:
            filas_a = int(self.ent_filas_a.get())
            cols_a = int(self.ent_columnas_a.get())
            
            if filas_a <= 0 or cols_a <= 0:
                raise ValueError("Las dimensiones deben ser numeros enteros positivos")

            # Limpiar cuadriculas existentes
            for widget in self.grilla_a: 
                widget.destroy()
            self.grilla_a = []

            # Inicializar listas
            self.entradas_a = [[None]*cols_a for _ in range(filas_a)]

            # Crear cuadricula para A
            for i in range(filas_a):
                for j in range(cols_a):
                    e = ctk.CTkEntry(self.marco_grilla_a, width=60)
                    e.grid(row=i, column=j, padx=2, pady=2)
                    self.grilla_a.append(e)
                    self.entradas_a[i][j] = e

            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0','Matriz lista para ingresar datos')

        except ValueError as e:
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f'Error: {e}')

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

    def calcular_propiedad_matricial(self):
        try:
            # Importar modulos de calculo
            try:
                from Complement import (
                    pasos_determinante, independenciaVectores
                )
            except ImportError:
                self.resultado_caja.delete('0.0', 'end')
                self.resultado_caja.insert('0.0', "ERROR: No se pudo cargar Complement.py")
                return

            A = self.leer_entradas_cuadricula(self.entradas_a)
                 
        except ValueError as e:
            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', f'Error de entrada: {e}')
            self.pasos_caja.delete('0.0', 'end')
            return
        except Exception as e:
            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', f'Error inesperado al leer matriz: {e}')
            self.pasos_caja.delete('0.0', 'end')
            return

        propiedad = self.propiedad_matricial_var.get()
        
        self.pasos_caja.delete('0.0','end')
        try:
            if propiedad == 'Determinante':
                if len(A) != len(A[0]):
                    raise ValueError("El determinante solo existe para matrices cuadradas")
                
                res = pasos_determinante(A) 
                if res['estado'] == 'exito':
                    self.pasos_caja.delete('0.0', 'end')
                    self.pasos_caja.insert('0.0', '\n'.join(res['pasos']))
                    self.resultado_caja.delete('0.0', 'end')
                    self.resultado_caja.insert('0.0', f"El determinante es: {fmt(res['determinante'])}")
                else:
                    self.resultado_caja.delete('0.0', 'end')
                    self.resultado_caja.insert('0.0', f"Error: {res['mensaje']}")

            elif propiedad == 'Independencia Lineal':
                ver = independenciaVectores(A)
                
                if ver.get('num_vectors',0)==0: 
                    self.resultado_caja.delete('0.0', 'end')
                    self.resultado_caja.insert('0.0', 'No hay vectores (matriz vacia)')
                else:
                    r,k = ver.get('rank'), ver.get('num_vectors')
                    self.resultado_caja.delete('0.0', 'end')
                    self.resultado_caja.insert('0.0', f"Rango = {r} / {k} vectores\n" + 
                                                  ('Linealmente Independiente' if ver.get('independent') else 'Linealmente Dependiente'))

            elif propiedad == 'Rango':
                # Usar independenciaVectores para calcular el rango
                ver = independenciaVectores(A)
                rango = ver.get('rank', 0)
                self.resultado_caja.delete('0.0', 'end')
                self.resultado_caja.insert('0.0', f"El rango de la matriz es: {rango}")

        except ValueError as e:
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f'Error: {e}')
        except Exception as e:
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0', f'Error inesperado al calcular: {e}')

    def limpiar_propiedades(self):
        for fila_entradas in self.entradas_a:
            for entrada in fila_entradas:
                if entrada: entrada.delete(0,'end')
        
        self.resultado_caja.delete('0.0','end')
        self.pasos_caja.delete('0.0','end')

    def mostrar(self):
        self.grid(row=0, column=0, sticky="nsew")