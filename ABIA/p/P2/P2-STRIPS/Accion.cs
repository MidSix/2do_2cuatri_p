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
            return this.Precondiciones.All(estadoActual.Hechos.Contains); // Sencillito es aplicable si el estado actual contiene todas las precondiciones
            // Si, lo mismo de antes, esta accion en especifico es
            // aplicable al estado actual si todos los factos que 
            // deben cumplirse, es decir, los factos dentro de la lista
            // precondiciones estan dentro del dominio/mundo, es decir,
            // los Hechos del estado que se esta evaluando.

            // Ya sabemos que no hace falta la funcion anonima.
            // Simplemente se pasa la referencia de la funcion que
            // verifica si un hecho forma parte del conjunto de Hechos
            // que componen un estado, y el metodo .All() ya se 
            // encarga de hacer un loop sobre cada elemento de un 
            // iterable, en este caso Precondiciones, y pasa los
            // elementos, es decir los factos, como argumento a la
            // funcion que comprueba si ese hecho esta en el estado
        }

        public Estado Aplicar(Estado estadoActual)//Aplicar la accion
        {
            Estado nuevoEstado = estadoActual.Clonar();//Clonamos
            // .Clonar() ya devuelve una instancia de la clase estado.

            foreach (var f in ListaBorrado)//Borramos los hechos que ahora son inciertos
                nuevoEstado.Eliminar(f);
            foreach (var f in ListaAdicion)//Y agregamos los que son cierts
                nuevoEstado.Agregar(f);
            // 'var' es una inferencia de tipos que se delega
            // al compilador.

            return nuevoEstado;
        }
        public override string ToString() => Nombre;
    }
}

