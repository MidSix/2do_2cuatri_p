/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/
using MundoBloques;//SI, ya se que tecnicamente no hace falta usar este using, pero me gusta como queda
//using TorresHanoi;
public class Program
{
    public static void Main(string[] args)
    {
        string menuPrincipal =
            @"¿Qué ejercicio desea realizar?
                1) Mundo de Bloques (Escenarios a y b)
                2) Torres de Hanoi (n discos)
                0) Salir
                Introduzca una opción:";

        int seleccion = -1;
        List<int> opcionesValidas = new List<int> { 1, 2, 0 };

        while (seleccion != 0)
        {
            Console.WriteLine(menuPrincipal);
            try
            {
                string? input = Console.ReadLine();
                if (string.IsNullOrEmpty(input)) continue;//esto es para evitar que el programa se crashee si el usuario no introduce nada y le da a enter,
                //  ya que Convert.ToInt32 no puede convertir una cadena vacía a un número, así que simplemente volvemos a mostrar el menú

                seleccion = Convert.ToInt32(input);

                if (opcionesValidas.Contains(seleccion))
                {
                    switch (seleccion)//Me apetecio aprender esto de los switch, aunque tampoco es que sea muy complicado, pero bueno, así se ve un poco más ordenado que con ifs
                    {//basicamente lo que haces es meter cada caso dentro de un case, y luego pones un break al final de cada caso para que no se ejecute el siguiente caso, es bastante sencillo
                        case 1:
                            Console.WriteLine("Introduzca el número del escenario de Mundo de Bloques a resolver (a o b):");
                            string ?escenario = Console.ReadLine();
                            if (escenario == "a")
                            {
                                MundoBloques.MundoBloques.ResolverEscenarioA();
                            }
                            else if (escenario == "b")
                            {
                                MundoBloques.MundoBloques.ResolverEscenarioB();
                            }
                            break;

                        case 2:
                            Console.Write("Introduzca el número de discos (n) para Hanoi: ");
                            if (int.TryParse(Console.ReadLine(), out int n))
                            {
                                //TorresHanoi.Resolver(n);//Aqui añades tu movida Sebas
                            }
                            else
                            {
                                Console.WriteLine("Error: El número de discos debe ser un entero.");
                            }
                            break;

                        case 0:
                            Console.WriteLine("Cerrando programa...");
                            break;
                    }
                }
                else
                {
                    Console.WriteLine("\nLa opción elegida no es válida. Inténtelo de nuevo.\n");
                }
            }
            catch (FormatException)
            {
                Console.WriteLine("\nError: Debe introducir un número entero.\n");
            }
            catch (Exception e)
            {
                Console.WriteLine($"\nError inesperado: {e.Message}\n");
            }
        }
    }
}