
/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/

using System.Globalization;

namespace TGR_1.Utils
{
    public static class StudentUtils
    {
        private const int ExpectedCsvColumns = 3;

        public static void LoadStudentsFromCsv(string filePath,
                                                List<Student> container)
        {
        /*
        Método estático para cargar estudiantes en una lista dada
        modifica in-place por tanto.
        */

            if (container == null)
            {
                Console.WriteLine("[ERROR] El contenedor de estudiantes no ha sido inicializado.");
                return;
            }
            if (!File.Exists(filePath))
            {
                Console.WriteLine($"[ERROR] El archivo '{filePath}' no fue encontrado.");
                return;
            }
            try
            {
                container.Clear(); // Limpiamos el objeto existente
                // para no duplicar datos si se carga varias veces
                // Es un built-in method.

                string[] lines = File.ReadAllLines(filePath);

                //Analogo al bucle for de python
                foreach (string line in lines)
                {
                    //No deberia porque se confia en que el dataset
                    //este correcto pero bueno, ahi esta.
                    if (string.IsNullOrWhiteSpace(line)) continue;
                    /*
                        Ya lo pone en la documentacion pero:
                        .split returns an array whose elements contain
                        the substrings from this instance that
                        are delimited by separator. O sea, nos quedamos
                        en cada iteracion con un array que tiene en cada
                        elemento el nombre, edad, nota del estudiante.
                    */
                    string[] parts = line.Split(',');
                    /*
                        En caso de que se quiera cambiar el numero de
                        Columnas esperables en el .csv habria que cambiar
                        el metodo ya que asi tal cual solo funciona con
                        3 columnas nombre/edad/nota. Pero es suficiente
                        Para el TGR.
                    */
                    if (parts.Length == ExpectedCsvColumns)
                    {
                        /*
                            Si el .csv esta bien formateado no deberia
                            haber espacios en los nombres, pero de nuevo
                            por si acaso
                        */
                        string name = parts[0].Trim();
                        /*
                            Basicamente intenta convertir, de poder
                            hacerlo entonces guarda el valor en la
                            variable a la que apunta "out".
                        */
                        if (int.TryParse(parts[1].Trim(), out int age) &&
                            double.TryParse(parts[2].Trim(),
                            NumberStyles.Any, CultureInfo.InvariantCulture,
                            out double grade))
                        {
                            container.Add(new Student(name, age, grade));
                        }
                        else
                        {
                            Console.WriteLine($"[DEBUG] Error parseando línea: '{line}'. Edad: '{parts[1]}', Nota: '{parts[2]}'");
                        }
                    }
                }
                Console.WriteLine($"\n[INFO] Lista actualizada. {container.Count} estudiantes en memoria.");
            }
            catch(ArgumentOutOfRangeException e)
            {
                Console.WriteLine($"Error with age inside .csv: {e.Message}");
            }
            catch(FormatException e)
            {
                Console.WriteLine($"Error with name inside .csv: {e.Message}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error al procesar el archivo: {ex.Message}");
            }
        }

        // Método estático para calcular la nota media
        public static double CalculateMeanGrade(List<Student> students)
        {
            if (students == null || students.Count == 0)
            {
                return 0.0;
            }
            /*
                Veras "var" seguido, no es ninguna declaracion
                de variables como Javascript, sino es un atajo propio
                de C# pero no tener que escribir el tipo de la variable
                que estamos creando, le decimos a Roslyn(el compilador)
                que deduzca el tipo de la variable en funcion del tipo
                del objeto que referencia. Si no pusieramos var s
                tendriamos que poner foreach (var Student s in students)
                pues ahora que escribo esto no parece tan relevante
                pero si fuera la lista seria List<Student> y ya es mas
                fastidiso escribir eso.
            */
            double sum = 0;
            foreach (Student s in students) // El for de python basicamente
            {
                sum += s.Grade;
            }
            return sum / students.Count;
        }

        // Calcular nota mínima y máxima
        public static (double min, double max) GetMinMaxGrades(List<Student> students)
        {
            if (students == null || students.Count == 0)
            {
                return (0.0, 0.0);
            }
            /*
                Aqui seteamos el min-max arbitrariamente con la nota
                que poseea el primer estudiante, es mejor hacer esto que
                inicializarlas en cero ya que en ese caso tendriamos
                que hacer mas asignaciones, sé que tienen coste O(1)
                pero si se pueden reducir el numero de asignaciones es
                mejor hacerlo
            */
            double min = students[0].Grade;
            double max = students[0].Grade;

            /*
                Analogo al for de python, simplemente recorremos los
                estudiantes en la lista de estudiantes, accedemos a sus
                notas(recordar que son objetos de tipo student) y
                vamos comparando.
            */
            foreach (var s in students) // O(n)
            {
                if (s.Grade < min) min = s.Grade; // O(1)
                if (s.Grade > max) max = s.Grade; // o(1)
            }
            return(min, max);
        }

