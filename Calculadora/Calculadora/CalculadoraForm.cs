using System;
using System.Collections.Generic;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Calculadora
{
    public partial class CalculadoraForm : Form
    {
        private NumericUpDown spinFilasA;
        private NumericUpDown spinColumnasA;
        private DataGridView tablaMatrizA;

        private NumericUpDown spinFilasB;
        private NumericUpDown spinColumnasB;
        private DataGridView tablaMatrizB;

        private RichTextBox pizarra;

        public CalculadoraForm()
        {
            initializeComponent();
            configurarEstilosGlobales();
        }

    private void initializeComponent()
        {
            this.SuspendLayout();

            this.Text = "Calculadora";
            this.Size = new Size(800, 700);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.BackColor = Color.FromArgb(30, 30, 30);

            TableLayoutPanel layoutPrincipal = new TableLayoutPanel();
            layoutPrincipal.Dock = DockStyle.Fill;

            layoutPrincipal.RowCount = 2;
            layoutPrincipal.ColumnCount = 2;
            layoutPrincipal.Padding = new Padding(20);

            layoutPrincipal.RowStyles.Add(new RowStyle(SizeType.Absolute, 60));
            layoutPrincipal.RowStyles.Add(new RowStyle(SizeType.Percent, 100));
            layoutPrincipal.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 60));
            layoutPrincipal.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 40));

            this.Controls.Add(layoutPrincipal);

            crearBanner(layoutPrincipal);

            TableLayoutPanel pasosPanel = new TableLayoutPanel();
            pasosPanel.Dock = DockStyle.Fill;
            pasosPanel.RowCount = 2;
            pasosPanel.ColumnCount = 1;
            pasosPanel.RowStyles.Add(new RowStyle(SizeType.Percent, 70));
            pasosPanel.RowStyles.Add(new RowStyle(SizeType.Percent, 30));
            crearPizarraResultados(pasosPanel);
            layoutPrincipal.Controls.Add(pasosPanel, 1, 1);

            TableLayoutPanel rightPanel = new TableLayoutPanel();
            rightPanel.Dock = DockStyle.Fill;
            rightPanel.RowCount = 3;
            rightPanel.ColumnCount = 1;
            rightPanel.RowStyles.Add(new RowStyle(SizeType.Percent, 45));
            rightPanel.RowStyles.Add(new RowStyle(SizeType.Percent, 45));
            rightPanel.RowStyles.Add(new RowStyle(SizeType.Absolute, 60));

            GroupBox grupoMatrizA = crearGrupoMatriz("Primera Matriz", "A");
            GroupBox grupoMatrizB = crearGrupoMatriz("Segunda Matriz", "B");
            rightPanel.Controls.Add(grupoMatrizA, 0, 0);
            rightPanel.Controls.Add(grupoMatrizB, 0, 1);
            crearBotonesOperacion(rightPanel);
            layoutPrincipal.Controls.Add(rightPanel, 0, 1);

            this.ResumeLayout(false);
        }

    private void crearBanner(TableLayoutPanel layoutPrincipal)
        {
            PictureBox bannerBox = new PictureBox();
            bannerBox.Dock = DockStyle.Fill;
            bannerBox.SizeMode = PictureBoxSizeMode.CenterImage;

            Bitmap bmp = new Bitmap(800, 60);
            using (Graphics g = Graphics.FromImage(bmp))
            {
                g.Clear(Color.FromArgb(30, 140, 255));
                using (Font f = new Font("Segoe UI", 18, FontStyle.Bold))
                using (Brush b = new SolidBrush(Color.White))
                {
                    StringFormat sf = new StringFormat();
                    sf.Alignment = StringAlignment.Center;
                    sf.LineAlignment = StringAlignment.Center;
                    g.TextRenderingHint = System.Drawing.Text.TextRenderingHint.ClearTypeGridFit;
                    g.DrawString("Matrices", f, b, new RectangleF(0, 0, bmp.Width, bmp.Height), sf);
                }
            }

            bannerBox.Image = bmp;

            layoutPrincipal.Controls.Add(bannerBox, 0, 0);
            layoutPrincipal.SetColumnSpan(bannerBox, 2);
        }

    private void crearSeccionMatrices(TableLayoutPanel layoutPrincipal)
        {
        }

    private GroupBox crearGrupoMatriz(string titulo, string idMatriz)
        {
            GroupBox grupo = new GroupBox();
            grupo.Text = titulo;
            grupo.Dock = DockStyle.Fill;
            grupo.Font = new Font("Segoe UI", 9, FontStyle.Bold);
            grupo.BackColor = Color.FromArgb(40, 40, 40);
            grupo.ForeColor = Color.White;
            grupo.Margin = new Padding(5);

            TableLayoutPanel layoutGrupo = new TableLayoutPanel();
            layoutGrupo.Dock = DockStyle.Fill;
            layoutGrupo.RowCount = 2;
            layoutGrupo.ColumnCount = 1;
            layoutGrupo.Padding = new Padding(10);
            layoutGrupo.RowStyles.Add(new RowStyle(SizeType.Absolute, 40));
            layoutGrupo.RowStyles.Add(new RowStyle(SizeType.Percent, 100));

            Panel panelDimensiones = new Panel();
            panelDimensiones.Dock = DockStyle.Fill;
            panelDimensiones.Height = 40;

            Label lblFilas = new Label();
            lblFilas.Text = "Filas:";
            lblFilas.Location = new Point(0, 12);
            lblFilas.Size = new Size(40, 20);
            lblFilas.ForeColor = Color.White;

            NumericUpDown spinFilas = new NumericUpDown();
            spinFilas.Minimum = 1;
            spinFilas.Value = 2;
            spinFilas.Location = new Point(45, 10);
            spinFilas.Size = new Size(50, 20);

            Label lblColumnas = new Label();
            lblColumnas.Text = "Columnas:";
            lblColumnas.Location = new Point(105, 12);
            lblColumnas.Size = new Size(60, 20);
            lblColumnas.ForeColor = Color.White;

            NumericUpDown spinColumnas = new NumericUpDown();
            spinColumnas.Minimum = 1;
            spinColumnas.Value = 2;
            spinColumnas.Location = new Point(170, 10);
            spinColumnas.Size = new Size(50, 20);

            Button btnCrear = new Button();
            btnCrear.Text = "Crear/Actualizar Matriz";
            btnCrear.Location = new Point(230, 8);
            btnCrear.Size = new Size(150, 25);
            btnCrear.BackColor = Color.FromArgb(30, 140, 255);
            btnCrear.ForeColor = Color.White;
            btnCrear.FlatStyle = FlatStyle.Flat;
            btnCrear.FlatAppearance.BorderSize = 0;

            panelDimensiones.Controls.AddRange(new Control[] { lblFilas, spinFilas, lblColumnas, spinColumnas, btnCrear });

            DataGridView dataGrid = new DataGridView();
            dataGrid.Dock = DockStyle.Fill;
            dataGrid.BackgroundColor = Color.FromArgb(40, 40, 40);
            dataGrid.GridColor = Color.FromArgb(30, 140, 255);
            dataGrid.DefaultCellStyle.ForeColor = Color.Black;
            dataGrid.DefaultCellStyle.BackColor = Color.White;
            dataGrid.DefaultCellStyle.SelectionForeColor = Color.Black;
            dataGrid.DefaultCellStyle.SelectionBackColor = Color.FromArgb(120, 190, 255);
            dataGrid.BorderStyle = BorderStyle.Fixed3D;
            dataGrid.AllowUserToAddRows = false;
            dataGrid.AllowUserToDeleteRows = false;
            dataGrid.RowHeadersVisible = false;
            dataGrid.ColumnHeadersVisible = false;
            dataGrid.SelectionMode = DataGridViewSelectionMode.CellSelect;

            actualizarTablaMatriz(2, 2, dataGrid);

            btnCrear.Click += (s, e) => actualizarTablaMatriz((int)spinFilas.Value, (int)spinColumnas.Value, dataGrid);

            if (idMatriz == "A")
            {
                this.spinFilasA = spinFilas;
                this.spinColumnasA = spinColumnas;
                this.tablaMatrizA = dataGrid;
            }
            else
            {
                this.spinFilasB = spinFilas;
                this.spinColumnasB = spinColumnas;
                this.tablaMatrizB = dataGrid;
            }

            layoutGrupo.Controls.Add(panelDimensiones, 0, 0);
            layoutGrupo.Controls.Add(dataGrid, 0, 1);
            grupo.Controls.Add(layoutGrupo);

            return grupo;
        }

    private void actualizarTablaMatriz(int filas, int columnas, DataGridView tabla)
        {
            tabla.Columns.Clear();
            tabla.Rows.Clear();

            for (int j = 0; j < columnas; j++)
            {
                tabla.Columns.Add($"Col{j}", $"");
                tabla.Columns[j].Width = tabla.Width / columnas - 2;
            }

            for (int i = 0; i < filas; i++)
            {
                tabla.Rows.Add();
                tabla.Rows[i].Height = Math.Max(25, (tabla.Height - 25) / filas);
            }
        }

    private void crearBotonesOperacion(TableLayoutPanel layoutPrincipal)
        {
            Panel panelBotones = new Panel
            {
                Dock = DockStyle.Fill,
                Height = 60
            };

            Button btnSumar = new Button
            {
                Text = "Sumar matrices",
                Size = new Size(120, 40),
                BackColor = Color.FromArgb(30, 140, 255),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Font = new Font("Segoe UI", 10)
            };
            btnSumar.FlatAppearance.BorderSize = 0;

            Button btnMultiplicar = new Button
            {
                Text = "Multiplicar matrices",
                Size = new Size(120, 40),
                BackColor = Color.FromArgb(30, 140, 255),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Font = new Font("Segoe UI", 10)
            };
            btnMultiplicar.FlatAppearance.BorderSize = 0;

            Button btnLimpiar = new Button
            {
                Text = "Limpiar",
                Size = new Size(120, 40),
                BackColor = Color.FromArgb(30, 140, 255),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Font = new Font("Segoe UI", 10)
            };
            btnLimpiar.FlatAppearance.BorderSize = 0;

            int spacing = 20;
            Action centrar = () =>
            {
                int totalWidth = btnSumar.Width + btnMultiplicar.Width + btnLimpiar.Width + spacing * 2;
                int startX = Math.Max(0, (panelBotones.Width - totalWidth) / 2);
                int centerY = Math.Max(0, (panelBotones.Height - btnSumar.Height) / 2);

                btnSumar.Location = new Point(startX, centerY);
                btnMultiplicar.Location = new Point(startX + btnSumar.Width + spacing, centerY);
                btnLimpiar.Location = new Point(startX + btnSumar.Width + spacing + btnMultiplicar.Width + spacing, centerY);
            };

            panelBotones.Resize += (s, e) => centrar();

            panelBotones.Controls.AddRange(new Control[] { btnSumar, btnMultiplicar, btnLimpiar });
            centrar();

            btnSumar.Click += realizarSuma;
            btnMultiplicar.Click += realizarMultiplicacion;
            btnLimpiar.Click += limpiarTodo;

            configurarEfectosHover(btnSumar);
            configurarEfectosHover(btnMultiplicar);
            configurarEfectosHover(btnLimpiar);

            layoutPrincipal.Controls.Add(panelBotones, 0, 2);
        }

    private void configurarEfectosHover(Button btn)
        {
            Color colorOriginal = btn.BackColor;
            Color colorHover = Color.FromArgb(10, 100, 200);
            Color colorPressed = Color.FromArgb(0, 80, 180);

            btn.MouseEnter += (s, e) => btn.BackColor = colorHover;
            btn.MouseLeave += (s, e) => btn.BackColor = colorOriginal;
            btn.MouseDown += (s, e) => btn.BackColor = colorPressed;
            btn.MouseUp += (s, e) => btn.BackColor = colorHover;
        }

    private void crearPizarraResultados(TableLayoutPanel layoutPrincipal)
        {
            GroupBox grupoPizarra = new GroupBox
            {
                Text = "Pasos",
                Dock = DockStyle.Fill,
                Font = new Font("Segoe UI", 9, FontStyle.Bold),
                BackColor = Color.FromArgb(40, 40, 40),
                ForeColor = Color.White,
                Margin = new Padding(5)
            };

            this.pizarra = new RichTextBox
            {
                Dock = DockStyle.Fill,
                ReadOnly = true,
                Font = new Font("Courier New", 11),
                BackColor = Color.FromArgb(30, 30, 30),
                ForeColor = Color.White,
                Margin = new Padding(10)
            };

            grupoPizarra.Controls.Add(this.pizarra);
            layoutPrincipal.Controls.Add(grupoPizarra, 0, 0);
        }

    private double[,] leerMatrizDesdeTabla(DataGridView tabla)
        {
            int filas = tabla.RowCount;
            int columnas = tabla.ColumnCount;
            double[,] matriz = new double[filas, columnas];

            for (int i = 0; i < filas; i++)
            {
                for (int j = 0; j < columnas; j++)
                {
                    string valor = tabla[j, i].Value?.ToString() ?? "";
                    if (string.IsNullOrEmpty(valor))
                    {
                        matriz[i, j] = 0.0;
                    }
                    else if (Validacion.esNumeroValido(valor))
                    {
                        matriz[i, j] = Validacion.convertirANumero(valor);
                    }
                    else
                    {
                        mostrarError("Valor no numérico", $"El valor en la celda [{i + 1}, {j + 1}] no es un número válido.");
                        return null;
                    }
                }
            }
            return matriz;
        }

        private string formatearMatrizHtml(double[,] matriz, string titulo = "")
        {
            StringBuilder html = new StringBuilder();
            if (!string.IsNullOrEmpty(titulo))
            {
                html.AppendLine($"=== {titulo} ===");
            }

            int filas = matriz.GetLength(0);
            int columnas = matriz.GetLength(1);

            for (int i = 0; i < filas; i++)
            {
                html.Append("[");
                for (int j = 0; j < columnas; j++)
                {
                    html.Append($"{matriz[i, j],8:F2}");
                    if (j < columnas - 1) html.Append("  ");
                }
                html.AppendLine("]");
            }
            html.AppendLine();
            return html.ToString();
        }

        private void realizarSuma(object sender, EventArgs e)
        {
            double[,] matrizA = leerMatrizDesdeTabla(this.tablaMatrizA);
            double[,] matrizB = leerMatrizDesdeTabla(this.tablaMatrizB);

            if (matrizA == null || matrizB == null)
                return;

            if (!Suma.validarSuma(matrizA, matrizB))
            {
                mostrarError("Error de Dimensiones", "Las matrices deben tener las mismas dimensiones para poder sumarse.");
                return;
            }

            this.pizarra.Clear();

            this.pizarra.AppendText("=== Matriz A ===\n");
            this.pizarra.AppendText(Suma.mostrarMatriz(matrizA));
            this.pizarra.AppendText("\n");

            this.pizarra.AppendText("=== Matriz B ===\n");
            this.pizarra.AppendText(Suma.mostrarMatriz(matrizB));
            this.pizarra.AppendText("\n");

            string[,] matrizOperaciones = Suma.crearMatrizOperacionesStr(matrizA, matrizB);
            this.pizarra.AppendText("=== Pasos intermedios de la suma ===\n");
            this.pizarra.AppendText(Suma.mostrarPasos(matrizOperaciones));
            this.pizarra.AppendText("\n");

            double[,] resultado = Suma.sumarMatriz(matrizA, matrizB);
            this.pizarra.AppendText("=== Resultado final de la operación ===\n");
            this.pizarra.AppendText(Suma.mostrarMatriz(resultado));
        }

        private void realizarMultiplicacion(object sender, EventArgs e)
        {
            double[,] matrizA = leerMatrizDesdeTabla(this.tablaMatrizA);
            double[,] matrizB = leerMatrizDesdeTabla(this.tablaMatrizB);

            if (matrizA == null || matrizB == null)
                return;

            if (!Multiplicacion.validarMultiplicacion(matrizA, matrizB))
            {
                mostrarError("Error de Dimensiones",
                    "El número de columnas de la Matriz A debe ser igual al número de filas de la Matriz B.");
                return;
            }

            this.pizarra.Clear();

            this.pizarra.AppendText("=== Matriz A ===\n");
            this.pizarra.AppendText(Suma.mostrarMatriz(matrizA));
            this.pizarra.AppendText("\n");

            this.pizarra.AppendText("=== Matriz B ===\n");
            this.pizarra.AppendText(Suma.mostrarMatriz(matrizB));
            this.pizarra.AppendText("\n");

            List<string> pasos = Multiplicacion.crearPasosMultiplicacion(matrizA, matrizB);
            this.pizarra.AppendText("=== Pasos del Cálculo ===\n");
            foreach (string paso in pasos)
            {
                this.pizarra.AppendText(paso + "\n");
            }
            this.pizarra.AppendText("\n");

            double[,] resultado = Multiplicacion.multiplicarMatrices(matrizA, matrizB);
            this.pizarra.AppendText("=== Resultado Final ===\n");
            this.pizarra.AppendText(Suma.mostrarMatriz(resultado));
        }

    private void limpiarTodo(object sender, EventArgs e)
        {
            for (int i = 0; i < this.tablaMatrizA.RowCount; i++)
            {
                for (int j = 0; j < this.tablaMatrizA.ColumnCount; j++)
                {
                    this.tablaMatrizA[j, i].Value = "";
                }
            }

            for (int i = 0; i < this.tablaMatrizB.RowCount; i++)
            {
                for (int j = 0; j < this.tablaMatrizB.ColumnCount; j++)
                {
                    this.tablaMatrizB[j, i].Value = "";
                }
            }

            this.pizarra.Clear();
        }

        private void mostrarError(string titulo, string mensaje)
        {
            MessageBox.Show(mensaje, titulo, MessageBoxButtons.OK, MessageBoxIcon.Error);
        }

        private void configurarEstilosGlobales()
        {
            this.BackColor = Color.FromArgb(30, 30, 30);
            this.ForeColor = Color.White;
        }
    }
}
