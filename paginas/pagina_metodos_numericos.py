import customtkinter as ctk
from paginas.pagina_base import PaginaBase
from app_config import COLOR_FONDO_SECUNDARIO, COLOR_NUMERICOS, COLOR_HOVER, COLOR_BOTON_SECUNDARIO, COLOR_BOTON_SECUNDARIO_HOVER
from app_config import parse_valor, fmt
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sympy as sp
import numpy as np

class PaginaMetodosNumericos(PaginaBase):
    def crear_widgets(self):
        self.configurar_grid()
        self.crear_interfaz()
    
    def configurar_grid(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def crear_interfaz(self):
        # Selector de Metodo
        marco_metodo = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_metodo.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        
        ctk.CTkLabel(marco_metodo, text="Metodo Numerico:", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=(12, 8), pady=12)
        
        self.metodo_numerico_var = ctk.StringVar(value="Biseccion")
        metodos = ["Biseccion"]
        
        for i, metodo in enumerate(metodos):
            rb = ctk.CTkRadioButton(marco_metodo, text=metodo, variable=self.metodo_numerico_var, 
                                   value=metodo, font=ctk.CTkFont(size=13))
            rb.grid(row=0, column=i+1, padx=8, pady=12)

        # Entrada de Funcion
        marco_funcion = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_funcion.grid(row=1, column=0, sticky="ew", padx=12, pady=(4, 8))
        marco_funcion.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_funcion, text="Funcion f(x) =", font=ctk.CTkFont(size=13)).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.ent_funcion_fx = ctk.CTkEntry(marco_funcion, placeholder_text="Ej: cos(x) - x  (usar 'x' como variable)")
        self.ent_funcion_fx.grid(row=0, column=1, columnspan=5, sticky="ew", padx=8, pady=6)
        
        # Fila 1: Intervalo y Tolerancia
        ctk.CTkLabel(marco_funcion, text="Intervalo [a, b]:", font=ctk.CTkFont(size=13)).grid(row=1, column=0, sticky="w", padx=8, pady=6)
        self.ent_intervalo_a = ctk.CTkEntry(marco_funcion, width=100, placeholder_text="a")
        self.ent_intervalo_a.grid(row=1, column=1, sticky="w", padx=(8,2), pady=6)
        self.ent_intervalo_b = ctk.CTkEntry(marco_funcion, width=100, placeholder_text="b")
        self.ent_intervalo_b.grid(row=1, column=2, sticky="w", padx=(2,8), pady=6)
        
        ctk.CTkLabel(marco_funcion, text="Tolerancia (E):", font=ctk.CTkFont(size=13)).grid(row=1, column=3, sticky="w", padx=(20, 2), pady=6)
        self.ent_tolerancia_e = ctk.CTkEntry(marco_funcion, width=100, placeholder_text="Ej: 0.0001")
        self.ent_tolerancia_e.grid(row=1, column=4, sticky="w", padx=(2, 8), pady=6)
        
        # Ejemplos
        marco_ejemplos = ctk.CTkFrame(self)
        marco_ejemplos.grid(row=2, column=0, sticky="ew", padx=12, pady=4)
        ctk.CTkLabel(marco_ejemplos, text="Cargar ejemplos:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=(4,6))
        
        from functools import partial
        ctk.CTkButton(marco_ejemplos, text="Ej 1: cos(x)-x", command=partial(self.cargar_ejemplo_biseccion, 1),
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, width=120).grid(row=0, column=1, padx=4)
        ctk.CTkButton(marco_ejemplos, text="Ej 2: log(x)-exp(-x)", command=partial(self.cargar_ejemplo_biseccion, 2),
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, width=120).grid(row=0, column=2, padx=4)
        ctk.CTkButton(marco_ejemplos, text="Ej 3: x**2 + 4", command=partial(self.cargar_ejemplo_biseccion, 3),
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, width=120).grid(row=0, column=3, padx=4)

        # Controles
        marco_controles = ctk.CTkFrame(self)
        marco_controles.grid(row=3, column=0, sticky="ew", padx=12, pady=(6,12))
        
        ctk.CTkButton(marco_controles, text="Calcular", command=self.calcular_operacion_numerica,
                      fg_color=COLOR_NUMERICOS, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        
        ctk.CTkButton(marco_controles, text="Limpiar", command=self.limpiar_numerico,
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=1, padx=6)

        # Botón para graficar función
        ctk.CTkButton(marco_controles, text="Graficar Funcion", command=self.graficar_funcion_interna,
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=2, padx=6)

        # Resultados
        marco_resultados = ctk.CTkFrame(self)
        marco_resultados.grid(row=4, column=0, sticky="nsew", padx=12, pady=(6,12))
        marco_resultados.grid_rowconfigure(0, weight=1)
        marco_resultados.grid_columnconfigure(0, weight=2)
        marco_resultados.grid_columnconfigure(1, weight=1)
        
        # Pasos
        marco_pasos = ctk.CTkFrame(marco_resultados)
        marco_pasos.grid(row=0, column=0, sticky="nswe", padx=(0,6))
        marco_pasos.grid_columnconfigure(0, weight=1)
        marco_pasos.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_pasos, text="Bitacora Paso a Paso", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        
        self.pasos_caja = ctk.CTkTextbox(marco_pasos, height=220, font=ctk.CTkFont(family="monospace", size=12), wrap="none")
        self.pasos_caja.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))
        
        # Resultado
        marco_resultado = ctk.CTkFrame(marco_resultados)
        marco_resultado.grid(row=0, column=1, sticky="nswe", padx=(6,0))
        marco_resultado.grid_columnconfigure(0, weight=1)
        marco_resultado.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_resultado, text="Resultado Final", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        
        self.resultado_caja = ctk.CTkTextbox(marco_resultado, height=220, font=ctk.CTkFont(family="monospace", size=12))
        self.resultado_caja.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))

    def cargar_ejemplo_biseccion(self, ej_num: int):
        self.limpiar_numerico()
        
        if ej_num == 1:
            self.ent_funcion_fx.insert(0, "cos(x) - x")
            self.ent_intervalo_a.insert(0, "0")
            self.ent_intervalo_b.insert(0, "1")
            self.ent_tolerancia_e.insert(0, "0.0001")
        elif ej_num == 2:
            self.ent_funcion_fx.insert(0, "log(x) - exp(-x)")
            self.ent_intervalo_a.insert(0, "0.5")
            self.ent_intervalo_b.insert(0, "2")
            self.ent_tolerancia_e.insert(0, "0.0001")
        elif ej_num == 3:
            self.ent_funcion_fx.insert(0, "x**2 + 4")
            self.ent_intervalo_a.insert(0, "-2")
            self.ent_intervalo_b.insert(0, "2")
            self.ent_tolerancia_e.insert(0, "0.0001")

    def calcular_operacion_numerica(self):
        try:
            # Importar modulo de metodos numericos
            try:
                from MetodosNumericos import metodo_biseccion
            except ImportError:
                self.resultado_caja.delete('0.0', 'end')
                self.resultado_caja.insert('0.0', "ERROR: No se pudo cargar MetodosNumericos.py.")
                return

            metodo = self.metodo_numerico_var.get()
            
            if metodo == 'Biseccion':
                try:
                    funcion_str = self.ent_funcion_fx.get()
                    a_str = self.ent_intervalo_a.get()
                    b_str = self.ent_intervalo_b.get()
                    tol_str = self.ent_tolerancia_e.get()
                    
                    if not funcion_str or not a_str or not b_str or not tol_str:
                        raise ValueError("Todos los campos son obligatorios.")
                    
                    a = parse_valor(a_str)
                    b = parse_valor(b_str)
                    tolerancia = parse_valor(tol_str)
                    
                    if tolerancia <= 0:
                        raise ValueError("La tolerancia debe ser un numero positivo.")
                    if a >= b:
                        raise ValueError("El intervalo es invalido (a debe ser menor que b).")

                    res = metodo_biseccion(funcion_str, a, b, tolerancia)
                    
                    self.pasos_caja.delete('0.0', 'end')
                    self.pasos_caja.insert('0.0', '\n'.join(res.get('pasos', ['No se generaron pasos.'])))
                    
                    self.resultado_caja.delete('0.0', 'end')
                    if res['estado'] == 'exito':
                        resultado_txt = (
                            f"Raiz encontrada (xr):\n{res['raiz']:.10f}\n\n"
                            f"Iteraciones: {res['iteraciones']}\n"
                            f"Error relativo final: {res.get('error', 'N/A'):.6e}"
                        )
                        self.resultado_caja.insert('0.0', resultado_txt)
                    elif res['estado'] == 'max_iter':
                        resultado_txt = (
                            f"Se alcanzo el maximo de iteraciones.\n\n"
                            f"Ultima aproximacion (xr):\n{res['raiz']:.10f}\n\n"
                            f"Ultimo error: {res.get('error', 'N/A'):.6e}"
                        )
                        self.resultado_caja.insert('0.0', resultado_txt)
                    else:
                        self.resultado_caja.insert('0.0', f"Error:\n{res['mensaje']}")

                except ValueError as e:
                    self.pasos_caja.delete('0.0', 'end')
                    self.resultado_caja.delete('0.0', 'end')
                    self.resultado_caja.insert('0.0', f"Error de entrada:\n{e}")
                except Exception as e:
                    self.pasos_caja.delete('0.0', 'end')
                    self.resultado_caja.delete('0.0', 'end')
                    self.resultado_caja.insert('0.0', f"Error inesperado en el calculo:\n{e}")

        except Exception as e:
            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', f"Error general: {e}")

    def graficar_funcion_interna(self):
        """Grafica función usando sympy."""
        try:
            funcion_str = self.ent_funcion_fx.get()
            if not funcion_str:
                raise ValueError("El campo de la función está vacío.")

            a_str = self.ent_intervalo_a.get()
            b_str = self.ent_intervalo_b.get()
            
            a = -10 if not a_str else parse_valor(a_str)
            b = 10 if not b_str else parse_valor(b_str)
            
            if a >= b:
                raise ValueError("El intervalo es inválido (a debe ser menor que b).")

            ventana_grafica = ctk.CTkToplevel(self)
            ventana_grafica.title(f"Gráfica de f(x) = {funcion_str}")
            ventana_grafica.geometry("1000x700")
            ventana_grafica.transient(self)
            ventana_grafica.grab_set()

            ventana_grafica.grid_rowconfigure(0, weight=1)
            ventana_grafica.grid_columnconfigure(0, weight=1)

            fig = Figure(figsize=(10, 8), dpi=100)
            ax = fig.add_subplot(111)

            try:
                x_sym = sp.Symbol('x')
                funcion_sympy = sp.sympify(funcion_str.replace('^', '**'))
                funcion_lambdified = sp.lambdify(x_sym, funcion_sympy, modules=['numpy', 'math'])
                
                x = np.linspace(a, b, 2000)
                y = funcion_lambdified(x)
                
                ax.plot(x, y, 'b-', linewidth=2.5, label=f'f(x) = {funcion_str}', alpha=0.8)
                ax.axhline(y=0, color='black', linewidth=1.5, alpha=0.7)
                ax.axvline(x=0, color='black', linewidth=1.5, alpha=0.7)
                ax.axvline(x=a, color='red', linestyle='--', alpha=0.6, linewidth=1, label=f'a = {a}')
                ax.axvline(x=b, color='green', linestyle='--', alpha=0.6, linewidth=1, label=f'b = {b}')
                ax.axvspan(a, b, alpha=0.1, color='gray', label='Intervalo de búsqueda')
                ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
                ax.set_axisbelow(True)
                ax.set_xlabel('x', fontsize=12, fontweight='bold')
                ax.set_ylabel('f(x)', fontsize=12, fontweight='bold')
                ax.set_title(f'Gráfica de f(x) = {funcion_str}\nIntervalo: [{a}, {b}]', 
                           fontsize=14, fontweight='bold', pad=20)
                ax.tick_params(axis='both', which='major', labelsize=10)
                
                y_min, y_max = np.nanmin(y), np.nanmax(y)
                y_range = y_max - y_min if y_max != y_min else 2
                ax.set_ylim(y_min - 0.1*y_range, y_max + 0.1*y_range)
                ax.legend(loc='best', fontsize=10, framealpha=0.9, shadow=True)
                
                # Intentar marcar raíz si existe en resultados
                contenido = self.resultado_caja.get('1.0', 'end-1c')
                if 'Raiz encontrada' in contenido:
                    lineas = contenido.split('\n')
                    for linea in lineas:
                        if 'Raiz encontrada' in contenido:
                            try:
                                for line in lineas:
                                    if 'Raiz encontrada' in line:
                                        raiz_str = line.split(':')[1].strip()
                                        raiz = float(raiz_str)
                                        f_raiz = float(funcion_sympy.subs(x_sym, raiz))
                                        ax.plot(raiz, f_raiz, 'ro', markersize=10, 
                                               label=f'Raíz ≈ {raiz:.6f}', zorder=5)
                                        ax.plot([raiz, raiz], [0, f_raiz], 'r--', alpha=0.7, linewidth=1)
                                        ax.annotate(f'x ≈ {raiz:.6f}', 
                                                   xy=(raiz, f_raiz), 
                                                   xytext=(10, 20), 
                                                   textcoords='offset points',
                                                   fontsize=10,
                                                   bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
                                                   arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0"))
                                        ax.legend(loc='best', fontsize=9)
                                        break
                            except:
                                pass

            except Exception as e:
                ax.text(0.5, 0.5, f'Error al graficar la función:\n\n{str(e)}', 
                       horizontalalignment='center', verticalalignment='center',
                       transform=ax.transAxes, fontsize=12, color='red',
                       bbox=dict(boxstyle="round,pad=1", facecolor="lightcoral", alpha=0.8))
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
                ax.set_title('Error en la gráfica', fontsize=14, fontweight='bold', color='red')

            canvas = FigureCanvasTkAgg(fig, ventana_grafica)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

            marco_controles = ctk.CTkFrame(ventana_grafica)
            marco_controles.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
            
            def guardar_imagen():
                from tkinter import filedialog
                archivo = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("All files", "*.*")],
                    title="Guardar gráfica como..."
                )
                if archivo:
                    try:
                        fig.savefig(archivo, dpi=300, bbox_inches='tight', facecolor='white')
                        self.resultado_caja.insert('0.0', f"\nGràfica guardada en: {archivo}")
                    except Exception as e:
                        self.resultado_caja.insert('0.0', f"\nError al guardar: {e}")

            ctk.CTkButton(marco_controles, text="Guardar Imagen", 
                         command=guardar_imagen,
                         fg_color=COLOR_BOTON_SECUNDARIO, 
                         hover_color=COLOR_BOTON_SECUNDARIO_HOVER).pack(side="left", padx=5)
            
            ctk.CTkButton(marco_controles, text="Cerrar", 
                         command=ventana_grafica.destroy,
                         fg_color=COLOR_NUMERICOS, hover_color=COLOR_HOVER).pack(side="right", padx=5)

        except ValueError as e:
            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', f"Error para graficar: {e}")
        except Exception as e:
            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', f"Error inesperado al crear la gráfica:\n{e}")

    def limpiar_numerico(self):
        if hasattr(self, 'ent_funcion_fx'):
            self.ent_funcion_fx.delete(0, 'end')
        if hasattr(self, 'ent_intervalo_a'):
            self.ent_intervalo_a.delete(0, 'end')
        if hasattr(self, 'ent_intervalo_b'):
            self.ent_intervalo_b.delete(0, 'end')
        if hasattr(self, 'ent_tolerancia_e'):
            self.ent_tolerancia_e.delete(0, 'end')
            
        if hasattr(self, 'pasos_caja'):
            self.pasos_caja.delete('0.0', 'end')
        if hasattr(self, 'resultado_caja'):
            self.resultado_caja.delete('0.0', 'end')

    def mostrar(self):
        self.grid(row=0, column=0, sticky="nsew")