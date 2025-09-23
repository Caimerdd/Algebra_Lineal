# Calculadora de Matrices en C#

Este proyecto es una conversión completa del código Python original a C# con Windows Forms, manteniendo exactamente la misma funcionalidad y diseño.

## Características

- **Interfaz idéntica**: Diseño 100% igual al original de Python con CustomTkinter
- **Funcionalidades completas**:
  - Suma de matrices
  - Resta de matrices  
  - Multiplicación de matrices
  - Resolución de sistemas de ecuaciones lineales con Gauss
  - Resolución de sistemas de ecuaciones lineales con Gauss-Jordan
- **Namespace**: Calculadora
- **Variables y funciones**: Todas en español con camelCase
- **Framework**: .NET Framework 4.8
- **UI**: Windows Forms

## Estructura del Proyecto

```
Calculadora/
├── FormularioPrincipal.cs          # Formulario principal (equivalente a MainApp)
├── FormularioPrincipal.Designer.cs # Diseñador del formulario
├── AlgebraLineal.cs                # Lógica matemática (equivalente a algebraLineal.py)
├── Program.cs                      # Punto de entrada
└── Properties/                     # Archivos de configuración
```

## Funcionalidades Implementadas

### 1. Operaciones con Matrices
- **Suma**: A + B (matrices del mismo tamaño)
- **Resta**: A - B (matrices del mismo tamaño)
- **Multiplicación**: A × B (columnas de A = filas de B)

### 2. Resolución de Sistemas Lineales
- **Método de Gauss**: Eliminación hacia adelante + sustitución hacia atrás
- **Método de Gauss-Jordan**: Eliminación completa para forma escalonada reducida

### 3. Interfaz de Usuario
- Panel de navegación izquierdo con menú de secciones
- Área principal con controles para configurar matrices
- Entrada de datos por grilla o texto
- Visualización de pasos del algoritmo
- Mostrar resultados y soluciones

## Cómo Usar

1. **Abrir el proyecto** en Visual Studio
2. **Compilar** el proyecto (Build → Build Solution)
3. **Ejecutar** la aplicación
4. **Seleccionar "Álgebra Lineal"** del menú izquierdo
5. **Configurar** el número de filas y columnas
6. **Elegir** la operación deseada
7. **Generar** las matrices e introducir los valores
8. **Calcular** para ver los resultados

## Equivalencias Python → C#

| Python | C# |
|--------|-----|
| `MainApp` | `FormularioPrincipal` |
| `algebraLineal.py` | `AlgebraLineal.cs` |
| `gauss_jordan_steps()` | `PasosGaussJordan()` |
| `gauss_steps()` | `PasosGauss()` |
| `fmt_number()` | `FormatearNumero()` |
| `parsear_ecuacion()` | `ParsearEcuacion()` |

## Requisitos del Sistema

- Windows 7 o superior
- .NET Framework 4.8
- Visual Studio 2019 o superior (para desarrollo)

## Notas Técnicas

- Todas las variables y métodos están en español con camelCase
- La lógica matemática es idéntica al código Python original
- El diseño visual replica fielmente la interfaz de CustomTkinter
- Manejo de errores y validaciones implementadas
- Formateo de números y matrices consistente con el original