# paginas/pagina_inicio.py

import customtkinter as ctk
from app_config import COLOR_ALGEBRA, COLOR_NUMERICOS, COLOR_ACENTO, COLOR_HOVER


class PaginaInicio(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        panel = ctk.CTkFrame(self, corner_radius=18, fg_color=("gray13", "gray13"))
        panel.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

        panel.grid_rowconfigure(2, weight=1)
        panel.grid_columnconfigure(0, weight=1)

        # Títulos principales
        ctk.CTkLabel(panel, text="MathPro",
                     font=ctk.CTkFont(size=34, weight="bold")).grid(row=0, column=0, pady=(25, 5))

        ctk.CTkLabel(
            panel,
            text="Herramientas Matemáticas Avanzadas",
            font=ctk.CTkFont(size=15),
            text_color="#B5B5B5"
        ).grid(row=1, column=0, pady=(0, 20))

        # Contenedor
        cont = ctk.CTkFrame(panel, fg_color="transparent")
        cont.grid(row=2, column=0, pady=10)

        cont.grid_columnconfigure((0, 1, 2), weight=1)
        cont.grid_rowconfigure((0, 1), weight=1)

        # ======================================================
        # TARJETA 1 — ÁLGEBRA LINEAL
        # ======================================================
        card_alg = ctk.CTkFrame(
            cont, width=650, height=460, corner_radius=20,
            border_width=3, border_color=COLOR_ALGEBRA,
            fg_color="black"
        )
        card_alg.grid(row=0, column=0, padx=20, pady=10)
        card_alg.grid_propagate(False)

        ctk.CTkLabel(card_alg, text="📐", font=ctk.CTkFont(size=60)).pack(pady=(25, 8))
        ctk.CTkLabel(card_alg, text="Álgebra Lineal",
                     font=ctk.CTkFont(size=20, weight="bold")).pack()

        ctk.CTkLabel(
            card_alg,
            text="Sistemas de ecuaciones\nOperaciones matriciales\nDeterminantes\nVectores propios",
            font=ctk.CTkFont(size=13),
            justify="center"
        ).pack(pady=(8, 12))

        ctk.CTkButton(
            card_alg, text="Explorar Álgebra Lineal",
            fg_color=COLOR_ALGEBRA, hover_color=COLOR_HOVER,
            command=lambda: self.app.mostrar_pagina("sistemas_ecuaciones")
        ).pack()

        # ======================================================
        # TARJETA 2 — MÉTODOS NUMÉRICOS
        # ======================================================
        card_num = ctk.CTkFrame(
            cont, width=650, height=460, corner_radius=20,
            border_width=3, border_color=COLOR_NUMERICOS,
            fg_color="black"
        )
        card_num.grid(row=0, column=1, padx=20, pady=10)
        card_num.grid_propagate(False)

        ctk.CTkLabel(card_num, text="🔢", font=ctk.CTkFont(size=60)).pack(pady=(25, 8))
        ctk.CTkLabel(card_num, text="Métodos Numéricos",
                     font=ctk.CTkFont(size=20, weight="bold")).pack()

        ctk.CTkLabel(
            card_num,
            text="Ecuaciones no lineales\nInterpolación\nDiferenciación numérica\nEcuaciones diferenciales",
            font=ctk.CTkFont(size=13),
            justify="center"
        ).pack(pady=(8, 12))

        ctk.CTkButton(
            card_num, text="Explorar Métodos Numéricos",
            fg_color=COLOR_NUMERICOS, hover_color=COLOR_HOVER,
            command=lambda: self.app.mostrar_pagina("metodos_numericos")
        ).pack()

        # ======================================================
        # TARJETA 3 — CÁLCULO (ABAJO CENTRADO)
        # ======================================================
        card_calc = ctk.CTkFrame(
            cont, width=650, height=460, corner_radius=20,
            border_width=3, border_color=COLOR_ACENTO,
            fg_color="black"
        )
        card_calc.grid(row=1, column=0, columnspan=3, pady=(20, 5))
        card_calc.grid_propagate(False)

        ctk.CTkLabel(card_calc, text="∫", font=ctk.CTkFont(size=70)).pack(pady=(20, 8))
        ctk.CTkLabel(card_calc, text="Cálculo",
                     font=ctk.CTkFont(size=20, weight="bold")).pack()

        ctk.CTkLabel(
            card_calc,
            text="Derivadas simbólicas\nIntegrales indefinidas\nDerivadas evaluadas\nIntegrales definidas",
            font=ctk.CTkFont(size=13),
            justify="center"
        ).pack(pady=(8, 12))

        ctk.CTkButton(
            card_calc, text="Explorar Cálculo",
            fg_color=COLOR_ACENTO, hover_color=COLOR_HOVER,
            command=lambda: self.app.mostrar_pagina("calculo")
        ).pack()

    def mostrar(self):
        pass