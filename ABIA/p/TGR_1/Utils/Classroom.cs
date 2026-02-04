/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/

namespace TGR_1.Utils
{
    public class Classroom
    {
        /*
            En los lenguajes de programacion se hace una distincion
            entre atributos de Clase y de Instancia. No es la excepcion
            en lenguajes interpretados o compilados. Para python esta
            distincion se da si:
            Atributo fuera del constructor __init__(self,..) -> de Clase
            Atributo dentro del constructor || -> De instancia.
            En C# y en los tipados esta distincion NO se da asi. Ambos
            tanto de clase como de instancia se declaran FUERA de todo
            metodo, lo que los diferencia es que los de clase tienen el
            modificador "static" y los de instancia no.
        */
        public List<Student> Students { get; set; }
        /*
            Otra cosa nueva de C#. El constructor de la clase se tiene
            que llamar exactamente igual que la clase, de lo contrario
            el compilador de C# piensa que se trata de un metodo comun
            y corriente y pedira que establezcas un tipo de retorno.
            Como se puede apreciar en los metodos del constructor es el
            unico metodo en una clase donde no tenemos que especificar
            tipos de retorno.
        */

        /*
            Otra cosa nueva mas: "Overloading" en python si hay dos
            metodos con el mismo nombre, el ultimo declarado reemplazara
            al anterior, sin embargo en C# y en general en los lenguajes
            de tipado fuerte como Java,C++, etc. Se pueden tener
            multiples definiciones para un mismo metodo en funcion
            de los argumentos y sus tipos que reciba, se parece al
            "Multiple-dispatch" de Julia, sin embargo ese se realiza en
            tiempo de ejecucion y este se realiza AOT(Ahead of time)
            pero en terminos practicos se puede establecer un marco
            mental que los trate como equivalente.
        */

        //Si no se pasa la lista student se inicializa vacia
        public Classroom()
        {
            Students = new List<Student>();
        }
        //Si se pasa no se inicializa vacia xd.
        public Classroom(List<Student> students)
        {
            Students = students;
        }

        /*
            Se entiende que "ParticularClassrooms" se refiere a clases
            INDIVIDUALES por cada estudiante, es decir, un profesor le
            dedica el tiempo a un solo estudiante en una sala fisica.
            Es la unica forma en la que le veo sentido crear una lista
            de objetos classroom solo con un estudiante.
            Se entiende que el punto de este ejercicio es evidenciar
            la diferencia entre guardar en variables las referencias
            a objetos ya existentes en memoria
            y crear nuevos a imagen y semejanza de los existentes
            para poder editar uno sin modificar el otro, aun asi
            conceptualmente me choco un poco una lista de classroom.
        */
        public List<Classroom> ParticularClassrooms()
        {
            /*
                Cada objeto de tipo classroom tendra una clase general
                que sera la lista student que cargamos con el metodo
                LoadStudentsFromCsv en la lista de estudiantes vacia
                para ese momento.
            */
            List<Classroom> particularClassrooms = new List<Classroom>();
            foreach (var student in Students)
            {
                // Instanciamos en cada iteracion del bucle, es decir
                // por cada alumno, un objeto de tipo classroom al que
                // agregaremos un solo estudiante
                Classroom particularClass = new Classroom();
                /*
                    Añadimos el estudiante CLONADO
                    para evitar referencias compartidas
                    el "Add" es un metodo buil-in como el .append()
                    de python que hace lo que dice el nombre.
                */
                particularClass.Students.Add(student.Clone());
                //Agregamos el objeto con el solo estudiante en su lista
                //A la lista de classrooms
                particularClassrooms.Add(particularClass);
            }
            return particularClassrooms;
        }
    }
}
