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
    }
}
