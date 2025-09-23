using System;
using System.Collections.Generic;
using System.Drawing;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace Calculadora
{
    public partial class FormularioPrincipal : Form
    {
        private TextBox[,] entradasA;
        private TextBox[,] entradasB;
        private List<TextBox> gridFrameA = new List<TextBox>();
        private List<TextBox> gridFrameB = new List<TextBox>();
        private string seccionActual = null;
        private Timer timerFechaHora;

        public FormularioPrincipal()
        {
            InitializeComponent();
            InicializarComponentesPersonalizados();
            MostrarSeccion("Álgebra Lineal");
            ActualizarFechaHora();
        }

        private void InicializarComponentesPersonalizados()
        {
            // Configurar timer para fecha y hora
            timerFechaHora = new Timer();
            timerFechaHora.Interval = 1000;
            timerFechaHora.Tick += TimerFechaHora_Tick;
            timerFechaHora.Start();
        }

        private void TimerFechaHora_Tick(object sender, EventArgs e)
        {
            ActualizarFechaHora();
        }

        private void ActualizarFechaHora()
        {
            DateTime ahora = DateTime.Now;
            string[] diasSemana = { "Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado" };
            string[] meses = { "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                              "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre" };
            
            string formateado = $"{diasSemana[(int)ahora.DayOfWeek]}, {ahora.Day} {meses[ahora.Month]} {ahora.Year} | {ahora:HH:mm:ss}";
            lblFechaHora.Text = formateado;
        }

        private void MostrarSeccion(string nombre)
        {
            seccionActual = nombre;
            lblTituloSeccion.Text = nombre;

            // Limpiar área de contenido
            foreach (Control control in panelContenido.Controls.OfType<Control>().ToList())
            {
                if (control != lblTituloSeccion && control != lblFechaHora)
                {
                    panelContenido.Controls.Remove(control);
                    control.Dispose();
                }
            }

            if (nombre == "Álgebra Lineal")
            {
                CrearInterfazCalculadoraMatrices();
            }
            else
            {
                Label lbl = new Label
                {
                    Text = $"Has seleccionado: {nombre}\n\nContenido de ejemplo para la sección.",
                    Location = new Point(12, 60),
                    Size = new Size(400, 100),
                    Font = new Font("Segoe UI", 10)
                };
                panelContenido.Controls.Add(lbl);
            }
        }

        private void CrearInterfazCalculadoraMatrices()
        {
            // Panel superior con controles
            Panel panelSuperior = new Panel
            {
                Location = new Point(12, 60),
                Size = new Size(760, 40),
                BackColor = Color.FromArgb(240, 240, 240),
                BorderStyle = BorderStyle.FixedSingle
            };

            Label lblFilas = new Label
            {
                Text = "Filas:",
                Location = new Point(8, 12),
                Size = new Size(40, 20),
                Font = new Font("Segoe UI", 9)
            };

            NumericUpDown nudFilas = new NumericUpDown
            {
                Name = "nudFilas",
                Location = new Point(50, 10),
                Size = new Size(60, 20),
                Value = 2,
                Minimum = 1,
                Maximum = 10
            };

            Label lblColumnas = new Label
            {
                Text = "Columnas:",
                Location = new Point(120, 12),
                Size = new Size(60, 20),
                Font = new Font("Segoe UI", 9)
            };

            NumericUpDown nudColumnas = new NumericUpDown
            {
                Name = "nudColumnas",
                Location = new Point(185, 10),
                Size = new Size(60, 20),
                Value = 2,
                Minimum = 1,
                Maximum = 10
            };

            ComboBox cmbOperacion = new ComboBox
            {
                Name = "cmbOperacion",
                Location = new Point(255, 10),
                Size = new Size(150, 20),
                DropDownStyle = ComboBoxStyle.DropDownList
            };
            cmbOperacion.Items.AddRange(new string[] { "Suma", "Resta", "Multiplicación", "Gauss/Gauss-Jordan" });
            cmbOperacion.SelectedIndex = 0;
            cmbOperacion.SelectedIndexChanged += CmbOperacion_SelectedIndexChanged;

            ComboBox cmbModoGauss = new ComboBox
            {
                Name = "cmbModoGauss",
                Location = new Point(415, 10),
                Size = new Size(100, 20),
                DropDownStyle = ComboBoxStyle.DropDownList,
                Visible = false
            };
            cmbModoGauss.Items.AddRange(new string[] { "Gauss", "Gauss-Jordan" });
            cmbModoGauss.SelectedIndex = 1;

            Button btnGenerar = new Button
            {
                Text = "Generar matrices",
                Location = new Point(525, 8),
                Size = new Size(120, 25),
                Font = new Font("Segoe UI", 9),
                BackColor = Color.FromArgb(0, 120, 215),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat
            };
            btnGenerar.Click += BtnGenerar_Click;

            panelSuperior.Controls.AddRange(new Control[] { lblFilas, nudFilas, lblColumnas, nudColumnas, cmbOperacion, cmbModoGauss, btnGenerar });
            panelContenido.Controls.Add(panelSuperior);

            // Panel medio con matrices
            Panel panelMedio = new Panel
            {
                Location = new Point(12, 110),
                Size = new Size(760, 150),
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle
            };

            // Frame Matriz A
            Panel frameA = new Panel
            {
                Name = "frameA",
                Location = new Point(5, 5),
                Size = new Size(370, 140),
                BackColor = Color.FromArgb(248, 248, 248),
                BorderStyle = BorderStyle.FixedSingle
            };

            Label lblMatrizA = new Label
            {
                Text = "Matriz A",
                Location = new Point(8, 8),
                Size = new Size(60, 20),
                Font = new Font("Segoe UI", 10, FontStyle.Bold)
            };

            TextBox txtMatrizA = new TextBox
            {
                Name = "txtMatrizA",
                Location = new Point(8, 30),
                Size = new Size(350, 60),
                Multiline = true,
                ScrollBars = ScrollBars.Both,
                Font = new Font("Consolas", 9)
            };

            Button btnLeerA = new Button
            {
                Text = "Leer desde texto",
                Location = new Point(8, 100),
                Size = new Size(120, 25),
                Font = new Font("Segoe UI", 9),
                BackColor = Color.FromArgb(0, 120, 215),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat
            };
            btnLeerA.Click += (s, e) => LeerMatrizDesdeTexto("A");

            frameA.Controls.AddRange(new Control[] { lblMatrizA, txtMatrizA, btnLeerA });

            // Frame Matriz B
            Panel frameB = new Panel
            {
                Name = "frameB",
                Location = new Point(385, 5),
                Size = new Size(370, 140),
                BackColor = Color.FromArgb(248, 248, 248),
                BorderStyle = BorderStyle.FixedSingle
            };

            Label lblMatrizB = new Label
            {
                Text = "Matriz B",
                Location = new Point(8, 8),
                Size = new Size(60, 20),
                Font = new Font("Segoe UI", 10, FontStyle.Bold)
            };

            TextBox txtMatrizB = new TextBox
            {
                Name = "txtMatrizB",
                Location = new Point(8, 30),
                Size = new Size(350, 60),
                Multiline = true,
                ScrollBars = ScrollBars.Both,
                Font = new Font("Consolas", 9)
            };

            Button btnLeerB = new Button
            {
                Text = "Leer desde texto",
                Location = new Point(8, 100),
                Size = new Size(120, 25),
                Font = new Font("Segoe UI", 9),
                BackColor = Color.FromArgb(0, 120, 215),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat
            };
            btnLeerB.Click += (s, e) => LeerMatrizDesdeTexto("B");

            frameB.Controls.AddRange(new Control[] { lblMatrizB, txtMatrizB, btnLeerB });

            panelMedio.Controls.AddRange(new Control[] { frameA, frameB });
            panelContenido.Controls.Add(panelMedio);

            // Panel de controles
            Panel panelControles = new Panel
            {
                Location = new Point(12, 270),
                Size = new Size(760, 40),
                BackColor = Color.FromArgb(240, 240, 240),
                BorderStyle = BorderStyle.FixedSingle
            };

            Button btnCalcular = new Button
            {
                Text = "Calcular",
                Location = new Point(10, 8),
                Size = new Size(80, 25),
                Font = new Font("Segoe UI", 9),
                BackColor = Color.FromArgb(0, 120, 215),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat
            };
            btnCalcular.Click += BtnCalcular_Click;

            Button btnLimpiar = new Button
            {
                Text = "Limpiar",
                Location = new Point(100, 8),
                Size = new Size(80, 25),
                Font = new Font("Segoe UI", 9),
                BackColor = Color.FromArgb(120, 120, 120),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat
            };
            btnLimpiar.Click += BtnLimpiar_Click;

            panelControles.Controls.AddRange(new Control[] { btnCalcular, btnLimpiar });
            panelContenido.Controls.Add(panelControles);

            // Panel inferior con pasos y resultado
            Panel panelInferior = new Panel
            {
                Location = new Point(12, 320),
                Size = new Size(760, 220),
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle
            };

            // Frame Pasos
            Panel framePasos = new Panel
            {
                Name = "framePasos",
                Location = new Point(5, 5),
                Size = new Size(370, 210),
                BackColor = Color.FromArgb(248, 248, 248),
                BorderStyle = BorderStyle.FixedSingle
            };

            Label lblPasos = new Label
            {
                Text = "Pasos:",
                Location = new Point(8, 8),
                Size = new Size(50, 20),
                Font = new Font("Segoe UI", 10, FontStyle.Bold)
            };

            TextBox txtPasos = new TextBox
            {
                Name = "txtPasos",
                Location = new Point(8, 30),
                Size = new Size(350, 170),
                Multiline = true,
                ScrollBars = ScrollBars.Both,
                ReadOnly = true,
                Font = new Font("Consolas", 8)
            };

            framePasos.Controls.AddRange(new Control[] { lblPasos, txtPasos });

            // Frame Resultado
            Panel frameResultado = new Panel
            {
                Name = "frameResultado",
                Location = new Point(385, 5),
                Size = new Size(370, 210),
                BackColor = Color.FromArgb(248, 248, 248),
                BorderStyle = BorderStyle.FixedSingle
            };

            Label lblResultado = new Label
            {
                Text = "Resultado:",
                Location = new Point(8, 8),
                Size = new Size(70, 20),
                Font = new Font("Segoe UI", 10, FontStyle.Bold)
            };

            TextBox txtResultado = new TextBox
            {
                Name = "txtResultado",
                Location = new Point(8, 30),
                Size = new Size(350, 170),
                Multiline = true,
                ScrollBars = ScrollBars.Both,
                ReadOnly = true,
                Font = new Font("Consolas", 9)
            };

            frameResultado.Controls.AddRange(new Control[] { lblResultado, txtResultado });

            panelInferior.Controls.AddRange(new Control[] { framePasos, frameResultado });
            panelContenido.Controls.Add(panelInferior);
        }

        private void CmbOperacion_SelectedIndexChanged(object sender, EventArgs e)
        {
            ComboBox cmb = sender as ComboBox;
            ComboBox cmbModoGauss = panelContenido.Controls.Find("cmbModoGauss", true).FirstOrDefault() as ComboBox;
            Panel frameB = panelContenido.Controls.Find("frameB", true).FirstOrDefault() as Panel;

            if (cmb.SelectedItem.ToString() == "Gauss/Gauss-Jordan")
            {
                if (cmbModoGauss != null) cmbModoGauss.Visible = true;
                if (frameB != null) frameB.Visible = false;
            }
            else
            {
                if (cmbModoGauss != null) cmbModoGauss.Visible = false;
                if (frameB != null) frameB.Visible = true;
            }
        }

        private void BtnGenerar_Click(object sender, EventArgs e)
        {
            NumericUpDown nudFilas = panelContenido.Controls.Find("nudFilas", true).FirstOrDefault() as NumericUpDown;
            NumericUpDown nudColumnas = panelContenido.Controls.Find("nudColumnas", true).FirstOrDefault() as NumericUpDown;
            ComboBox cmbOperacion = panelContenido.Controls.Find("cmbOperacion", true).FirstOrDefault() as ComboBox;
            TextBox txtResultado = panelContenido.Controls.Find("txtResultado", true).FirstOrDefault() as TextBox;

            if (nudFilas == null || nudColumnas == null || cmbOperacion == null || txtResultado == null)
                return;

            try
            {
                int filas = (int)nudFilas.Value;
                int columnas = (int)nudColumnas.Value;

                if (filas <= 0 || columnas <= 0)
                    throw new ArgumentException();

                GenerarGrillasMatrices(filas, columnas, cmbOperacion.SelectedItem.ToString());

                txtResultado.Clear();
                txtResultado.Text = "Matrices listas. Puedes completar las entradas o pegar texto y usar \"Leer desde texto\".";
            }
            catch
            {
                TextBox txtResultado2 = panelContenido.Controls.Find("txtResultado", true).FirstOrDefault() as TextBox;
                if (txtResultado2 != null)
                {
                    txtResultado2.Clear();
                    txtResultado2.Text = "Filas y columnas deben ser enteros positivos.";
                }
            }
        }

        private void GenerarGrillasMatrices(int filas, int columnas, string operacion)
        {
            // Limpiar grillas existentes
            foreach (var txt in gridFrameA)
                txt.Dispose();
            foreach (var txt in gridFrameB)
                txt.Dispose();

            gridFrameA.Clear();
            gridFrameB.Clear();

            Panel frameA = panelContenido.Controls.Find("frameA", true).FirstOrDefault() as Panel;
            Panel frameB = panelContenido.Controls.Find("frameB", true).FirstOrDefault() as Panel;

            if (frameA == null) return;

            entradasA = new TextBox[filas, columnas];

            // Crear entradas para matriz A
            for (int r = 0; r < filas; r++)
            {
                for (int c = 0; c < columnas; c++)
                {
                    TextBox txt = new TextBox
                    {
                        Location = new Point(8 + c * 65, 130 + r * 25),
                        Size = new Size(60, 20),
                        Font = new Font("Consolas", 9),
                        TextAlign = HorizontalAlignment.Center
                    };
                    frameA.Controls.Add(txt);
                    gridFrameA.Add(txt);
                    entradasA[r, c] = txt;
                }
            }

            // Solo crear entradas para matriz B si no es modo Gauss
            if (operacion != "Gauss/Gauss-Jordan" && frameB != null)
            {
                entradasB = new TextBox[filas, columnas];
                for (int r = 0; r < filas; r++)
                {
                    for (int c = 0; c < columnas; c++)
                    {
                        TextBox txt = new TextBox
                        {
                            Location = new Point(8 + c * 65, 130 + r * 25),
                            Size = new Size(60, 20),
                            Font = new Font("Consolas", 9),
                            TextAlign = HorizontalAlignment.Center
                        };
                        frameB.Controls.Add(txt);
                        gridFrameB.Add(txt);
                        entradasB[r, c] = txt;
                    }
                }
            }
        }

        private List<List<double>> ParsearEntradasMatriz(TextBox[,] entradas)
        {
            if (entradas == null) return new List<List<double>>();

            int filas = entradas.GetLength(0);
            int columnas = entradas.GetLength(1);
            var matriz = new List<List<double>>();

            for (int i = 0; i < filas; i++)
            {
                var fila = new List<double>();
                for (int j = 0; j < columnas; j++)
                {
                    string txt = entradas[i, j].Text.Trim();
                    if (string.IsNullOrEmpty(txt))
                    {
                        fila.Add(0.0);
                    }
                    else
                    {
                        if (!double.TryParse(txt, NumberStyles.Float, CultureInfo.InvariantCulture, out double val))
                            throw new ArgumentException($"Valor inválido en ({i + 1},{j + 1}): \"{txt}\"");
                        fila.Add(val);
                    }
                }
                matriz.Add(fila);
            }

            return matriz;
        }

        private void LeerMatrizDesdeTexto(string cual)
        {
            ComboBox cmbOperacion = panelContenido.Controls.Find("cmbOperacion", true).FirstOrDefault() as ComboBox;
            TextBox txtResultado = panelContenido.Controls.Find("txtResultado", true).FirstOrDefault() as TextBox;

            if (cmbOperacion?.SelectedItem.ToString() == "Gauss/Gauss-Jordan" && cual == "B")
            {
                if (txtResultado != null)
                {
                    txtResultado.Clear();
                    txtResultado.Text = "En modo Gauss/Gauss-Jordan sólo se permite una matriz (Matriz A).";
                }
                return;
            }

            TextBox txtObjetivo = panelContenido.Controls.Find(cual == "A" ? "txtMatrizA" : "txtMatrizB", true).FirstOrDefault() as TextBox;
            if (txtObjetivo == null) return;

            string contenido = txtObjetivo.Text.Trim();
            if (string.IsNullOrEmpty(contenido))
            {
                if (txtResultado != null)
                {
                    txtResultado.Clear();
                    txtResultado.Text = "Texto vacío para la matriz.";
                }
                return;
            }

            try
            {
                var lineas = contenido.Split(new[] { '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries)
                                    .Where(ln => !string.IsNullOrWhiteSpace(ln)).ToArray();

                var matriz = new List<List<double>>();
                foreach (var ln in lineas)
                {
                    var partes = ln.Replace(',', ' ').Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries);
                    var fila = new List<double>();
                    foreach (var p in partes)
                    {
                        if (!double.TryParse(p, NumberStyles.Float, CultureInfo.InvariantCulture, out double val))
                        {
                            if (txtResultado != null)
                            {
                                txtResultado.Clear();
                                txtResultado.Text = $"Valor inválido al parsear: {p}";
                            }
                            return;
                        }
                        fila.Add(val);
                    }
                    matriz.Add(fila);
                }

                // Verificar que sea rectangular
                if (matriz.Any(r => r.Count != matriz[0].Count))
                {
                    if (txtResultado != null)
                    {
                        txtResultado.Clear();
                        txtResultado.Text = "La matriz no es rectangular (filas con distinta cantidad de columnas).";
                    }
                    return;
                }

                int filas = matriz.Count;
                int columnas = matriz[0].Count;

                // Actualizar controles y regenerar grillas
                NumericUpDown nudFilas = panelContenido.Controls.Find("nudFilas", true).FirstOrDefault() as NumericUpDown;
                NumericUpDown nudColumnas = panelContenido.Controls.Find("nudColumnas", true).FirstOrDefault() as NumericUpDown;

                if (nudFilas != null) nudFilas.Value = filas;
                if (nudColumnas != null) nudColumnas.Value = columnas;

                GenerarGrillasMatrices(filas, columnas, cmbOperacion?.SelectedItem.ToString() ?? "Suma");

                // Poblar entradas
                var entradas = cual == "A" ? entradasA : entradasB;
                if (entradas != null)
                {
                    for (int i = 0; i < filas; i++)
                    {
                        for (int j = 0; j < columnas; j++)
                        {
                            entradas[i, j].Text = matriz[i][j].ToString(CultureInfo.InvariantCulture);
                        }
                    }
                }

                if (txtResultado != null)
                {
                    txtResultado.Clear();
                    txtResultado.Text = $"Matriz {cual} leída ({filas}x{columnas}).";
                }
            }
            catch (Exception ex)
            {
                if (txtResultado != null)
                {
                    txtResultado.Clear();
                    txtResultado.Text = $"Error al poblar entradas: {ex.Message}";
                }
            }
        }

        private void BtnCalcular_Click(object sender, EventArgs e)
        {
            ComboBox cmbOperacion = panelContenido.Controls.Find("cmbOperacion", true).FirstOrDefault() as ComboBox;
            ComboBox cmbModoGauss = panelContenido.Controls.Find("cmbModoGauss", true).FirstOrDefault() as ComboBox;
            TextBox txtPasos = panelContenido.Controls.Find("txtPasos", true).FirstOrDefault() as TextBox;
            TextBox txtResultado = panelContenido.Controls.Find("txtResultado", true).FirstOrDefault() as TextBox;

            if (cmbOperacion == null || txtResultado == null) return;

            string operacion = cmbOperacion.SelectedItem.ToString();

            // Para métodos Gauss solo necesitamos una matriz (usar A)
            if (operacion == "Gauss/Gauss-Jordan")
            {
                string modo = cmbModoGauss?.SelectedItem?.ToString() ?? "Gauss-Jordan";
                try
                {
                    var A = ParsearEntradasMatriz(entradasA);
                    ResultadoGauss resultado;

                    if (modo == "Gauss")
                        resultado = AlgebraLineal.PasosGauss(A);
                    else
                        resultado = AlgebraLineal.PasosGaussJordan(A);

                    // Mostrar pasos
                    if (txtPasos != null)
                    {
                        txtPasos.Clear();
                        for (int i = 0; i < resultado.Pasos.Count; i++)
                        {
                            txtPasos.AppendText($"Paso {i}:\r\n");
                            foreach (var fila in resultado.Pasos[i])
                            {
                                txtPasos.AppendText(string.Join("  ", fila.Select(v => AlgebraLineal.FormatearNumero(v))) + "\r\n");
                            }
                            txtPasos.AppendText("\r\n");
                        }
                    }

                    // Mostrar estado/solución
                    txtResultado.Clear();
                    if (resultado.Estado == "única" && resultado.Solucion != null)
                    {
                        txtResultado.Text = "Solución única:\r\n";
                        for (int i = 0; i < resultado.Solucion.Count; i++)
                        {
                            txtResultado.AppendText($"x{i + 1} = {AlgebraLineal.FormatearNumero(resultado.Solucion[i])}\r\n");
                        }
                    }
                    else if (resultado.Estado == "inconsistente")
                    {
                        txtResultado.Text = "El sistema es inconsistente (sin solución).";
                    }
                    else if (resultado.Estado == "infinitas")
                    {
                        txtResultado.Text = "El sistema tiene infinitas soluciones (variables libres).";
                    }
                    else
                    {
                        txtResultado.Text = $"Estado: {resultado.Estado}";
                    }
                }
                catch (Exception ex)
                {
                    txtResultado.Clear();
                    txtResultado.Text = $"Error: {ex.Message}";
                }
                return;
            }

            // Operaciones binarias entre matrices A y B
            try
            {
                var A = ParsearEntradasMatriz(entradasA);
                var B = ParsearEntradasMatriz(entradasB);

                int filaA = A.Count;
                int colA = filaA > 0 ? A[0].Count : 0;
                int filaB = B.Count;
                int colB = filaB > 0 ? B[0].Count : 0;

                List<List<double>> resultado = null;

                if (operacion == "Suma" || operacion == "Resta")
                {
                    if (filaA != filaB || colA != colB)
                        throw new ArgumentException("Para suma/resta ambas matrices deben tener las mismas dimensiones.");

                    resultado = new List<List<double>>();
                    for (int i = 0; i < filaA; i++)
                    {
                        var fila = new List<double>();
                        for (int j = 0; j < colA; j++)
                        {
                            if (operacion == "Suma")
                                fila.Add(A[i][j] + B[i][j]);
                            else
                                fila.Add(A[i][j] - B[i][j]);
                        }
                        resultado.Add(fila);
                    }
                }
                else if (operacion == "Multiplicación")
                {
                    if (colA != filaB)
                        throw new ArgumentException("Para multiplicación A.columnas debe ser igual a B.filas (A.cols == B.rows).");

                    resultado = new List<List<double>>();
                    for (int i = 0; i < filaA; i++)
                    {
                        var fila = new List<double>();
                        for (int j = 0; j < colB; j++)
                        {
                            double suma = 0;
                            for (int k = 0; k < colA; k++)
                            {
                                suma += A[i][k] * B[k][j];
                            }
                            fila.Add(suma);
                        }
                        resultado.Add(fila);
                    }
                }
                else
                {
                    throw new ArgumentException("Operación desconocida");
                }

                // Mostrar resultado
                var lineasSalida = new List<string>();
                foreach (var fila in resultado)
                {
                    lineasSalida.Add(string.Join("  ", fila.Select(v => AlgebraLineal.FormatearNumero(v))));
                }

                txtResultado.Clear();
                txtResultado.Text = string.Join("\r\n", lineasSalida);
            }
            catch (Exception ex)
            {
                txtResultado.Clear();
                txtResultado.Text = $"Error: {ex.Message}";
            }
        }

        private void BtnLimpiar_Click(object sender, EventArgs e)
        {
            // Limpiar grillas de entrada y cuadros de texto
            try
            {
                if (entradasA != null)
                {
                    for (int i = 0; i < entradasA.GetLength(0); i++)
                    {
                        for (int j = 0; j < entradasA.GetLength(1); j++)
                        {
                            entradasA[i, j].Clear();
                        }
                    }
                }

                if (entradasB != null)
                {
                    for (int i = 0; i < entradasB.GetLength(0); i++)
                    {
                        for (int j = 0; j < entradasB.GetLength(1); j++)
                        {
                            entradasB[i, j].Clear();
                        }
                    }
                }

                TextBox txtMatrizA = panelContenido.Controls.Find("txtMatrizA", true).FirstOrDefault() as TextBox;
                TextBox txtMatrizB = panelContenido.Controls.Find("txtMatrizB", true).FirstOrDefault() as TextBox;
                TextBox txtResultado = panelContenido.Controls.Find("txtResultado", true).FirstOrDefault() as TextBox;
                TextBox txtPasos = panelContenido.Controls.Find("txtPasos", true).FirstOrDefault() as TextBox;

                txtMatrizA?.Clear();
                txtMatrizB?.Clear();
                txtResultado?.Clear();
                txtPasos?.Clear();
            }
            catch { }
        }

        private void BtnMatematicaBasica_Click(object sender, EventArgs e)
        {
            MostrarSeccion("Matemática Básica");
        }

        private void BtnCalculo_Click(object sender, EventArgs e)
        {
            MostrarSeccion("Cálculo");
        }

        private void BtnCalculo2_Click(object sender, EventArgs e)
        {
            MostrarSeccion("Cálculo II");
        }

        private void BtnAlgebraLineal_Click(object sender, EventArgs e)
        {
            MostrarSeccion("Álgebra Lineal");
        }

        private void BtnConfiguracion_Click(object sender, EventArgs e)
        {
            MostrarSeccion("Configuración");
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                timerFechaHora?.Stop();
                timerFechaHora?.Dispose();
            }
            base.Dispose(disposing);
        }
    }
}