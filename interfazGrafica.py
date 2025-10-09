from datetime import datetime
import customtkinter as ctk

# ======= Configuración de “paso a paso” =======
DETALLE_MAX = 6        # si max(filas, cols) > DETALLE_MAX -> modo resumen
BLOQUE_DETALLE = 3     # tamaño del bloque 3x3 para mostrar detalle parcial
MAX_SNAPSHOTS = 80     # máximo de snapshots a imprimir para Gauss/Jordan
PASO_SALTOS = 5        # luego de los primeros 20 pasos, imprimir 1 de cada PASO_SALTOS

def _fmt(x: float) -> str:
    return f"{x:.4g}"


class AplicacionPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Menú Principal Mathpro")
        self.geometry("900x600")
        self.minsize(800, 500)

        # --- Layout raíz
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Panel de navegación izquierdo
        self._crear_panel_nav()

        # --- Contenedor principal (cabecera + contenido)
        self._crear_panel_principal()

        # Sección inicial
        self.seccion_actual = None
        self.mostrar_seccion('Álgebra Lineal')

        # Reloj del encabezado
        self.actualizar_fecha_hora()

    # ------------------------------------------------------------
    # Construcción UI
    # ------------------------------------------------------------
    def _crear_panel_nav(self):
        self.marco_nav = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.marco_nav.grid(row=0, column=0, sticky="nswe")
        self.marco_nav.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=0)
        self.marco_nav.grid_rowconfigure(6, weight=1)

        titulo = ctk.CTkLabel(self.marco_nav, text="Menú", font=ctk.CTkFont(size=18, weight="bold"))
        titulo.grid(row=0, column=0, padx=12, pady=(12, 8), sticky="w")

        self.btn_algebra_lineal = ctk.CTkButton(
            self.marco_nav,
            text="  Álgebra Lineal",
            anchor="w",
            command=lambda: self.mostrar_seccion('Álgebra Lineal')
        )
        self.btn_algebra_lineal.grid(row=1, column=0, sticky="ew", padx=12, pady=6)

        ctk.CTkLabel(self.marco_nav, text="").grid(row=6, column=0, sticky="nswe")

    def _crear_panel_principal(self):
        self.marco_principal = ctk.CTkFrame(self, corner_radius=0)
        self.marco_principal.grid(row=0, column=1, sticky="nswe", padx=12, pady=12)
        self.marco_principal.grid_rowconfigure(0, weight=0)
        self.marco_principal.grid_rowconfigure(1, weight=1)
        self.marco_principal.grid_columnconfigure(0, weight=1)

        # Cabecera
        self.cabecera = ctk.CTkFrame(self.marco_principal, height=60, corner_radius=0)
        self.cabecera.grid(row=0, column=0, sticky="ew")
        self.cabecera.grid_columnconfigure(0, weight=1)
        self.cabecera.grid_columnconfigure(1, weight=0)

        self.etiqueta_cabecera = ctk.CTkLabel(self.cabecera, text="", font=ctk.CTkFont(size=20, weight="bold"))
        self.etiqueta_cabecera.grid(row=0, column=0, sticky="w", padx=10)

        self.etiqueta_fecha_hora = ctk.CTkLabel(self.cabecera, text="", font=ctk.CTkFont(size=11))
        self.etiqueta_fecha_hora.grid(row=0, column=1, sticky="e", padx=10)

        # Contenido
        self.contenido = ctk.CTkFrame(self.marco_principal, corner_radius=6)
        self.contenido.grid(row=1, column=0, sticky="nswe", pady=(12, 0))
        self.contenido.grid_rowconfigure(0, weight=1)
        self.contenido.grid_columnconfigure(0, weight=1)

        self.etiqueta_contenido = ctk.CTkLabel(
            self.contenido, text="Selecciona una sección del menú a la izquierda.", anchor="w"
        )
        self.etiqueta_contenido.grid(row=0, column=0, sticky="nw", padx=12, pady=12)

    # ------------------------------------------------------------
    # Secciones
    # ------------------------------------------------------------
    def mostrar_seccion(self, nombre: str):
        self.seccion_actual = nombre
        self.etiqueta_cabecera.configure(text=nombre)

        for widget in self.contenido.winfo_children():
            widget.destroy()

        if nombre == 'Álgebra Lineal':
            self._cargar_ui_algebra_lineal()
        else:
            ctk.CTkLabel(
                self.contenido,
                text=f"Has seleccionado: {nombre}\n\nContenido de ejemplo para la sección.",
                justify="left"
            ).grid(row=0, column=0, sticky="nw", padx=12, pady=12)

    def _cargar_ui_algebra_lineal(self):
        # Grid del contenedor de contenido
        self.contenido.grid_rowconfigure(0, weight=0)   # barra superior
        self.contenido.grid_rowconfigure(1, weight=1)   # matrices (A,B)
        self.contenido.grid_rowconfigure(2, weight=0)   # controles
        self.contenido.grid_rowconfigure(3, weight=1)   # pasos+resultado
        self.contenido.grid_columnconfigure(0, weight=1)

        # --- Barra superior
        marco_sup = ctk.CTkFrame(self.contenido)
        marco_sup.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        marco_sup.grid_columnconfigure(tuple(range(0, 8)), weight=0)

        ctk.CTkLabel(marco_sup, text="Filas:").grid(row=0, column=0, padx=(4, 2))
        self.filas_var = ctk.StringVar(value="2")
        self.ent_filas = ctk.CTkEntry(marco_sup, width=60, textvariable=self.filas_var)
        self.ent_filas.grid(row=0, column=1, padx=(0, 8))

        ctk.CTkLabel(marco_sup, text="Columnas:").grid(row=0, column=2, padx=(4, 2))
        self.columnas_var = ctk.StringVar(value="2")
        self.ent_columnas = ctk.CTkEntry(marco_sup, width=60, textvariable=self.columnas_var)
        self.ent_columnas.grid(row=0, column=3, padx=(0, 8))

        self.opcion_var = ctk.StringVar(value="Suma")
        menu_opciones = ctk.CTkOptionMenu(
            marco_sup,
            values=["Suma", "Resta", "Multiplicación", "Gauss/Gauss-Jordan", "Independencia"],
            variable=self.opcion_var
        )
        menu_opciones.grid(row=0, column=4, padx=(8, 8))

        # Modo Gauss
        self.modo_gauss_var = ctk.StringVar(value="Gauss-Jordan")
        self.menu_modo_gauss = ctk.CTkOptionMenu(marco_sup, values=["Gauss", "Gauss-Jordan"], variable=self.modo_gauss_var)
        self.menu_modo_gauss.grid(row=0, column=5, padx=(4, 4))
        self.menu_modo_gauss.grid_remove()

        # Traza de cambio de operación
        try:
            self.opcion_var.trace_add('write', lambda *args: self.al_cambiar_operacion())
        except Exception:
            self.opcion_var.trace('w', lambda *args: self.al_cambiar_operacion())

        self.btn_generar = ctk.CTkButton(marco_sup, text="Generar matrices", command=self.generar_cuadriculas_matriz)
        self.btn_generar.grid(row=0, column=6, padx=(8, 4))

        # --- Zona media (matrices A y B)
        medio = ctk.CTkFrame(self.contenido)
        medio.grid(row=1, column=0, sticky="nswe", padx=12, pady=6)
        medio.grid_columnconfigure(0, weight=1)
        medio.grid_columnconfigure(1, weight=1)

        # Matriz A
        self.marco_a = ctk.CTkFrame(medio)
        self.marco_a.grid(row=0, column=0, sticky="nswe", padx=(0, 6))
        self.etiqueta_a = ctk.CTkLabel(self.marco_a, text="Matriz A")
        self.etiqueta_a.grid(row=0, column=0, sticky="w", padx=8, pady=6)

        self.texto_a = ctk.CTkTextbox(self.marco_a, height=100)
        self.texto_a.grid(row=1, column=0, sticky="we", padx=8)

        ctk.CTkButton(self.marco_a, text="Leer desde texto",
                      command=lambda: self.leer_matriz_desde_texto('A'))\
            .grid(row=2, column=0, sticky="w", padx=8, pady=6)

        # >>> Campo escalar de A (junto a la grilla) <<<
        self.lbl_coef_a = ctk.CTkLabel(self.marco_a, text="α:")
        self.lbl_coef_a.grid(row=3, column=0, sticky="w", padx=(8, 2), pady=(0, 2))
        self.ent_coef_a = ctk.CTkEntry(self.marco_a, width=48)
        self.ent_coef_a.grid(row=3, column=0, sticky="w", padx=(36, 0), pady=(0, 2))

        # Matriz B
        self.marco_b = ctk.CTkFrame(medio)
        self.marco_b.grid(row=0, column=1, sticky="nswe", padx=(6, 0))
        ctk.CTkLabel(self.marco_b, text="Matriz B").grid(row=0, column=0, sticky="w", padx=8, pady=6)

        self.texto_b = ctk.CTkTextbox(self.marco_b, height=100)
        self.texto_b.grid(row=1, column=0, sticky="we", padx=8)

        ctk.CTkButton(self.marco_b, text="Leer desde texto",
                      command=lambda: self.leer_matriz_desde_texto('B'))\
            .grid(row=2, column=0, sticky="w", padx=8, pady=6)

        # >>> Campo escalar de B (junto a la grilla) <<<
        self.lbl_coef_b = ctk.CTkLabel(self.marco_b, text="β:")
        self.lbl_coef_b.grid(row=3, column=0, sticky="w", padx=(8, 2), pady=(0, 2))
        self.ent_coef_b = ctk.CTkEntry(self.marco_b, width=48)
        self.ent_coef_b.grid(row=3, column=0, sticky="w", padx=(36, 0), pady=(0, 2))

        # --- Controles (Calcular / Limpiar)
        controles = ctk.CTkFrame(self.contenido)
        controles.grid(row=2, column=0, sticky="ew", padx=12, pady=(6, 12))
        ctk.CTkButton(controles, text="Calcular", command=self.calcular_operacion).grid(row=0, column=0, padx=6)
        ctk.CTkButton(controles, text="Limpiar", command=self.limpiar_matrices).grid(row=0, column=1, padx=6)

        # --- Pasos (izq) + Resultado (der)
        inferior = ctk.CTkFrame(self.contenido)
        inferior.grid(row=3, column=0, sticky="nswe", padx=12, pady=(6, 12))
        inferior.grid_rowconfigure(0, weight=1)
        inferior.grid_columnconfigure(0, weight=1)
        inferior.grid_columnconfigure(1, weight=1)

        # Pasos
        self.marco_pasos = ctk.CTkFrame(inferior)
        self.marco_pasos.grid(row=0, column=0, sticky="nswe", padx=(0, 6))
        self.marco_pasos.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.marco_pasos, text="Pasos:").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.pasos_caja = ctk.CTkTextbox(self.marco_pasos, height=220)
        self.pasos_caja.grid(row=1, column=0, sticky="nswe", padx=8, pady=(0, 8))

        # Resultado
        self.marco_resultado = ctk.CTkFrame(inferior)
        self.marco_resultado.grid(row=0, column=1, sticky="nswe", padx=(6, 0))
        self.marco_resultado.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.marco_resultado, text="Resultado:").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.resultado_caja = ctk.CTkTextbox(self.marco_resultado, height=220)
        self.resultado_caja.grid(row=1, column=0, sticky="nswe", padx=8, pady=(0, 8))

        # Estado de rejillas
        self.entradas_a = []
        self.entradas_b = []
        self.grilla_a = []
        self.grilla_b = []

        # Ajustar visibilidad según operación
        self.al_cambiar_operacion()

    # ------------------------------------------------------------
    # Utilidades internas UI
    # ------------------------------------------------------------
    def _set_resultado(self, texto: str, limpiar_pasos: bool = False):
        if limpiar_pasos:
            self.pasos_caja.delete('0.0', 'end')
        self.resultado_caja.delete('0.0', 'end')
        self.resultado_caja.insert('0.0', texto)

    def _append_matriz(self, M, titulo=None):
        if titulo:
            self.pasos_caja.insert('end', f'{titulo}\n')
        for fila in M:
            self.pasos_caja.insert('end', '  '.join(_fmt(v) for v in fila) + '\n')
        self.pasos_caja.insert('end', '\n')

    def _leer_escalar(self, entry_widget) -> float:
        """Lee un escalar; vacío -> 1, '+' -> 1, '-' -> -1."""
        txt = entry_widget.get().strip() if entry_widget else ''
        if txt in ('', '+'):
            return 1.0
        if txt == '-':
            return -1.0
        return float(txt)

    def _es_grande(self, f, c) -> bool:
        return max(f, c) > DETALLE_MAX

    # ------------------------------------------------------------
    # Acciones UI
    # ------------------------------------------------------------
    def generar_cuadriculas_matriz(self):
        # Validar dimensiones
        try:
            filas = int(self.ent_filas.get())
            columnas = int(self.ent_columnas.get())
            if filas <= 0 or columnas <= 0:
                raise ValueError()
        except Exception:
            self._set_resultado('Filas y columnas deben ser enteros positivos.', limpiar_pasos=False)
            return

        # Limpiar cuadriculas previas
        for w in self.grilla_a:
            w.destroy()
        for w in self.grilla_b:
            w.destroy()
        self.grilla_a, self.grilla_b = [], []

        # Crear rejillas (empezamos en fila 4 para dejar sitio al escalar)
        self.entradas_a = [[None] * columnas for _ in range(filas)]
        self.entradas_b = [[None] * columnas for _ in range(filas)] if self.opcion_var.get() not in ('Gauss/Gauss-Jordan', 'Independencia') else []

        start_row = 4
        for i in range(filas):
            for j in range(columnas):
                e = ctk.CTkEntry(self.marco_a, width=60)
                e.grid(row=start_row + i, column=j, padx=4, pady=2)
                self.grilla_a.append(e)
                self.entradas_a[i][j] = e

                if self.opcion_var.get() not in ('Gauss/Gauss-Jordan', 'Independencia'):
                    e2 = ctk.CTkEntry(self.marco_b, width=60)
                    e2.grid(row=start_row + i, column=j, padx=4, pady=2)
                    self.grilla_b.append(e2)
                    self.entradas_b[i][j] = e2

        # Mensaje contextual
        if self.opcion_var.get() == 'Independencia':
            self._set_resultado('Conjuntos listos. Completa entradas o pega vectores (uno por línea) y usa "Leer desde texto".')
        else:
            self._set_resultado('Matrices listas. Completa entradas o pega texto y usa "Leer desde texto".')

    def al_cambiar_operacion(self):
        op = self.opcion_var.get()
        self.etiqueta_a.configure(text='Conjuntos de Vectores' if op == 'Independencia' else 'Matriz A')
        self.btn_generar.configure(text='Generar conjuntos' if op == 'Independencia' else 'Generar matrices')

        # Menú Gauss
        self.menu_modo_gauss.grid() if op == 'Gauss/Gauss-Jordan' else self.menu_modo_gauss.grid_remove()

        # Panel B (oculto en Gauss/Independencia)
        if op in ('Gauss/Gauss-Jordan', 'Independencia'):
            self.marco_b.grid_remove()
        else:
            self.marco_b.grid()

        # Escalares: visibles siempre; deshabilitados en multiplicación
        usar_escalars = op in ('Suma', 'Resta')
        try:
            state = 'normal' if usar_escalars else 'disabled'
            self.ent_coef_a.configure(state=state)
            self.ent_coef_b.configure(state=state)
            self.lbl_coef_a.configure(text='α:' if usar_escalars else 'α')
            self.lbl_coef_b.configure(text='β:' if usar_escalars else 'β')
        except Exception:
            pass

    def leer_entradas_matriz(self, entradas):
        filas = len(entradas)
        columnas = len(entradas[0]) if filas > 0 else 0
        matriz = [[0.0] * columnas for _ in range(filas)]
        for i in range(filas):
            for j in range(columnas):
                txt = entradas[i][j].get().strip()
                try:
                    matriz[i][j] = float(txt) if txt != '' else 0.0
                except Exception:
                    raise ValueError(f'Valor inválido en ({i + 1},{j + 1}): "{txt}"')
        return matriz

    def leer_matriz_desde_texto(self, cual='A'):
        if self.opcion_var.get() == 'Gauss/Gauss-Jordan' and cual == 'B':
            self._set_resultado('En modo Gauss/Gauss-Jordan sólo se permite una matriz (Matriz A).')
            return

        destino_texto = self.texto_a if cual == 'A' else self.texto_b
        contenido = destino_texto.get('0.0', 'end').strip()
        if contenido == '':
            self._set_resultado('Texto vacío para la matriz.')
            return

        lineas = [ln.strip() for ln in contenido.splitlines() if ln.strip() != '']
        matriz_txt = []
        try:
            for ln in lineas:
                partes = [p for p in ln.replace(',', ' ').split()]
                matriz_txt.append([float(p) for p in partes])
        except Exception as e:
            self._set_resultado(f'Valor inválido al parsear: {e}')
            return

        if self.opcion_var.get() == 'Independencia':
            if not matriz_txt:
                self._set_resultado('No se detectaron vectores en el texto.')
                return
            tam = len(matriz_txt[0])
            if any(len(v) != tam for v in matriz_txt):
                self._set_resultado('Todos los vectores deben tener la misma dimensión.')
                return
            filas = tam
            columnas = len(matriz_txt)
            matriz = [[0.0] * columnas for _ in range(filas)]
            for c, v in enumerate(matriz_txt):
                for r in range(filas):
                    matriz[r][c] = v[r]
        else:
            matriz = matriz_txt

        if any(len(f) != len(matriz[0]) for f in matriz):
            self._set_resultado('La matriz no es rectangular (filas con distinta cantidad de columnas).')
            return

        filas, columnas = len(matriz), len(matriz[0])

        try:
            if self.entradas_a and len(self.entradas_a) == filas and len(self.entradas_a[0]) == columnas:
                entradas = self.entradas_a if cual == 'A' else self.entradas_b
                for i in range(filas):
                    for j in range(columnas):
                        entradas[i][j].delete(0, 'end')
                        entradas[i][j].insert(0, str(matriz[i][j]))
            else:
                self.ent_filas.delete(0, 'end');  self.ent_filas.insert(0, str(filas))
                self.ent_columnas.delete(0, 'end'); self.ent_columnas.insert(0, str(columnas))
                self.generar_cuadriculas_matriz()
                entradas = self.entradas_a if cual == 'A' else self.entradas_b
                for i in range(filas):
                    for j in range(columnas):
                        entradas[i][j].insert(0, str(matriz[i][j]))
            self._set_resultado(f'Matriz {cual} leída ({filas}x{columnas}).')
        except Exception as e:
            self._set_resultado(f'Error al poblar entradas: {e}')

    # ------------------------------------------------------------
    # Cálculos
    # ------------------------------------------------------------
    def _detalle_bloque(self, fa, ca):
        return min(BLOQUE_DETALLE, fa), min(BLOQUE_DETALLE, ca)

    def calcular_operacion(self):
        op = self.opcion_var.get()

        # ----------------- Métodos de Gauss -----------------
        if op == 'Gauss/Gauss-Jordan':
            try:
                A = self.leer_entradas_matriz(self.entradas_a)
            except Exception as e:
                self._set_resultado(f'Error: {e}')
                return

            from Complement import gauss_steps, gauss_jordan_steps
            modo = self.modo_gauss_var.get() if hasattr(self, 'modo_gauss_var') else 'Gauss-Jordan'
            res = gauss_steps(A) if modo == 'Gauss' else gauss_jordan_steps(A)

            # Pasos (con límite)
            self.pasos_caja.delete('0.0', 'end')
            steps = res.get('steps', [])
            ops = res.get('ops', [])
            total = len(steps)
            mostrados = 0
            for i, paso in enumerate(steps):
                if i < 20 or i % PASO_SALTOS == 0:
                    # mostrar la operación textual que generó este paso (si existe)
                    if i < len(ops) and ops[i]:
                        self.pasos_caja.insert('end', f'Op: {ops[i]}\n')
                    self._append_matriz(paso, f'Paso {i}:')
                    mostrados += 1
                if mostrados >= MAX_SNAPSHOTS:
                    break
            if total > mostrados:
                self.pasos_caja.insert('end', f'… ({total - mostrados} pasos omitidos)\n\n')

            # Resultado
            status = res.get('status'); sol = res.get('solution')
            if status == 'unique' and sol is not None:
                texto = 'Solución única:\n' + '\n'.join(f'x{i + 1} = {v:.6g}' for i, v in enumerate(sol))
            elif status == 'inconsistent':
                texto = 'El sistema es inconsistente (sin solución).'
            elif status in ('infinite', 'incomplete'):
                texto = 'El sistema tiene infinitas soluciones o faltan pivotes.'
            elif status == 'empty':
                texto = 'Matriz vacía.'
            else:
                texto = f"Estado: {status}"
            self._set_resultado(texto)
            return

        # --------------- Independencia de vectores ---------------
        if op == 'Independencia':
            try:
                A = self.leer_entradas_matriz(self.entradas_a)
            except Exception as e:
                self._set_resultado(f'Error: {e}')
                return

            from Complement import independenciaVectores, gauss_jordan_steps
            veredicto = independenciaVectores(A)

            # Paso a paso (RREF) con límite
            self.pasos_caja.delete('0.0', 'end')
            try:
                rref = gauss_jordan_steps(A)
                steps = rref.get('steps', [])
                ops = rref.get('ops', [])
                total = len(steps)
                mostrados = 0
                for i, paso in enumerate(steps):
                    if i < 20 or i % PASO_SALTOS == 0:
                        # mostrar operación textual si está disponible
                        if i < len(ops) and ops[i]:
                            self.pasos_caja.insert('end', f'Op: {ops[i]}\n')
                        self._append_matriz(paso, f'Paso {i} (RREF):')
                        mostrados += 1
                    if mostrados >= MAX_SNAPSHOTS:
                        break
                if total > mostrados:
                    self.pasos_caja.insert('end', f'… ({total - mostrados} pasos omitidos)\n\n')
            except Exception as e:
                self.pasos_caja.insert('end', f'No se pudo mostrar el paso a paso: {e}\n')

            # Resultado
            if veredicto.get('num_vectors', 0) == 0:
                self._set_resultado('No hay vectores (matriz vacía).')
            else:
                r = veredicto.get('rank'); k = veredicto.get('num_vectors')
                msg = f"Rank = {r} / {k}.\n"
                msg += 'Linealmente independiente.' if veredicto.get('independent') else 'Linealmente dependiente.'
                self._set_resultado(msg)
            return

        # ----------------- Operaciones A y B (Suma/Resta/Multiplicación) -----------------
        try:
            A = self.leer_entradas_matriz(self.entradas_a)
            B = self.leer_entradas_matriz(self.entradas_b)
        except Exception as e:
            self._set_resultado(f'Error: {e}')
            return

        fa = len(A); ca = len(A[0]) if fa > 0 else 0
        fb = len(B); cb = len(B[0]) if fb > 0 else 0

        self.pasos_caja.delete('0.0', 'end')  # siempre mostrar pasos

        try:
            if op in ('Suma', 'Resta'):
                if fa != fb or ca != cb:
                    raise ValueError('Para suma/resta ambas matrices deben tener las mismas dimensiones.')

                # escalares (vacío -> 1, '-' -> -1)
                alpha = self._leer_escalar(self.ent_coef_a)
                beta = self._leer_escalar(self.ent_coef_b)
                signo = 1.0 if op == 'Suma' else -1.0

                # imprimir A y B
                self._append_matriz(A, 'Matriz A:')
                self._append_matriz(B, 'Matriz B:')

                # αA y (±)βB
                Aesc = [[alpha * A[i][j] for j in range(ca)] for i in range(fa)]
                Besc = [[signo * beta * B[i][j] for j in range(cb)] for i in range(fb)]

                self._append_matriz(Aesc, f'α·A (α={_fmt(alpha)}):')
                self._append_matriz(Besc, f'{"+" if signo>0 else "-"} β·B (β={_fmt(beta)}):')

                # Resultado
                C = [[Aesc[i][j] + Besc[i][j] for j in range(ca)] for i in range(fa)]

                # Detalle por entrada (completo o resumido)
                if self._es_grande(fa, ca):
                    rdet, cdet = self._detalle_bloque(fa, ca)
                    self.pasos_caja.insert('end', f'Detalle por entrada (bloque {rdet}×{cdet}):\n')
                    for i in range(rdet):
                        for j in range(cdet):
                            self.pasos_caja.insert(
                                'end',
                                f'C[{i+1},{j+1}] = {_fmt(alpha)}·{_fmt(A[i][j])} '
                                f'{"+" if signo>0 else "-"} {_fmt(beta)}·{_fmt(B[i][j])} = {_fmt(C[i][j])}\n'
                            )
                    self.pasos_caja.insert('end', '… (resto de entradas resumidas)\n\n')
                else:
                    for i in range(fa):
                        for j in range(ca):
                            self.pasos_caja.insert(
                                'end',
                                f'C[{i+1},{j+1}] = {_fmt(alpha)}·{_fmt(A[i][j])} '
                                f'{"+" if signo>0 else "-"} {_fmt(beta)}·{_fmt(B[i][j])} = {_fmt(C[i][j])}\n'
                            )
                    self.pasos_caja.insert('end', '\n')

                self._append_matriz(C, 'Resultado C = αA ' + ('+' if signo>0 else '−') + ' βB:')
                matriz_resultado = C

            elif op == 'Multiplicación':
                if ca != fb:
                    raise ValueError('Para multiplicación: columnas de A deben igualar filas de B.')

                self._append_matriz(A, 'Matriz A:')
                self._append_matriz(B, 'Matriz B:')

                C = [[0.0 for _ in range(cb)] for _ in range(fa)]
                # detalle (completo o 3x3)
                rdet, cdet = (fa, cb) if not self._es_grande(fa, cb) else self._detalle_bloque(fa, cb)
                self.pasos_caja.insert('end', f'Detalle de producto punto para {rdet}×{cdet} entradas:\n')
                for i in range(rdet):
                    for j in range(cdet):
                        terminos = []
                        s = 0.0
                        for k in range(ca):
                            terminos.append(f'{_fmt(A[i][k])}·{_fmt(B[k][j])}')
                            s += A[i][k] * B[k][j]
                        self.pasos_caja.insert('end', f'C[{i+1},{j+1}] = ' + ' + '.join(terminos) + f' = {_fmt(s)}\n')
                        C[i][j] = s
                if self._es_grande(fa, cb):
                    self.pasos_caja.insert('end', '… (resto de entradas resumidas)\n')
                    # completar resto sin escribir detalle
                    for i in range(fa):
                        for j in range(cb):
                            if i < rdet and j < cdet:
                                continue
                            C[i][j] = sum(A[i][k] * B[k][j] for k in range(ca))

                self.pasos_caja.insert('end', '\n')
                self._append_matriz(C, 'Resultado C = A·B:')
                matriz_resultado = C

            else:
                raise ValueError('Operación desconocida')
        except Exception as e:
            self._set_resultado(f'Error: {e}')
            return

        # Mostrar resultado
        self.resultado_caja.delete('0.0', 'end')
        self.resultado_caja.insert('0.0', '\n'.join('  '.join(_fmt(v) for v in fila) for fila in matriz_resultado))

    def limpiar_matrices(self):
        try:
            for r in self.entradas_a:
                for e in r:
                    e.delete(0, 'end')
            for r in self.entradas_b:
                for e in r:
                    e.delete(0, 'end')
        except Exception:
            pass
        self.texto_a.delete('0.0', 'end')
        self.texto_b.delete('0.0', 'end')
        self.resultado_caja.delete('0.0', 'end')
        self.pasos_caja.delete('0.0', 'end')
        try:
            self.ent_coef_a.delete(0, 'end')
            self.ent_coef_b.delete(0, 'end')
        except Exception:
            pass

    # ------------------------------------------------------------
    # Reloj de cabecera
    # ------------------------------------------------------------
    def actualizar_fecha_hora(self):
        ahora = datetime.now()
        formateado = ahora.strftime("%A, %d %B %Y | %H:%M:%S")
        self.etiqueta_fecha_hora.configure(text=formateado)
        self.after(1000, self.actualizar_fecha_hora)


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = AplicacionPrincipal()
    app.mainloop()