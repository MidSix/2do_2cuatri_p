/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/
string exerciseMenu =
        @"¿Que ejercicio desea realizar?
        1) Ejercicio 1
        2) Ejercicio 2
        3) Ejercicio 3
        0) Salir

        Introduzca una opción:";
        int selectExercise = -1;
        List<int> opcionesPosibles = [1,2,3,0];
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
                        Semana_1.Ejecucion1.Semana1();
                    }
                    else if(selectExercise == 2)
                    {
                        //semana_2.Ejecucion2.Semana2();
                    }
                    else if(selectExercise == 3)
                    {
                        //semana_3.Ejecucion3.Semana3();

                    }
                    else{}

                }
                else
                {
                    Console.WriteLine("->La opcion elegida no existe\n" +
                    "Por favor introduzca de nuevo un valor.\n");
                }
            }
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


