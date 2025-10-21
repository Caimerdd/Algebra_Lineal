from datetime import datetime
import customtkinter as ctk

DETALLE_MAX = 6
BLOQUE_DETALLE = 3
MAX_SNAPSHOTS = 80
PASO_SALTOS = 5

def _fmt(x: float) -> str:
    return f"{x:.4g}"

class AplicacionPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Menú Principal Mathpro")
        self.geometry("900x600"); self.minsize(800, 500)
        self.grid_rowconfigure(0, weight=1); self.grid_columnconfigure(1, weight=1)
        self._crear_panel_nav(); self._crear_panel_principal()
        self.seccion_actual = None; self.mostrar_seccion('Álgebra Lineal')
        self.actualizar_fecha_hora()

    def _crear_panel_nav(self):
        self.marco_nav = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.marco_nav.grid(row=0, column=0, sticky="nswe")
        self.marco_nav.grid_rowconfigure(6, weight=1)
        ctk.CTkLabel(self.marco_nav, text="Menú", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=12, pady=(12, 8), sticky="w")
        ctk.CTkButton(self.marco_nav, text="  Álgebra Lineal", anchor="w",
                      command=lambda: self.mostrar_seccion('Álgebra Lineal')).grid(row=1, column=0, sticky="ew", padx=12, pady=6)
        ctk.CTkLabel(self.marco_nav, text="").grid(row=6, column=0, sticky="nswe")

    def _crear_panel_principal(self):
        self.marco_principal = ctk.CTkFrame(self, corner_radius=0)
        self.marco_principal.grid(row=0, column=1, sticky="nswe", padx=12, pady=12)
        self.marco_principal.grid_rowconfigure(0, weight=0); self.marco_principal.grid_rowconfigure(1, weight=1)
        self.marco_principal.grid_columnconfigure(0, weight=1)

        self.cabecera = ctk.CTkFrame(self.marco_principal, height=60, corner_radius=0)
        self.cabecera.grid(row=0, column=0, sticky="ew"); self.cabecera.grid_columnconfigure(0, weight=1)
        self.etiqueta_cabecera = ctk.CTkLabel(self.cabecera, text="", font=ctk.CTkFont(size=20, weight="bold"))
        self.etiqueta_cabecera.grid(row=0, column=0, sticky="w", padx=10)
        self.etiqueta_fecha_hora = ctk.CTkLabel(self.cabecera, text="", font=ctk.CTkFont(size=11))
        self.etiqueta_fecha_hora.grid(row=0, column=1, sticky="e", padx=10)

        self.contenido = ctk.CTkFrame(self.marco_principal, corner_radius=6)
        self.contenido.grid(row=1, column=0, sticky="nswe", pady=(12, 0))
        self.contenido.grid_rowconfigure(0, weight=1); self.contenido.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.contenido, text="Selecciona una sección del menú a la izquierda.", anchor="w").grid(row=0, column=0, sticky="nw", padx=12, pady=12)

    def mostrar_seccion(self, nombre: str):
        self.seccion_actual = nombre; self.etiqueta_cabecera.configure(text=nombre)
        for w in self.contenido.winfo_children(): w.destroy()
        if nombre == 'Álgebra Lineal': self._cargar_ui_algebra_lineal()
        else:
            ctk.CTkLabel(self.contenido, text=f"Has seleccionado: {nombre}\n\nContenido de ejemplo.", justify="left").grid(row=0, column=0, sticky="nw", padx=12, pady=12)

    def _cargar_ui_algebra_lineal(self):
        self.contenido.grid_rowconfigure(0, weight=0)
        self.contenido.grid_rowconfigure(1, weight=1) 
        self.contenido.grid_rowconfigure(2, weight=0)
        self.contenido.grid_rowconfigure(3, weight=1)
        self.contenido.grid_columnconfigure(0, weight=1)

        # --- CAMBIO: Barra superior simplificada ---
        barra = ctk.CTkFrame(self.contenido); barra.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        self.opcion_var = ctk.StringVar(value="Suma")
        ctk.CTkLabel(barra, text="Operación:").grid(row=0, column=0, padx=(4,2))
        ctk.CTkOptionMenu(barra, values=["Suma","Resta","Multiplicación","Gauss/Gauss-Jordan","Independencia","Inversa", "Determinante"],
                          variable=self.opcion_var).grid(row=0, column=1, padx=(8,8))
        self.modo_gauss_var = ctk.StringVar(value="Gauss-Jordan")
        self.menu_modo_gauss = ctk.CTkOptionMenu(barra, values=["Gauss","Gauss-Jordan"], variable=self.modo_gauss_var)
        self.menu_modo_gauss.grid(row=0, column=2, padx=(4,4)); self.menu_modo_gauss.grid_remove()

        try: self.opcion_var.trace_add('write', lambda *_: self.al_cambiar_operacion())
        except Exception: self.opcion_var.trace('w', lambda *_: self.al_cambiar_operacion())

        ctk.CTkButton(barra, text="Generar Matrices", command=self.generar_cuadriculas_matriz).grid(row=0, column=3, padx=(16,4))

        medio = ctk.CTkFrame(self.contenido); medio.grid(row=1, column=0, sticky="nswe", padx=8, pady=4)
        medio.grid_columnconfigure(0, weight=1); medio.grid_columnconfigure(1, weight=1)

        # --- CAMBIO: Contenedor Matriz A con sus propias dimensiones ---
        self.marco_a = ctk.CTkFrame(medio); self.marco_a.grid(row=0, column=0, sticky="nswe", padx=(0,6))
        self.etiqueta_a = ctk.CTkLabel(self.marco_a, text="Matriz A"); self.etiqueta_a.grid(row=0, column=0, columnspan=4, sticky="w", padx=8, pady=6)
        
        marco_dims_a = ctk.CTkFrame(self.marco_a, fg_color="transparent")
        marco_dims_a.grid(row=1, column=0, columnspan=4, sticky="ew", padx=8, pady=(0, 4))
        ctk.CTkLabel(marco_dims_a, text="Filas:").grid(row=0, column=0, padx=(0,2))
        self.ent_filas_a = ctk.CTkEntry(marco_dims_a, width=50); self.ent_filas_a.insert(0,"2"); self.ent_filas_a.grid(row=0, column=1, padx=(0,8))
        ctk.CTkLabel(marco_dims_a, text="Cols:").grid(row=0, column=2, padx=(4,2))
        self.ent_columnas_a = ctk.CTkEntry(marco_dims_a, width=50); self.ent_columnas_a.insert(0,"2"); self.ent_columnas_a.grid(row=0, column=3)

        self.lbl_coef_a = ctk.CTkLabel(self.marco_a, text="α:"); self.lbl_coef_a.grid(row=11, column=0, sticky="w", padx=(8,2), pady=(4,2))
        self.ent_coef_a = ctk.CTkEntry(self.marco_a, width=48); self.ent_coef_a.grid(row=11, column=0, sticky="w", padx=(36,0), pady=(4,2))

        # --- CAMBIO: Contenedor Matriz B con sus propias dimensiones ---
        self.marco_b = ctk.CTkFrame(medio); self.marco_b.grid(row=0, column=1, sticky="nswe", padx=(6,0))
        ctk.CTkLabel(self.marco_b, text="Matriz B").grid(row=0, column=0, columnspan=4, sticky="w", padx=8, pady=6)
        
        self.marco_dims_b = ctk.CTkFrame(self.marco_b, fg_color="transparent")
        self.marco_dims_b.grid(row=1, column=0, columnspan=4, sticky="ew", padx=8, pady=(0, 4))
        ctk.CTkLabel(self.marco_dims_b, text="Filas:").grid(row=0, column=0, padx=(0,2))
        self.ent_filas_b = ctk.CTkEntry(self.marco_dims_b, width=50); self.ent_filas_b.insert(0,"2"); self.ent_filas_b.grid(row=0, column=1, padx=(0,8))
        ctk.CTkLabel(self.marco_dims_b, text="Cols:").grid(row=0, column=2, padx=(4,2))
        self.ent_columnas_b = ctk.CTkEntry(self.marco_dims_b, width=50); self.ent_columnas_b.insert(0,"2"); self.ent_columnas_b.grid(row=0, column=3)

        self.lbl_coef_b = ctk.CTkLabel(self.marco_b, text="β:"); self.lbl_coef_b.grid(row=11, column=0, sticky="w", padx=(8,2), pady=(4,2))
        self.ent_coef_b = ctk.CTkEntry(self.marco_b, width=48); self.ent_coef_b.grid(row=11, column=0, sticky="w", padx=(36,0), pady=(4,2))
        
        controles = ctk.CTkFrame(self.contenido); controles.grid(row=2, column=0, sticky="ew", padx=12, pady=(6,12))
        ctk.CTkButton(controles, text="Calcular", command=self.calcular_operacion).grid(row=0, column=0, padx=6)
        ctk.CTkButton(controles, text="Limpiar", command=self.limpiar_matrices).grid(row=0, column=1, padx=6)

        inferior = ctk.CTkFrame(self.contenido); inferior.grid(row=3, column=0, sticky="nswe", padx=12, pady=(6,12))
        inferior.grid_rowconfigure(0, weight=1); inferior.grid_columnconfigure(0, weight=1); inferior.grid_columnconfigure(1, weight=1)

        self.marco_pasos = ctk.CTkFrame(inferior); self.marco_pasos.grid(row=0, column=0, sticky="nswe", padx=(0,6))
        self.marco_pasos.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.marco_pasos, text="Pasos:").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.pasos_caja = ctk.CTkTextbox(self.marco_pasos, height=220); self.pasos_caja.grid(row=1, column=0, sticky="nswe", padx=8, pady=(0,8))

        self.marco_resultado = ctk.CTkFrame(inferior); self.marco_resultado.grid(row=0, column=1, sticky="nswe", padx=(6,0))
        self.marco_resultado.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.marco_resultado, text="Resultado:").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.resultado_caja = ctk.CTkTextbox(self.marco_resultado, height=220); self.resultado_caja.grid(row=1, column=0, sticky="nswe", padx=8, pady=(0,8))

        self.entradas_a = []; self.entradas_b = []; self.grilla_a = []; self.grilla_b = []
        self.al_cambiar_operacion()

    def _set_resultado(self, texto: str, limpiar_pasos=False):
        if limpiar_pasos: self.pasos_caja.delete('0.0', 'end')
        self.resultado_caja.delete('0.0', 'end'); self.resultado_caja.insert('0.0', texto)

    def _append_matriz(self, M, titulo=None):
        if titulo: self.pasos_caja.insert('end', f'{titulo}\n')
        for f in M: self.pasos_caja.insert('end', '  '.join(_fmt(v) for v in f) + '\n')
        self.pasos_caja.insert('end', '\n')

    def _leer_escalar(self, e):
        t = e.get().strip() if e else ''
        if t in ('','+'): return 1.0
        if t == '-': return -1.0
        return float(t)

    def _es_grande(self, f, c): return max(f, c) > DETALLE_MAX

    def generar_cuadriculas_matriz(self):
        # --- CAMBIO: Leer de las nuevas casillas de dimensiones ---
        op = self.opcion_var.get()
        usa_b = op not in ('Gauss/Gauss-Jordan','Independencia','Inversa', 'Determinante')

        try:
            filas_a = int(self.ent_filas_a.get()); cols_a = int(self.ent_columnas_a.get())
            if filas_a <= 0 or cols_a <= 0: raise ValueError("Dimensiones de A deben ser positivas.")
            
            filas_b, cols_b = 0, 0
            if usa_b:
                filas_b = int(self.ent_filas_b.get()); cols_b = int(self.ent_columnas_b.get())
                if filas_b <= 0 or cols_b <= 0: raise ValueError("Dimensiones de B deben ser positivas.")

        except Exception as e:
            self._set_resultado(f'Error: {e}'); return

        for widget in self.grilla_a: widget.destroy()
        for widget in self.grilla_b: widget.destroy()
        self.grilla_a = []; self.grilla_b = []

        self.entradas_a = [[None]*cols_a for _ in range(filas_a)]
        self.entradas_b = [[None]*cols_b for _ in range(filas_b)] if usa_b else []

        start_row = 2 # Las casillas ahora empiezan en la fila 2
        for i in range(filas_a):
            for j in range(cols_a):
                e = ctk.CTkEntry(self.marco_a, width=60)
                e.grid(row=start_row + i, column=j, padx=2, pady=2, columnspan=1)
                self.grilla_a.append(e); self.entradas_a[i][j] = e

        if usa_b:
            for i in range(filas_b):
                for j in range(cols_b):
                    e2 = ctk.CTkEntry(self.marco_b, width=60)
                    e2.grid(row=start_row + i, column=j, padx=2, pady=2, columnspan=1)
                    self.grilla_b.append(e2); self.entradas_b[i][j] = e2

        if op == 'Gauss/Gauss-Jordan': self._set_resultado('Usa matriz aumentada [A | b].')
        elif op in ('Inversa', 'Determinante'): self._set_resultado('La matriz A debe ser cuadrada.')
        else: self._set_resultado('Matrices listas.')

    def al_cambiar_operacion(self):
        op = self.opcion_var.get()
        if op == 'Independencia': self.etiqueta_a.configure(text='Conjuntos de Vectores')
        elif op == 'Gauss/Gauss-Jordan': self.etiqueta_a.configure(text='Matriz A (aumentada [A|b])')
        elif op in ('Inversa', 'Determinante'): self.etiqueta_a.configure(text='Matriz A (cuadrada)')
        else: self.etiqueta_a.configure(text='Matriz A')

        self.menu_modo_gauss.grid() if op=='Gauss/Gauss-Jordan' else self.menu_modo_gauss.grid_remove()
        
        if op in ('Gauss/Gauss-Jordan','Independencia','Inversa', 'Determinante'):
            self.marco_b.grid_remove()
        else:
            self.marco_b.grid()

        use_scalars = op in ('Suma','Resta')
        
        if use_scalars:
            self.lbl_coef_a.grid(); self.ent_coef_a.grid()
            self.lbl_coef_b.grid(); self.ent_coef_b.grid()
        else:
            self.lbl_coef_a.grid_remove(); self.ent_coef_a.grid_remove()
            self.lbl_coef_b.grid_remove(); self.ent_coef_b.grid_remove()

    def _leer_entradas_de_cuadricula(self, entradas):
        if not entradas:
            return [] # Devuelve lista vacía si la matriz no se usa (ej. Matriz B en Inversa)
        if not entradas[0]:
            raise ValueError("Primero debe generar una matriz.")
        
        filas = len(entradas); cols = len(entradas[0])
        M = [[0.0]*cols for _ in range(filas)]
        celdas_no_vacias = 0

        for i in range(filas):
            for j in range(cols):
                if entradas[i][j] is not None:
                    t = entradas[i][j].get().strip()
                    if t: 
                        celdas_no_vacias += 1
                        try:
                            M[i][j] = float(t)
                        except ValueError:
                            raise ValueError(f'Valor inválido en ({i+1},{j+1}): "{t}"')
        
        if celdas_no_vacias == 0:
            raise ValueError("La matriz no puede estar vacía. Ingrese al menos un valor.")
            
        return M

    def _detalle_bloque(self, fa, ca): return min(BLOQUE_DETALLE, fa), min(BLOQUE_DETALLE, ca)

    def calcular_operacion(self):
        op = self.opcion_var.get()
        try:
            A = self._leer_entradas_de_cuadricula(self.entradas_a)
            B = self._leer_entradas_de_cuadricula(self.entradas_b)
        except Exception as e:
            self._set_resultado(f'Error de entrada: {e}', limpiar_pasos=True); return
        
        if op == 'Determinante':
            from Complement import pasos_determinante
            res = pasos_determinante(A)
            if res['estado'] == 'exito':
                self.pasos_caja.delete('0.0', 'end')
                self.pasos_caja.insert('0.0', '\n'.join(res['pasos']))
                self._set_resultado(f"El determinante es: {_fmt(res['determinante'])}")
            else:
                self._set_resultado(f"Error: {res['mensaje']}", limpiar_pasos=True)
            return

        if op == 'Gauss/Gauss-Jordan':
            from Complement import gauss_steps, gauss_jordan_steps
            modo = self.modo_gauss_var.get() if hasattr(self,'modo_gauss_var') else 'Gauss-Jordan'
            res = gauss_steps(A) if modo=='Gauss' else gauss_jordan_steps(A)
            self.pasos_caja.delete('0.0','end')
            steps, ops = res.get('steps',[]), res.get('ops',[])
            total = len(steps); shown = 0
            for i, paso in enumerate(steps):
                if i < 20 or i % PASO_SALTOS == 0:
                    if i < len(ops) and ops[i]: self.pasos_caja.insert('end', f'Op: {ops[i]}\n')
                    self._append_matriz(paso, f'Paso {i}:'); shown += 1
                if shown >= MAX_SNAPSHOTS: break
            if total > shown: self.pasos_caja.insert('end', f'… ({total-shown} pasos omitidos)\n\n')
            status = res.get('status'); sol = res.get('solution')
            if status=='unique' and sol is not None:
                txt = 'Solución única:\n' + '\n'.join(f'x{i+1} = {v:.6g}' for i,v in enumerate(sol))
            elif status=='inconsistent': txt = 'El sistema es inconsistente (sin solución).'
            elif status=='infinite':
                libres = res.get('free_vars', []); base = res.get('basic_solution', {})
                m = len(A[0])-1 if A and len(A[0])>0 else 0
                lineas=[]
                for i in range(m):
                    if i in libres: lineas.append(f'x{i+1} variable libre')
                    else: lineas.append(f'x{i+1} = {base.get(i,0.0):.6g}   (con libres = 0)')
                txt = 'Soluciones infinitas:\n' + '\n'.join(lineas)
            elif status=='empty': txt = 'Matriz vacía.'
            else: txt = f"Estado: {status}"
            self._set_resultado(txt); return
        if op == 'Inversa':
            n = len(A)
            if n==0 or any(len(f)!=n for f in A): self._set_resultado('A debe ser cuadrada.'); return
            from Complement import inverse_steps
            res = inverse_steps(A)
            self.pasos_caja.delete('0.0','end')
            steps, ops = res.get('steps',[]), res.get('ops',[])
            total = len(steps); shown = 0
            for i, M in enumerate(steps):
                if i < 20 or i % PASO_SALTOS == 0:
                    if i < len(ops) and ops[i]: self.pasos_caja.insert('end', f'Op: {ops[i]}\n')
                    self._append_matriz(M, f'Paso {i}:'); shown += 1
                if shown >= MAX_SNAPSHOTS: break
            if total > shown: self.pasos_caja.insert('end', f'… ({total-shown} pasos omitidos)\n\n')
            if res.get('status') == 'invertible':
                inv = res['inverse']
                self._set_resultado('A es invertible. A⁻¹ =\n' + '\n'.join('  '.join(_fmt(x) for x in fila) for fila in inv))
            else: self._set_resultado('A es singular (no tiene inversa).')
            return
        if op == 'Independencia':
            from Complement import independenciaVectores, gauss_jordan_steps
            ver = independenciaVectores(A)
            self.pasos_caja.delete('0.0','end')
            try:
                rref = gauss_jordan_steps(A); steps, ops = rref.get('steps',[]), rref.get('ops',[])
                total=len(steps); shown=0
                for i,paso in enumerate(steps):
                    if i<20 or i%PASO_SALTOS==0:
                        if i<len(ops) and ops[i]: self.pasos_caja.insert('end', f'Op: {ops[i]}\n')
                        self._append_matriz(paso, f'Paso {i} (RREF):'); shown+=1
                    if shown>=MAX_SNAPSHOTS: break
                if total>shown: self.pasos_caja.insert('end', f'… ({total-shown} pasos omitidos)\n\n')
            except Exception as e: self.pasos_caja.insert('end', f'No se pudo mostrar el paso a paso: {e}\n')
            if ver.get('num_vectors',0)==0: self._set_resultado('No hay vectores (matriz vacía).')
            else:
                r,k = ver.get('rank'), ver.get('num_vectors')
                self._set_resultado(f"Rank = {r} / {k}.\n" + ('Linealmente independiente.' if ver.get('independent') else 'Linealmente dependiente.'))
            return
        fa, ca = len(A), len(A[0]) if A else 0
        fb, cb = len(B), len(B[0]) if B else 0
        self.pasos_caja.delete('0.0','end')
        try:
            if op in ('Suma','Resta'):
                if fa!=fb or ca!=cb: raise ValueError('Dimensiones incompatibles.')
                alpha = self._leer_escalar(self.ent_coef_a); beta = self._leer_escalar(self.ent_coef_b)
                sgn = 1.0 if op=='Suma' else -1.0
                self._append_matriz(A,'Matriz A:'); self._append_matriz(B,'Matriz B:')
                Aesc = [[alpha*A[i][j] for j in range(ca)] for i in range(fa)]
                Besc = [[sgn*beta*B[i][j] for j in range(cb)] for i in range(fb)]
                self._append_matriz(Aesc, f'α·A (α={_fmt(alpha)}):')
                self._append_matriz(Besc, f'{"+" if sgn>0 else "-"} β·B (β={_fmt(beta)}):')
                C = [[Aesc[i][j]+Besc[i][j] for j in range(ca)] for i in range(fa)]
                R = C
            elif op == 'Multiplicación':
                if ca!=fb: raise ValueError('Para A·B: columnas(A) = filas(B).')
                self._append_matriz(A,'Matriz A:'); self._append_matriz(B,'Matriz B:')
                C = [[sum(A[i][k]*B[k][j] for k in range(ca)) for j in range(cb)] for i in range(fa)]
                R = C
            else: raise ValueError('Operación desconocida')
            # Limpiar y mostrar pasos/resultado para Suma, Resta y Multiplicación
            self.pasos_caja.delete('0.0', 'end')
            if op in ('Suma', 'Resta'):
                for i in range(fa):
                    for j in range(ca):
                        self.pasos_caja.insert('end', f'C[{i+1},{j+1}] = {_fmt(alpha)}·{_fmt(A[i][j])} {"+" if sgn>0 else "-"} {_fmt(beta)}·{_fmt(B[i][j])} = {_fmt(C[i][j])}\n')
                self._append_matriz(C, 'Resultado C = αA ' + ('+' if sgn>0 else '−') + ' βB:')
            elif op == 'Multiplicación':
                 for i in range(fa):
                    for j in range(cb):
                        terms = [f'{_fmt(A[i][k])}·{_fmt(B[k][j])}' for k in range(ca)]
                        self.pasos_caja.insert('end', f'C[{i+1},{j+1}] = ' + ' + '.join(terms) + f' = {_fmt(C[i][j])}\n')
                 self._append_matriz(C,'Resultado C = A·B:')
            self.resultado_caja.delete('0.0','end')
            self.resultado_caja.insert('0.0','\n'.join('  '.join(_fmt(v) for v in fila) for fila in R))
        except Exception as e:
            self._set_resultado(f'Error: {e}'); return
        
    def limpiar_matrices(self):
        for r in self.entradas_a:
            for e in r:
                if e: e.delete(0,'end')
        for r in self.entradas_b:
            for e in r:
                if e: e.delete(0,'end')
        self.resultado_caja.delete('0.0','end'); self.pasos_caja.delete('0.0','end')

    def actualizar_fecha_hora(self):
        self.etiqueta_fecha_hora.configure(text=datetime.now().strftime("%A, %d %B %Y | %H:%M:%S"))
        self.after(1000, self.actualizar_fecha_hora)

if __name__ == "__main__":
    ctk.set_appearance_mode("System"); ctk.set_default_color_theme("blue")
    app = AplicacionPrincipal(); app.mainloop()