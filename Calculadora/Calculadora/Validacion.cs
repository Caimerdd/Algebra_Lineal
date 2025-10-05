using System;

namespace Calculadora
{
    public static class Validacion
    {
        public static bool validarMatriz(double[,] matriz)
        {
            int filas = matriz.GetLength(0);
            int columnas = matriz.GetLength(1);

            for (int i = 0; i < filas; i++)
            {
                for (int j = 0; j < columnas; j++)
                {
                    if (double.IsNaN(matriz[i, j]) || double.IsInfinity(matriz[i, j]))
                        return false;
                }
            }
            return true;
        }

        public static bool esNumeroValido(string texto)
        {
            texto = texto.Replace(',', '.');
            return double.TryParse(texto, out _);
        }

        public static double convertirANumero(string texto)
        {
            texto = texto.Replace(',', '.');
            if (double.TryParse(texto, out double resultado))
                return resultado;
            return 0.0; 
        }
    }
}