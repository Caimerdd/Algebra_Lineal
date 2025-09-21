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
			# example: show a description and a button to open the algebraLineal module
			lbl = ctk.CTkLabel(self.content, text="Álgebra Lineal\n\nResolver sistemas de ecuaciones y operaciones matriciales.", justify="left")
			lbl.grid(row=0, column=0, sticky="nw", padx=12, pady=12)

			run_btn = ctk.CTkButton(self.content, text="Abrir herramienta de Álgebra Lineal", command=self.open_algebra)
			run_btn.grid(row=1, column=0, sticky="w", padx=12, pady=(6,12))
		else:
			lbl = ctk.CTkLabel(self.content, text=f"Has seleccionado: {name}\n\nContenido de ejemplo para la sección.", justify="left")
			lbl.grid(row=0, column=0, sticky="nw", padx=12, pady=12)

	def open_algebra(self):
		try:
			import algebraLineal as al
			# simple action: show a message in the content area
			lbl = ctk.CTkLabel(self.content, text="Módulo de Álgebra Lineal cargado. Ejecuta desde consola para ingresar ecuaciones.")
			lbl.grid(row=2, column=0, sticky="nw", padx=12, pady=6)
		except Exception as e:
			lbl = ctk.CTkLabel(self.content, text=f"Error al cargar módulo: {e}")
			lbl.grid(row=2, column=0, sticky="nw", padx=12, pady=6)

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
