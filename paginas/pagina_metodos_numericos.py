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
from tkinter import filedialog
import re

# Importación segura del backend
try:
    from MetodosNumericos import (
        metodo_biseccion, metodo_falsa_posicion, 
        metodo_newton_raphson, metodo_secante
    )
    LOGICA_DISPONIBLE = True
except ImportError:
    LOGICA_DISPONIBLE = False
    def metodo_biseccion(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}
    def metodo_falsa_posicion(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}
    def metodo_newton_raphson(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}
    def metodo_secante(*args): return {'estado': 'error', 'mensaje': 'Lógica no disponible'}

class PaginaMetodosNumericos(PaginaBase):
    def crear_widgets(self):
        self.configurar_grid()
        self.crear_barra_navegacion()
        self.crear_interfaz()
        self._actualizar_entradas_metodo()
    
    def configurar_grid(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def crear_barra_navegacion(self):
        marco_nav = ctk.CTkFrame(self, fg_color="transparent", height=40)
        marco_nav.grid(row=0, column=0, sticky="ew", padx=12, pady=(8,0))
        
        btn_raices = ctk.CTkButton(marco_nav, text="Raíces (Ecuaciones No Lineales)", 
                                   fg_color=COLOR_NUMERICOS, state="disabled", 
                                   text_color_disabled=("white", "white"), height=30)
        btn_raices.pack(side="left", padx=(0, 5), expand=True, fill="x")
    
    def crear_interfaz(self):
        marco_metodo = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_metodo.grid(row=1, column=0, sticky="ew", padx=12, pady=8)
        
        ctk.CTkLabel(marco_metodo, text="Método Numérico:", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=(12, 8), pady=12)
        
        self.metodo_numerico_var = ctk.StringVar(value="Biseccion")
        metodos = ["Biseccion", "Falsa Posicion", "Newton-Raphson", "Secante"]
        
        for i, metodo in enumerate(metodos):
            rb = ctk.CTkRadioButton(marco_metodo, text=metodo, variable=self.metodo_numerico_var, 
                                   value=metodo, font=ctk.CTkFont(size=13),
                                   command=self._actualizar_entradas_metodo)
            rb.grid(row=0, column=i+1, padx=8, pady=12)

        marco_funcion = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_funcion.grid(row=2, column=0, sticky="ew", padx=12, pady=(4, 8))
        marco_funcion.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_funcion, text="Función f(x) =", font=ctk.CTkFont(size=13)).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        
        self.ent_funcion_fx = ctk.CTkEntry(marco_funcion, placeholder_text="Ej: x^3 - x - 2")
        self.ent_funcion_fx.grid(row=0, column=1, columnspan=5, sticky="ew", padx=8, pady=6)
        
        self.lbl_intervalo = ctk.CTkLabel(marco_funcion, text="Intervalo [a, b]:", font=ctk.CTkFont(size=13))
        self.lbl_intervalo.grid(row=1, column=0, sticky="w", padx=8, pady=6)
        
        self.ent_intervalo_a = ctk.CTkEntry(marco_funcion, width=100, placeholder_text="a")
        self.ent_intervalo_a.grid(row=1, column=1, sticky="w", padx=(8,2), pady=6)
        
        self.ent_intervalo_b = ctk.CTkEntry(marco_funcion, width=100, placeholder_text="b")
        self.ent_intervalo_b.grid(row=1, column=2, sticky="w", padx=(2,8), pady=6)
        
        ctk.CTkLabel(marco_funcion, text="Tolerancia:", font=ctk.CTkFont(size=13)).grid(row=1, column=3, sticky="w", padx=(20, 2), pady=6)
        self.ent_tolerancia_e = ctk.CTkEntry(marco_funcion, width=100)
        self.ent_tolerancia_e.insert(0, "0.0001")
        self.ent_tolerancia_e.grid(row=1, column=4, sticky="w", padx=(2, 8), pady=6)
        
        marco_controles = ctk.CTkFrame(self)
        marco_controles.grid(row=3, column=0, sticky="ew", padx=12, pady=(6,12))
        
        ctk.CTkButton(marco_controles, text="Calcular Raíz", command=self.calcular_operacion_numerica,
                      fg_color=COLOR_NUMERICOS, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        
        ctk.CTkButton(marco_controles, text="Graficar", command=self.graficar_funcion_interna,
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=1, padx=6)
                      
        ctk.CTkButton(marco_controles, text="Limpiar", command=self.limpiar_numerico,
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=2, padx=6)

        ctk.CTkButton(marco_controles, text="Ayuda ❓", command=lambda: self.app.mostrar_ayuda_sympy(),
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, width=80).grid(row=0, column=3, padx=6)

        marco_resultados = ctk.CTkFrame(self)
        marco_resultados.grid(row=4, column=0, sticky="nsew", padx=12, pady=(6,12))
        marco_resultados.grid_rowconfigure(0, weight=1)
        marco_resultados.grid_columnconfigure(0, weight=2)
        marco_resultados.grid_columnconfigure(1, weight=1)
        
        marco_pasos = ctk.CTkFrame(marco_resultados)
        marco_pasos.grid(row=0, column=0, sticky="nswe", padx=(0,6))
        marco_pasos.grid_columnconfigure(0, weight=1)
        marco_pasos.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_pasos, text="Bitácora y Análisis", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        
        self.pasos_scroll_frame = ctk.CTkScrollableFrame(marco_pasos, fg_color=COLOR_FONDO_SECUNDARIO)
        self.pasos_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))
        self.pasos_scroll_frame.grid_columnconfigure(0, weight=1)
        
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

    def _limpiar_pasos_scroll(self):
        for widget in self.pasos_scroll_frame.winfo_children(): widget.destroy()
            
    def _crear_bloque_texto(self, titulo: str, texto: str):
        paso_frame = ctk.CTkFrame(self.pasos_scroll_frame, fg_color="transparent")
        paso_frame.pack(fill="x", pady=(0, 10))
        
        lbl_titulo = ctk.CTkLabel(paso_frame, text=titulo.upper(), 
                                  font=ctk.CTkFont(size=12, weight="bold"),
                                  text_color=COLOR_NUMERICOS[0])
        lbl_titulo.pack(anchor="w", padx=5)
        
        lbl_texto = ctk.CTkLabel(paso_frame, text=texto, 
                                font=ctk.CTkFont(family="Consolas", size=14), 
                                justify="left")
        lbl_texto.pack(anchor="w", padx=20, pady=2)
        
    def _crear_tabla_pasos(self, headers: list, data: list):
        tabla_frame = ctk.CTkFrame(self.pasos_scroll_frame, fg_color=COLOR_FONDO_SECUNDARIO)
        tabla_frame.pack(fill="x", expand=True, pady=10)
        
        for c, header in enumerate(headers):
            cell = ctk.CTkLabel(tabla_frame, text=header, 
                                font=ctk.CTkFont(family="monospace", size=12, weight="bold"),
                                text_color=COLOR_NUMERICOS[0])
            cell.grid(row=0, column=c, padx=8, pady=4, sticky="w")
            
        for r, row_data in enumerate(data):
            for c, cell_data in enumerate(row_data):
                # FIX: Forzar conversión a float para formateo limpio
                try:
                    val = float(cell_data)
                    if abs(val) > 1e4 or (abs(val) < 1e-3 and val != 0):
                        texto = f"{val:.4e}"
                    else:
                        texto = f"{val:.6f}"
                except (ValueError, TypeError):
                    texto = str(cell_data)
                    
                cell = ctk.CTkLabel(tabla_frame, text=texto, 
                                    font=ctk.CTkFont(family="monospace", size=12))
                cell.grid(row=r + 1, column=c, padx=8, pady=2, sticky="w")
    
    def _actualizar_entradas_metodo(self):
        metodo = self.metodo_numerico_var.get()
        self.ent_intervalo_b.grid() 
        
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

    def _procesar_texto_funcion(self, texto):
        texto = texto.lower().replace('^', '**')
        texto = texto.replace('ln', 'log') 
        if 'e**' in texto: texto = texto.replace('e**', 'exp(') + ')' 
        return texto

    def calcular_operacion_numerica(self):
        self._limpiar_pasos_scroll()
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete('0.0', 'end')
        
        if not LOGICA_DISPONIBLE:
            self.resultado_caja.insert('0.0', "ERROR: MetodosNumericos.py no disponible.")
            self.resultado_caja.configure(state="disabled")
            return

        metodo = self.metodo_numerico_var.get()
        try:
            funcion_raw = self.ent_funcion_fx.get()
            tol_str = self.ent_tolerancia_e.get()
            
            if not funcion_raw or not tol_str: raise ValueError("Función y tolerancia son requeridas.")
            tolerancia = parse_valor(tol_str)
            if tolerancia <= 0: raise ValueError("La tolerancia debe ser > 0.")

            # --- VISUALIZACIÓN ---
            funcion_str = self._procesar_texto_funcion(funcion_raw)
            try:
                x = sp.Symbol('x')
                expr = sp.sympify(funcion_str, evaluate=False)
                texto_bonito = sp.pretty(expr, use_unicode=True).replace('⋅', '')
                self._crear_bloque_texto("FUNCIÓN", texto_bonito)
            except:
                self._crear_bloque_texto("FUNCIÓN", funcion_raw)

            # --- CÁLCULO ---
            res = None
            if metodo in ['Biseccion', 'Falsa Posicion']:
                a_str, b_str = self.ent_intervalo_a.get(), self.ent_intervalo_b.get()
                if not a_str or not b_str: raise ValueError("Faltan intervalos.")
                a, b = parse_valor(a_str), parse_valor(b_str)
                res = metodo_biseccion(funcion_str, a, b, tolerancia) if metodo == 'Biseccion' else metodo_falsa_posicion(funcion_str, a, b, tolerancia)
            
            elif metodo == 'Newton-Raphson':
                x0_str = self.ent_intervalo_a.get()
                if not x0_str: raise ValueError("Falta x0.")
                x0 = parse_valor(x0_str)
                res = metodo_newton_raphson(funcion_str, x0, tolerancia)

            elif metodo == 'Secante':
                x0_str, x1_str = self.ent_intervalo_a.get(), self.ent_intervalo_b.get()
                if not x0_str or not x1_str: raise ValueError("Faltan x0 y x1.")
                x0, x1 = parse_valor(x0_str), parse_valor(x1_str)
                res = metodo_secante(funcion_str, x0, x1, tolerancia)

            if res.get('info_previa'): self._crear_bloque_texto("DATOS INICIALES", "\n".join(res['info_previa']))
            if res.get('tabla_data'): self._crear_tabla_pasos(res['tabla_headers'], res['tabla_data'])
            
            if res['estado'] == 'exito':
                # FIX: Convertir a float estándar antes de formatear
                val_raiz = float(res['raiz'])
                val_error = float(res.get('error', 0.0))
                
                txt = f"Raíz Aproximada: {val_raiz:.10f}\nIteraciones: {res['iteraciones']}\nError Final: {val_error:.6e}"
                self.resultado_caja.insert('0.0', txt)
            else:
                self.resultado_caja.insert('0.0', f"Error / Divergencia:\n{res['mensaje']}")

        except ValueError as e:
            self.resultado_caja.insert('0.0', f"Entrada inválida: {e}")
        except Exception as e:
            self.resultado_caja.insert('0.0', f"Error de cálculo: {e}")
            
        self.resultado_caja.configure(state="disabled")

    def graficar_funcion_interna(self):
        try:
            funcion_raw = self.ent_funcion_fx.get()
            if not funcion_raw: raise ValueError("Ingrese una función.")
            
            funcion_str = self._procesar_texto_funcion(funcion_raw)

            a_str, b_str = self.ent_intervalo_a.get(), self.ent_intervalo_b.get()
            metodo = self.metodo_numerico_var.get()
            
            a_plot, b_plot = -10, 10
            try:
                if metodo != "Newton-Raphson" and a_str and b_str:
                    v1, v2 = parse_valor(a_str), parse_valor(b_str)
                    ctr = (v1 + v2) / 2
                    anch = abs(v2 - v1) * 2
                    if anch < 2: anch = 10
                    a_plot, b_plot = ctr - anch, ctr + anch
                elif metodo == "Newton-Raphson" and a_str:
                    v1 = parse_valor(a_str)
                    a_plot, b_plot = v1 - 5, v1 + 5
            except: pass
            
            if hasattr(self, 'ventana_grafica') and self.ventana_grafica is not None:
                if self.ventana_grafica.winfo_exists():
                    self.ventana_grafica.destroy()

            self.ventana_grafica = ctk.CTkToplevel(self)
            self.ventana_grafica.title(f"Gráfica: {funcion_raw}")
            self.ventana_grafica.geometry("1000x700")
            self.ventana_grafica.lift() 
            self.ventana_grafica.attributes('-topmost', True)
            self.ventana_grafica.after(100, lambda: self.ventana_grafica.attributes('-topmost', False))

            fig = Figure(figsize=(10, 8), dpi=100)
            ax = fig.add_subplot(111)

            x_sym = sp.Symbol('x')
            funcion_sympy = sp.sympify(funcion_str)
            f_lamb = sp.lambdify(x_sym, funcion_sympy, modules=['numpy', 'math'])
            
            x_vals = np.linspace(a_plot, b_plot, 2000)
            y_vals = f_lamb(x_vals)
            if isinstance(y_vals, (int, float)): y_vals = np.full_like(x_vals, y_vals)
            
            ax.plot(x_vals, y_vals, color='#2196F3', linewidth=2.5, label=f'f(x)')
            ax.axhline(0, color='black', linewidth=1.5, alpha=0.7)
            ax.axvline(0, color='black', linewidth=1.5, alpha=0.7)
            ax.grid(True, linestyle='--', alpha=0.5)
            
            ax.set_title(f"Análisis Gráfico: {funcion_raw}", fontsize=14, fontweight='bold', pad=15)
            ax.set_xlabel("Eje X", fontsize=11)
            ax.set_ylabel("f(x)", fontsize=11)

            try:
                if metodo != "Newton-Raphson" and a_str and b_str:
                    va, vb = parse_valor(a_str), parse_valor(b_str)
                    ax.axvline(va, color='#F44336', linestyle='--', linewidth=1.5, label='a')
                    ax.axvline(vb, color='#4CAF50', linestyle='--', linewidth=1.5, label='b')
                    ax.axvspan(min(va, vb), max(va, vb), alpha=0.1, color='gray')
                elif metodo == "Newton-Raphson" and a_str:
                    vx = parse_valor(a_str)
                    ax.plot(vx, f_lamb(vx), 'ro', markersize=8, label='x0', zorder=5)
            except: pass
            
            try:
                self.resultado_caja.configure(state="normal")
                contenido = self.resultado_caja.get('1.0', 'end')
                self.resultado_caja.configure(state="disabled")
                if "Raíz Aproximada:" in contenido:
                    linea_raiz = [l for l in contenido.split('\n') if "Raíz Aproximada:" in l][0]
                    raiz_val = float(linea_raiz.split(':')[1].strip())
                    if a_plot <= raiz_val <= b_plot:
                        f_raiz = float(f_lamb(raiz_val))
                        ax.plot(raiz_val, f_raiz, 'yo', markersize=10, markeredgecolor='black', label='Raíz', zorder=10)
                        ax.annotate(f"{raiz_val:.4f}", (raiz_val, f_raiz), xytext=(10, 20), 
                                   textcoords='offset points', arrowprops=dict(arrowstyle="->"))
            except: pass

            ax.legend(loc='best', shadow=True)

            canvas = FigureCanvasTkAgg(fig, self.ventana_grafica)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

            marco_botones = ctk.CTkFrame(self.ventana_grafica)
            marco_botones.pack(fill="x", padx=10, pady=(0, 10))

            def guardar_imagen():
                archivo = filedialog.asksaveasfilename(defaultextension=".png", 
                                                     filetypes=[("PNG", "*.png"), ("PDF", "*.pdf")],
                                                     title="Guardar Gráfica")
                if archivo: fig.savefig(archivo, dpi=300)

            ctk.CTkButton(marco_botones, text="Guardar Imagen", command=guardar_imagen,
                         fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).pack(side="left", padx=5)
            
            ctk.CTkButton(marco_botones, text="Cerrar", command=self.ventana_grafica.destroy,
                         fg_color="#F44336", hover_color="#D32F2F").pack(side="right", padx=5)

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
        self.ent_tolerancia_e.insert(0, "0.0001") 
        self._limpiar_pasos_scroll()
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete('0.0', 'end')
        self.resultado_caja.configure(state="disabled")
            
    def mostrar(self):
        self.grid(row=0, column=0, sticky="nsew")