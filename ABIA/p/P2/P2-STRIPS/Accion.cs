/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/

namespace STRIPS{

    public class Accion
    {
        public string Nombre { get; set; }
        
        public List<Facto> Precondiciones { get; set; }//Esto lo dimos en clase, es lo que ha de ser ciert
        //para que se pueda llevar a cabo la acción, por ejemplo para la acción "Mover(A, B, C)" 
        // las precondiciones podrían ser "En(A, B)" y "Libre(C)"  
        public List<Facto> ListaBorrado { get; set; } // Lo que deja de ser verdad tras la acción
        public List<Facto> ListaAdicion { get; set; } // Lo que pasa a ser verdad tras la acción
        public Accion(string nombre)
        {
            Nombre = nombre;
            Precondiciones = new List<Facto>();
            ListaBorrado = new List<Facto>();
            ListaAdicion = new List<Facto>();
        }
        public bool EsAplicable(Estado estadoActual) // Verifica si esta acción se puede realizar en un estado dado.

        {
            return Precondiciones.All(p => estadoActual.Hechos.Contains(p)); // Sencillito es aplicable si el estado actual contiene todas las precondiciones

        }

        public Estado Aplicar(Estado estadoActual)//Aplicar la accion
        {
            Estado nuevoEstado = estadoActual.Clonar();//Clonamos

            foreach (var f in ListaBorrado)//Borramos los hechos que ahora son inciertos
                nuevoEstado.Eliminar(f);

            foreach (var f in ListaAdicion)//Y agregamos los  que son cierts
                nuevoEstado.Agregar(f);

            return nuevoEstado;
        }
        public override string ToString() => Nombre;
    }
}