        // Añadir un nuevo estudiante (Pura: recibe el objeto ya creado)
        public static void AddStudent(List<Student> container, Student newStudent)
        {
            if (newStudent != null)
            {
                container.Add(newStudent);
                Console.WriteLine($"[INFO] {newStudent.Name} añadido correctamente.");
            }
        }

        /**/
        // Find funciona como un foreach (analogo al for de python)
        public static bool EditStudentGrade(List<Student> students, string name, double newGrade)
        {
            var student = students.Find(s => s.Name.Equals(name, StringComparison.OrdinalIgnoreCase));
            if (student != null)
            {
                student.Grade = newGrade;
                return true;
            }
            return false;
        }

        // Guardar lista en archivo CSV
        public static void SaveStudentsToCsv(string filePath, List<Student> students)
        {
            try
            {
                /*
                    Aqui comprobamos si el path que nos pasa el usuario
                    es un directorio, de ser asi entonces le agregamos
                    a ese path el nombre por defecto que tendra
                    el archivo que guardaremos dentro.

                    - TrimEnd() -> Simplemente elimina los posibles
                    espacios que pueden tener las direcciones de los
                    usuarios, en caso que todo el path usara guiones
                    bajos TrimEnd() no solucionaria ningun problema
                    porque no habria ninguno que solucionar xd, pero
                    por robustez se mantiene.
                    -EndsWith() -> Self-explanatory
                */
                if (filePath.TrimEnd().EndsWith(Path.DirectorySeparatorChar) ||
                    filePath.TrimEnd().EndsWith(Path.AltDirectorySeparatorChar) ||
                    Directory.Exists(filePath))
                {
                    string defaultName = "StudentList.csv";
                    // Solo informar si es algo explícito (para no spammear)
                    Console.WriteLine($"[INFO] La ruta es un directorio. Guardando como '{defaultName}' dentro de él.");
                    /*
                        Este metodo es simplemente una concatenacion.
                        Pero una avanzada porque tiene en cuenta el SO
                        el usuario. Si es windows concatena con "\" y
                        si es MacOS o Linux concatena con "/" las
                        direcciones.
                    */
                    filePath = Path.Combine(filePath, defaultName);
                }

                // Verificar y crear el directorio padre si no existe
                string? parentDir = Path.GetDirectoryName(filePath);
                if (!string.IsNullOrEmpty(parentDir) && !Directory.Exists(parentDir))
                {
                    Console.WriteLine($"[INFO] Creando directorio: {parentDir}");
                    Directory.CreateDirectory(parentDir);
                }

                using (StreamWriter writer = new StreamWriter(filePath))
                {
                    foreach (var s in students)
                    {
                        // Usamos InvariantCulture para guardar con punto decimal
                        string line = $"{s.Name}, {s.Age}, {s.Grade.ToString(CultureInfo.InvariantCulture)}";
                        writer.WriteLine(line);
                    }
                }
                Console.WriteLine($"[INFO] Archivo guardado correctamente en: {filePath}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[ERROR] No se pudo guardar el archivo: {ex.Message}");
            }
        }

        public static bool IsStudentsEmpty(List<Student> students)
        {
            if(students.Count != 0)
            {
                return false;
            }
            else
            {
                Console.WriteLine("Por favor carga primero\n" +
                "una lista de estudiantes no vacia\n");
                return true;
            }
        }

        public static void ValidateName(string name)
        {
            /*
            Si el usuario escribe un numero como nombre, al ser int
            un tipo mas restrictivo que string, es decir, string
            contiene a int, un int, o un numero en general, escrito
            por el usuario puede convertirse a string, y si es un string
            el programa no ve ningun fallo en que el alumno x se llame
            175829035723405, pero en la vida real nadie tiene de nombre
            un numero xd, entonces para validar que el nombre no es un
            numero se implementa la siguiente logica.
            El usuario proporciona un string como nombre, nosotros
            pasamos ese nombre a esta funcion, intentamos convertir ese
            nombre en un entero.
            Si se puede -> Es un número, lanzamos FormatException.
            Si no se puede -> Es un nombre real y no hacemos nada.
            Dejamos que el programa continue.

            - TryParse devuelve true si lo puede transformar
            por eso si no puede hacerlo no se activa el if y no raisea
            ninguna excepcion.
            */
            if (int.TryParse(name, out _))
            {
                throw new FormatException("Un nombre no puede ser un número.");
            }
            if (double.TryParse(name, out _))
            {
            throw new FormatException("Un nombre no puede ser un número (demasiado grande).");
            }
        }
    }
}