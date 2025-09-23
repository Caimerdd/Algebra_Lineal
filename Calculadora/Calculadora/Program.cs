using System;
using System.Drawing;
using System.Windows.Forms;

namespace Calculadora
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new CalculadoraForm());
        }
    }
}   