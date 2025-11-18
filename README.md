Calculadora de Álgebra Lineal en Python

Este proyecto es una calculadora de álgebra lineal desarrollada en Python, utilizando la librería customtkinter para la interfaz gráfica. Permite realizar diversas operaciones con matrices y resolver sistemas de ecuaciones lineales, mostrando los pasos de los cálculos.

Creadores
Farid Zuñiga
Luis Guadamuz 
Joshua Vilchez
Critopher Rodriguez

#Características Principales

Interfaz Gráfica Intuitiva: Diseño claro con customtkinter para facilitar la entrada de datos y visualización de resultados.

Operaciones Matriciales: Suma, resta y multiplicación de matrices.

Resolución de Sistemas:

Método de Eliminación Gaussiana.

Método de Gauss-Jordan (para forma escalonada reducida).

Regla de Cramer (con pasos detallados mostrando los determinantes).

Propiedades de Matrices:

Cálculo de la Matriz Inversa (usando Gauss-Jordan sobre [A|I]).

Cálculo del Determinante (elige automáticamente entre expansión por cofactores para matrices pequeñas y eliminación gaussiana para matrices grandes, mostrando los pasos del método elegido).

Verificación de Independencia Lineal de vectores (columnas de una matriz).

Visualización de Pasos: Muestra los pasos intermedios para los métodos de resolución, inversa y determinantes, ayudando a entender el proceso.

Entrada Flexible: Permite definir dimensiones diferentes para las matrices A y B.

Manejo de Errores: Valida las dimensiones de las matrices según la operación seleccionada y detecta entradas no válidas.

Estructura del Proyecto

interfazGrafica.py: Contiene toda la lógica de la interfaz de usuario (ventanas, botones, campos de entrada) y coordina las llamadas a las funciones matemáticas.

Complement.py: Alberga todas las funciones matemáticas puras (algoritmos de Gauss, Cramer, determinante, inversa, etc.).

Funcionalidades Implementadas

1. Operaciones Básicas

Suma: α*A + β*B (matrices deben tener la misma dimensión).

Resta: α*A - β*B (matrices deben tener la misma dimensión).

Multiplicación: A * B (columnas de A deben ser igual a filas de B).

2. Resolución de Sistemas Lineales (Ax=b)

Gauss: Transforma la matriz aumentada [A|b] a forma escalonada y usa sustitución hacia atrás (si hay solución única).

Gauss-Jordan: Transforma la matriz aumentada [A|b] a forma escalonada reducida. Identifica si el sistema tiene solución única, infinitas soluciones (indicando variables libres) o es inconsistente.

Regla de Cramer: Calcula la solución usando determinantes (xi = Di / D). Requiere que la matriz A sea cuadrada y det(A) != 0. Se ingresa la matriz aumentada [A|b]. Muestra los pasos del cálculo de cada determinante.

3. Propiedades y Operaciones Avanzadas

Independencia Lineal: Determina si los vectores columna de la matriz A son linealmente independientes o dependientes, mostrando el rango.

Inversa: Calcula la matriz inversa de A (A⁻¹) usando el método de Gauss-Jordan sobre [A|I]. Requiere que A sea cuadrada e invertible. Muestra los pasos de la reducción.

Determinante: Calcula el determinante de A.

Si A es 3x3 o menor, usa expansión por cofactores mostrando los pasos recursivos.

Si A es 4x4 o mayor, usa eliminación gaussiana mostrando los pasos de la triangulación y el producto de la diagonal.

Requiere que A sea cuadrada.

Cómo Usar

Asegúrate de tener Python instalado y la librería customtkinter (pip install customtkinter).

Ejecuta el archivo interfazGrafica.py.

Selecciona "Álgebra Lineal" en el menú (ya está por defecto).

Elige la Operación deseada en el menú desplegable.

Introduce las Filas y Columnas para la Matriz A (y Matriz B si aplica).

Presiona "Generar Matrices".

Rellena las casillas de las matrices con los números deseados.

Si es Suma o Resta, introduce los escalares α y β (si no, déjalos vacíos, se tomarán como 1).

Presiona "Calcular".

Observa los Pasos en la caja izquierda y el Resultado final en la caja derecha.

Usa "Limpiar" para borrar las matrices y resultados.

Requisitos

Python 3.x

Librería