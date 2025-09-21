from datetime import datetime
import customtkinter as ctk


class MainApp(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("Menú Principal Mathpro")
		self.geometry("900x600")
		self.minsize(800, 500)

		# configure grid
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)

		# left navigation frame
		self.nav_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
		self.nav_frame.grid(row=0, column=0, sticky="nswe")
		self.nav_frame.grid_rowconfigure((0,1,2,3,4,5), weight=0)
		self.nav_frame.grid_rowconfigure(6, weight=1)

		title = ctk.CTkLabel(self.nav_frame, text="Menú", font=ctk.CTkFont(size=18, weight="bold"))
		title.grid(row=0, column=0, padx=12, pady=(12, 8), sticky="w")

		# Buttons in left menu
		self.btn_basic = ctk.CTkButton(self.nav_frame, text="  Matemática Básica", anchor="w", command=lambda: self.show_section('Matemática Básica'))
		self.btn_basic.grid(row=1, column=0, sticky="ew", padx=12, pady=6)

		self.btn_calc = ctk.CTkButton(self.nav_frame, text="  Cálculo", anchor="w", command=lambda: self.show_section('Cálculo'))
		self.btn_calc.grid(row=2, column=0, sticky="ew", padx=12, pady=6)

		self.btn_calc2 = ctk.CTkButton(self.nav_frame, text="  Cálculo II", anchor="w", command=lambda: self.show_section('Cálculo II'))
		self.btn_calc2.grid(row=3, column=0, sticky="ew", padx=12, pady=6)

		self.btn_linear = ctk.CTkButton(self.nav_frame, text="  Álgebra Lineal", anchor="w", command=lambda: self.show_section('Álgebra Lineal'))
		self.btn_linear.grid(row=4, column=0, sticky="ew", padx=12, pady=6)

		self.btn_config = ctk.CTkButton(self.nav_frame, text="  Configuración", anchor="w", command=lambda: self.show_section('Configuración'))
		self.btn_config.grid(row=5, column=0, sticky="ew", padx=12, pady=6)

		# filler to push items up
		self.filler = ctk.CTkLabel(self.nav_frame, text="")
		self.filler.grid(row=6, column=0, sticky="nswe")

		# main content frame
		self.main_frame = ctk.CTkFrame(self, corner_radius=0)
		self.main_frame.grid(row=0, column=1, sticky="nswe", padx=12, pady=12)
		self.main_frame.grid_rowconfigure(0, weight=1)
		self.main_frame.grid_columnconfigure(0, weight=1)

		# top area: title and datetime
		self.header = ctk.CTkFrame(self.main_frame, height=60, corner_radius=0)
		self.header.grid(row=0, column=0, sticky="ew")
		self.header.grid_columnconfigure(0, weight=1)
		self.header.grid_columnconfigure(1, weight=0)

		self.header_label = ctk.CTkLabel(self.header, text="", font=ctk.CTkFont(size=20, weight="bold"))
		self.header_label.grid(row=0, column=0, sticky="w", padx=10)

		self.datetime_label = ctk.CTkLabel(self.header, text="", font=ctk.CTkFont(size=11))
		self.datetime_label.grid(row=0, column=1, sticky="e", padx=10)

		# area for content
		self.content = ctk.CTkFrame(self.main_frame, corner_radius=6)
		self.content.grid(row=1, column=0, sticky="nswe", pady=(12,0))
		self.content.grid_rowconfigure(0, weight=1)
		self.content.grid_columnconfigure(0, weight=1)

		# default content
		self.content_label = ctk.CTkLabel(self.content, text="Selecciona una sección del menú a la izquierda.", anchor="w")
		self.content_label.grid(row=0, column=0, sticky="nw", padx=12, pady=12)

		# start with default section
		self.current_section = None
		self.show_section('Álgebra Lineal')

		# update clock
		self.update_datetime()

	def show_section(self, name: str):
		self.current_section = name
		self.header_label.configure(text=name)
		# replace content area depending on section
		for widget in self.content.winfo_children():
			widget.destroy()
		if name == 'Álgebra Lineal':
			# MATRIX CALCULATOR UI
			top_frame = ctk.CTkFrame(self.content)
			top_frame.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
			# make sure content rows allocate space for middle/result/steps
			self.content.grid_rowconfigure(0, weight=0)
			self.content.grid_rowconfigure(1, weight=1)
			self.content.grid_rowconfigure(2, weight=0)
			self.content.grid_rowconfigure(3, weight=1)
			self.content.grid_rowconfigure(4, weight=1)
			top_frame.grid_columnconfigure((0,1,2,3,4,5), weight=0)

			r_lbl = ctk.CTkLabel(top_frame, text="Filas:")
			r_lbl.grid(row=0, column=0, padx=(4,2))
			self.rows_var = ctk.IntVar(value=2)
			self.ent_rows = ctk.CTkEntry(top_frame, width=60, textvariable=self.rows_var)
			self.ent_rows.grid(row=0, column=1, padx=(0,8))

			c_lbl = ctk.CTkLabel(top_frame, text="Columnas:")
			c_lbl.grid(row=0, column=2, padx=(4,2))
			self.cols_var = ctk.IntVar(value=2)
			self.ent_cols = ctk.CTkEntry(top_frame, width=60, textvariable=self.cols_var)
			self.ent_cols.grid(row=0, column=3, padx=(0,8))

			self.op_var = ctk.StringVar(value="Suma")
			op_menu = ctk.CTkOptionMenu(top_frame, values=["Suma", "Resta", "Multiplicación", "Gauss/Gauss-Jordan"], variable=self.op_var)
			op_menu.grid(row=0, column=4, padx=(8,8))
			# gauss mode selector (visible only when Gauss/Gauss-Jordan selected)
			self.gauss_mode_var = ctk.StringVar(value="Gauss-Jordan")
			self.gauss_mode_menu = ctk.CTkOptionMenu(top_frame, values=["Gauss", "Gauss-Jordan"], variable=self.gauss_mode_var)
			self.gauss_mode_menu.grid(row=0, column=5, padx=(4,4))
			# start hidden unless op is Gauss/Gauss-Jordan
			self.gauss_mode_menu.grid_remove()
			# trace changes to operation selection
			try:
				self.op_var.trace_add('write', lambda *args: self.on_operation_change())
			except Exception:
				self.op_var.trace('w', lambda *args: self.on_operation_change())

			gen_btn = ctk.CTkButton(top_frame, text="Generar matrices", command=self.generate_matrix_grids)
			gen_btn.grid(row=0, column=5, padx=(8,4))

			# Middle: matrices input area
			middle = ctk.CTkFrame(self.content)
			middle.grid(row=1, column=0, sticky="nswe", padx=12, pady=6)
			middle.grid_columnconfigure(0, weight=1)
			middle.grid_columnconfigure(1, weight=1)

			# Left: Matrix A
			self.frame_a = ctk.CTkFrame(middle)
			self.frame_a.grid(row=0, column=0, sticky="nswe", padx=(0,6))
			lbl_a = ctk.CTkLabel(self.frame_a, text="Matriz A")
			lbl_a.grid(row=0, column=0, sticky="w", padx=8, pady=6)
			self.text_a = ctk.CTkTextbox(self.frame_a, height=100)
			self.text_a.grid(row=1, column=0, sticky="we", padx=8)
			load_a = ctk.CTkButton(self.frame_a, text="Leer desde texto", command=lambda: self.read_matrix_from_text('A'))
			load_a.grid(row=2, column=0, sticky="w", padx=8, pady=6)

			# Right: Matrix B
			self.frame_b = ctk.CTkFrame(middle)
			self.frame_b.grid(row=0, column=1, sticky="nswe", padx=(6,0))
			lbl_b = ctk.CTkLabel(self.frame_b, text="Matriz B")
			lbl_b.grid(row=0, column=0, sticky="w", padx=8, pady=6)
			self.text_b = ctk.CTkTextbox(self.frame_b, height=100)
			self.text_b.grid(row=1, column=0, sticky="we", padx=8)
			self.load_b = ctk.CTkButton(self.frame_b, text="Leer desde texto", command=lambda: self.read_matrix_from_text('B'))
			self.load_b.grid(row=2, column=0, sticky="w", padx=8, pady=6)


			# Bottom container that holds Steps and Result side-by-side
			self.bottom = ctk.CTkFrame(self.content)
			self.bottom.grid(row=3, column=0, sticky="nswe", padx=12, pady=(6,12))
			self.bottom.grid_rowconfigure(0, weight=1)
			self.bottom.grid_columnconfigure(0, weight=1)
			self.bottom.grid_columnconfigure(1, weight=1)

			# Steps/subtable area (for Gauss methods) - placed in bottom column 0
			self.steps_frame = ctk.CTkFrame(self.bottom)
			self.steps_frame.grid(row=0, column=0, sticky="nswe", padx=(0,6), pady=0)
			self.steps_frame.grid_columnconfigure(0, weight=1)
			self.steps_label = ctk.CTkLabel(self.steps_frame, text="Pasos:")
			self.steps_label.grid(row=0, column=0, sticky="w", padx=8, pady=6)
			self.steps_box = ctk.CTkTextbox(self.steps_frame, height=220)
			self.steps_box.grid(row=1, column=0, sticky="nswe", padx=8, pady=(0,8))

			# Controls: calculate and clear
			ctrl = ctk.CTkFrame(self.content)
			ctrl.grid(row=2, column=0, sticky="ew", padx=12, pady=(6,12))
			calc_btn = ctk.CTkButton(ctrl, text="Calcular", command=self.calculate_operation)
			calc_btn.grid(row=0, column=0, padx=6)
			clear_btn = ctk.CTkButton(ctrl, text="Limpiar", command=self.clear_matrices)
			clear_btn.grid(row=0, column=1, padx=6)

			# Result area - placed in bottom column 1 (side-by-side with steps)
			self.result_frame = ctk.CTkFrame(self.bottom)
			self.result_frame.grid(row=0, column=1, sticky="nswe", padx=(6,0), pady=0)
			self.result_frame.grid_columnconfigure(0, weight=1)
			self.result_label = ctk.CTkLabel(self.result_frame, text="Resultado:")
			self.result_label.grid(row=0, column=0, sticky="w", padx=8, pady=6)
			self.result_box = ctk.CTkTextbox(self.result_frame, height=220)
			self.result_box.grid(row=1, column=0, sticky="nswe", padx=8, pady=(0,8))

			# storage for entry grids
			self.entries_a = []
			self.entries_b = []
			# ensure B visible by default
			self.on_operation_change()
		else:
			lbl = ctk.CTkLabel(self.content, text=f"Has seleccionado: {name}\n\nContenido de ejemplo para la sección.", justify="left")
			lbl.grid(row=0, column=0, sticky="nw", padx=12, pady=12)

	def open_algebra(self):
		try:
			import algebraLineal as al
			lbl = ctk.CTkLabel(self.content, text="Módulo de Álgebra Lineal cargado. Ejecuta desde consola para ingresar ecuaciones.")
			lbl.grid(row=2, column=0, sticky="nw", padx=12, pady=6)
		except Exception as e:
			lbl = ctk.CTkLabel(self.content, text=f"Error al cargar módulo: {e}")
			lbl.grid(row=2, column=0, sticky="nw", padx=12, pady=6)

	# --- New matrix calculator helpers ---
	def generate_matrix_grids(self):
		try:
			rows = int(self.ent_rows.get())
			cols = int(self.ent_cols.get())
			if rows <= 0 or cols <= 0:
				raise ValueError()
		except Exception:
			self.result_box.delete('0.0', 'end')
			self.result_box.insert('0.0', 'Filas y columnas deben ser enteros positivos.')
			return

		# clear any existing entry grids
		for w in getattr(self, 'grid_frame_a', []):
			w.destroy()
		for w in getattr(self, 'grid_frame_b', []):
			w.destroy()

		# create grid frames
		self.grid_frame_a = []
		self.grid_frame_b = []
		self.entries_a = [[None]*cols for _ in range(rows)]
		# only create storage for B if not in Gauss mode
		if self.op_var.get() != 'Gauss/Gauss-Jordan':
			self.entries_b = [[None]*cols for _ in range(rows)]
		else:
			self.entries_b = []

		for r in range(rows):
			for c in range(cols):
				e = ctk.CTkEntry(self.frame_a, width=60)
				e.grid(row=3+r, column=c, padx=4, pady=2)
				self.grid_frame_a.append(e)
				self.entries_a[r][c] = e

				# only create entries for B if not in Gauss mode
				if self.op_var.get() != 'Gauss/Gauss-Jordan':
					e2 = ctk.CTkEntry(self.frame_b, width=60)
					e2.grid(row=3+r, column=c, padx=4, pady=2)
					self.grid_frame_b.append(e2)
					self.entries_b[r][c] = e2

		# clear result
		self.result_box.delete('0.0', 'end')
		self.result_box.insert('0.0', 'Matrices listas. Puedes completar las entradas o pegar texto y usar "Leer desde texto".')

	def on_operation_change(self):
		op = self.op_var.get()
		if op == 'Gauss/Gauss-Jordan':
			# show gauss mode selector, hide B frame controls
			self.gauss_mode_menu.grid()
			self.frame_b.grid_remove()
		else:
			self.gauss_mode_menu.grid_remove()
			self.frame_b.grid()


	def parse_matrix_entries(self, entries):
		rows = len(entries)
		cols = len(entries[0]) if rows>0 else 0
		mat = [[0.0]*cols for _ in range(rows)]
		for i in range(rows):
			for j in range(cols):
				txt = entries[i][j].get().strip()
				if txt == '':
					val = 0.0
				else:
					try:
						val = float(txt)
					except Exception:
						raise ValueError(f'Valor inválido en ({i+1},{j+1}): "{txt}"')
				mat[i][j] = val
		return mat

	def read_matrix_from_text(self, which='A'):
		# If in unified Gauss mode, only A is allowed
		if self.op_var.get() == 'Gauss/Gauss-Jordan' and which == 'B':
			self.result_box.delete('0.0', 'end')
			self.result_box.insert('0.0', 'En modo Gauss/Gauss-Jordan sólo se permite una matriz (Matriz A).')
			return
		target_text = self.text_a if which=='A' else self.text_b
		content = target_text.get('0.0', 'end').strip()
		if content == '':
			self.result_box.delete('0.0', 'end')
			self.result_box.insert('0.0', 'Texto vacío para la matriz.')
			return

		lines = [ln.strip() for ln in content.splitlines() if ln.strip()!='']
		mat = []
		for ln in lines:
			parts = [p for p in ln.replace(',', ' ').split()]
			row = []
			for p in parts:
				try:
					row.append(float(p))
				except Exception:
					self.result_box.delete('0.0', 'end')
					self.result_box.insert('0.0', f'Valor inválido al parsear: {p}')
					return
			mat.append(row)

		# check rectangular
		if any(len(r)!=len(mat[0]) for r in mat):
			self.result_box.delete('0.0', 'end')
			self.result_box.insert('0.0', 'La matriz no es rectangular (filas con distinta cantidad de columnas).')
			return

		rows = len(mat)
		cols = len(mat[0])

		# if entry grids exist, try to populate them, otherwise set rows/cols and generate
		try:
			if hasattr(self, 'entries_a') and self.entries_a and len(self.entries_a)==rows and len(self.entries_a[0])==cols:
				entries = self.entries_a if which=='A' else self.entries_b
				for i in range(rows):
					for j in range(cols):
						entries[i][j].delete(0, 'end')
						entries[i][j].insert(0, str(mat[i][j]))
			else:
				# update rows/cols and regenerate
				self.ent_rows.delete(0, 'end')
				self.ent_rows.insert(0, str(rows))
				self.ent_cols.delete(0, 'end')
				self.ent_cols.insert(0, str(cols))
				self.generate_matrix_grids()
				entries = self.entries_a if which=='A' else self.entries_b
				for i in range(rows):
					for j in range(cols):
						entries[i][j].insert(0, str(mat[i][j]))

			self.result_box.delete('0.0', 'end')
			self.result_box.insert('0.0', f'Matriz {which} leída ({rows}x{cols}).')
		except Exception as e:
			self.result_box.delete('0.0', 'end')
			self.result_box.insert('0.0', f'Error al poblar entradas: {e}')

	def calculate_operation(self):
		op = self.op_var.get()
		# For Gauss methods we only need one matrix (use A)
		if op == 'Gauss/Gauss-Jordan':
			# Determine actual gauss mode from selector
			mode = self.gauss_mode_var.get() if hasattr(self, 'gauss_mode_var') else 'Gauss-Jordan'
			try:
				A = self.parse_matrix_entries(self.entries_a)
			except Exception as e:
				self.result_box.delete('0.0', 'end')
				self.result_box.insert('0.0', f'Error: {e}')
				return
			# build augmented matrix: assume last column of A is RHS if A has more columns? We'll treat input A as full augmented matrix
			from algebraLineal import gauss_steps, gauss_jordan_steps
			if mode == 'Gauss':
				res = gauss_steps(A)
			else:
				res = gauss_jordan_steps(A)
			# display steps
			self.steps_box.delete('0.0', 'end')
			for i, s in enumerate(res.get('steps', [])):
				self.steps_box.insert('end', f'Paso {i}:\n')
				for row in s:
					self.steps_box.insert('end', '  '.join(f'{v:.4g}' for v in row) + '\n')
				self.steps_box.insert('end', '\n')
			# show status/solution
			self.result_box.delete('0.0', 'end')
			if res.get('status') == 'unique' and res.get('solution') is not None:
				sol = res['solution']
				self.result_box.insert('0.0', 'Solución única:\n')
				self.result_box.insert('end', '\n'.join(f'x{i+1} = {v:.6g}' for i, v in enumerate(sol)))
			elif res.get('status') == 'inconsistent':
				self.result_box.insert('0.0', 'El sistema es inconsistente (sin solución).')
			elif res.get('status') == 'infinite':
				self.result_box.insert('0.0', 'El sistema tiene infinitas soluciones (variables libres).')
			else:
				self.result_box.insert('0.0', f"Estado: {res.get('status')}")
			return
		
		# Otherwise treat as binary matrix operations between A and B
		try:
			A = self.parse_matrix_entries(self.entries_a)
			B = self.parse_matrix_entries(self.entries_b)
		except Exception as e:
			self.result_box.delete('0.0', 'end')
			self.result_box.insert('0.0', f'Error: {e}')
			return

		ra = len(A); ca = len(A[0]) if ra>0 else 0
		rb = len(B); cb = len(B[0]) if rb>0 else 0

		result = None
		try:
			if op == 'Suma' or op == 'Resta':
				if ra!=rb or ca!=cb:
					raise ValueError('Para suma/resta ambas matrices deben tener las mismas dimensiones.')
				result = [[(A[i][j] + B[i][j]) if op=='Suma' else (A[i][j] - B[i][j]) for j in range(ca)] for i in range(ra)]
			elif op == 'Multiplicación':
				if ca != rb:
					raise ValueError('Para multiplicación A.columnas debe ser igual a B.filas (A.cols == B.rows).')
				# multiply
				result = [[sum(A[i][k]*B[k][j] for k in range(ca)) for j in range(cb)] for i in range(ra)]
			else:
				raise ValueError('Operación desconocida')
		except Exception as e:
			self.result_box.delete('0.0', 'end')
			self.result_box.insert('0.0', f'Error: {e}')
			return

		# display result nicely
		out_lines = []
		for row in result:
			out_lines.append('  '.join(f'{v:.4g}' for v in row))
		self.result_box.delete('0.0', 'end')
		self.result_box.insert('0.0', '\n'.join(out_lines))

	def clear_matrices(self):
		# clear entry grids and textboxes
		try:
			for r in self.entries_a:
				for e in r:
					e.delete(0, 'end')
			for r in self.entries_b:
				for e in r:
					e.delete(0, 'end')
		except Exception:
			pass
		self.text_a.delete('0.0', 'end')
		self.text_b.delete('0.0', 'end')
		self.result_box.delete('0.0', 'end')

	def update_datetime(self):
		now = datetime.now()
		formatted = now.strftime("%A, %d %B %Y | %H:%M:%S")
		self.datetime_label.configure(text=formatted)
		# schedule next update
		self.after(1000, self.update_datetime)


if __name__ == "__main__":
	ctk.set_appearance_mode("System")
	ctk.set_default_color_theme("blue")
	app = MainApp()
	app.mainloop()
