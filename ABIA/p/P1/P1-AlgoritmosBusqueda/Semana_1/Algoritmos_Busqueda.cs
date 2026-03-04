/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/
namespace n_reinas
{   
public class AlgoritmoDeBusqueda
{
    public IListaCandidatos? Lista { get; set; }
    
    public virtual int CalculoDePrioridad(object nodo_info, object? calculo_heuristica = null)
    {
        return 0;  
    }

    /// <summary>
    /// Algoritmo de búsqueda genérico (BFS, DFS, A*, etc. según la implementación de Lista)
    /// </summary>
    /// <param name="solucionInicial">ESTADO INICIAL: La solución de partida del problema</param>
    /// <param name="criterioParada">Función que determina si una solución es meta (criterio de finalización)</param>
    /// <param name="obtenerVecinos">GENERACIÓN DE VECINOS: Función que dado un estado, devuelve sus estados vecinos</param>
    /// <param name="calculoCoste">Calcula el coste incremental entre dos estados consecutivos</param>
    /// <param name="calculoHeuristica">Función heurística opcional para A*</param>
    /// <returns>Tupla con (solución encontrada o null, número de nodos expandidos)</returns>
    public (Solucion?, int) Busqueda(
        Solucion solucionInicial, 
        Func<Solucion, bool> criterioParada,
        Func<Solucion, List<Solucion>> obtenerVecinos,
        Func<Solucion,Solucion ,int> calculoCoste,
        Func<Solucion, int>? calculoHeuristica = null)
    {
        IListaCandidatos candidatos = Lista ?? throw new InvalidOperationException("La lista no está inicializada.");
        
        // ESTADO INICIAL: Se añade la solución inicial a la cola con prioridad 0
        candidatos.Anhadir(solucionInicial, 0); 
        
        // Diccionario para evitar ciclos/revisitar nodos
        var vistos = new Dictionary<string, int>();
        bool finalizado = false;
        int revisados = 0;
        Solucion? solucionEncontrada = null;

        // BUCLE PRINCIPAL: Continúa mientras no se encuentre solución y haya candidatos
        while (!finalizado && candidatos.Count > 0)
        {
            // Extrae el siguiente candidato según la política de la Lista
            var solucion = candidatos.ObtenerSiguiente();
            vistos[solucion.ToString()] = solucion.Coste;
            revisados += 1;

            // CRITERIO DE FINALIZACIÓN: Si se cumple el criterio de parada, hemos encontrado la meta
            if (criterioParada(solucion))
            {
                finalizado = true;
                solucionEncontrada = solucion;
                break;
            }

            // GENERACIÓN DE VECINOS: Obtener todos los estados sucesores del estado actual
            var vecinos = obtenerVecinos(solucion);
            foreach (var vecino in vecinos)
            {
                var nueva_solucion = new Solucion(0, vecino.Coords);

                // Solo procesa vecinos no visitados (evita ciclos)
                if (!vistos.ContainsKey(nueva_solucion.ToString()))
                //Este condicional es fundamental.
                {
                    // Calcula el coste acumulado y añade a candidatos con su prioridad
                    nueva_solucion.Coste = solucion.Coste + calculoCoste(solucion, nueva_solucion);
                    candidatos.Anhadir(nueva_solucion, CalculoDePrioridad(nueva_solucion, calculoHeuristica));
                }
            }
        }

        return (solucionEncontrada, revisados);
    }
}

/// Implementación concreta: Algoritmo A*
public class AEstrella : AlgoritmoDeBusqueda
{
    public AEstrella()
    {
        // UTILIDAD DE ColaDePrioridad:
        // - Ordena los candidatos por f(n) = g(n) + h(n)
        // - g(n) = coste acumulado desde inicio
        // - h(n) = heurística estimada al objetivo
        // - Permite exploración eficiente del espacio de búsqueda
        Lista = new ColaDePrioridad(); 
    }

    /// Calcula f(n) = g(n) + h(n) para ordenar la cola de prioridad
    public override int CalculoDePrioridad(object nodo_info, object? calculo_heuristica = null)
    {
        var solucion = nodo_info as Solucion ?? throw new ArgumentException("nodo_info debe ser Solucion");
        var heur = calculo_heuristica as Func<Solucion, int>;
        return solucion.Coste + (heur?.Invoke(solucion) ?? 0);
    }
}
}