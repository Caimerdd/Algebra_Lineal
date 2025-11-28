import customtkinter as ctk
from paginas.pagina_base import PaginaBase
from app_config import (COLOR_FONDO_SECUNDARIO, COLOR_INTEGRAL, 
                        COLOR_HOVER, COLOR_BOTON_SECUNDARIO, 
                        COLOR_BOTON_SECUNDARIO_HOVER)

# Importación segura
try:
    from LogicaIntegral import (
        calcular_integral_basica, calcular_area_entre_curvas,
        calcular_volumen_revolucion, calcular_longitud_arco
    )
    LOGICA_DISPONIBLE = True
except ImportError:
    LOGICA_DISPONIBLE = False
    # Dummies
    def calcular_integral_basica(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}
    def calcular_area_entre_curvas(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}
    def calcular_volumen_revolucion(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}
    def calcular_longitud_arco(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}


class PaginaIntegral(PaginaBase):
    def crear_widgets(self):
        self.configurar_grid()
        self.crear_barra_navegacion()
        self.crear_secciones()
        self.mostrar_seccion("basicas") # Default
    
    def configurar_grid(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def crear_barra_navegacion(self):
        marco_nav = ctk.CTkFrame(self, fg_color="transparent", height=40)
        marco_nav.grid(row=0, column=0, sticky="ew", padx=12, pady=(8,0))
        
        self.btn_basicas = ctk.CTkButton(marco_nav, text="Integrales", 
                                       fg_color=COLOR_INTEGRAL, height=30,
                                       command=lambda: self.mostrar_seccion("basicas"))
        self.btn_basicas.pack(side="left", padx=(0, 5), expand=True, fill="x")
        
        self.btn_areas = ctk.CTkButton(marco_nav, text="Área entre Curvas", 
                                     fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, height=30,
                                     command=lambda: self.mostrar_seccion("areas"))
        self.btn_areas.pack(side="left", padx=5, expand=True, fill="x")
        
        self.btn_apli = ctk.CTkButton(marco_nav, text="Volúmenes y Longitud", 
                                    fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, height=30,
                                    command=lambda: self.mostrar_seccion("aplicaciones"))
        self.btn_apli.pack(side="left", padx=(5, 0), expand=True, fill="x")

    def crear_secciones(self):
        self.marco_contenido = ctk.CTkFrame(self, fg_color="transparent")
        self.marco_contenido.grid(row=1, column=0, sticky="nsew")
        self.marco_contenido.grid_columnconfigure(0, weight=1)
        
        self.marco_contenido.grid_rowconfigure(0, weight=0)
        self.marco_contenido.grid_rowconfigure(1, weight=0)
        self.marco_contenido.grid_rowconfigure(2, weight=1)
        
        # --- ZONA DE ENTRADAS ---
        self.marco_inputs = ctk.CTkFrame(self.marco_contenido, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_inputs.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        
        self.marco_inputs.grid_columnconfigure(0, weight=0) 
        self.marco_inputs.grid_columnconfigure(1, weight=1) 
        self.marco_inputs.grid_columnconfigure(2, weight=0) 
        self.marco_inputs.grid_columnconfigure(3, weight=1) 

        # --- ELEMENTOS DE INTERFAZ ---
        self.lbl_op = ctk.CTkLabel(self.marco_inputs, text="Tipo:", font=ctk.CTkFont(size=14, weight="bold"))
        
        # Contenedor para los radiobuttons (Los crearemos dinámicamente)
        self.marco_radios = ctk.CTkFrame(self.marco_inputs, fg_color="transparent")
        self.tipo_var = ctk.StringVar(value="Indefinida")
        
        # Función Principal
        self.lbl_f = ctk.CTkLabel(self.marco_inputs, text="Función f(x):", font=ctk.CTkFont(size=13))
        self.ent_f = ctk.CTkEntry(self.marco_inputs, placeholder_text="Ej: x^2 * sin(x)", height=35)
        
        # Función Secundaria
        self.lbl_g = ctk.CTkLabel(self.marco_inputs, text="Función g(x):", font=ctk.CTkFont(size=13))
        self.ent_g = ctk.CTkEntry(self.marco_inputs, placeholder_text="Ej: x", height=35)
        
        # Límites
        self.marco_limites = ctk.CTkFrame(self.marco_inputs, fg_color="transparent")
        self.lbl_a = ctk.CTkLabel(self.marco_limites, text="Límite Inf. (a):", font=ctk.CTkFont(size=13))
        self.ent_a = ctk.CTkEntry(self.marco_limites, width=100, justify="center")
        self.lbl_b = ctk.CTkLabel(self.marco_limites, text="Límite Sup. (b):", font=ctk.CTkFont(size=13))
        self.ent_b = ctk.CTkEntry(self.marco_limites, width=100, justify="center")
        
        self.lbl_a.pack(side="left", padx=(0,5))
        self.ent_a.pack(side="left", padx=(0,20))
        self.lbl_b.pack(side="left", padx=(0,5))
        self.ent_b.pack(side="left")

        # --- CONTROLES ---
        marco_btns = ctk.CTkFrame(self.marco_contenido, fg_color="transparent")
        marco_btns.grid(row=1, column=0, sticky="ew", padx=12, pady=0)
        
        ctk.CTkButton(marco_btns, text="CALCULAR", command=self.calcular, 
                      fg_color=COLOR_INTEGRAL, hover_color=COLOR_HOVER, height=40, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5, expand=True, fill="x")
        
        ctk.CTkButton(marco_btns, text="Limpiar", command=self.limpiar, 
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, height=40).pack(side="left", padx=5)
        
        ctk.CTkButton(marco_btns, text="Ayuda ❓", command=lambda: self.app.mostrar_ayuda_sympy(), 
                      fg_color=COLOR_BOTON_SECUNDARIO, width=50, height=40).pack(side="left", padx=5)

        # --- RESULTADOS ---
        marco_res = ctk.CTkFrame(self.marco_contenido)
        marco_res.grid(row=2, column=0, sticky="nsew", padx=12, pady=(12, 12))
        marco_res.grid_rowconfigure(0, weight=1)
        marco_res.grid_columnconfigure(0, weight=1)
        marco_res.grid_columnconfigure(1, weight=1)
        
        f_bita = ctk.CTkFrame(marco_res, fg_color="transparent")
        f_bita.grid(row=0, column=0, sticky="nsew", padx=(5,5), pady=5)
        ctk.CTkLabel(f_bita, text="Bitácora y Pasos", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0,5))
        self.scroll_pasos = ctk.CTkScrollableFrame(f_bita, fg_color=COLOR_FONDO_SECUNDARIO)
        self.scroll_pasos.pack(fill="both", expand=True)
        
        f_res = ctk.CTkFrame(marco_res, fg_color="transparent")
        f_res.grid(row=0, column=1, sticky="nsew", padx=(5,5), pady=5)
        ctk.CTkLabel(f_res, text="Resultado Final", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0,5))
        self.txt_res = ctk.CTkTextbox(f_res, font=ctk.CTkFont(family="Consolas", size=14, weight="bold"), 
                                      border_color=COLOR_INTEGRAL[1], border_width=2)
        self.txt_res.pack(fill="both", expand=True)
        self.txt_res.configure(state="disabled")
        
        self.seccion_actual = "basicas"

    def mostrar_seccion(self, seccion):
        self.seccion_actual = seccion
        
        self.btn_basicas.configure(fg_color=COLOR_BOTON_SECUNDARIO if seccion!="basicas" else COLOR_INTEGRAL)
        self.btn_areas.configure(fg_color=COLOR_BOTON_SECUNDARIO if seccion!="areas" else COLOR_INTEGRAL)
        self.btn_apli.configure(fg_color=COLOR_BOTON_SECUNDARIO if seccion!="aplicaciones" else COLOR_INTEGRAL)
        
        # Limpiar inputs visuales
        self.lbl_op.grid_forget(); self.marco_radios.grid_forget()
        self.lbl_f.grid_forget(); self.ent_f.grid_forget()
        self.lbl_g.grid_forget(); self.ent_g.grid_forget()
        self.marco_limites.grid_forget()

        # Limpiar y recrear RadioButtons para evitar error de 'value'
        for widget in self.marco_radios.winfo_children(): widget.destroy()

        if seccion == "basicas":
            # Crear RadioButtons nuevos
            self.tipo_var.set("Indefinida")
            ctk.CTkRadioButton(self.marco_radios, text="Indefinida", variable=self.tipo_var, value="Indefinida", command=self._update_inputs).pack(side="left", padx=10)
            ctk.CTkRadioButton(self.marco_radios, text="Definida", variable=self.tipo_var, value="Definida", command=self._update_inputs).pack(side="left", padx=10)

            self.lbl_op.grid(row=0, column=0, padx=15, pady=15, sticky="e")
            self.marco_radios.grid(row=0, column=1, padx=15, pady=15, sticky="w", columnspan=3)
            
            self.lbl_f.grid(row=1, column=0, padx=15, pady=10, sticky="e")
            self.ent_f.grid(row=1, column=1, padx=15, pady=10, sticky="ew", columnspan=3)
            
            self._update_inputs()

        elif seccion == "areas":
            self.lbl_f.configure(text="Función f(x) [Techo]:")
            self.lbl_f.grid(row=0, column=0, padx=10, pady=15, sticky="e")
            self.ent_f.grid(row=0, column=1, padx=10, pady=15, sticky="ew")
            
            self.lbl_g.grid(row=0, column=2, padx=10, pady=15, sticky="e")
            self.ent_g.grid(row=0, column=3, padx=10, pady=15, sticky="ew")
            
            self.marco_limites.grid(row=1, column=0, columnspan=4, pady=15)

        elif seccion == "aplicaciones":
            # Crear RadioButtons nuevos
            self.tipo_var.set("Volumen Revolución (Eje X)")
            ctk.CTkRadioButton(self.marco_radios, text="Volumen Revolución", variable=self.tipo_var, value="Volumen Revolución (Eje X)").pack(side="left", padx=10)
            ctk.CTkRadioButton(self.marco_radios, text="Longitud de Arco", variable=self.tipo_var, value="Longitud de Arco").pack(side="left", padx=10)

            self.lbl_op.grid(row=0, column=0, padx=15, pady=15, sticky="e")
            self.marco_radios.grid(row=0, column=1, padx=15, pady=15, sticky="w", columnspan=3)
            
            self.lbl_f.configure(text="Función f(x):")
            self.lbl_f.grid(row=1, column=0, padx=15, pady=10, sticky="e")
            self.ent_f.grid(row=1, column=1, padx=15, pady=10, sticky="ew", columnspan=3)
            
            self.marco_limites.grid(row=2, column=0, columnspan=4, pady=15)

    def _update_inputs(self):
        if self.seccion_actual == "basicas":
            modo = self.tipo_var.get()
            if modo == "Indefinida":
                self.marco_limites.grid_forget()
            else:
                self.marco_limites.grid(row=2, column=0, columnspan=4, pady=15)

    def _crear_bloque_texto(self, titulo, math):
        f = ctk.CTkFrame(self.scroll_pasos, fg_color="transparent")
        f.pack(fill="x", pady=5)
        ctk.CTkLabel(f, text=titulo, text_color=COLOR_INTEGRAL[0], font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        ctk.CTkLabel(f, text=math, font=ctk.CTkFont(family="Consolas", size=14), justify="left").pack(anchor="w", padx=10)

    def calcular(self):
        for w in self.scroll_pasos.winfo_children(): w.destroy()
        self.txt_res.configure(state="normal"); self.txt_res.delete('0.0', 'end')
        
        if not LOGICA_DISPONIBLE:
            self.txt_res.insert('0.0', "Error: Lógica no disponible."); self.txt_res.configure(state="disabled")
            return

        try:
            f_str = self.ent_f.get()
            if not f_str: raise ValueError("Falta la función f(x)")

            res = None
            
            if self.seccion_actual == "basicas":
                tipo = self.tipo_var.get()
                a = self.ent_a.get() if tipo == "Definida" else None
                b = self.ent_b.get() if tipo == "Definida" else None
                res = calcular_integral_basica(f_str, a, b, tipo)
            
            elif self.seccion_actual == "areas":
                g_str = self.ent_g.get()
                a = self.ent_a.get(); b = self.ent_b.get()
                if not g_str or not a or not b: raise ValueError("Faltan datos (g(x), a, o b).")
                res = calcular_area_entre_curvas(f_str, g_str, a, b)
                
            elif self.seccion_actual == "aplicaciones":
                tipo = self.tipo_var.get()
                a = self.ent_a.get(); b = self.ent_b.get()
                if not a or not b: raise ValueError("Faltan límites de integración.")
                
                if "Volumen" in tipo:
                    res = calcular_volumen_revolucion(f_str, a, b)
                else:
                    res = calcular_longitud_arco(f_str, a, b)

            if res.get('pasos'):
                for p in res['pasos']: self._crear_bloque_texto(p['titulo'], p['math'])
            
            if res['estado'] == 'exito':
                self.txt_res.insert('0.0', res['resultado_math'])
            else:
                self.txt_res.insert('0.0', f"Error:\n{res['mensaje']}")

        except ValueError as e: self.txt_res.insert('0.0', f"Error entrada: {e}")
        except Exception as e: self.txt_res.insert('0.0', f"Error: {e}")
        
        self.txt_res.configure(state="disabled")

    def limpiar(self):
        self.ent_f.delete(0, 'end'); self.ent_g.delete(0, 'end')
        self.ent_a.delete(0, 'end'); self.ent_b.delete(0, 'end')
        for w in self.scroll_pasos.winfo_children(): w.destroy()
        self.txt_res.configure(state="normal"); self.txt_res.delete('0.0', 'end'); self.txt_res.configure(state="disabled")