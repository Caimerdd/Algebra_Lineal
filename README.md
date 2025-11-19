# 🧮 MathPro - Herramientas Matemáticas Avanzadas

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/Interfaz-CustomTkinter-005fd4?style=for-the-badge)
![Math](https://img.shields.io/badge/Motor-SymPy-3b6c12?style=for-the-badge)
![Build](https://img.shields.io/badge/Build-PyInstaller-orange?style=for-the-badge)

**MathPro** es una suite de software de escritorio diseñada para estudiantes y profesionales de ingeniería. Ofrece soluciones paso a paso para problemas complejos de Álgebra Lineal, Cálculo y Métodos Numéricos, todo envuelto en una interfaz moderna, oscura y amigable.

**Creada por** 
* **Luis Guadamuz**
* **Farid Zuñiga**
* **Joshua Vilchez**
* **Cristopher Rodríguez **


---

## ✨ Características Principales

### 📐 Álgebra Lineal
* **Sistemas de Ecuaciones:** Resolución por Gauss, Gauss-Jordan, Regla de Cramer y Matriz Inversa.
* **Operaciones Matriciales:** Suma, Resta, Multiplicación y Escalar.
* **Propiedades:** Cálculo de Determinantes (Expansión/Gauss), Rango e Independencia Lineal.
* **Bitácora Paso a Paso:** Visualización detallada de las operaciones fila por fila y cálculos intermedios.

### 🔢 Métodos Numéricos
* **Ecuaciones No Lineales:**
    * Métodos Cerrados: Bisección, Falsa Posición.
    * Métodos Abiertos: Newton-Raphson, Secante.
* **Gráficas Integradas:** Visualización automática de funciones e intervalos de convergencia.
* **Tablas de Iteración:** Tablas formateadas con precisión científica y cálculo de error.

### 🧮 Fundamentos y Cálculo (En Desarrollo)
* **Fundamentos:** Operaciones con polinomios (Suma, Resta, Multiplicación) y búsqueda de raíces.
* **Cálculo Diferencial:** Estructura lista para Límites y Derivadas.
* **Cálculo Integral:** Estructura lista para Integrales definidas, indefinidas y series.

### 🎨 Experiencia de Usuario (UX)
* **Intro Cinemática:** Splash screen animado con OpenCV al iniciar la aplicación.
* **Modo Oscuro/Claro:** Interfaz adaptativa construida con CustomTkinter.
* **Bitácora Estilo "Photomath":** Explicaciones claras, formateadas matemáticamente y fáciles de leer.

---

## 🛠️ Tecnologías Utilizadas

Este proyecto ha sido construido con las siguientes librerías de Python:

* **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter):** Para una interfaz gráfica moderna.
* **[SymPy](https://www.sympy.org/):** Para el cálculo simbólico y álgebra exacta.
* **[Matplotlib](https://matplotlib.org/):** Para graficar funciones matemáticas.
* **[OpenCV (cv2)](https://opencv.org/):** Para la reproducción de video en la intro.
* **[Pillow (PIL)](https://python-pillow.org/):** Para manejo de imágenes e íconos.
* **[PyInstaller](https://pyinstaller.org/):** Para compilar el proyecto en un ejecutable `.exe`.

---

## 🚀 Instalación y Uso

### Prerrequisitos
Asegúrate de tener Python instalado. Luego, instala las dependencias necesarias ejecutando:

```bash
pip install customtkinter sympy matplotlib opencv-python pillow pyinstaller
Ejecución (Modo Desarrollador)
Para correr el programa desde el código fuente:

Bash

python main.py
📦 Crear Ejecutable (.exe)
El proyecto incluye un script automatizado para compilar el programa, empaquetar los recursos (video e ícono) y crear accesos directos.

Asegúrate de tener los archivos icono.ico y intro.mp4 en la carpeta raíz del proyecto.

Ejecuta el archivo batch incluido:

👉 actualizar_exe.bat

Este script realizará automáticamente:

Limpieza de carpetas de compilación anteriores (build, dist).

Empaquetado de librerías y recursos multimedia.

Generación del archivo MathPro_Final.exe.

Creación de un acceso directo en tu Escritorio.

📂 Estructura del Proyecto
Plaintext

ALGEBRA_LUIS/
│
├── paginas/                  # Módulos de la interfaz gráfica
│   ├── pagina_base.py        # Clase padre para todas las páginas
│   ├── pagina_inicio.py      # Menú principal con tarjetas
│   ├── pagina_sistemas...py  # Interfaz para sistemas de ecuaciones
│   ├── pagina_metodos...py   # Interfaz para métodos numéricos
│   └── ... (otras páginas)
│
├── ui_components/            # Componentes reutilizables
│   └── ventana_ayuda.py      # Ventana emergente de ayuda SymPy
│
├── Complement.py             # Lógica matemática (Gauss, Cramer, Inversa)
├── LogicaFundamentos.py      # Lógica para polinomios (SymPy)
├── MetodosNumericos.py       # Algoritmos numéricos (Newton, Bisección, etc.)
├── app_config.py             # Colores, configuraciones y utilidades globales
├── main.py                   # Punto de entrada de la aplicación
│
├── intro.mp4                 # Video de splash screen
├── icono.ico                 # Ícono de la aplicación
└── actualizar_exe.bat        # Script de compilación automática
🤝 Contribución
Este es un proyecto académico/profesional en constante evolución.

<div align="center"> <p>Desarrollado con ❤️ y mucho ☕</p> <p><b>MathPro © 2025</b></p> </div>
