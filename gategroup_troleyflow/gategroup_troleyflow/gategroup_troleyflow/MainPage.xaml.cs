using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Xamarin.Forms;

namespace gategroup_troleyflow
{
    public partial class MainPage : ContentPage
    {
        public MainPage()
        {
            InitializeComponent();
        }

        private void OnEvaluateClicked(object sender, EventArgs e)
        {
            // Obtener los valores de los controles
            int allow = int.Parse(allowed.Text);  // "Sí" es 0, "No" es 1
            if (allow != 0 && allow != 1)
            {
                DisplayAlert("Error", "Por favor, seleccione si se permiten botellas abiertas.", "OK");
                return;  // No continuar si el valor es incorrecto
            }
            int sealedBottle = int.Parse(@sealed.Text);
            if (sealedBottle != 0 && sealedBottle != 1 && sealedBottle != 2)
            {
                DisplayAlert("Error", "Por favor, seleccione el estado de la botella sellada.", "OK");
                return;  // No continuar si el valor es incorrecto
            }


            // Validar la entrada de porcentaje
            double percent = 0;
            if (string.IsNullOrEmpty(percentEntry.Text) || !double.TryParse(percentEntry.Text, out percent))
            {
                DisplayAlert("Error", "Por favor, ingrese un valor válido para el porcentaje de contenido.", "OK");
                return;  // No continuar si el valor es incorrecto
            }

            // Validar la entrada de limpieza
            double clean = 0;
            if (string.IsNullOrEmpty(cleanEntry.Text) || !double.TryParse(cleanEntry.Text, out clean))
            {
                DisplayAlert("Error", "Por favor, ingrese un valor válido para el nivel de limpieza.", "OK");
                return;  // No continuar si el valor es incorrecto
            }

            // Crear la instancia de la clase Bebidas
            Bebidas bebida = new Bebidas(allow, sealedBottle, percent, clean);

            // Obtener el mensaje de decisión final
            string result = bebida.FinalDecision();

            // Mostrar el resultado
            resultLabel.Text = result;
        }
    }
}