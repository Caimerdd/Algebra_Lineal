import customtkinter as ctk
from paginas.pagina_base import PaginaBase
from app_config import (
    COLOR_FONDO_SECUNDARIO,
    COLOR_DIFERENCIAL,
    COLOR_HOVER,
    COLOR_BOTON_SECUNDARIO,
    COLOR_BOTON_SECUNDARIO_HOVER,
    parse_valor,
)

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import sympy as sp
import numpy as np

# Importamos la lógica de Cálculo Diferencial
try:
    from LogicaDiferencial import (
        calcular_limite_en_punto,
        derivada_fx,
        derivada_orden_n,
        recta_tangente_y_normal,
        tasa_cambio_promedio_e_instantanea,
    )
    LOGICA_DIFERENCIAL_DISPONIBLE = True
    print("✅ LogicaDiferencial.py cargado correctamente")
except Exception as e:
    LOGICA_DIFERENCIAL_DISPONIBLE = False
    print(f"❌ Error cargando LogicaDiferencial.py: {e}")


class PaginaDiferencial(PaginaBase):
    def crear_widgets(self):
        self.configurar_grid()

        # Selector de operación
        marco_metodo = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_metodo.grid(row=0, column=0, sticky="ew", padx=12, pady=8)

        ctk.CTkLabel(
            marco_metodo,
            text="Operación:",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).grid(row=0, column=0, padx=(12, 8), pady=12)

        self.operacion_var = ctk.StringVar(value="Límite en un punto")
        operaciones = [
            "Límite en un punto",
            "Derivada de f(x)",
            "Derivada de orden n",
            "Recta tangente y normal",
            "Tasa de cambio promedio e instantánea",
        ]

        for i, op in enumerate(operaciones):
            rb = ctk.CTkRadioButton(
                marco_metodo,
                text=op,
                variable=self.operacion_var,
                value=op,
                font=ctk.CTkFont(size=13),
                command=self._actualizar_ui_operacion,
            )
            rb.grid(row=0, column=i + 1, padx=8, pady=12)

        # Entradas de datos
        marco_entradas = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO)
        marco_entradas.grid(row=1, column=0, sticky="ew", padx=12, pady=(4, 8))
        marco_entradas.grid_columnconfigure(1, weight=1)
        marco_entradas.grid_columnconfigure(2, weight=0)

        self.lbl_fx = ctk.CTkLabel(
            marco_entradas, text="f(x) =", font=ctk.CTkFont(size=13)
        )
        self.lbl_fx.grid(row=0, column=0, sticky="w", padx=8, pady=6)

        self.ent_fx = ctk.CTkEntry(
            marco_entradas,
            placeholder_text="Ej: x^2 + 3*x - 4  (usar 'x' como variable)",
        )
        self.ent_fx.grid(row=0, column=1, columnspan=2, sticky="ew", padx=8, pady=6)

        self.lbl_extra = ctk.CTkLabel(
            marco_entradas,
            text="",
            font=ctk.CTkFont(size=13),
        )
        self.ent_extra1 = ctk.CTkEntry(marco_entradas, width=120)
        self.ent_extra2 = ctk.CTkEntry(marco_entradas, width=120)

        self.lbl_extra.grid(row=1, column=0, sticky="w", padx=8, pady=6)
        self.ent_extra1.grid(row=1, column=1, sticky="w", padx=(8, 4), pady=6)
        self.ent_extra2.grid(row=1, column=2, sticky="w", padx=(4, 8), pady=6)

        # Controles
        marco_controles = ctk.CTkFrame(self)
        marco_controles.grid(row=2, column=0, sticky="ew", padx=12, pady=(6, 12))

        ctk.CTkButton(
            marco_controles,
            text="Calcular",
            command=self.calcular,
            fg_color=COLOR_DIFERENCIAL[0],
            hover_color=COLOR_HOVER,
        ).grid(row=0, column=0, padx=6)

        ctk.CTkButton(
            marco_controles,
            text="Limpiar",
            command=self.limpiar,
            fg_color=COLOR_BOTON_SECUNDARIO,
            hover_color=COLOR_BOTON_SECUNDARIO_HOVER,
        ).grid(row=0, column=1, padx=6)

        ctk.CTkButton(
            marco_controles,
            text="Ver gráfica",
            command=self.graficar_funcion_diferencial,
            fg_color=COLOR_BOTON_SECUNDARIO,
            hover_color=COLOR_BOTON_SECUNDARIO_HOVER,
        ).grid(row=0, column=2, padx=6)

        # Resultados
        marco_resultados = ctk.CTkFrame(self)
        marco_resultados.grid(row=3, column=0, sticky="nsew", padx=12, pady=(6, 12))
        marco_resultados.grid_rowconfigure(0, weight=1)
        marco_resultados.grid_columnconfigure(0, weight=2)
        marco_resultados.grid_columnconfigure(1, weight=1)

        marco_pasos = ctk.CTkFrame(marco_resultados)
        marco_pasos.grid(row=0, column=0, sticky="nswe", padx=(0, 6))
        marco_pasos.grid_columnconfigure(0, weight=1)
        marco_pasos.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            marco_pasos,
            text="Bitácora Paso a Paso (Cálculo Diferencial)",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=8, pady=6)

        self.pasos_scroll_frame = ctk.CTkScrollableFrame(
            marco_pasos, fg_color=COLOR_FONDO_SECUNDARIO
        )
        self.pasos_scroll_frame.grid(
            row=1, column=0, sticky="nsew", padx=8, pady=(0, 8)
        )
        self.pasos_scroll_frame.grid_columnconfigure(0, weight=1)

        marco_resultado = ctk.CTkFrame(marco_resultados)
        marco_resultado.grid(row=0, column=1, sticky="nswe", padx=(6, 0))
        marco_resultado.grid_columnconfigure(0, weight=1)
        marco_resultado.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            marco_resultado,
            text="Resultado Final",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=8, pady=6)

        self.resultado_caja = ctk.CTkTextbox(
            marco_resultado,
            height=220,
            font=ctk.CTkFont(family="monospace", size=14, weight="bold"),
            border_color=COLOR_DIFERENCIAL[1],
            border_width=2,
            wrap="none",
        )
        self.resultado_caja.grid(
            row=1, column=0, sticky="nsew", padx=8, pady=(0, 8)
        )
        self.resultado_caja.configure(state="disabled")

        self._actualizar_ui_operacion()

    def configurar_grid(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _limpiar_pasos_scroll(self):
        for widget in self.pasos_scroll_frame.winfo_children():
            widget.destroy()

    def _crear_bloque_paso(self, titulo: str, math: str):
        paso_frame = ctk.CTkFrame(self.pasos_scroll_frame, fg_color="transparent")
        paso_frame.pack(fill="x", pady=(0, 15))

        lbl_titulo = ctk.CTkLabel(
            paso_frame,
            text=titulo.upper(),
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLOR_DIFERENCIAL[0],
        )
        lbl_titulo.pack(anchor="w", padx=5)

        lbl_math = ctk.CTkLabel(
            paso_frame,
            text=math,
            font=ctk.CTkFont(family="monospace", size=14),
            justify="left",
            anchor="w",
        )
        lbl_math.pack(anchor="w", padx=10, pady=(2, 0))

    def _renderizar_pasos(self, pasos):
        self._limpiar_pasos_scroll()
        for paso in pasos or []:
            titulo = paso.get("titulo", "Paso")
            math = paso.get("math", "")
            self._crear_bloque_paso(titulo, math)

    def _actualizar_ui_operacion(self):
        op = self.operacion_var.get()

        if op == "Límite en un punto":
            self.lbl_extra.configure(text="x →")
            self.lbl_extra.grid()
            self.ent_extra1.grid()
            self.ent_extra2.grid_remove()

            self.ent_extra1.delete(0, "end")
            self.ent_extra2.delete(0, "end")
            self.ent_extra1.configure(placeholder_text="Ej: 1")

        elif op == "Derivada de f(x)":
            self.lbl_extra.grid_remove()
            self.ent_extra1.grid_remove()
            self.ent_extra2.grid_remove()

        elif op == "Derivada de orden n":
            self.lbl_extra.configure(text="Orden n =")
            self.lbl_extra.grid()
            self.ent_extra1.grid()
            self.ent_extra2.grid_remove()

            self.ent_extra1.delete(0, "end")
            self.ent_extra2.delete(0, "end")
            self.ent_extra1.configure(placeholder_text="Ej: 2")

        elif op == "Recta tangente y normal":
            self.lbl_extra.configure(text="Punto x₀ =")
            self.lbl_extra.grid()
            self.ent_extra1.grid()
            self.ent_extra2.grid_remove()

            self.ent_extra1.delete(0, "end")
            self.ent_extra2.delete(0, "end")
            self.ent_extra1.configure(placeholder_text="Ej: 1")

        elif op == "Tasa de cambio promedio e instantánea":
            self.lbl_extra.configure(text="Intervalo [a, b] =")
            self.lbl_extra.grid()
            self.ent_extra1.grid()
            self.ent_extra2.grid()

            self.ent_extra1.delete(0, "end")
            self.ent_extra2.delete(0, "end")
            self.ent_extra1.configure(placeholder_text="a")
            self.ent_extra2.configure(placeholder_text="b")

    def limpiar(self):
        self.ent_fx.delete(0, "end")
        self.ent_extra1.delete(0, "end")
        self.ent_extra2.delete(0, "end")
        self._limpiar_pasos_scroll()

        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete("0.0", "end")
        self.resultado_caja.configure(state="disabled")

        self.ent_fx.configure(
            placeholder_text="Ej: x^2 + 3*x - 4  (usar 'x' como variable)"
        )
        self._actualizar_ui_operacion()

    def calcular(self):
        self._limpiar_pasos_scroll()
        self.resultado_caja.configure(state="normal")
        self.resultado_caja.delete("0.0", "end")

        if not LOGICA_DIFERENCIAL_DISPONIBLE:
            self.resultado_caja.insert(
                "0.0",
                "Error: No se pudo cargar 'LogicaDiferencial.py'.\n"
                "Revisa que el archivo exista en la misma carpeta que main.py.",
            )
            self.resultado_caja.configure(state="disabled")
            return

        op = self.operacion_var.get()
        fx = self.ent_fx.get().strip()
        extra1 = self.ent_extra1.get().strip()
        extra2 = self.ent_extra2.get().strip()

        if not fx:
            self.resultado_caja.insert(
                "0.0", "Error de entrada:\nLa función f(x) no puede estar vacía."
            )
            self.resultado_caja.configure(state="disabled")
            return

        try:
            if op == "Límite en un punto":
                res = calcular_limite_en_punto(fx, extra1 or "")
            elif op == "Derivada de f(x)":
                res = derivada_fx(fx)
            elif op == "Derivada de orden n":
                res = derivada_orden_n(fx, extra1 or "")
            elif op == "Recta tangente y normal":
                res = recta_tangente_y_normal(fx, extra1 or "")
            elif op == "Tasa de cambio promedio e instantánea":
                res = tasa_cambio_promedio_e_instantanea(
                    fx, extra1 or "", extra2 or ""
                )
            else:
                res = {
                    "estado": "error",
                    "mensaje": f"Operación no soportada: {op}",
                    "pasos": [],
                }

            if res.get("pasos"):
                self._renderizar_pasos(res["pasos"])

            if res.get("estado") == "exito":
                texto_res = (
                    res.get("resultado_math")
                    or res.get("resultado_str")
                    or "Operación completada."
                )
                self.resultado_caja.insert("0.0", texto_res)
            else:
                self.resultado_caja.insert(
                    "0.0",
                    f"Error durante el cálculo:\n{res.get('mensaje', 'Error desconocido')}",
                )

        except ValueError as e:
            self.resultado_caja.insert("0.0", f"Error de entrada: {e}")
        except Exception as e:
            self.resultado_caja.insert("0.0", f"Error inesperado: {e}")

        self.resultado_caja.configure(state="disabled")

    def graficar_funcion_diferencial(self):
        try:
            funcion_str = self.ent_fx.get().strip()
            if not funcion_str:
                raise ValueError("El campo de la función está vacío.")

            op = self.operacion_var.get()
            extra1 = self.ent_extra1.get().strip()
            extra2 = self.ent_extra2.get().strip()

            a, b = -10.0, 10.0

            if op == "Recta tangente y normal" and extra1:
                try:
                    x0_val = float(parse_valor(extra1))
                    margen = 5.0
                    a, b = x0_val - margen, x0_val + margen
                except Exception:
                    pass
            elif (
                op == "Tasa de cambio promedio e instantánea"
                and extra1
                and extra2
            ):
                try:
                    a_val = float(parse_valor(extra1))
                    b_val = float(parse_valor(extra2))
                    if a_val != b_val:
                        margen = max(1.0, 0.2 * abs(b_val - a_val))
                        a = min(a_val, b_val) - margen
                        b = max(a_val, b_val) + margen
                    else:
                        a, b = a_val - 5.0, a_val + 5.0
                except Exception:
                    pass

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
                x_sym = sp.Symbol("x")
                expr = sp.sympify(
                    funcion_str.replace("^", "**"),
                    locals={
                        "x": x_sym,
                        "pi": sp.pi,
                        "e": sp.E,
                        "sin": sp.sin,
                        "cos": sp.cos,
                        "tan": sp.tan,
                        "log": sp.log,
                        "exp": sp.exp,
                        "sqrt": sp.sqrt,
                    },
                )
                f_lamb = sp.lambdify(x_sym, expr, modules=["numpy"])

                x_vals = np.linspace(a, b, 2000)
                y_vals = f_lamb(x_vals)

                ax.plot(
                    x_vals,
                    y_vals,
                    "b-",
                    linewidth=2.5,
                    label=f"f(x) = {funcion_str}",
                    alpha=0.8,
                )
                ax.axhline(y=0, color="black", linewidth=1.5, alpha=0.7)
                ax.axvline(x=0, color="black", linewidth=1.5, alpha=0.7)

                if op == "Recta tangente y normal" and extra1:
                    try:
                        x0_val = float(parse_valor(extra1))
                        y0_val = float(f_lamb(x0_val))

                        ax.scatter(
                            [x0_val],
                            [y0_val],
                            color="red",
                            s=60,
                            zorder=5,
                            label=f"P(x₀, f(x₀)) = ({x0_val:.3g}, {y0_val:.3g})",
                        )

                        h = (b - a) / 1000.0 or 1e-3
                        y_plus = float(f_lamb(x0_val + h))
                        y_minus = float(f_lamb(x0_val - h))
                        m_tan = (y_plus - y_minus) / (2.0 * h)

                        y_tan = m_tan * (x_vals - x0_val) + y0_val
                        ax.plot(
                            x_vals,
                            y_tan,
                            linestyle="--",
                            color="orange",
                            linewidth=2.0,
                            label=f"Tangente (m ≈ {m_tan:.3g})",
                        )

                        if abs(m_tan) > 1e-9:
                            m_norm = -1.0 / m_tan
                            y_norm = m_norm * (x_vals - x0_val) + y0_val
                            ax.plot(
                                x_vals,
                                y_norm,
                                linestyle="--",
                                color="green",
                                linewidth=2.0,
                                label=f"Normal (m ≈ {m_norm:.3g})",
                            )
                    except Exception:
                        pass

                if (
                    op == "Tasa de cambio promedio e instantánea"
                    and extra1
                    and extra2
                ):
                    try:
                        a_val = float(parse_valor(extra1))
                        b_val = float(parse_valor(extra2))
                        y_a = float(f_lamb(a_val))
                        y_b = float(f_lamb(b_val))

                        ax.scatter(
                            [a_val, b_val],
                            [y_a, y_b],
                            color="red",
                            s=60,
                            zorder=5,
                            label="Puntos a y b",
                        )

                        if b_val != a_val:
                            m_sec = (y_b - y_a) / (b_val - a_val)
                            y_sec = m_sec * (x_vals - a_val) + y_a
                            ax.plot(
                                x_vals,
                                y_sec,
                                linestyle="--",
                                color="purple",
                                linewidth=2.0,
                                label=f"Secante (m_prom ≈ {m_sec:.3g})",
                            )

                        h = (b - a) / 1000.0 or 1e-3
                        y_plus = float(f_lamb(a_val + h))
                        y_minus = float(f_lamb(a_val - h))
                        m_inst = (y_plus - y_minus) / (2.0 * h)

                        y_tan = m_inst * (x_vals - a_val) + y_a
                        ax.plot(
                            x_vals,
                            y_tan,
                            linestyle="--",
                            color="orange",
                            linewidth=2.0,
                            label=f"Tangente en a (m_inst ≈ {m_inst:.3g})",
                        )
                    except Exception:
                        pass

                ax.grid(True, alpha=0.3, linestyle="-", linewidth=0.5)
                ax.set_axisbelow(True)
                ax.set_xlabel("x", fontsize=12, fontweight="bold")
                ax.set_ylabel("f(x)", fontsize=12, fontweight="bold")
                ax.set_title(
                    f"Gráfica de f(x) = {funcion_str}\nRango de ploteo: [{a:.2f}, {b:.2f}]",
                    fontsize=14,
                    fontweight="bold",
                )
                ax.legend(loc="best", fontsize=10)

            except Exception as e:
                ax.text(
                    0.5,
                    0.5,
                    f"Error al graficar la función:\n\n{str(e)}",
                    horizontalalignment="center",
                    verticalalignment="center",
                    transform=ax.transAxes,
                    fontsize=12,
                    color="red",
                    bbox=dict(
                        boxstyle="round,pad=1",
                        facecolor="lightcoral",
                        alpha=0.8,
                    ),
                )

            canvas = FigureCanvasTkAgg(fig, ventana_grafica)
            canvas.draw()
            canvas.get_tk_widget().grid(
                row=0, column=0, sticky="nsew", padx=10, pady=10
            )

            marco_controles = ctk.CTkFrame(ventana_grafica)
            marco_controles.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

            def guardar_imagen():
                from tkinter import filedialog

                archivo = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[
                        ("PNG files", "*.png"),
                        ("PDF files", "*.pdf"),
                        ("All files", "*.*"),
                    ],
                    title="Guardar gráfica como...",
                )
                if archivo:
                    try:
                        fig.savefig(
                            archivo,
                            dpi=300,
                            bbox_inches="tight",
                            facecolor="white",
                        )
                    except Exception as e:
                        self.resultado_caja.configure(state="normal")
                        self.resultado_caja.insert(
                            "end", f"\nError al guardar la gráfica: {e}"
                        )
                        self.resultado_caja.configure(state="disabled")

            ctk.CTkButton(
                marco_controles,
                text="Guardar imagen",
                command=guardar_imagen,
                fg_color=COLOR_DIFERENCIAL[0],
                hover_color=COLOR_HOVER,
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                marco_controles,
                text="Cerrar",
                command=ventana_grafica.destroy,
                fg_color=COLOR_DIFERENCIAL[1],
                hover_color=COLOR_HOVER,
            ).pack(side="right", padx=5)

        except ValueError as e:
            self.resultado_caja.configure(state="normal")
            self.resultado_caja.delete("0.0", "end")
            self.resultado_caja.insert("0.0", f"Error para graficar: {e}")
            self.resultado_caja.configure(state="disabled")
        except Exception as e:
            self.resultado_caja.configure(state="normal")
            self.resultado_caja.delete("0.0", "end")
            self.resultado_caja.insert(
                "0.0", f"Error inesperado al crear la gráfica:\n{e}"
            )
            self.resultado_caja.configure(state="disabled")
