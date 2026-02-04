/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/

using TGR_1.Utils; // Importamos el namespace donde viven nuestos Utils.
public class Exercise1
{
    public static void exercise1()
        {
        var students = new List<Student>();
        /*
            No se solicita pero se agrega un path por defecto en caso
            que el usuario no quiera escribir la ruta entera cada vez
            que quiera cargar la lista que puede resultar molesto.
            El programa se ejecuta con los archivos compilados que se
            encuentran dentro de bin/Debug/net10.0 Por eso subimos 3
            niveles porque asumimos como defaultPath tener el .csv
            en el workspace del proyecto, en caso que no este alli pues
            ya te toca pegar la direccion del proyecto.
        */
        string defaultPath = "../../../StudentList.csv";


        string menuString =
        @"¿Qué acción desea realizar?
        1) Cargar la lista de estudiantes
        2) Obtener la nota media
        3) Obtener las notas máxima y mínima
        4) Añadir un nuevo estudiante
        5) Editar la nota de un estudiante
        6) Guardar la lista de estudiantes
        0) Salir

        Introduzca una opción:";
        /*
            "var" es simplemente un atajo que nos permite evitar
            escribir el tipo de la variable menu, le estamos diciendo al
            compilador que deduzca el tipo en funcion de aquello con lo
            que la estamos definiendo.

            "Action" es un tipo de Callable que le dice al compilador
            que la funcion que tiene ese tipo no retorna ningun
            valor, como valor de cada clave en el diccionario hayan
            dos funciones (La anonima y las llamadas a los metodos de
            StudentUtils) lo que le interesa al compilador es la
            funcion en la capa mas exterior, esa es la funcion anonima
            y como puedes ver no hay ningun return dentro de la
            secuencia de instrucciones que le pasamos a la fun anonima.
            Si la funcion devoliera algo ya el tipo no seria Action sino
            Func<argumentos_de_entrada,salida>.

            "funciones anonimas"
            "en python la sintaxis de una func. anonima es:
            lambda argumentos: codigo" -> ejem: lambda x,y: x + y.
            En C# la sintaxis es
            (argumento/s) => instruccion
            (argumento/s) => {secuencia_instrucciones}
            Lo que estamos haciendo con cada menu[option](students) es
            acceder al valor de la clave option del diccionario menu
            que resulta ser una referencia a las funciones anonimas que
            se definen abajo, a esas funciones anonimas les estamos
            pasando la lista students. Luego esas funciones anonimas
            se encargan de llamar a los metodos de nuestro Utils y
            hacer todas las operaciones necesarias antes de
            llamarlas. Basicamente funcionan como Wrappers en este caso
            que es el mismo funcionamiento que los getters y setters
            (Si, tambien se podia simplemente hacer
            muchos condicionales e implementar la misma logica abajo
            dentro de cada if a lo yandere dev pero bueno xd)
        */
        var menu = new Dictionary<int, Action<List<Student>>>
        {
            {1, (students) =>
                {
                    Console.WriteLine("Introduzca el path del .csv o pulse\n" +
                    $"|enter| para cargar la ruta por defecto {defaultPath}");
                    /*
                        el "?" en string? es porque el tipo string es
                        nullable, es decir, puede llegar a ser nulo.
                        Eso ocurre si el usuario corta el flujo del
                        programa.
                    */
                    string? filePath = Console.ReadLine() ?? "";
                    if (filePath.Length == 0)
                    {
                        StudentUtils.LoadStudentsFromCsv(defaultPath, students);
                    }
                    else
                    {
                        StudentUtils.LoadStudentsFromCsv(filePath, students);
                    }
                }
            },

            {2, (students) =>
                {
                    double mean = StudentUtils.CalculateMeanGrade(students);
                    Console.WriteLine($"The mean is: {mean:F3}");
                }
            },

            {3, (students) =>
                {
                    (double min, double max) = StudentUtils.GetMinMaxGrades(students);
                    Console.WriteLine($"[Notas]: Mínima: {min:F2} | Máxima: {max:F2}");
                }
            },


            { 4, (students) =>
                {
                    if(!StudentUtils.IsStudentsEmpty(students))
                    {
                        Console.Write("Nombre: ");
                        /*
                        "??" esto lo aprendi haciendo esto, se llamma
                        operador de coalescencia nula, es un op. que
                        hace lo que conseguirias con op. ternarios en
                        python o simplemente haciendo un if-else amplio.
                        if-else amplio:
                        if (Console.ReadLine() != null)
                        {
                            n = Console.ReadLine();
                        }
                        else
                        {
                            n = "SinNombre";
                        }
                        En lugar de hacer eso usas el ?? que lo hace
                        por debajo.
                        */
                        string n = Console.ReadLine() ?? "SinNombre";
                        /*
                            Hay que recordar como se transmiten las
                            excepciones. Estas suben hasta encontrar
                            un bloque de codigo que se encargue de
                            ellas, si no encuentran ninguno es ahi
                            cuando rompen el programa. Sin embargo ya
                            el bucle handlea estas excepciones de tipo
                            FormatExcepction que pueden surgir si el
                            usuario escribe mal y los Convert.* no
                            pueden trabajar.
                        */
                        Console.Write("Edad: ");
                        int a = Convert.ToInt32(Console.ReadLine());
                        Console.Write("Nota: ");
                        double g = Convert.ToDouble(Console.ReadLine());
                        StudentUtils.AddStudent(students, new Student(n, a, g));
                    }
                }
            },
            { 5, (students) =>
                {
                    if (!StudentUtils.IsStudentsEmpty(students))
                    {
                        Console.Write("Nombre del estudiante a editar: ");
                        string name = Console.ReadLine() ?? "SinNombre";
                        Console.Write("Nueva nota: ");
                        double grade = Convert.ToDouble(Console.ReadLine());
                        bool ok = StudentUtils.EditStudentGrade(students, name, grade);
                        //Operador ternario.
                        Console.WriteLine(ok ? "[OK] Editado." : "[ERROR] No encontrado.");
                    }
                }
            },
            { 6, (students) =>
                {
                    if (!StudentUtils.IsStudentsEmpty(students))
                    {
                        Console.Write($"Guardar en (Enter para '{defaultPath}'): \n" +
                        "o escribe el path donde quieras guardar el archivo\n");
                        string? p = Console.ReadLine();
                        /*
                            condicion ? valor_si_verdadero : valor_si_falso
                            equivalente en python a:
                            valor_si_verdadero if condicion else valor_si_falso
                        */
                        string target = string.IsNullOrWhiteSpace(p) ? defaultPath : p;
                        StudentUtils.SaveStudentsToCsv(target, students);
                    }
                }
            },
        };

        // Ejecucion del bucle principal
        int option = -1;

        while (option != 0)
        {
            Console.WriteLine(menuString);
            try
            {
                option = Convert.ToInt32(Console.ReadLine());
                if(option == 0)
                {
                    return;
                }
                menu[option](students);
            }

            catch(FormatException e)
            {
                Console.WriteLine($"Error {e}\n" +
                "La opcion proporcionada ni existe ni es entera\n" +
                "Por favor, escribe un numero entero\n");
            }
            catch(KeyNotFoundException e)
            {
                Console.WriteLine($"Error {e}\n" +
                "La opcion proporcionada no existe\n");
            }
            catch(ArgumentNullException e)
            {
                Console.WriteLine($"Error {e}\n" +
                "Cortaste el flujo del programa\n");
            }
            catch(Exception e)
            {
                Console.WriteLine($"Error desconocido\n{e}");
            }
        }
    }
}