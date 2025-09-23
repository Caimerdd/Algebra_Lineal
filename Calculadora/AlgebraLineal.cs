using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace Calculadora
{
    public class AlgebraLineal
    {
        private const double EPS = 1e-12;

        public static string NormalizarGuiones(string s)
        {
            return s.Replace('−', '-').Replace('–', '-').Replace('—', '-').Replace(" ", "");
        }

        public static (Dictionary<string, double> variables, double constante) ParsearLado(string expr)
        {
            string s = NormalizarGuiones(expr);
            if (string.IsNullOrEmpty(s))
                throw new ArgumentException("Lado vacío");

            if (s[0] != '+' && s[0] != '-')
                s = "+" + s;

            s = s.Replace("-", "+-");
            var partes = s.Split('+').Where(t => !string.IsNullOrEmpty(t)).ToArray();

            var varsDict = new Dictionary<string, double>();
            double constante = 0.0;

            foreach (var p in partes)
            {
                int idx = 0;
                while (idx < p.Length && (char.IsDigit(p[idx]) || p[idx] == '.' || p[idx] == '-'))
                    idx++;

                string coefStr;
                string variable;

                if (idx == 0 && char.IsLetter(p[0]))
                {
                    coefStr = "";
                    variable = p;
                }
                else if (idx == p.Length)
                {
                    constante += double.Parse(p, CultureInfo.InvariantCulture);
                    continue;
                }
                else
                {
                    coefStr = p.Substring(0, idx);
                    variable = p.Substring(idx);
                }

                double coef;
                if (coefStr == "" || coefStr == "+")
                    coef = 1.0;
                else if (coefStr == "-")
                    coef = -1.0;
                else
                    coef = double.Parse(coefStr, CultureInfo.InvariantCulture);

                if (varsDict.ContainsKey(variable))
                    varsDict[variable] += coef;
                else
                    varsDict[variable] = coef;
            }

            return (varsDict, constante);
        }

        public static (Dictionary<string, double> variables, double constante) ParsearEcuacion(string eq)
        {
            string s = eq.Replace(" ", "");
            s = s.Replace('−', '-').Replace('–', '-').Replace('—', '-');

            if (s.Count(c => c == '=') != 1)
                throw new ArgumentException("La ecuación debe tener un '='.");

            var partes = s.Split('=');
            string lhs = partes[0];
            string rhs = partes[1];

            var (varsLhs, constLhs) = ParsearLado(lhs);
            var (varsRhs, constRhs) = ParsearLado(rhs);

            var varsFinal = new Dictionary<string, double>();

            foreach (var kvp in varsLhs)
            {
                if (varsFinal.ContainsKey(kvp.Key))
                    varsFinal[kvp.Key] += kvp.Value;
                else
                    varsFinal[kvp.Key] = kvp.Value;
            }

            foreach (var kvp in varsRhs)
            {
                if (varsFinal.ContainsKey(kvp.Key))
                    varsFinal[kvp.Key] -= kvp.Value;
                else
                    varsFinal[kvp.Key] = -kvp.Value;
            }

            double constanteFinal = constRhs - constLhs;
            return (varsFinal, constanteFinal);
        }

        public static string FormatearNumero(double x)
        {
            if (Math.Abs(x) < EPS)
                return "0";
            if (Math.Abs(x - Math.Round(x)) < 1e-9)
                return ((int)Math.Round(x)).ToString();

            string s = x.ToString("F6", CultureInfo.InvariantCulture).TrimEnd('0').TrimEnd('.');
            return s;
        }

        public static List<List<double>> CopiarMatriz(List<List<double>> matriz)
        {
            var copia = new List<List<double>>();
            foreach (var fila in matriz)
            {
                copia.Add(new List<double>(fila));
            }
            return copia;
        }

        public static ResultadoGauss PasosGaussJordan(List<List<double>> matriz)
        {
            var A = CopiarMatriz(matriz);
            int n = A.Count;
            if (n == 0)
                return new ResultadoGauss { Pasos = new List<List<List<double>>>(), Estado = "vacío", Solucion = null };

            int m = A[0].Count - 1;
            var pasos = new List<List<List<double>>> { CopiarMatriz(A) };

            int fila = 0;
            var mapasPivote = new Dictionary<int, int>();

            for (int col = 0; col < m; col++)
            {
                // buscar pivote
                int? sel = null;
                for (int r = fila; r < n; r++)
                {
                    if (Math.Abs(A[r][col]) > EPS)
                    {
                        sel = r;
                        break;
                    }
                }

                if (sel == null)
                    continue;

                // intercambiar filas
                if (sel != fila)
                {
                    var temp = A[fila];
                    A[fila] = A[sel.Value];
                    A[sel.Value] = temp;
                    pasos.Add(CopiarMatriz(A));
                }

                // normalizar pivote
                double pivote = A[fila][col];
                for (int c = 0; c < m + 1; c++)
                {
                    A[fila][c] /= pivote;
                }
                pasos.Add(CopiarMatriz(A));

                // eliminar en otras filas
                for (int r = 0; r < n; r++)
                {
                    if (r != fila && Math.Abs(A[r][col]) > EPS)
                    {
                        double factor = A[r][col];
                        for (int c = 0; c < m + 1; c++)
                        {
                            A[r][c] -= factor * A[fila][c];
                        }
                        pasos.Add(CopiarMatriz(A));
                    }
                }

                mapasPivote[col] = fila;
                fila++;
                if (fila == n)
                    break;
            }

            // detectar inconsistencia
            bool sistemaInconsistente = false;
            for (int r = 0; r < n; r++)
            {
                bool todosCero = true;
                for (int c = 0; c < m; c++)
                {
                    if (Math.Abs(A[r][c]) > EPS)
                    {
                        todosCero = false;
                        break;
                    }
                }
                if (todosCero && Math.Abs(A[r][m]) > EPS)
                {
                    sistemaInconsistente = true;
                    break;
                }
            }

            if (sistemaInconsistente)
            {
                return new ResultadoGauss { Pasos = pasos, Estado = "inconsistente", Solucion = null };
            }
            else if (mapasPivote.Count == m)
            {
                var sol = new double[m];
                foreach (var kvp in mapasPivote)
                {
                    sol[kvp.Key] = A[kvp.Value][m];
                }
                return new ResultadoGauss { Pasos = pasos, Estado = "única", Solucion = sol.ToList() };
            }
            else
            {
                var libres = new List<int>();
                for (int c = 0; c < m; c++)
                {
                    if (!mapasPivote.ContainsKey(c))
                        libres.Add(c);
                }
                return new ResultadoGauss { Pasos = pasos, Estado = "infinitas", VariablesLibres = libres };
            }
        }

        public static ResultadoGauss PasosGauss(List<List<double>> matriz)
        {
            var A = CopiarMatriz(matriz);
            int n = A.Count;
            if (n == 0)
                return new ResultadoGauss { Pasos = new List<List<List<double>>>(), Estado = "vacío", Solucion = null };

            int m = A[0].Count - 1;
            var pasos = new List<List<List<double>>> { CopiarMatriz(A) };

            // Eliminación hacia adelante para hacer triangular superior
            int fila = 0;
            var columnasPivote = new List<int>();

            for (int col = 0; col < m; col++)
            {
                int? sel = null;
                for (int r = fila; r < n; r++)
                {
                    if (Math.Abs(A[r][col]) > EPS)
                    {
                        sel = r;
                        break;
                    }
                }

                if (sel == null)
                    continue;

                if (sel != fila)
                {
                    var temp = A[fila];
                    A[fila] = A[sel.Value];
                    A[sel.Value] = temp;
                    pasos.Add(CopiarMatriz(A));
                }

                // eliminar hacia abajo
                for (int r = fila + 1; r < n; r++)
                {
                    if (Math.Abs(A[r][col]) > EPS)
                    {
                        double factor = A[r][col] / A[fila][col];
                        for (int c = col; c < m + 1; c++)
                        {
                            A[r][c] -= factor * A[fila][c];
                        }
                        pasos.Add(CopiarMatriz(A));
                    }
                }

                columnasPivote.Add(col);
                fila++;
                if (fila == n)
                    break;
            }

            // verificar inconsistencia
            for (int r = 0; r < n; r++)
            {
                bool todosCero = true;
                for (int c = 0; c < m; c++)
                {
                    if (Math.Abs(A[r][c]) > EPS)
                    {
                        todosCero = false;
                        break;
                    }
                }
                if (todosCero && Math.Abs(A[r][m]) > EPS)
                {
                    return new ResultadoGauss { Pasos = pasos, Estado = "inconsistente", Solucion = null };
                }
            }

            // sustitución hacia atrás si es posible (solución única)
            if (columnasPivote.Count == m)
            {
                var x = new double[m];
                for (int i = columnasPivote.Count - 1; i >= 0; i--)
                {
                    int col = columnasPivote[i];
                    int r = i;
                    double s = A[r][m];
                    for (int c = col + 1; c < m; c++)
                    {
                        s -= A[r][c] * x[c];
                    }
                    x[col] = s / A[r][col];
                }
                return new ResultadoGauss { Pasos = pasos, Estado = "única", Solucion = x.ToList() };
            }
            else
            {
                return new ResultadoGauss { Pasos = pasos, Estado = "incompleto", Solucion = null };
            }
        }
    }

    public class ResultadoGauss
    {
        public List<List<List<double>>> Pasos { get; set; }
        public string Estado { get; set; }
        public List<double> Solucion { get; set; }
        public List<int> VariablesLibres { get; set; }
    }
}