import customtkinter as ctk
from paginas.pagina_base import PaginaBase
from app_config import (COLOR_FONDO_SECUNDARIO, COLOR_DIFERENCIAL, 
                        COLOR_HOVER, COLOR_BOTON_SECUNDARIO, 
                        COLOR_BOTON_SECUNDARIO_HOVER)

# Importación segura
try:
    from LogicaDiferencial import calcular_limite, calcular_derivada, analisis_puntos_criticos
    LOGICA_DISPONIBLE = True
except ImportError:
    LOGICA_DISPONIBLE = False
    def calcular_limite(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}
    def calcular_derivada(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}
    def analisis_puntos_criticos(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}

class PaginaDiferencial(PaginaBase):
    def crear_widgets(self):
        self.configurar_grid()
        self.crear_barra_navegacion()
        self.crear_secciones()
        self.mostrar_seccion("derivadas") # Default
    
    def configurar_grid(self):
        # 0: Nav, 1: Contenido
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def crear_barra_navegacion(self):
        marco_nav = ctk.CTkFrame(self, fg_color="transparent", height=40)
        marco_nav.grid(row=0, column=0, sticky="ew", padx=12, pady=(8,0))
        
        self.btn_limites = ctk.CTkButton(marco_nav, text="Límites", 
                                       fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, height=30,
                                       command=lambda: self.mostrar_seccion("limites"))
        self.btn_limites.pack(side="left", padx=(0, 5), expand=True, fill="x")
        
        self.btn_derivadas = ctk.CTkButton(marco_nav, text="Derivadas", 
                                     fg_color=COLOR_DIFERENCIAL, height=30,
                                     command=lambda: self.mostrar_seccion("derivadas"))
        self.btn_derivadas.pack(side="left", padx=5, expand=True, fill="x")
        
        self.btn_apli = ctk.CTkButton(marco_nav, text="Aplicaciones (Máx/Mín)", 
                                    fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, height=30,
                                    command=lambda: self.mostrar_seccion("aplicaciones"))
        self.btn_apli.pack(side="left", padx=(5, 0), expand=True, fill="x")

    def crear_secciones(self):
        self.marco_contenido = ctk.CTkFrame(self, fg_color="transparent")
        self.marco_contenido.grid(row=1, column=0, sticky="nsew")
        self.marco_contenido.grid_columnconfigure(0, weight=1)
        
        # Filas: Inputs, Botones, Resultados
        self.marco_contenido.grid_rowconfigure(0, weight=0)
        self.marco_contenido.grid_rowconfigure(1, weight=0)
        self.marco_contenido.grid_rowconfigure(2, weight=1)
        
        # --- ZONA DE ENTRADAS ---
        self.marco_inputs = ctk.CTkFrame(self.marco_contenido, fg_color=COLOR_FONDO_SECUNDARIO)
        self.marco_inputs.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        
        self.marco_inputs.grid_columnconfigure(0, weight=0) 
        self.marco_inputs.grid_columnconfigure(1, weight=1)
        self.marco_inputs.grid_columnconfigure(2, weight=0)
        self.marco_inputs.grid_columnconfigure(3, weight=0)

        # Elementos UI
        self.lbl_f = ctk.CTkLabel(self.marco_inputs, text="Función f(x):", font=ctk.CTkFont(size=14))
        self.ent_f = ctk.CTkEntry(self.marco_inputs, placeholder_text="Ej: x^3 - 3x", height=35)
        
        # Para Límites
        self.lbl_tendencia = ctk.CTkLabel(self.marco_inputs, text="x tiende a:", font=ctk.CTkFont(size=13))
        self.ent_tendencia = ctk.CTkEntry(self.marco_inputs, width=80, justify="center")
        self.opt_dir = ctk.CTkOptionMenu(self.marco_inputs, values=["Ambos lados", "Derecha (+)", "Izquierda (-)"], width=120)
        
        # Para Derivadas
        self.lbl_orden = ctk.CTkLabel(self.marco_inputs, text="Orden:", font=ctk.CTkFont(size=13))
        self.ent_orden = ctk.CTkEntry(self.marco_inputs, width=60, justify="center")
        self.ent_orden.insert(0, "1")

        # Layout Inicial (Derivadas)
        self.lbl_f.grid(row=0, column=0, padx=10, pady=15, sticky="e")
        self.ent_f.grid(row=0, column=1, padx=10, pady=15, sticky="ew")
        self.lbl_orden.grid(row=0, column=2, padx=5, pady=15)
        self.ent_orden.grid(row=0, column=3, padx=10, pady=15)

        # --- CONTROLES ---
        marco_btns = ctk.CTkFrame(self.marco_contenido, fg_color="transparent")
        marco_btns.grid(row=1, column=0, sticky="ew", padx=12, pady=0)
        
        ctk.CTkButton(marco_btns, text="CALCULAR", command=self.calcular, 
                      fg_color=COLOR_DIFERENCIAL, hover_color=COLOR_HOVER, height=40, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5, expand=True, fill="x")
        
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
                                      border_color=COLOR_DIFERENCIAL[1], border_width=2)
        self.txt_res.pack(fill="both", expand=True)
        self.txt_res.configure(state="disabled")
        
        self.seccion_actual = "derivadas"

    def mostrar_seccion(self, seccion):
        self.seccion_actual = seccion
        
        # Colores botones
        btns = [self.btn_limites, self.btn_derivadas, self.btn_apli]
        names = ["limites", "derivadas", "aplicaciones"]
        for btn, name in zip(btns, names):
            btn.configure(fg_color=COLOR_DIFERENCIAL if seccion==name else COLOR_BOTON_SECUNDARIO)
        
        # Limpiar Inputs adicionales
        self.lbl_tendencia.grid_forget(); self.ent_tendencia.grid_forget(); self.opt_dir.grid_forget()
        self.lbl_orden.grid_forget(); self.ent_orden.grid_forget()

        # Configurar Inputs
        if seccion == "limites":
            self.lbl_tendencia.grid(row=0, column=2, padx=5, pady=15)
            self.ent_tendencia.grid(row=0, column=3, padx=5, pady=15)
            self.opt_dir.grid(row=1, column=1, padx=10, pady=(0,15), sticky="w")
        
        elif seccion == "derivadas":
            self.lbl_orden.grid(row=0, column=2, padx=5, pady=15)
            self.ent_orden.grid(row=0, column=3, padx=10, pady=15)
            
        elif seccion == "aplicaciones":
            # Solo necesita la función f(x), ocultamos los extras
            pass

    def _crear_bloque_texto(self, titulo, math):
        f = ctk.CTkFrame(self.scroll_pasos, fg_color="transparent")
        f.pack(fill="x", pady=5)
        ctk.CTkLabel(f, text=titulo, text_color=COLOR_DIFERENCIAL[0], font=ctk.CTkFont(weight="bold")).pack(anchor="w")
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

            if self.seccion_actual == "limites":
                tendencia = self.ent_tendencia.get()
                if not tendencia: raise ValueError("Falta el valor de tendencia 'a'.")
                
                d_map = {"Ambos lados": "both", "Derecha (+)": "+", "Izquierda (-)": "-"}
                dir_val = d_map[self.opt_dir.get()]
                res = calcular_limite(f_str, tendencia, dir_val)
            
            elif self.seccion_actual == "derivadas":
                orden = self.ent_orden.get()
                res = calcular_derivada(f_str, orden)
            
            elif self.seccion_actual == "aplicaciones":
                res = analisis_puntos_criticos(f_str)

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
        self.ent_f.delete(0, 'end')
        self.ent_tendencia.delete(0, 'end')
        self.ent_orden.delete(0, 'end'); self.ent_orden.insert(0, "1")
        for w in self.scroll_pasos.winfo_children(): w.destroy()
        self.txt_res.configure(state="normal"); self.txt_res.delete('0.0', 'end'); self.txt_res.configure(state="disabled")