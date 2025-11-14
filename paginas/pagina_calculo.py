# paginas/pagina_calculo.py

import customtkinter as ctk
from typing import Optional
from app_config import (
    COLOR_BOTON_SECUNDARIO,
    COLOR_BOTON_SECUNDARIO_HOVER,
    COLOR_ACENTO,
    COLOR_HOVER,
)
import Calculo  # Módulo que acabamos de crear


class PaginaCalculo(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Variables de estado
        self.modo_calculo = ctk.StringVar(value="derivada")   # 'derivada' o 'integral'
        self.tipo_integral = ctk.StringVar(value="indefinida")  # 'indefinida' o 'definida'

        # ===================== CABECERA =====================
        marco_titulo = ctk.CTkFrame(self, fg_color="transparent")
        marco_titulo.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(15, 5))
        marco_titulo.grid_columnconfigure(0, weight=1)

        lbl_titulo = ctk.CTkLabel(
            marco_titulo,
            text="Cálculo",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        lbl_titulo.grid(row=0, column=0, sticky="w")

        lbl_desc = ctk.CTkLabel(
            marco_titulo,
            text="Derivadas e Integrales",
            font=ctk.CTkFont(size=14),
            text_color=("#B0B0B0", "#A0A0A0")
        )
        lbl_desc.grid(row=1, column=0, sticky="w", pady=(0, 5))

        # ===================== CONTROLES SUPERIORES =====================
        marco_controles = ctk.CTkFrame(self)
        marco_controles.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 10))
        marco_controles.grid_columnconfigure(0, weight=1)
        marco_controles.grid_columnconfigure(1, weight=1)
        marco_controles.grid_columnconfigure(2, weight=1)
        marco_controles.grid_columnconfigure(3, weight=1)

        # Selector de modo (Derivadas / Integrales)
        lbl_modo = ctk.CTkLabel(
            marco_controles,
            text="Modo:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        lbl_modo.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        rb_derivada = ctk.CTkRadioButton(
            marco_controles,
            text="Derivadas",
            variable=self.modo_calculo,
            value="derivada",
            command=self._actualizar_modo,
        )
        rb_derivada.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        rb_integral = ctk.CTkRadioButton(
            marco_controles,
            text="Integrales",
            variable=self.modo_calculo,
            value="integral",
            command=self._actualizar_modo,
        )
        rb_integral.grid(row=0, column=2, sticky="w", padx=5, pady=5)

        # Campo función f(x)
        lbl_fx = ctk.CTkLabel(marco_controles, text="Función f(x) =", font=ctk.CTkFont(size=13))
        lbl_fx.grid(row=1, column=0, sticky="w", padx=5, pady=(10, 5))

        self.entry_funcion = ctk.CTkEntry(
            marco_controles,
            placeholder_text="Ej: x**2 + 3*x - 1   (usar 'x' como variable)"
        )
        self.entry_funcion.grid(row=1, column=1, columnspan=3, sticky="ew", padx=5, pady=(10, 5))

        # Variable
        lbl_var = ctk.CTkLabel(marco_controles, text="Variable:", font=ctk.CTkFont(size=13))
        lbl_var.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.entry_variable = ctk.CTkEntry(marco_controles, width=80)
        self.entry_variable.insert(0, "x")
        self.entry_variable.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Controles específicos para DERIVADAS
        # Orden
        self.lbl_orden = ctk.CTkLabel(marco_controles, text="Orden de derivada:", font=ctk.CTkFont(size=13))
        self.lbl_orden.grid(row=3, column=0, sticky="w", padx=5, pady=5)

        self.entry_orden = ctk.CTkEntry(marco_controles, width=80)
        self.entry_orden.insert(0, "1")
        self.entry_orden.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # Punto de evaluación
        self.lbl_punto = ctk.CTkLabel(
            marco_controles,
            text="Punto de evaluación (opcional):",
            font=ctk.CTkFont(size=13)
        )
        self.lbl_punto.grid(row=3, column=2, sticky="w", padx=5, pady=5)

        self.entry_punto = ctk.CTkEntry(
            marco_controles,
            width=120,
            placeholder_text="Ej: 0, 1, pi/2"
        )
        self.entry_punto.grid(row=3, column=3, sticky="w", padx=5, pady=5)

        # Controles específicos para INTEGRALES
        self.lbl_tipo_int = ctk.CTkLabel(
            marco_controles,
            text="Tipo de integral:",
            font=ctk.CTkFont(size=13)
        )

        self.rb_int_indef = ctk.CTkRadioButton(
            marco_controles,
            text="Indefinida",
            variable=self.tipo_integral,
            value="indefinida",
            command=self._actualizar_tipo_integral
        )

        self.rb_int_def = ctk.CTkRadioButton(
            marco_controles,
            text="Definida",
            variable=self.tipo_integral,
            value="definida",
            command=self._actualizar_tipo_integral
        )

        self.lbl_lim_inf = ctk.CTkLabel(marco_controles, text="Límite inferior:", font=ctk.CTkFont(size=13))
        self.entry_lim_inf = ctk.CTkEntry(marco_controles, width=100, placeholder_text="Ej: 0")

        self.lbl_lim_sup = ctk.CTkLabel(marco_controles, text="Límite superior:", font=ctk.CTkFont(size=13))
        self.entry_lim_sup = ctk.CTkEntry(marco_controles, width=100, placeholder_text="Ej: 1")

        # Botones de acción
        marco_botones = ctk.CTkFrame(self, fg_color="transparent")
        marco_botones.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 5))
        marco_botones.grid_columnconfigure(0, weight=0)
        marco_botones.grid_columnconfigure(1, weight=0)
        marco_botones.grid_columnconfigure(2, weight=1)

        self.btn_calcular = ctk.CTkButton(
            marco_botones,
            text="Calcular",
            fg_color=COLOR_ACENTO,
            hover_color=COLOR_HOVER,
            command=self._on_calcular
        )
        self.btn_calcular.grid(row=0, column=0, padx=(0, 8), pady=5)

        self.btn_limpiar = ctk.CTkButton(
            marco_botones,
            text="Limpiar",
            fg_color=COLOR_BOTON_SECUNDARIO,
            hover_color=COLOR_BOTON_SECUNDARIO_HOVER,
            command=self._on_limpiar
        )
        self.btn_limpiar.grid(row=0, column=1, padx=(0, 8), pady=5)

        # ===================== BITÁCORA Y RESULTADO =====================
        marco_bitacora = ctk.CTkFrame(self)
        marco_bitacora.grid(row=3, column=0, sticky="nsew", padx=(20, 10), pady=(5, 20))
        marco_bitacora.grid_rowconfigure(1, weight=1)
        marco_bitacora.grid_columnconfigure(0, weight=1)

        lbl_bit = ctk.CTkLabel(
            marco_bitacora,
            text="Bitácora Paso a Paso",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        lbl_bit.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        self.text_bitacora = ctk.CTkTextbox(marco_bitacora)
        self.text_bitacora.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        marco_resultado = ctk.CTkFrame(self)
        marco_resultado.grid(row=3, column=1, sticky="nsew", padx=(10, 20), pady=(5, 20))
        marco_resultado.grid_rowconfigure(1, weight=1)
        marco_resultado.grid_columnconfigure(0, weight=1)

        lbl_res = ctk.CTkLabel(
            marco_resultado,
            text="Resultado Final",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        lbl_res.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        self.text_resultado = ctk.CTkTextbox(marco_resultado)
        self.text_resultado.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Inicializar estado visual
        self._actualizar_modo()

    # ======================================================
    # Métodos de control de interfaz
    # ======================================================

    def mostrar(self):
        """Método llamado desde main al activar esta página (si necesitas refrescar algo)."""
        # Por ahora no hace nada especial, pero queda para futuro.
        pass

    def _actualizar_modo(self):
        """Muestra / oculta controles según 'derivada' o 'integral'."""
        modo = self.modo_calculo.get()

        # Ocultar primero los controles de integrales
        self.lbl_tipo_int.grid_remove()
        self.rb_int_indef.grid_remove()
        self.rb_int_def.grid_remove()
        self.lbl_lim_inf.grid_remove()
        self.entry_lim_inf.grid_remove()
        self.lbl_lim_sup.grid_remove()
        self.entry_lim_sup.grid_remove()

        if modo == "derivada":
            # Controles de derivada ya están visibles por defecto
            self.lbl_orden.grid()
            self.entry_orden.grid()
            self.lbl_punto.grid()
            self.entry_punto.grid()
        else:
            # Ocultar los de derivada
            self.lbl_orden.grid_remove()
            self.entry_orden.grid_remove()
            self.lbl_punto.grid_remove()
            self.entry_punto.grid_remove()

            # Mostrar controles de integrales
            row_start = 3
            self.lbl_tipo_int.grid(row=row_start, column=0, sticky="w", padx=5, pady=5)
            self.rb_int_indef.grid(row=row_start, column=1, sticky="w", padx=5, pady=5)
            self.rb_int_def.grid(row=row_start, column=2, sticky="w", padx=5, pady=5)

            # Límites de integración (se mostrarán solo si es definida)
            self._actualizar_tipo_integral()

    def _actualizar_tipo_integral(self):
        """Muestra / oculta los límites de integración según el tipo."""
        modo = self.modo_calculo.get()
        if modo != "integral":
            return

        tipo = self.tipo_integral.get()
        # Ocultamos primero
        self.lbl_lim_inf.grid_remove()
        self.entry_lim_inf.grid_remove()
        self.lbl_lim_sup.grid_remove()
        self.entry_lim_sup.grid_remove()

        if tipo == "definida":
            self.lbl_lim_inf.grid(row=4, column=0, sticky="w", padx=5, pady=5)
            self.entry_lim_inf.grid(row=4, column=1, sticky="w", padx=5, pady=5)
            self.lbl_lim_sup.grid(row=4, column=2, sticky="w", padx=5, pady=5)
            self.entry_lim_sup.grid(row=4, column=3, sticky="w", padx=5, pady=5)

    def _on_limpiar(self):
        self.entry_funcion.delete(0, "end")
        self.entry_variable.delete(0, "end")
        self.entry_variable.insert(0, "x")
        self.entry_orden.delete(0, "end")
        self.entry_orden.insert(0, "1")
        self.entry_punto.delete(0, "end")
        self.entry_lim_inf.delete(0, "end")
        self.entry_lim_sup.delete(0, "end")
        self.text_bitacora.delete("1.0", "end")
        self.text_resultado.delete("1.0", "end")

    def _on_calcular(self):
        """
        Por ahora NO hace cálculos, solo envía la info al módulo Calculo.py
        y muestra la descripción en la bitácora.
        """
        funcion_str = self.entry_funcion.get().strip()
        variable = self.entry_variable.get().strip() or "x"

        self.text_bitacora.delete("1.0", "end")
        self.text_resultado.delete("1.0", "end")

        if self.modo_calculo.get() == "derivada":
            orden_str = self.entry_orden.get().strip() or "1"
            punto_eval = self.entry_punto.get().strip()

            try:
                orden = int(orden_str)
            except ValueError:
                orden = 1

            resultado = Calculo.preparar_derivada(
                funcion_str=funcion_str,
                variable=variable,
                orden=orden,
                punto_eval=punto_eval
            )

        else:
            tipo = self.tipo_integral.get()
            lim_inf = self.entry_lim_inf.get().strip()
            lim_sup = self.entry_lim_sup.get().strip()

            resultado = Calculo.preparar_integral(
                funcion_str=funcion_str,
                variable=variable,
                tipo=tipo,
                limite_inferior=lim_inf,
                limite_superior=lim_sup
            )

        # Mostrar en bitácora
        for linea in resultado.get("pasos", []):
            self.text_bitacora.insert("end", linea + "\n")

        # Resultado final (por ahora solo texto de “pendiente”)
        self.text_resultado.insert(
            "end",
            "Módulo de Cálculo en fase de diseño.\n"
            "Por ahora solo se muestran los datos de entrada.\n"
            "Más adelante aquí se mostrará el valor de la derivada o integral."
        )
