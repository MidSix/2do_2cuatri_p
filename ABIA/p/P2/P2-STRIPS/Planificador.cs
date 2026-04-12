/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/

namespace STRIPS{

    public class Planificador
    {
        //Declaramos la lista de acciones
        private readonly List<Accion> _acciones;// Aqui no usamos 
        // getters y setters ya que dichos wrappers sirven para
        // controlar el permiso en los accesos para lectura y escritura
        // de una variable fuera de la clase que la contiene.
        // Pero como la variable es private y por tanto no se puede 
        // acceder desde un scope distinto a este modulo, 
        // no hay ninguna necesidad
        // (tampoco ninguna prohibicion pero simplemente no tiene
        // sentido) de definir getters y setters.  

        // readonly impide la modificacion de la direccion de memoria
        // a la que su identificador apunta, pero NO impide la
        // asignacion en el constructor, o sea, impide la modificacion
        // una vez le hayamos pasado un valor en el constructor, antes
        // de hacerlo evidentemente no porque si no no se le podria
        // dar ningun valor xd
        private readonly IAlgoritmoBusqueda _algoritmo;// Declaramos
        // la variable que maneja el algoritmo al que llamara el
        // planificador.

        public Planificador(List<Accion> acciones, IAlgoritmoBusqueda algoritmo)
        {
            _acciones = acciones;
            _algoritmo = algoritmo; // Aqui se pasara el algoritmo de
            // busqueda que usara el planificador, BFS funciona muy bien 
            // en el mundo de bloques pero en TorresHanoi tiene su 
            // dificultad ya que el problema permite llamar con 
            // n discos, por eso creo esto para poder pasar por aqui
            // el algoritmo que vaya a usar para TorresHanoi.
        }
        public List<Accion>? GenerarPlan(Estado inicial, Estado objetivo)
        {
            // El planificador delega la responsabilidad matemática y simplemente orquesta
            return _algoritmo.Buscar(inicial, objetivo, _acciones);
        }
    }
}
