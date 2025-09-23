namespace Calculadora
{
    partial class FormularioPrincipal
    {
        private System.ComponentModel.IContainer components = null;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            this.panelNavegacion = new System.Windows.Forms.Panel();
            this.lblTituloMenu = new System.Windows.Forms.Label();
            this.btnMatematicaBasica = new System.Windows.Forms.Button();
            this.btnCalculo = new System.Windows.Forms.Button();
            this.btnCalculo2 = new System.Windows.Forms.Button();
            this.btnAlgebraLineal = new System.Windows.Forms.Button();
            this.btnConfiguracion = new System.Windows.Forms.Button();
            this.panelContenido = new System.Windows.Forms.Panel();
            this.panelEncabezado = new System.Windows.Forms.Panel();
            this.lblTituloSeccion = new System.Windows.Forms.Label();
            this.lblFechaHora = new System.Windows.Forms.Label();
            this.panelNavegacion.SuspendLayout();
            this.panelContenido.SuspendLayout();
            this.panelEncabezado.SuspendLayout();
            this.SuspendLayout();
            // 
            // panelNavegacion
            // 
            this.panelNavegacion.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(45)))), ((int)(((byte)(45)))), ((int)(((byte)(48)))));
            this.panelNavegacion.Controls.Add(this.lblTituloMenu);
            this.panelNavegacion.Controls.Add(this.btnMatematicaBasica);
            this.panelNavegacion.Controls.Add(this.btnCalculo);
            this.panelNavegacion.Controls.Add(this.btnCalculo2);
            this.panelNavegacion.Controls.Add(this.btnAlgebraLineal);
            this.panelNavegacion.Controls.Add(this.btnConfiguracion);
            this.panelNavegacion.Dock = System.Windows.Forms.DockStyle.Left;
            this.panelNavegacion.Location = new System.Drawing.Point(0, 0);
            this.panelNavegacion.Name = "panelNavegacion";
            this.panelNavegacion.Size = new System.Drawing.Size(220, 600);
            this.panelNavegacion.TabIndex = 0;
            // 
            // lblTituloMenu
            // 
            this.lblTituloMenu.AutoSize = true;
            this.lblTituloMenu.Font = new System.Drawing.Font("Segoe UI", 18F, System.Drawing.FontStyle.Bold);
            this.lblTituloMenu.ForeColor = System.Drawing.Color.White;
            this.lblTituloMenu.Location = new System.Drawing.Point(12, 12);
            this.lblTituloMenu.Name = "lblTituloMenu";
            this.lblTituloMenu.Size = new System.Drawing.Size(73, 32);
            this.lblTituloMenu.TabIndex = 0;
            this.lblTituloMenu.Text = "Menú";
            // 
            // btnMatematicaBasica
            // 
            this.btnMatematicaBasica.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(120)))), ((int)(((byte)(215)))));
            this.btnMatematicaBasica.FlatAppearance.BorderSize = 0;
            this.btnMatematicaBasica.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btnMatematicaBasica.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.btnMatematicaBasica.ForeColor = System.Drawing.Color.White;
            this.btnMatematicaBasica.Location = new System.Drawing.Point(12, 60);
            this.btnMatematicaBasica.Name = "btnMatematicaBasica";
            this.btnMatematicaBasica.Size = new System.Drawing.Size(196, 35);
            this.btnMatematicaBasica.TabIndex = 1;
            this.btnMatematicaBasica.Text = "  Matemática Básica";
            this.btnMatematicaBasica.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.btnMatematicaBasica.UseVisualStyleBackColor = false;
            this.btnMatematicaBasica.Click += new System.EventHandler(this.BtnMatematicaBasica_Click);
            // 
            // btnCalculo
            // 
            this.btnCalculo.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(120)))), ((int)(((byte)(215)))));
            this.btnCalculo.FlatAppearance.BorderSize = 0;
            this.btnCalculo.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btnCalculo.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.btnCalculo.ForeColor = System.Drawing.Color.White;
            this.btnCalculo.Location = new System.Drawing.Point(12, 101);
            this.btnCalculo.Name = "btnCalculo";
            this.btnCalculo.Size = new System.Drawing.Size(196, 35);
            this.btnCalculo.TabIndex = 2;
            this.btnCalculo.Text = "  Cálculo";
            this.btnCalculo.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.btnCalculo.UseVisualStyleBackColor = false;
            this.btnCalculo.Click += new System.EventHandler(this.BtnCalculo_Click);
            // 
            // btnCalculo2
            // 
            this.btnCalculo2.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(120)))), ((int)(((byte)(215)))));
            this.btnCalculo2.FlatAppearance.BorderSize = 0;
            this.btnCalculo2.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btnCalculo2.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.btnCalculo2.ForeColor = System.Drawing.Color.White;
            this.btnCalculo2.Location = new System.Drawing.Point(12, 142);
            this.btnCalculo2.Name = "btnCalculo2";
            this.btnCalculo2.Size = new System.Drawing.Size(196, 35);
            this.btnCalculo2.TabIndex = 3;
            this.btnCalculo2.Text = "  Cálculo II";
            this.btnCalculo2.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.btnCalculo2.UseVisualStyleBackColor = false;
            this.btnCalculo2.Click += new System.EventHandler(this.BtnCalculo2_Click);
            // 
            // btnAlgebraLineal
            // 
            this.btnAlgebraLineal.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(120)))), ((int)(((byte)(215)))));
            this.btnAlgebraLineal.FlatAppearance.BorderSize = 0;
            this.btnAlgebraLineal.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btnAlgebraLineal.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.btnAlgebraLineal.ForeColor = System.Drawing.Color.White;
            this.btnAlgebraLineal.Location = new System.Drawing.Point(12, 183);
            this.btnAlgebraLineal.Name = "btnAlgebraLineal";
            this.btnAlgebraLineal.Size = new System.Drawing.Size(196, 35);
            this.btnAlgebraLineal.TabIndex = 4;
            this.btnAlgebraLineal.Text = "  Álgebra Lineal";
            this.btnAlgebraLineal.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.btnAlgebraLineal.UseVisualStyleBackColor = false;
            this.btnAlgebraLineal.Click += new System.EventHandler(this.BtnAlgebraLineal_Click);
            // 
            // btnConfiguracion
            // 
            this.btnConfiguracion.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(120)))), ((int)(((byte)(215)))));
            this.btnConfiguracion.FlatAppearance.BorderSize = 0;
            this.btnConfiguracion.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btnConfiguracion.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.btnConfiguracion.ForeColor = System.Drawing.Color.White;
            this.btnConfiguracion.Location = new System.Drawing.Point(12, 224);
            this.btnConfiguracion.Name = "btnConfiguracion";
            this.btnConfiguracion.Size = new System.Drawing.Size(196, 35);
            this.btnConfiguracion.TabIndex = 5;
            this.btnConfiguracion.Text = "  Configuración";
            this.btnConfiguracion.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.btnConfiguracion.UseVisualStyleBackColor = false;
            this.btnConfiguracion.Click += new System.EventHandler(this.BtnConfiguracion_Click);
            // 
            // panelContenido
            // 
            this.panelContenido.BackColor = System.Drawing.Color.White;
            this.panelContenido.Controls.Add(this.panelEncabezado);
            this.panelContenido.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panelContenido.Location = new System.Drawing.Point(220, 0);
            this.panelContenido.Name = "panelContenido";
            this.panelContenido.Padding = new System.Windows.Forms.Padding(12);
            this.panelContenido.Size = new System.Drawing.Size(680, 600);
            this.panelContenido.TabIndex = 1;
            // 
            // panelEncabezado
            // 
            this.panelEncabezado.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(240)))), ((int)(((byte)(240)))), ((int)(((byte)(240)))));
            this.panelEncabezado.Controls.Add(this.lblTituloSeccion);
            this.panelEncabezado.Controls.Add(this.lblFechaHora);
            this.panelEncabezado.Dock = System.Windows.Forms.DockStyle.Top;
            this.panelEncabezado.Location = new System.Drawing.Point(12, 12);
            this.panelEncabezado.Name = "panelEncabezado";
            this.panelEncabezado.Size = new System.Drawing.Size(656, 40);
            this.panelEncabezado.TabIndex = 0;
            // 
            // lblTituloSeccion
            // 
            this.lblTituloSeccion.AutoSize = true;
            this.lblTituloSeccion.Font = new System.Drawing.Font("Segoe UI", 20F, System.Drawing.FontStyle.Bold);
            this.lblTituloSeccion.Location = new System.Drawing.Point(10, 5);
            this.lblTituloSeccion.Name = "lblTituloSeccion";
            this.lblTituloSeccion.Size = new System.Drawing.Size(0, 37);
            this.lblTituloSeccion.TabIndex = 0;
            // 
            // lblFechaHora
            // 
            this.lblFechaHora.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.lblFechaHora.Font = new System.Drawing.Font("Segoe UI", 11F);
            this.lblFechaHora.Location = new System.Drawing.Point(400, 10);
            this.lblFechaHora.Name = "lblFechaHora";
            this.lblFechaHora.Size = new System.Drawing.Size(250, 20);
            this.lblFechaHora.TabIndex = 1;
            this.lblFechaHora.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // FormularioPrincipal
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(900, 600);
            this.Controls.Add(this.panelContenido);
            this.Controls.Add(this.panelNavegacion);
            this.MinimumSize = new System.Drawing.Size(800, 500);
            this.Name = "FormularioPrincipal";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Menú Principal Mathpro";
            this.panelNavegacion.ResumeLayout(false);
            this.panelNavegacion.PerformLayout();
            this.panelContenido.ResumeLayout(false);
            this.panelEncabezado.ResumeLayout(false);
            this.panelEncabezado.PerformLayout();
            this.ResumeLayout(false);
        }

        private System.Windows.Forms.Panel panelNavegacion;
        private System.Windows.Forms.Label lblTituloMenu;
        private System.Windows.Forms.Button btnMatematicaBasica;
        private System.Windows.Forms.Button btnCalculo;
        private System.Windows.Forms.Button btnCalculo2;
        private System.Windows.Forms.Button btnAlgebraLineal;
        private System.Windows.Forms.Button btnConfiguracion;
        private System.Windows.Forms.Panel panelContenido;
        private System.Windows.Forms.Panel panelEncabezado;
        private System.Windows.Forms.Label lblTituloSeccion;
        private System.Windows.Forms.Label lblFechaHora;
    }
}