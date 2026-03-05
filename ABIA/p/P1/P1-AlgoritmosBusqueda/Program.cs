/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/
using Ejecuciones;
public class Program
{
    public static void Main(string[] args)
    {
        string exerciseMenu =
            @"¿Qué ejercicio desea realizar?
            1) Ejercicio 1
            2) Ejercicio 2
            3) Ejercicio 3
            0) Salir
            Introduzca una opción:";

        int selectExercise = -1;
        List<int> opcionesPosibles = [1, 2, 3, 0];

        while (selectExercise != 0)
        {
            Console.WriteLine(exerciseMenu);
            try
            {
                string? input = Console.ReadLine();
                if (string.IsNullOrEmpty(input)) continue;

                selectExercise = Convert.ToInt32(input);
                if (opcionesPosibles.Contains(selectExercise))
                {
                    if (selectExercise == 1)
                    {
                        Ejecucion1.Semana1();
                    }
                    else if (selectExercise == 2)
                    {
                        Ejecucion2.Semana2();
                    }
                    else if (selectExercise == 3)
                    {
                        Ejecucion3.Semana3();
                    }
                }
                else
                {
                    Console.WriteLine("-> La opción elegida no existe\n" +
                                      "Por favor introduzca de nuevo un valor.\n");
                }
            }
            catch (FormatException)
            {
                Console.WriteLine("Error: Por favor introduce un número entero\n");
            }
            catch (Exception e)
            {
                Console.WriteLine($"Excepción desconocida: {e.Message}\n" +
                                  "-> Por favor vuelva a intentarlo\n");
            }
        }
    }
}
