/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/

namespace TGR_1.Utils
{
    public class Student
    {
        public string Name { get; set; }
        public int Age { get; set; }
        public double Grade { get; set; }

        public Student(string name, int age, double grade)
        {
            Name = name;
            Age = age;
            Grade = grade;
        }

        // Sobrescribimos ToString para facilitar la impresión luego
        public override string ToString()
        {
            return $"{Name} (Edad: {Age}, Nota: {Grade})";
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
