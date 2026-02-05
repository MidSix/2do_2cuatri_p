/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/

/*
    En C# se siguen las convenciones PascalCase tanto para
    clases(como python) como para metodos(en lugar del snake_case)
    las variables, parametros y demas tienen la convencion camelCase
    por lo tanto a lo largo de este proyecto se intentara seguir esta
    convencion.
*/

class Program
{
    static void Main(string[] args)
    {
        string exerciseMenu =
        @"¿Que ejercicio desea realizar?
        1) Ejercicio 1
        2) Ejercicio 2
        0) Salir

        Introduzca una opción:";
        int selectExercise = -1;
        List<int> opcionesPosibles = [1,2,0];
        while(selectExercise != 0)
        {
            Console.WriteLine(exerciseMenu);
            try
            {
                selectExercise = Convert.ToInt32(Console.ReadLine());
                if (opcionesPosibles.Contains(selectExercise))
                {
                    if(selectExercise == 1)
                    {
                        Exercise1.exercise1();
                    }
                    else if(selectExercise == 2)
                    {
                        Exercise2.exercise2();
                    }
                    else{}
                }
                else
                {
                    Console.WriteLine("->La opcion elegida no existe\n" +
                    "Por favor introduzca de nuevo un valor.\n");
                }
            }
            /*
                Si te preguntas de donde se saco el nombre de estas
                exepciones, simplemente hay que hacer hover al .ToInt32
                que es el metodo al que le estamos pasando el return del
                Console.ReadLine() los metodos en lineas generales
                raisean sus except cuando pasa algo y la documentacion
                de este lenguaje lo refleja, en la documentacion de
                cada metodo te muestra que excepciones puede lanzar.
            */
            catch(FormatException e)
            {
                Console.WriteLine($"Error: {e.Message}\n" +
                "->Por favor introduce un numero entero\n");
            }
            catch(Exception e)
            {
                Console.WriteLine($"Excepcion desconocida: {e.Message}\n" +
                "->Por favor vuelva a intentarlo\n");
            }
        }
    }
}