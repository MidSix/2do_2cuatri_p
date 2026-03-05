/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/

namespace n_reinas
{
    /// <summary>
    /// Búsqueda en anchura (BFS).
    /// </summary>
    public class BusquedaEnAnchura : AlgoritmoDeBusqueda
    {
        public BusquedaEnAnchura()
        {
            Lista = new Cola();
        }

        // BFS no utiliza prioridades, pero el método padre lo requiere.
        public override int CalculoDePrioridad(object nodo_info, object? calculo_heuristica = null)
        {
            return 0;
        }
    }

    /// <summary>
    /// Búsqueda en profundidad (DFS).
    /// </summary>
    public class BusquedaEnProfundidad : AlgoritmoDeBusqueda
    {
        public BusquedaEnProfundidad()
        {
            Lista = new Pila();
        }

        public override int CalculoDePrioridad(object nodo_info, object? calculo_heuristica = null)
        {
            return 0;
        }
    }
}
