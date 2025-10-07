from datetime import datetime
import customtkinter as ctk


class AplicacionPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Menú Principal Mathpro")
        self.geometry("900x600")
        self.minsize(800, 500)

        # configurar grilla
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # panel de navegación izquierdo
        self.marco_nav = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.marco_nav.grid(row=0, column=0, sticky="nswe")
        self.marco_nav.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=0)
        self.marco_nav.grid_rowconfigure(6, weight=1)

        titulo = ctk.CTkLabel(self.marco_nav, text="Menú", font=ctk.CTkFont(size=18, weight="bold"))
        titulo.grid(row=0, column=0, padx=12, pady=(12, 8), sticky="w")

        # Menú izquierdo: solo Álgebra Lineal
        self.btn_algebra_lineal = ctk.CTkButton(
            self.marco_nav, text="  Álgebra Lineal", anchor="w",
            command=lambda: self.mostrar_seccion('Álgebra Lineal')
        )
        self.btn_algebra_lineal.grid(row=1, column=0, sticky="ew", padx=12, pady=6)

        # relleno para empujar elementos arriba
        self.relleno = ctk.CTkLabel(self.marco_nav, text="")
        self.relleno.grid(row=6, column=0, sticky="nswe")

        # marco de contenido principal
        self.marco_principal = ctk.CTkFrame(self, corner_radius=0)
        self.marco_principal.grid(row=0, column=1, sticky="nswe", padx=12, pady=12)
        self.marco_principal.grid_rowconfigure(0, weight=1)
        self.marco_principal.grid_columnconfigure(0, weight=1)

        # cabecera: título y fecha/hora
        self.cabecera = ctk.CTkFrame(self.marco_principal, height=60, corner_radius=0)
        self.cabecera.grid(row=0, column=0, sticky="ew")
        self.cabecera.grid_columnconfigure(0, weight=1)
        self.cabecera.grid_columnconfigure(1, weight=0)

        self.etiqueta_cabecera = ctk.CTkLabel(self.cabecera, text="", font=ctk.CTkFont(size=20, weight="bold"))
        self.etiqueta_cabecera.grid(row=0, column=0, sticky="w", padx=10)

        self.etiqueta_fecha_hora = ctk.CTkLabel(self.cabecera, text="", font=ctk.CTkFont(size=11))
        self.etiqueta_fecha_hora.grid(row=0, column=1, sticky="e", padx=10)

        # área de contenido
        self.contenido = ctk.CTkFrame(self.marco_principal, corner_radius=6)
        self.contenido.grid(row=1, column=0, sticky="nswe", pady=(12, 0))
        self.contenido.grid_rowconfigure(0, weight=1)
        self.contenido.grid_columnconfigure(0, weight=1)

        # contenido por defecto
        self.etiqueta_contenido = ctk.CTkLabel(self.contenido, text="Selecciona una sección del menú a la izquierda.", anchor="w")
        self.etiqueta_contenido.grid(row=0, column=0, sticky="nw", padx=12, pady=12)

        # sección inicial
        self.seccion_actual = None
        self.mostrar_seccion('Álgebra Lineal')

        # actualizar reloj
        self.actualizar_fecha_hora()

    def mostrar_seccion(self, nombre: str):
        self.seccion_actual = nombre
        self.etiqueta_cabecera.configure(text=nombre)

        # reemplazar contenido
        for widget in self.contenido.winfo_children():
            widget.destroy()

        if nombre == 'Álgebra Lineal':
            # UI Calculadora de matrices
            marco_superior = ctk.CTkFrame(self.contenido)
            marco_superior.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
            self.contenido.grid_rowconfigure(0, weight=0)
            self.contenido.grid_rowconfigure(1, weight=1)
            self.contenido.grid_rowconfigure(2, weight=0)
            self.contenido.grid_rowconfigure(3, weight=1)
            self.contenido.grid_rowconfigure(4, weight=1)
            marco_superior.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=0)

            lbl_filas = ctk.CTkLabel(marco_superior, text="Filas:")
            lbl_filas.grid(row=0, column=0, padx=(4, 2))
            self.filas_var = ctk.StringVar(value="2")
            self.ent_filas = ctk.CTkEntry(marco_superior, width=60, textvariable=self.filas_var)
            self.ent_filas.grid(row=0, column=1, padx=(0, 8))

            lbl_columnas = ctk.CTkLabel(marco_superior, text="Columnas:")
            lbl_columnas.grid(row=0, column=2, padx=(4, 2))
            self.columnas_var = ctk.StringVar(value="2")
            self.ent_columnas = ctk.CTkEntry(marco_superior, width=60, textvariable=self.columnas_var)
            self.ent_columnas.grid(row=0, column=3, padx=(0, 8))

            self.opcion_var = ctk.StringVar(value="Suma")
            menu_opciones = ctk.CTkOptionMenu(
                marco_superior,
                values=["Suma", "Resta", "Multiplicación", "Gauss/Gauss-Jordan", "Independencia"],
                variable=self.opcion_var
            )
            menu_opciones.grid(row=0, column=4, padx=(8, 8))

            # selector modo Gauss
            self.modo_gauss_var = ctk.StringVar(value="Gauss-Jordan")
            self.menu_modo_gauss = ctk.CTkOptionMenu(marco_superior, values=["Gauss", "Gauss-Jordan"], variable=self.modo_gauss_var)
            self.menu_modo_gauss.grid(row=0, column=5, padx=(4, 4))
            self.menu_modo_gauss.grid_remove()

            # rastro de cambio de operación
            try:
                self.opcion_var.trace_add('write', lambda *args: self.al_cambiar_operacion())
            except Exception:
                self.opcion_var.trace('w', lambda *args: self.al_cambiar_operacion())

            self.btn_generar = ctk.CTkButton(marco_superior, text="Generar matrices", command=self.generar_cuadriculas_matriz)
            self.btn_generar.grid(row=0, column=5, padx=(8, 4))

            # zona media: entrada de matrices
            medio = ctk.CTkFrame(self.contenido)
            medio.grid(row=1, column=0, sticky="nswe", padx=12, pady=6)
            medio.grid_columnconfigure(0, weight=1)
            medio.grid_columnconfigure(1, weight=1)

            # Izquierda: Matriz A
            self.marco_a = ctk.CTkFrame(medio)
            self.marco_a.grid(row=0, column=0, sticky="nswe", padx=(0, 6))
            texto_lbl_a = "Matriz A"
            if hasattr(self, 'opcion_var') and self.opcion_var.get() == 'Independencia':
                texto_lbl_a = "Conjuntos de Vectores"
            self.etiqueta_a = ctk.CTkLabel(self.marco_a, text=texto_lbl_a)
            self.etiqueta_a.grid(row=0, column=0, sticky="w", padx=8, pady=6)
            self.texto_a = ctk.CTkTextbox(self.marco_a, height=100)
            self.texto_a.grid(row=1, column=0, sticky="we", padx=8)
            btn_cargar_a = ctk.CTkButton(self.marco_a, text="Leer desde texto", command=lambda: self.leer_matriz_desde_texto('A'))
            btn_cargar_a.grid(row=2, column=0, sticky="w", padx=8, pady=6)

            # Derecha: Matriz B
            self.marco_b = ctk.CTkFrame(medio)
            self.marco_b.grid(row=0, column=1, sticky="nswe", padx=(6, 0))
            lbl_b = ctk.CTkLabel(self.marco_b, text="Matriz B")
            lbl_b.grid(row=0, column=0, sticky="w", padx=8, pady=6)
            self.texto_b = ctk.CTkTextbox(self.marco_b, height=100)
            self.texto_b.grid(row=1, column=0, sticky="we", padx=8)
            self.btn_cargar_b = ctk.CTkButton(self.marco_b, text="Leer desde texto", command=lambda: self.leer_matriz_desde_texto('B'))
            self.btn_cargar_b.grid(row=2, column=0, sticky="w", padx=8, pady=6)

            # contenedor inferior con Pasos y Resultado
            self.inferior = ctk.CTkFrame(self.contenido)
            self.inferior.grid(row=3, column=0, sticky="nswe", padx=12, pady=(6, 12))
            self.inferior.grid_rowconfigure(0, weight=1)
            self.inferior.grid_columnconfigure(0, weight=1)
            self.inferior.grid_columnconfigure(1, weight=1)

            # Pasos (col 0)
            self.marco_pasos = ctk.CTkFrame(self.inferior)
            self.marco_pasos.grid(row=0, column=0, sticky="nswe", padx=(0, 6), pady=0)
            self.marco_pasos.grid_columnconfigure(0, weight=1)
            self.etiqueta_pasos = ctk.CTkLabel(self.marco_pasos, text="Pasos:")
            self.etiqueta_pasos.grid(row=0, column=0, sticky="w", padx=8, pady=6)
            self.pasos_caja = ctk.CTkTextbox(self.marco_pasos, height=220)
            self.pasos_caja.grid(row=1, column=0, sticky="nswe", padx=8, pady=(0, 8))

            # Controles
            controles = ctk.CTkFrame(self.contenido)
            controles.grid(row=2, column=0, sticky="ew", padx=12, pady=(6, 12))
            btn_calcular = ctk.CTkButton(controles, text="Calcular", command=self.calcular_operacion)
            btn_calcular.grid(row=0, column=0, padx=6)
            btn_limpiar = ctk.CTkButton(controles, text="Limpiar", command=self.limpiar_matrices)
            btn_limpiar.grid(row=0, column=1, padx=6)

            # Resultado (col 1)
            self.marco_resultado = ctk.CTkFrame(self.inferior)
            self.marco_resultado.grid(row=0, column=1, sticky="nswe", padx=(6, 0), pady=0)
            self.marco_resultado.grid_columnconfigure(0, weight=1)
            self.etiqueta_resultado = ctk.CTkLabel(self.marco_resultado, text="Resultado:")
            self.etiqueta_resultado.grid(row=0, column=0, sticky="w", padx=8, pady=6)
            self.resultado_caja = ctk.CTkTextbox(self.marco_resultado, height=220)
            self.resultado_caja.grid(row=1, column=0, sticky="nswe", padx=8, pady=(0, 8))

            # almacenamiento de entradas
            self.entradas_a = []
            self.entradas_b = []
            self.al_cambiar_operacion()
        else:
            lbl = ctk.CTkLabel(self.contenido, text=f"Has seleccionado: {nombre}\n\nContenido de ejemplo para la sección.", justify="left")
            lbl.grid(row=0, column=0, sticky="nw", padx=12, pady=12)

    def abrir_algebra(self):
        try:
            import algebraLineal as al  # noqa
            lbl = ctk.CTkLabel(self.contenido, text="Módulo de Álgebra Lineal cargado. Ejecuta desde consola para ingresar ecuaciones.")
            lbl.grid(row=2, column=0, sticky="nw", padx=12, pady=6)
        except Exception as e:
            lbl = ctk.CTkLabel(self.contenido, text=f"Error al cargar módulo: {e}")
            lbl.grid(row=2, column=0, sticky="nw", padx=12, pady=6)

    # --- Auxiliares calculadora de matrices ---
    def generar_cuadriculas_matriz(self):
        try:
            filas = int(self.ent_filas.get())
            columnas = int(self.ent_columnas.get())
            if filas <= 0 or columnas <= 0:
                raise ValueError()
        except Exception:
            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', 'Filas y columnas deben ser enteros positivos.')
            return

        # limpiar cuadriculas previas
        for w in getattr(self, 'grilla_a', []):
            w.destroy()
        for w in getattr(self, 'grilla_b', []):
            w.destroy()

        self.grilla_a = []
        self.grilla_b = []
        self.entradas_a = [[None] * columnas for _ in range(filas)]
        if self.opcion_var.get() != 'Gauss/Gauss-Jordan':
            self.entradas_b = [[None] * columnas for _ in range(filas)]
        else:
            self.entradas_b = []

        for i in range(filas):
            for j in range(columnas):
                e = ctk.CTkEntry(self.marco_a, width=60)
                e.grid(row=3 + i, column=j, padx=4, pady=2)
                self.grilla_a.append(e)
                self.entradas_a[i][j] = e

                if self.opcion_var.get() != 'Gauss/Gauss-Jordan':
                    e2 = ctk.CTkEntry(self.marco_b, width=60)
                    e2.grid(row=3 + i, column=j, padx=4, pady=2)
                    self.grilla_b.append(e2)
                    self.entradas_b[i][j] = e2

        # mensaje contextual
        self.resultado_caja.delete('0.0', 'end')
        if self.opcion_var.get() == 'Independencia':
            self.resultado_caja.insert('0.0', 'Conjuntos listos. Completa entradas o pega vectores (uno por línea) y usa "Leer desde texto".')
        else:
            self.resultado_caja.insert('0.0', 'Matrices listas. Completa entradas o pega texto y usa "Leer desde texto".')

    def al_cambiar_operacion(self):
        op = self.opcion_var.get()
        try:
            if op == 'Independencia':
                self.etiqueta_a.configure(text='Conjuntos de Vectores')
            else:
                self.etiqueta_a.configure(text='Matriz A')
        except Exception:
            pass
        try:
            if op == 'Independencia':
                self.btn_generar.configure(text='Generar conjuntos')
            else:
                self.btn_generar.configure(text='Generar matrices')
        except Exception:
            pass

        if op == 'Gauss/Gauss-Jordan':
            self.menu_modo_gauss.grid()
            self.marco_b.grid_remove()
        elif op == 'Independencia':
            self.menu_modo_gauss.grid_remove()
            self.marco_b.grid_remove()
        else:
            self.menu_modo_gauss.grid_remove()
            self.marco_b.grid()

    def leer_entradas_matriz(self, entradas):
        filas = len(entradas)
        columnas = len(entradas[0]) if filas > 0 else 0
        matriz = [[0.0] * columnas for _ in range(filas)]
        for i in range(filas):
            for j in range(columnas):
                txt = entradas[i][j].get().strip()
                if txt == '':
                    valor = 0.0
                else:
                    try:
                        valor = float(txt)
                    except Exception:
                        raise ValueError(f'Valor inválido en ({i + 1},{j + 1}): "{txt}"')
                matriz[i][j] = valor
        return matriz

    def leer_matriz_desde_texto(self, cual='A'):
        # en modo Gauss/Gauss-Jordan, sólo A
        if self.opcion_var.get() == 'Gauss/Gauss-Jordan' and cual == 'B':
            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', 'En modo Gauss/Gauss-Jordan sólo se permite una matriz (Matriz A).')
            return

        destino_texto = self.texto_a if cual == 'A' else self.texto_b
        contenido = destino_texto.get('0.0', 'end').strip()
        if contenido == '':
            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', 'Texto vacío para la matriz.')
            return

        lineas = [ln.strip() for ln in contenido.splitlines() if ln.strip() != '']
        matriz = []
        for ln in lineas:
            partes = [p for p in ln.replace(',', ' ').split()]
            fila = []
            for p in partes:
                try:
                    fila.append(float(p))
                except Exception:
                    self.resultado_caja.delete('0.0', 'end')
                    self.resultado_caja.insert('0.0', f'Valor inválido al parsear: {p}')
                    return
            matriz.append(fila)

        # modo Independencia: cada línea es un vector -> columnas de A
        if self.opcion_var.get() == 'Independencia':
            if not matriz:
                self.resultado_caja.delete('0.0', 'end')
                self.resultado_caja.insert('0.0', 'No se detectaron vectores en el texto.')
                return
            tam = len(matriz[0])
            if any(len(v) != tam for v in matriz):
                self.resultado_caja.delete('0.0', 'end')
                self.resultado_caja.insert('0.0', 'Todos los vectores deben tener la misma dimensión.')
                return
            # transponer a columnas = vectores
            filas = tam
            columnas = len(matriz)
            M = [[0.0] * columnas for _ in range(filas)]
            for c, v in enumerate(matriz):
                for r in range(filas):
                    M[r][c] = v[r]
            matriz = M

        # rectangularidad
        if any(len(f) != len(matriz[0]) for f in matriz):
            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', 'La matriz no es rectangular (filas con distinta cantidad de columnas).')
            return

        filas = len(matriz)
        columnas = len(matriz[0])

        # poblar rejillas de entrada
        try:
            if hasattr(self, 'entradas_a') and self.entradas_a and len(self.entradas_a) == filas and len(self.entradas_a[0]) == columnas:
                entradas = self.entradas_a if cual == 'A' else self.entradas_b
                for i in range(filas):
                    for j in range(columnas):
                        entradas[i][j].delete(0, 'end')
                        entradas[i][j].insert(0, str(matriz[i][j]))
            else:
                self.ent_filas.delete(0, 'end')
                self.ent_filas.insert(0, str(filas))
                self.ent_columnas.delete(0, 'end')
                self.ent_columnas.insert(0, str(columnas))
                self.generar_cuadriculas_matriz()
                entradas = self.entradas_a if cual == 'A' else self.entradas_b
                for i in range(filas):
                    for j in range(columnas):
                        entradas[i][j].insert(0, str(matriz[i][j]))

            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', f'Matriz {cual} leída ({filas}x{columnas}).')
        except Exception as e:
            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', f'Error al poblar entradas: {e}')

    def calcular_operacion(self):
        op = self.opcion_var.get()

        # Métodos de Gauss
        if op == 'Gauss/Gauss-Jordan':
            modo = self.modo_gauss_var.get() if hasattr(self, 'modo_gauss_var') else 'Gauss-Jordan'
            try:
                A = self.leer_entradas_matriz(self.entradas_a)
            except Exception as e:
                self.resultado_caja.delete('0.0', 'end')
                self.resultado_caja.insert('0.0', f'Error: {e}')
                return

            from algebraLineal import gauss_steps, gauss_jordan_steps
            res = gauss_steps(A) if modo == 'Gauss' else gauss_jordan_steps(A)

            self.pasos_caja.delete('0.0', 'end')
            for i, paso in enumerate(res.get('steps', [])):
                self.pasos_caja.insert('end', f'Paso {i}:\n')
                for fila in paso:
                    self.pasos_caja.insert('end', '  '.join(f'{v:.4g}' for v in fila) + '\n')
                self.pasos_caja.insert('end', '\n')

            self.resultado_caja.delete('0.0', 'end')
            if res.get('status') == 'unique' and res.get('solution') is not None:
                sol = res['solution']
                self.resultado_caja.insert('0.0', 'Solución única:\n')
                self.resultado_caja.insert('end', '\n'.join(f'x{i + 1} = {v:.6g}' for i, v in enumerate(sol)))
            elif res.get('status') == 'inconsistent':
                self.resultado_caja.insert('0.0', 'El sistema es inconsistente (sin solución).')
            elif res.get('status') == 'infinite':
                self.resultado_caja.insert('0.0', 'El sistema tiene infinitas soluciones (variables libres).')
            else:
                self.resultado_caja.insert('0.0', f"Estado: {res.get('status')}")
            return

        # Independencia de vectores (columnas de A)
        if op == 'Independencia':
            try:
                A = self.leer_entradas_matriz(self.entradas_a)
            except Exception as e:
                self.resultado_caja.delete('0.0', 'end')
                self.resultado_caja.insert('0.0', f'Error: {e}')
                return

            # 1) Resultado (rank e independencia)
            from algebraLineal import independenciaVectores
            resultado_ind = independenciaVectores(A)

            # 2) Paso a paso (RREF de A) para mostrar el procedimiento
            self.pasos_caja.delete('0.0', 'end')
            try:
                from algebraLineal import gauss_jordan_steps
                res_rref = gauss_jordan_steps(A)
                for i, paso in enumerate(res_rref.get('steps', [])):
                    self.pasos_caja.insert('end', f'Paso {i} (RREF):\n')
                    for fila in paso:
                        self.pasos_caja.insert('end', '  '.join(f'{v:.4g}' for v in fila) + '\n')
                    self.pasos_caja.insert('end', '\n')
            except Exception as e:
                # si no está disponible, al menos avisamos
                self.pasos_caja.insert('end', f'No se pudo mostrar el paso a paso: {e}\n')

            # 3) Mostrar veredicto
            self.resultado_caja.delete('0.0', 'end')
            if resultado_ind.get('num_vectors', 0) == 0:
                self.resultado_caja.insert('0.0', 'No hay vectores (matriz vacía).')
            else:
                r = resultado_ind.get('rank')
                k = resultado_ind.get('num_vectors')
                msg = f"Rank = {r} / {k}.\n"
                msg += 'Linealmente independiente.' if resultado_ind.get('independent') else 'Linealmente dependiente.'
                self.resultado_caja.insert('0.0', msg)
            return

        # Operaciones binarias A y B
        try:
            A = self.leer_entradas_matriz(self.entradas_a)
            B = self.leer_entradas_matriz(self.entradas_b)
        except Exception as e:
            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', f'Error: {e}')
            return

        fa = len(A); ca = len(A[0]) if fa > 0 else 0
        fb = len(B); cb = len(B[0]) if fb > 0 else 0

        try:
            if op == 'Suma' or op == 'Resta':
                if fa != fb or ca != cb:
                    raise ValueError('Para suma/resta ambas matrices deben tener las mismas dimensiones.')
                C = [[(A[i][j] + B[i][j]) if op == 'Suma' else (A[i][j] - B[i][j]) for j in range(ca)] for i in range(fa)]
            elif op == 'Multiplicación':
                if ca != fb:
                    raise ValueError('Para multiplicación A.columnas debe ser igual a B.filas (A.cols == B.rows).')
                C = [[sum(A[i][k] * B[k][j] for k in range(ca)) for j in range(cb)] for i in range(fa)]
            else:
                raise ValueError('Operación desconocida')
        except Exception as e:
            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', f'Error: {e}')
            return

        # mostrar resultado
        lineas = []
        for fila in C:
            lineas.append('  '.join(f'{v:.4g}' for v in fila))
        self.resultado_caja.delete('0.0', 'end')
        self.resultado_caja.insert('0.0', '\n'.join(lineas))

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

    def actualizar_fecha_hora(self):
        ahora = datetime.now()
        formateado = ahora.strftime("%A, %d %B %Y | %H:%M:%S")
        self.etiqueta_fecha_hora.configure(text=formateado)
        # siguiente actualización
        self.after(1000, self.actualizar_fecha_hora)


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = AplicacionPrincipal()
    app.mainloop()
