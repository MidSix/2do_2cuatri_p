/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/

using TGR_1.Utils;

public class Exercise2
{
    public static void exercise2()
    {
        //Simplemente obiene la ruta a donde el compilador guarda sus bins
        string currentDir = AppDomain.CurrentDomain.BaseDirectory;
        /*
            Navegamos hacia arriba para encontrar el archivo en la raiz del proyecto
            Asumimos estructura bin/Debug/net10.0/ -> ../../../StudentList.csv
            Tambien asumimos que en la raiz de proyecto hay un .csv que cargar
            No nos pidieron implementar la funcionalidad de que el usur
        */
        string defaultPath = Path.Combine(currentDir, "../../../StudentList.csv");
        // Normalizamos la ruta
        defaultPath = Path.GetFullPath(defaultPath);

        Console.WriteLine($"[INFO] Cargando datos desde: {defaultPath}");

        //Creamos la clase general.
        Classroom generalClass = new Classroom();
        StudentUtils.LoadStudentsFromCsv(defaultPath, generalClass.Students);

        if (generalClass.Students.Count == 0)
        {
             Console.WriteLine("[ERROR] No se han cargado estudiantes. Revisa la ruta o el archivo.\n" +
             "Asegurate de tener un .csv valido en la raiz del proyecto.\n");
             return;
        }

        // Crear la lista de clases particulares a partir de la clase general
        List<Classroom> particularClasses = generalClass.ParticularClassrooms();

        // Modificar las notas de los estudiantes en
        // las clases particulares para que todos tengan un 10
        foreach (var pClass in particularClasses)
        {
            // Cada clase particular tiene 1 solo alumno
            foreach (var student in pClass.Students)
            {
                student.Grade = 10.0;
            }
        }

        // Mostrar por pantalla las notas de la clase general
        // y de las clases particulares
        Console.WriteLine("\nNotas en clase general:");
        foreach (var s in generalClass.Students)
        {
            //Simplemente formato de impresion
            Console.WriteLine($"{s.Name}: {s.Grade:0.0}");
        }

        Console.WriteLine("Notas en clase particular:");
        foreach (var pClass in particularClasses)
        {
            foreach (var s in pClass.Students)
            {
                // Deberian ser todo 10
                Console.WriteLine($"{s.Name}: {s.Grade}");
            }
        }

        // Esperar input para no cerrar inmediatamente si se ejecuta
        // solo esto (aunque el menu principal lo gestiona)
        Console.WriteLine("\nPresione Enter para volver al menú...");
        Console.ReadLine();
    }
}
