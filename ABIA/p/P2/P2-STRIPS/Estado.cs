/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/

namespace STRIPS{

    public class Estado
    {
        public HashSet<Facto> Hechos { get; private set; }//Aqui el hashset mencionado en el comentario de Facto.cs
        public Estado()
        {
            Hechos = new HashSet<Facto>();
        }
        public Estado(IEnumerable<Facto> hechosIniciales)//Esto es para crear un estado a partir de una lista de hechos, por ejemplo el estado inicial del mundo
        {
            Hechos = new HashSet<Facto>(hechosIniciales);
        }

        public void Agregar(Facto f) => Hechos.Add(f);//Añadir un facto
        public void Eliminar(Facto f) => Hechos.Remove(f);//Eliminar un facto

        public bool Satisface(Estado objetivo) // Compara dos estados, en la practica se usará para comparar el estado actual del mundo con el estado objetivo
        {
            return objetivo.Hechos.All(h => Hechos.Contains(h));//Sencillito, si los hechos son identicos, los estados tambien
        }


        public Estado Clonar()//Esto lo usará el planer para simular acciones sin reventar los estados
        {
            return new Estado(this.Hechos.Select(f => new Facto(f.Nombre, f.Argumentos.ToArray())));
        }

        public void Mostrar()//Esto es para mostrar el estado por consola, para debuggear y asi
        {
            foreach (var hecho in Hechos.OrderBy(h => h.Nombre))
            {
                Console.WriteLine($" - {hecho}");
            }
        }
    }
}
