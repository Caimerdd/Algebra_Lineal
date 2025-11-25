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

class PaginaMetodosNumericos(PaginaBase):
    def crear_widgets(self):
        self.configurar_grid()
        self.crear_interfaz()
        self._actualizar_entradas_metodo()
    
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
        metodos = ["Biseccion", "Falsa Posicion", "Newton-Raphson", "Secante"]
        
        for i, metodo in enumerate(metodos):
            rb = ctk.CTkRadioButton(marco_metodo, text=metodo, variable=self.metodo_numerico_var, 
                                   value=metodo, font=ctk.CTkFont(size=13),
                                   command=self._actualizar_entradas_metodo)
            rb.grid(row=0, column=i+1, padx=8, pady=12)

        # Entrada de Funcion
        marco_funcion = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_funcion.grid(row=1, column=0, sticky="ew", padx=12, pady=(4, 8))
        marco_funcion.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(marco_funcion, text="Funcion f(x) =", font=ctk.CTkFont(size=13)).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.ent_funcion_fx = ctk.CTkEntry(marco_funcion, placeholder_text="Ej: cos(x) - x  (usar 'x' como variable)")
        self.ent_funcion_fx.grid(row=0, column=1, columnspan=5, sticky="ew", padx=8, pady=6)
        
        # Fila 1: Entradas de Intervalo/Puntos
        self.lbl_intervalo = ctk.CTkLabel(marco_funcion, text="Intervalo [a, b]:", font=ctk.CTkFont(size=13))
        self.lbl_intervalo.grid(row=1, column=0, sticky="w", padx=8, pady=6)
        
        self.ent_intervalo_a = ctk.CTkEntry(marco_funcion, width=100, placeholder_text="a")
        self.ent_intervalo_a.grid(row=1, column=1, sticky="w", padx=(8,2), pady=6)
        
        self.ent_intervalo_b = ctk.CTkEntry(marco_funcion, width=100, placeholder_text="b")
        self.ent_intervalo_b.grid(row=1, column=2, sticky="w", padx=(2,8), pady=6)
        
        ctk.CTkLabel(marco_funcion, text="Tolerancia (E):", font=ctk.CTkFont(size=13)).grid(row=1, column=3, sticky="w", padx=(20, 2), pady=6)
        self.ent_tolerancia_e = ctk.CTkEntry(marco_funcion, width=100, placeholder_text="Ej: 0.0001")
        self.ent_tolerancia_e.insert(0, "0.0001")
        self.ent_tolerancia_e.grid(row=1, column=4, sticky="w", padx=(2, 8), pady=6)
        
        # Ejemplos
        marco_ejemplos = ctk.CTkFrame(self)
        marco_ejemplos.grid(row=2, column=0, sticky="ew", padx=12, pady=4)
        ctk.CTkLabel(marco_ejemplos, text="Cargar ejemplos:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=(4,6))
        
        ctk.CTkButton(marco_ejemplos, text="Ej 1: cos(x)-x", command=partial(self.cargar_ejemplo, 1),
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, width=120).grid(row=0, column=1, padx=4)
        ctk.CTkButton(marco_ejemplos, text="Ej 2: log(x)-exp(-x)", command=partial(self.cargar_ejemplo, 2),
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, width=120).grid(row=0, column=2, padx=4)
        ctk.CTkButton(marco_ejemplos, text="Ej 3: x**2 + 4", command=partial(self.cargar_ejemplo, 3),
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, width=120).grid(row=0, column=3, padx=4)

        # Controles
        marco_controles = ctk.CTkFrame(self)
        marco_controles.grid(row=3, column=0, sticky="ew", padx=12, pady=(6,12))
        
        ctk.CTkButton(marco_controles, text="Calcular", command=self.calcular_operacion_numerica,
                      fg_color=COLOR_NUMERICOS, hover_color=COLOR_HOVER).grid(row=0, column=0, padx=6)
        
        ctk.CTkButton(marco_controles, text="Limpiar", command=self.limpiar_numerico,
                      fg_color=COLOR_BOTON_SECUNDARIO, hover_color=COLOR_BOTON_SECUNDARIO_HOVER).grid(row=0, column=1, padx=6)

        ctk.CTkButton(marco_controles, text="Graficar Funcion", command=self.graficar_funcion_interna,
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
        
        ctk.CTkLabel(marco_pasos, text="Bitacora Paso a Paso", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        
        self.pasos_scroll_frame = ctk.CTkScrollableFrame(marco_pasos, fg_color=COLOR_FONDO_SECUNDARIO)
        self.pasos_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))
        self.pasos_scroll_frame.grid_columnconfigure(0, weight=1)
        
        # Resultado
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

    # --- NUEVAS FUNCIONES DE UI OPTIMIZADAS ---
    def _limpiar_pasos_scroll(self):
        """Elimina todos los widgets hijos del frame de pasos."""
        try:
            for widget in self.pasos_scroll_frame.winfo_children():
                widget.destroy()
        except Exception as e:
            print(f"Error al limpiar pasos: {e}")
            
    def _crear_bloque_texto(self, titulo: str, texto: str):
        """Crea un bloque de texto (título + cuerpo) en el frame de pasos."""
        try:
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
        except Exception as e:
            print(f"Error al crear bloque de texto: {e}")
            
    def _crear_tabla_pasos(self, headers: list, data: list):
        """Crea una tabla gráfica dentro del frame de pasos."""
        try:
            tabla_frame = ctk.CTkFrame(self.pasos_scroll_frame, fg_color=COLOR_FONDO_SECUNDARIO)
            tabla_frame.pack(fill="x", expand=True, pady=10)
            
            num_cols = len(headers)
            
            # --- Crear Encabezados ---
            for c, header in enumerate(headers):
                cell = ctk.CTkLabel(tabla_frame, text=header, 
                                    font=ctk.CTkFont(family="monospace", size=12, weight="bold"),
                                    text_color=COLOR_NUMERICOS[0])
                cell.grid(row=0, column=c, padx=8, pady=4, sticky="w")
                
            # --- Crear Filas de Datos ---
            for r, row_data in enumerate(data):
                for c, cell_data in enumerate(row_data):
                    # Formatear el dato
                    if isinstance(cell_data, float):
                        if abs(cell_data) > 1e4 or abs(cell_data) < 1e-3 and cell_data != 0:
                            texto = f"{cell_data:.4e}" # Científica
                        else:
                            texto = f"{cell_data:.6f}" # Decimal
                    else:
                        texto = str(cell_data)
                        
                    cell = ctk.CTkLabel(tabla_frame, text=texto, 
                                        font=ctk.CTkFont(family="monospace", size=12))
                    cell.grid(row=r + 1, column=c, padx=8, pady=2, sticky="w")
        except Exception as e:
            print(f"Error al crear tabla: {e}")
    
    # --- FUNCIONES MODIFICADAS Y OPTIMIZADAS ---
    def _actualizar_entradas_metodo(self):
        """Actualiza la interfaz según el método seleccionado."""
        try:
            metodo = self.metodo_numerico_var.get()
            if metodo in ["Biseccion", "Falsa Posicion"]:
                self.lbl_intervalo.configure(text="Intervalo [a, b]:")
                self.ent_intervalo_a.configure(placeholder_text="a")
                self.ent_intervalo_b.configure(placeholder_text="b")
                self.ent_intervalo_b.grid() 
            elif metodo == "Newton-Raphson":
                self.lbl_intervalo.configure(text="Punto Inicial (x0):")
                self.ent_intervalo_a.configure(placeholder_text="x0")
                self.ent_intervalo_b.grid_remove() 
            elif metodo == "Secante":
                self.lbl_intervalo.configure(text="Puntos [x0, x1]:")
                self.ent_intervalo_a.configure(placeholder_text="x0")
                self.ent_intervalo_b.configure(placeholder_text="x1")
                self.ent_intervalo_b.grid() 
        except Exception as e:
            print(f"Error al actualizar entradas: {e}")

    def cargar_ejemplo(self, ej_num: int):
        """Carga ejemplos predefinidos en la interfaz."""
        try:
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
                
            # Actualizar UI según el método
            self._actualizar_entradas_metodo()
            
        except Exception as e:
            print(f"Error al cargar ejemplo: {e}")

    def calcular_operacion_numerica(self):
        """Ejecuta el método numérico seleccionado."""
        self._limpiar_pasos_scroll()
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete('0.0', 'end')
        
        try:
            from MetodosNumericos import (
                metodo_biseccion, metodo_falsa_posicion, 
                metodo_newton_raphson, metodo_secante
            )
        except ImportError:
            self.resultado_caja.insert('0.0', "ERROR: No se pudo cargar MetodosNumericos.py.")
            self.resultado_caja.configure(state="disabled")
            return

        metodo = self.metodo_numerico_var.get()
        
        try:
            funcion_str = self.ent_funcion_fx.get().strip()
            tol_str = self.ent_tolerancia_e.get().strip()
            
            if not funcion_str:
                raise ValueError("La función no puede estar vacía.")
            if not tol_str:
                raise ValueError("La tolerancia no puede estar vacía.")
            
            tolerancia = parse_valor(tol_str)
            if tolerancia <= 0: 
                raise ValueError("La tolerancia debe ser un numero positivo.")

            res = None
            
            if metodo == 'Biseccion' or metodo == 'Falsa Posicion':
                a_str, b_str = self.ent_intervalo_a.get().strip(), self.ent_intervalo_b.get().strip()
                if not a_str or not b_str: 
                    raise ValueError("Los campos 'a' y 'b' son obligatorios.")
                a, b = parse_valor(a_str), parse_valor(b_str)
                if a >= b: 
                    raise ValueError("El intervalo es invalido (a debe ser menor que b).")
                res = metodo_biseccion(funcion_str, a, b, tolerancia) if metodo == 'Biseccion' else metodo_falsa_posicion(funcion_str, a, b, tolerancia)
            
            elif metodo == 'Newton-Raphson':
                x0_str = self.ent_intervalo_a.get().strip()
                if not x0_str: 
                    raise ValueError("El punto inicial 'x0' es obligatorio.")
                x0 = parse_valor(x0_str)
                res = metodo_newton_raphson(funcion_str, x0, tolerancia)

            elif metodo == 'Secante':
                x0_str, x1_str = self.ent_intervalo_a.get().strip(), self.ent_intervalo_b.get().strip()
                if not x0_str or not x1_str: 
                    raise ValueError("Los puntos 'x0' y 'x1' son obligatorios.")
                x0, x1 = parse_valor(x0_str), parse_valor(x1_str)
                if x0 == x1: 
                    raise ValueError("Los puntos iniciales no pueden ser iguales.")
                res = metodo_secante(funcion_str, x0, x1, tolerancia)

            # --- RENDERIZADO DE RESULTADOS OPTIMIZADO ---
            
            # 1. Mostrar info previa (si existe)
            if res.get('info_previa'):
                self._crear_bloque_texto("DATOS INICIALES", "\n".join(res['info_previa']))
            
            # 2. Mostrar la tabla (si existe)
            if res.get('tabla_headers') and res.get('tabla_data'):
                self._crear_tabla_pasos(res['tabla_headers'], res['tabla_data'])

            # 3. Mostrar mensaje final de la tabla (si existe)
            if res.get('mensaje_final'):
                self._crear_bloque_texto("RESULTADO DE ITERACIÓN", res['mensaje_final'])

            # 4. Mostrar resultado final o error
            if res['estado'] == 'exito':
                resultado_txt = (
                    f"Raíz (xr):   {res['raiz']:.10f}\n"
                    f"Iteraciones: {res['iteraciones']}\n"
                    f"Error final: {res.get('error', 'N/A'):.6e}"
                )
                self.resultado_caja.insert('0.0', resultado_txt)
            else:
                self.resultado_caja.insert('0.0', f"Error:\n{res['mensaje']}")

        except ValueError as e:
            self.resultado_caja.insert('0.0', f"Error de entrada:\n{e}")
        except Exception as e:
            self.resultado_caja.insert('0.0', f"Error inesperado en el calculo:\n{e}")
            
        self.resultado_caja.configure(state="disabled")

    def graficar_funcion_interna(self):
        """Muestra la gráfica de la función actual."""
        try:
            funcion_str = self.ent_funcion_fx.get().strip()
            if not funcion_str:
                raise ValueError("El campo de la función está vacío.")

            a_str = self.ent_intervalo_a.get().strip()
            b_str = self.ent_intervalo_b.get().strip()
            metodo = self.metodo_numerico_var.get()
            
            a, b = -10, 10  # Valores por defecto
            
            try:
                if metodo in ["Biseccion", "Falsa Posicion", "Secante"] and a_str and b_str:
                    a = parse_valor(a_str)
                    b = parse_valor(b_str)
                    if a > b: 
                        a, b = b, a  # Asegurar orden correcto
                elif metodo == "Newton-Raphson" and a_str:
                    x0 = parse_valor(a_str)
                    a = x0 - 5  # Margen alrededor de x0
                    b = x0 + 5
            except:
                pass  # Usar valores por defecto si hay error
            
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
                
                if metodo in ["Biseccion", "Falsa Posicion", "Secante"] and a_str and b_str:
                    a_val = parse_valor(a_str)
                    b_val = parse_valor(b_str)
                    ax.axvline(x=a_val, color='red', linestyle='--', alpha=0.6, linewidth=1, label=f'a/x0 = {a_val}')
                    ax.axvline(x=b_val, color='green', linestyle='--', alpha=0.6, linewidth=1, label=f'b/x1 = {b_val}')
                    ax.axvspan(min(a_val, b_val), max(a_val, b_val), alpha=0.1, color='gray', label='Intervalo inicial')
                elif metodo == "Newton-Raphson" and a_str:
                    x0_val = parse_valor(a_str)
                    ax.axvline(x=x0_val, color='red', linestyle='--', alpha=0.6, linewidth=1, label=f'x0 = {x0_val}')
                
                ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
                ax.set_axisbelow(True)
                ax.set_xlabel('x', fontsize=12, fontweight='bold')
                ax.set_ylabel('f(x)', fontsize=12, fontweight='bold')
                ax.set_title(f'Gráfica de f(x) = {funcion_str}\nRango de ploteo: [{a:.2f}, {b:.2f}]', 
                           fontsize=14, fontweight='bold', pad=20)
                ax.tick_params(axis='both', which='major', labelsize=10)
                
                y_clean = y[np.isfinite(y)]
                if len(y_clean) > 0:
                    y_min, y_max = np.nanmin(y_clean), np.nanmax(y_clean)
                    y_range = y_max - y_min if y_max != y_min else 2
                    ax.set_ylim(y_min - 0.1*y_range, y_max + 0.1*y_range)
                
                ax.legend(loc='best', fontsize=10, framealpha=0.9, shadow=True)
                
                # Mostrar raíz si está disponible en resultados
                self.resultado_caja.configure(state="normal")
                contenido = self.resultado_caja.get('1.0', 'end-1c')
                self.resultado_caja.configure(state="disabled")
                
                if 'Raíz (xr)' in contenido:
                    lineas = contenido.split('\n')
                    try:
                        raiz_str = lineas[0].split(':')[-1].strip()
                        raiz = float(raiz_str)
                        if a <= raiz <= b: 
                            f_raiz = float(funcion_lambdified(raiz))
                            ax.plot(raiz, f_raiz, 'ro', markersize=10, 
                                   label=f'Raíz ≈ {raiz:.6f}', zorder=5)
                            ax.annotate(f'x ≈ {raiz:.6f}', 
                                       xy=(raiz, f_raiz), xytext=(10, 20), 
                                       textcoords='offset points', fontsize=10,
                                       bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
                                       arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0"))
                            ax.legend(loc='best', fontsize=9)
                    except:
                        pass  # No mostrar raíz si hay error

            except Exception as e:
                ax.text(0.5, 0.5, f'Error al graficar la función:\n\n{str(e)}', 
                       horizontalalignment='center', verticalalignment='center',
                       transform=ax.transAxes, fontsize=12, color='red',
                       bbox=dict(boxstyle="round,pad=1", facecolor="lightcoral", alpha=0.8))

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
                        self.resultado_caja.configure(state="normal")
                        self.resultado_caja.insert('end', f"\nGráfica guardada correctamente.")
                        self.resultado_caja.configure(state="disabled")
                    except Exception as e:
                        self.resultado_caja.configure(state="normal")
                        self.resultado_caja.insert('end', f"\nError al guardar: {e}")
                        self.resultado_caja.configure(state="disabled")

            ctk.CTkButton(marco_controles, text="Guardar Imagen", 
                         command=guardar_imagen,
                         fg_color=COLOR_BOTON_SECUNDARIO, 
                         hover_color=COLOR_BOTON_SECUNDARIO_HOVER).pack(side="left", padx=5)
            
            ctk.CTkButton(marco_controles, text="Cerrar", 
                         command=ventana_grafica.destroy,
                         fg_color=COLOR_NUMERICOS, hover_color=COLOR_HOVER).pack(side="right", padx=5)

        except ValueError as e:
            self.resultado_caja.configure(state="normal")
            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', f"Error para graficar: {e}")
            self.resultado_caja.configure(state="disabled")
        except Exception as e:
            self.resultado_caja.configure(state="normal")
            self.resultado_caja.delete('0.0', 'end')
            self.resultado_caja.insert('0.0', f"Error inesperado al crear la gráfica:\n{e}")
            self.resultado_caja.configure(state="disabled")

    def limpiar_numerico(self):
        """Limpia completamente la interfaz de métodos numéricos - VERSIÓN CORREGIDA"""
        try:
            # Limpiar campos de entrada
            if hasattr(self, 'ent_funcion_fx'):
                self.ent_funcion_fx.delete(0, 'end')
            
            if hasattr(self, 'ent_intervalo_a'):
                self.ent_intervalo_a.delete(0, 'end')
            
            if hasattr(self, 'ent_intervalo_b'):
                self.ent_intervalo_b.delete(0, 'end')
                
            # Restablecer tolerancia por defecto
            if hasattr(self, 'ent_tolerancia_e'):
                self.ent_tolerancia_e.delete(0, 'end')
                self.ent_tolerancia_e.insert(0, "0.0001")
            
            # Restablecer método por defecto y actualizar UI
            if hasattr(self, 'metodo_numerico_var'):
                self.metodo_numerico_var.set("Biseccion")
                self._actualizar_entradas_metodo()
            
            # Limpiar resultados
            if hasattr(self, 'resultado_caja'):
                self.resultado_caja.configure(state="normal")
                self.resultado_caja.delete('0.0', 'end')
                self.resultado_caja.configure(state="disabled")
            
            # Limpiar bitácora de pasos
            if hasattr(self, 'pasos_scroll_frame'):
                self._limpiar_pasos_scroll()
                
        except Exception as e:
            print(f"Error al limpiar interfaz numérica: {e}")

    def mostrar(self):
        self.grid(row=0, column=0, sticky="nsew")