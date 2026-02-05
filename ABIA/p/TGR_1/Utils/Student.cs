/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/

using System.Runtime.CompilerServices;

namespace TGR_1.Utils
{
    public class Student
    {
        /*
            Los datos deberian YA venir validados al ser cargados
            desde un .csv, pero por si acaso se aplican getters y
            setters explicitos.
        */
        private string _Name = string.Empty; //Aseguramos que NUNCA sea null.
        public int _Age;
        /*
            La validacion del grade, a diferencia del nombre y de la
            edad, puede cambiar en funcion del sistema de evaluacion
            que se tenga, en lugar de sobre 10 podria ser sobre 20 o
            sobre 100, y nota negativa con lo que restan los tipo test
            y demas pues podria ser.

            Entonces creo que no necesita validacion extra mas alla
            de la que ya nos ofrece el propio tipo Grade (double - Si
            intentaras setear un valor NO convertible a double lanzaria
            excepcion por los tipos, asi que ya con eso creo que basta).
        */
        public double Grade { get; set; }

        public string Name
        {
            get
            {
                return _Name;
            }
            set
            {
                try
                {
                    // Usamos 'value', que es el dato que el usuario quiere setear
                    //Es una keyword para el contexto del setter.
                    StudentUtils.ValidateName(value);
                    _Name = value;
                }
                catch(FormatException e)
                {
                    // Relanzamos con más contexto
                    throw new FormatException($"Student Name '{value}' not valid. {e.Message}");
                }
            }
        }
        public int Age
        {
            get
            {
                return _Age;
            }
            set
            {
                //Hay que recordar que lo que pasa el usuario para
                //setear se guarda dentro de la variable "value"
                if(value < 0 || value > 122)
                {
                    throw new ArgumentOutOfRangeException("Nobody " +
                    $"can have that age common.\nStudent age '{value}' of student with name '{this.Name}' not valid.");
                }
            }
        }

        public Student(string Name, int Age, double grade)
        {
            // Asignamos a la PROPIEDAD para
            // para que se ejecute la validacion del setter
            this.Name = Name;
            this.Age = Age;
            Grade = grade;
        }

        // Metodo para clonar el estudiante (Deep Copy)

        public Student Clone()
        {
            /*
                Es como el self. de python, en Java es obligatorio
                Y en C# no lo es, es obligatorio su uso solo para\
                desambiguar su tuviera una variable local en este metodo
                que entrara en conflicto con el atributo, como no es el
                caso no es necesario el this pero bueno, como en otros
                lenguajes es obligatorio es mejor aprender lo general
                que sirve en todos xd.
            */
            return new Student(this.Name, this.Age, this.Grade);
        }
    }
}
