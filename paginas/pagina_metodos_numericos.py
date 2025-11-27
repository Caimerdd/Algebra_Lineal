import customtkinter as ctk
from paginas.pagina_base import PaginaBase
from app_config import (COLOR_FONDO_SECUNDARIO, COLOR_NUMERICOS, COLOR_HOVER, 
                        COLOR_BOTON_SECUNDARIO, COLOR_BOTON_SECUNDARIO_HOVER)
from app_config import parse_valor, fmt
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sympy as sp
import numpy as np
from functools import partial

# Importación segura del backend
try:
    from MetodosNumericos import (
        metodo_biseccion, metodo_falsa_posicion, 
        metodo_newton_raphson, metodo_secante
    )
    LOGICA_DISPONIBLE = True
    print("✅ MetodosNumericos.py cargado exitosamente")
except ImportError as e:
    LOGICA_DISPONIBLE = False
    print(f"❌ Error cargando MetodosNumericos.py: {e}")
    # Funciones dummy
    def metodo_biseccion(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}
    def metodo_falsa_posicion(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}
    def metodo_newton_raphson(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}
    def metodo_secante(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}

class PaginaMetodosNumericos(PaginaBase):
    def crear_widgets(self):
        self.configurar_grid()
        self.crear_interfaz()
        self._actualizar_entradas_metodo()
    
    def configurar_grid(self):
        self.grid_rowconfigure(0, weight=0) # Selector
        self.grid_rowconfigure(1, weight=0) # Función
        self.grid_rowconfigure(2, weight=0) # Ejemplos
        self.grid_rowconfigure(3, weight=0) # Controles
        self.grid_rowconfigure(4, weight=1) # Resultados
        self.grid_columnconfigure(0, weight=1)
    
    def crear_interfaz(self):
        # Selector de Metodo
        marco_metodo = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_metodo.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        
        ctk.CTkLabel(marco_metodo, text="Método Numérico:", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=(12, 8), pady=12)
        
        self.metodo_numerico_var = ctk.StringVar(value="Biseccion")
        metodos = ["Biseccion", "Falsa Posicion", "Newton-Raphson", "Secante"]
        
        for i, metodo in enumerate(metodos):
            rb = ctk.CTkRadioButton(marco_metodo, text=metodo, variable=self.metodo_numerico_var, 
                                   value=metodo, font=ctk.CTkFont(size=13),
                                   command=self._actualizar_entradas_metodo)
            rb.grid(row=0, column=i+1, padx=8, pady=12)

        # Entrada de Funcion e Intervalos
        marco_funcion = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_funcion.grid(row=1, column=0, sticky="ew", padx=12, pady=(4, 8))
        marco_funcion.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_funcion, text="Función f(x) =", font=ctk.CTkFont(size=13)).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.ent_funcion_fx = ctk.CTkEntry(marco_funcion, placeholder_text="Ej: cos(x) - x")
        self.ent_funcion_fx.grid(row=0, column=1, columnspan=5, sticky="ew", padx=8, pady=6)
        
        # Fila 1: Entradas de Intervalo/Puntos
        self.lbl_intervalo = ctk.CTkLabel(marco_funcion, text="Intervalo [a, b]:", font=ctk.CTkFont(size=13))
        self.lbl_intervalo.grid(row=1, column=0, sticky="w", padx=8, pady=6)
        
        self.ent_intervalo_a = ctk.CTkEntry(marco_funcion, width=100, placeholder_text="a")
        self.ent_intervalo_a.grid(row=1, column=1, sticky="w", padx=(8,2), pady=6)
        
        self.ent_intervalo_b = ctk.CTkEntry(marco_funcion, width=100, placeholder_text="b")
        self.ent_intervalo_b.grid(row=1, column=2, sticky="w", padx=(2,8), pady=6)
        
        ctk.CTkLabel(marco_funcion, text="Tolerancia:", font=ctk.CTkFont(size=13)).grid(row=1, column=3, sticky="w", padx=(20, 2), pady=6)
        self.ent_tolerancia_e = ctk.CTkEntry(marco_funcion, width=100, placeholder_text="Ej: 0.0001")
        # INICIO LIMPIO: No insertamos valores por defecto
        self.ent_tolerancia_e.grid(row=1, column=4, sticky="w", padx=(2, 8), pady=6)
        
        # Botones de Ejemplos Rápidos (Opcionales, pero útiles para testear)
        marco_ejemplos = ctk.CTkFrame(self)
        marco_ejemplos.grid(row=2, column=0, sticky="ew", padx=12, pady=4)
        ctk.CTkLabel(marco_ejemplos, text="Cargar ejemplo:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=(4,6))
        
        ctk.CTkButton(marco_ejemplos, text="Trigonométrica", command=partial(self.cargar_ejemplo, 1),
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, width=100).grid(row=0, column=1, padx=4)
        ctk.CTkButton(marco_ejemplos, text="Exponencial", command=partial(self.cargar_ejemplo, 2),
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, width=100).grid(row=0, column=2, padx=4)
        ctk.CTkButton(marco_ejemplos, text="Polinomio", command=partial(self.cargar_ejemplo, 3),
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, width=100).grid(row=0, column=3, padx=4)

        # Controles
        marco_controles = ctk.CTkFrame(self)
        marco_controles.grid(row=3, column=0, sticky="ew", padx=12, pady=(6,12))
        
        ctk.CTkButton(marco_controles, text="Calcular Raíz", command=self.calcular_operacion_numerica,
                      fg_color=COLOR_NUMERICOS, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        
        ctk.CTkButton(marco_controles, text="Graficar", command=self.graficar_funcion_interna,
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=1, padx=6)
                      
        ctk.CTkButton(marco_controles, text="Limpiar", command=self.limpiar_numerico,
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=2, padx=6)

        # Resultados
        marco_resultados = ctk.CTkFrame(self)
        marco_resultados.grid(row=4, column=0, sticky="nsew", padx=12, pady=(6,12))
        marco_resultados.grid_rowconfigure(0, weight=1)
        marco_resultados.grid_columnconfigure(0, weight=2) # Pasos más anchos
        marco_resultados.grid_columnconfigure(1, weight=1)
        
        # Bitácora (ScrollableFrame)
        marco_pasos = ctk.CTkFrame(marco_resultados)
        marco_pasos.grid(row=0, column=0, sticky="nswe", padx=(0,6))
        marco_pasos.grid_columnconfigure(0, weight=1)
        marco_pasos.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_pasos, text="Tabla de Iteraciones", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        
        self.pasos_scroll_frame = ctk.CTkScrollableFrame(marco_pasos, fg_color=COLOR_FONDO_SECUNDARIO)
        self.pasos_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))
        self.pasos_scroll_frame.grid_columnconfigure(0, weight=1)
        
        # Resultado Final
        marco_resultado = ctk.CTkFrame(marco_resultados)
        marco_resultado.grid(row=0, column=1, sticky="nswe", padx=(6,0))
        marco_resultado.grid_columnconfigure(0, weight=1)
        marco_resultado.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_resultado, text="Resultado Final", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        
        self.resultado_caja = ctk.CTkTextbox(marco_resultado, height=220, 
                                             font=ctk.CTkFont(family="monospace", size=14, weight="bold"),
                                             border_color=COLOR_NUMERICOS[1],
                                             border_width=2,
                                             wrap="none")
        self.resultado_caja.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))
        self.resultado_caja.configure(state="disabled")

    # --- NUEVAS FUNCIONES DE UI ---
    def _limpiar_pasos_scroll(self):
        for widget in self.pasos_scroll_frame.winfo_children():
            widget.destroy()
            
    def _crear_bloque_texto(self, titulo: str, texto: str):
        paso_frame = ctk.CTkFrame(self.pasos_scroll_frame, fg_color="transparent")
        paso_frame.pack(fill="x", pady=(0, 10))
        
        lbl_titulo = ctk.CTkLabel(paso_frame, text=titulo.upper(), 
                                  font=ctk.CTkFont(size=12, weight="bold"),
                                  text_color=COLOR_NUMERICOS[0])
        lbl_titulo.pack(anchor="w", padx=5)
        
        lbl_texto = ctk.CTkLabel(paso_frame, text=texto, 
                                font=ctk.CTkFont(family="monospace", size=13), 
                                justify="left")
        lbl_texto.pack(anchor="w", padx=20, pady=2)
        
    def _crear_tabla_pasos(self, headers: list, data: list):
        tabla_frame = ctk.CTkFrame(self.pasos_scroll_frame, fg_color=COLOR_FONDO_SECUNDARIO)
        tabla_frame.pack(fill="x", expand=True, pady=10)
        
        # Encabezados
        for c, header in enumerate(headers):
            cell = ctk.CTkLabel(tabla_frame, text=header, 
                                font=ctk.CTkFont(family="monospace", size=12, weight="bold"),
                                text_color=COLOR_NUMERICOS[0])
            cell.grid(row=0, column=c, padx=8, pady=4, sticky="w")
            
        # Filas
        for r, row_data in enumerate(data):
            for c, cell_data in enumerate(row_data):
                if isinstance(cell_data, float):
                    if abs(cell_data) > 1e4 or (abs(cell_data) < 1e-3 and cell_data != 0):
                        texto = f"{cell_data:.4e}"
                    else:
                        texto = f"{cell_data:.6f}"
                else:
                    texto = str(cell_data)
                    
                cell = ctk.CTkLabel(tabla_frame, text=texto, 
                                    font=ctk.CTkFont(family="monospace", size=12))
                cell.grid(row=r + 1, column=c, padx=8, pady=2, sticky="w")
    
    # --- LÓGICA ---
    def _actualizar_entradas_metodo(self):
        metodo = self.metodo_numerico_var.get()
        self.ent_intervalo_b.grid() # Reset visibility
        
        if metodo in ["Biseccion", "Falsa Posicion"]:
            self.lbl_intervalo.configure(text="Intervalo [a, b]:")
            self.ent_intervalo_a.configure(placeholder_text="a")
            self.ent_intervalo_b.configure(placeholder_text="b")
        elif metodo == "Newton-Raphson":
            self.lbl_intervalo.configure(text="Punto Inicial (x0):")
            self.ent_intervalo_a.configure(placeholder_text="x0")
            self.ent_intervalo_b.grid_remove() 
        elif metodo == "Secante":
            self.lbl_intervalo.configure(text="Puntos [x0, x1]:")
            self.ent_intervalo_a.configure(placeholder_text="x0")
            self.ent_intervalo_b.configure(placeholder_text="x1")

    def cargar_ejemplo(self, ej_num: int):
        self.limpiar_numerico()
        # Solo llenamos si el usuario hace clic explícitamente en el botón
        self.ent_tolerancia_e.delete(0, 'end'); self.ent_tolerancia_e.insert(0, "0.0001")
        
        if ej_num == 1:
            self.ent_funcion_fx.insert(0, "cos(x) - x")
            self.ent_intervalo_a.insert(0, "0")
            self.ent_intervalo_b.insert(0, "1")
        elif ej_num == 2:
            self.ent_funcion_fx.insert(0, "log(x) - exp(-x)")
            self.ent_intervalo_a.insert(0, "0.5")
            self.ent_intervalo_b.insert(0, "2")
        elif ej_num == 3:
            self.ent_funcion_fx.insert(0, "x**2 - 4")
            self.ent_intervalo_a.insert(0, "0")
            self.ent_intervalo_b.insert(0, "3")

    def calcular_operacion_numerica(self):
        self._limpiar_pasos_scroll()
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete('0.0', 'end')
        
        if not LOGICA_DISPONIBLE:
            self.resultado_caja.insert('0.0', "ERROR: No se pudo cargar MetodosNumericos.py.")
            self.resultado_caja.configure(state="disabled")
            return

        metodo = self.metodo_numerico_var.get()
        
        try:
            funcion_str = self.ent_funcion_fx.get()
            tol_str = self.ent_tolerancia_e.get()
            
            if not funcion_str or not tol_str:
                raise ValueError("La función y la tolerancia son obligatorias.")
            
            tolerancia = parse_valor(tol_str)
            if tolerancia <= 0: raise ValueError("La tolerancia debe ser positiva.")

            res = None
            
            if metodo == 'Biseccion' or metodo == 'Falsa Posicion':
                a_str, b_str = self.ent_intervalo_a.get(), self.ent_intervalo_b.get()
                if not a_str or not b_str: raise ValueError("Faltan los valores del intervalo.")
                a, b = parse_valor(a_str), parse_valor(b_str)
                # Validación de intervalo básica
                if metodo == 'Biseccion' and a >= b: 
                     # Permitimos que la lógica intente, pero avisamos. 
                     # Bisección suele requerir a < b, pero a veces intercambia solo.
                     pass 
                
                res = metodo_biseccion(funcion_str, a, b, tolerancia) if metodo == 'Biseccion' else metodo_falsa_posicion(funcion_str, a, b, tolerancia)
            
            elif metodo == 'Newton-Raphson':
                x0_str = self.ent_intervalo_a.get()
                if not x0_str: raise ValueError("Falta el punto inicial x0.")
                x0 = parse_valor(x0_str)
                res = metodo_newton_raphson(funcion_str, x0, tolerancia)

            elif metodo == 'Secante':
                x0_str, x1_str = self.ent_intervalo_a.get(), self.ent_intervalo_b.get()
                if not x0_str or not x1_str: raise ValueError("Faltan los puntos x0 y x1.")
                x0, x1 = parse_valor(x0_str), parse_valor(x1_str)
                if x0 == x1: raise ValueError("Los puntos iniciales no pueden ser iguales.")
                res = metodo_secante(funcion_str, x0, x1, tolerancia)

            # --- RENDERIZADO ---
            if res.get('info_previa'):
                self._crear_bloque_texto("DATOS INICIALES", "\n".join(res['info_previa']))
            
            if res.get('tabla_headers') and res.get('tabla_data'):
                self._crear_tabla_pasos(res['tabla_headers'], res['tabla_data'])

            if res.get('mensaje_final'):
                self._crear_bloque_texto("ESTADO", res['mensaje_final'])

            if res['estado'] == 'exito':
                resultado_txt = (
                    f"Raíz Aproximada: {res['raiz']:.10f}\n"
                    f"Iteraciones:     {res['iteraciones']}\n"
                    f"Error Final:     {res.get('error', 0.0):.6e}"
                )
                self.resultado_caja.insert('0.0', resultado_txt)
            else:
                self.resultado_caja.insert('0.0', f"Error / Divergencia:\n{res['mensaje']}")

        except ValueError as e:
            self.resultado_caja.insert('0.0', f"Error de entrada:\n{e}")
        except Exception as e:
            self.resultado_caja.insert('0.0', f"Error de cálculo:\n{e}")
            
        self.resultado_caja.configure(state="disabled")

    def graficar_funcion_interna(self):
        try:
            funcion_str = self.ent_funcion_fx.get()
            if not funcion_str: raise ValueError("Ingrese una función para graficar.")

            a_str = self.ent_intervalo_a.get()
            b_str = self.ent_intervalo_b.get()
            metodo = self.metodo_numerico_var.get()
            
            # Definir rango de ploteo inteligente
            a_plot, b_plot = -10, 10
            try:
                if metodo != "Newton-Raphson" and a_str and b_str:
                    v1, v2 = parse_valor(a_str), parse_valor(b_str)
                    centro = (v1 + v2) / 2
                    ancho = abs(v2 - v1) * 2
                    if ancho < 2: ancho = 10 # Zoom mínimo
                    a_plot, b_plot = centro - ancho, centro + ancho
                elif metodo == "Newton-Raphson" and a_str:
                    v1 = parse_valor(a_str)
                    a_plot, b_plot = v1 - 5, v1 + 5
            except:
                pass # Si fallan los números, usamos -10 a 10 por defecto
            
            ventana_grafica = ctk.CTkToplevel(self)
            ventana_grafica.title(f"Gráfica: {funcion_str}")
            ventana_grafica.geometry("800x600")
            
            fig = Figure(figsize=(8, 6), dpi=100)
            ax = fig.add_subplot(111)

            x_sym = sp.Symbol('x')
            # Usamos sympy para convertir string a funcion python segura
            funcion_sympy = sp.sympify(funcion_str.replace('^', '**'))
            f_lamb = sp.lambdify(x_sym, funcion_sympy, modules=['numpy', 'math'])
            
            x_vals = np.linspace(a_plot, b_plot, 1000)
            try:
                y_vals = f_lamb(x_vals)
                # Manejar singularidades (valores infinitos o complejos)
                if isinstance(y_vals, (int, float)): y_vals = np.full_like(x_vals, y_vals) # Caso constante
                
                ax.plot(x_vals, y_vals, label=f'f(x)={funcion_str}', color=COLOR_NUMERICOS[1], linewidth=2)
                ax.axhline(0, color='black', linewidth=1)
                ax.axvline(0, color='black', linewidth=1)
                ax.grid(True, linestyle='--', alpha=0.6)
                ax.legend()
                
                # Marcar intervalo si existe
                if metodo != "Newton-Raphson" and a_str and b_str:
                    try:
                        va, vb = parse_valor(a_str), parse_valor(b_str)
                        ax.axvline(va, color='red', linestyle='--', label='a')
                        ax.axvline(vb, color='green', linestyle='--', label='b')
                    except: pass
                elif metodo == "Newton-Raphson" and a_str:
                     try:
                        vx = parse_valor(a_str)
                        ax.plot(vx, f_lamb(vx), 'ro', label='x0')
                     except: pass
                     
            except Exception as e:
                ax.text(0.5, 0.5, f"No se pudo graficar:\n{e}", ha='center', va='center', color='red')

            canvas = FigureCanvasTkAgg(fig, ventana_grafica)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            self.resultado_caja.configure(state="normal")
            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', f"Error graficando: {e}")
            self.resultado_caja.configure(state="disabled")

    def limpiar_numerico(self):
        self.ent_funcion_fx.delete(0, 'end')
        self.ent_intervalo_a.delete(0, 'end')
        self.ent_intervalo_b.delete(0, 'end')
        self.ent_tolerancia_e.delete(0, 'end')
        
        self._limpiar_pasos_scroll()
        
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete('0.0', 'end')
        self.resultado_caja.configure(state="disabled")
            
    def mostrar(self):
        self.grid(row=0, column=0, sticky="nsew")