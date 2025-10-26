using System;
using System.Collections.Generic;
using System.Text;

namespace gategroup_troleyflow
{
    public class Bebidas
    {
        private int _allow;
        private int _sealed;
        private double _clean;
        private double _percent;

        // Constructor
        public Bebidas(int allow, int sealedBottle, double percent, double clean)
        {
            _allow = allow;
            _sealed = sealedBottle;
            _clean = clean;
            _percent = percent;
        }

        // Propiedades
        public int Allow { get { return _allow; } set { _allow = value; } }
        public int Sealed { get { return _sealed; } set { _sealed = value; } }
        public double Clean { get { return _clean; } set { _clean = value; } }
        public double Percent { get { return _percent; } set { _percent = value; } }

        // Métodos de evaluación
        public int Region() => _allow == 0 ? 1 : 0;
        public int FirstBarrier() => _sealed == 0 ? 1 : 0;
        public int FillLevel() => _percent >= 0.5 ? 1 : 0;
        public int Clear() => _clean >= 0.7 ? 1 : 0;
        public int MaxFeel() => _percent >= 0.9 ? 1 : 0;

        // Método principal de decisión
        public string FinalDecision()
        {
            int count = 0;
            int res = 0;
            string resultMessage = string.Empty;

            // Verificación de las condiciones
            int op1 = Region();
            if (op1 == 1)
            {
                resultMessage += "Se permite las botellas abiertas\n";
                count += 1;
                int op2 = FirstBarrier();
                resultMessage += op2 >= 1 ? "La botella está cerrada\n" : "La botella está abierta\n";

                int op3 = FillLevel();
                if (op3 == 1)
                {
                    resultMessage += "Cumple con más del 50% de contenido\n";
                    count += 1;
                }
                else
                {
                    resultMessage += "No cumple con más del 50% de contenido\n";
                }
                int op4 = Clear();
                if (op4 == 1)
                {
                    resultMessage += "Cumple con el 70% de limpieza\n";
                    count += 1;
                    int op5 = MaxFeel();
                    if (op5 == 1)
                    {
                        count += 1;
                        resultMessage += "Se posee más del 90% del contenido\n";
                    }
                }
                else
                {
                    resultMessage += "No cumple con el 70% de limpieza\n";
                }
            }
            else
            {
                resultMessage += "No se permiten las botellas abiertas\n";

                int op22 = FirstBarrier();
                if (op22 == 1)
                {
                    resultMessage += "La botella está cerrada\n";
                    count += 1;
                    int op33 = FillLevel();
                    if (op33 == 1)
                    {
                        resultMessage += "Cumple con más del 50% de contenido\n";
                        count += 1;
                    }
                    else
                    {
                        resultMessage += "No cumple con más del 50% de contenido\n";
                    }
                    int op44 = Clear();
                    if (op44 == 1)
                    {
                        count += 1;
                        resultMessage += "Cumple con el 70% de limpieza\n";
                        int op55 = MaxFeel();
                        if (op55 == 1)
                        {
                            count += 1;
                            resultMessage += "Se posee más del 90% del contenido\n";
                        }
                    }
                    else
                    {
                        resultMessage += "No cumple con el 70% de limpieza\n";
                    }
                }
                else
                {
                    resultMessage += "La botella está abierta\n";
                    res = 1;
                }
            }



            // Decisión final
            if (res == 1)
            {
                resultMessage += "Se descarta el producto por las políticas del destino\n";
            }
            else
            {
                switch (count)
                {
                    case 1:
                        resultMessage += "Descartar\n";
                        break;
                    case 2:
                        resultMessage += "Reemplazar\n";
                        break;
                    case 3:
                        resultMessage += "Rellenar\n";
                        break;
                    case 4:
                        resultMessage += "Mantener\n";
                        break;
                }

            }

            return resultMessage;
        }
    }
}

