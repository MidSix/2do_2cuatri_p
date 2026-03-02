/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/
using n_reinas;
public class BusquedaAvara : AlgoritmoDeBusqueda
{/* 
Implementación de la búsqueda A* con heurística avara se trata de una búsqueda 
que solo considera la heurística para decidir qué nodo expandir, sin tener en cuenta 
el coste acumulado desde el nodo inicial. En otras palabras, A* con heurística avara 
se comporta como una búsqueda voraz, siempre eligiendo el nodo que parece estar más 
cerca de la meta según la heurística, sin importar cuánto haya costado llegar a ese nodo. 
Esto puede llevar a soluciones subóptimas o incluso a no encontrar una solución si la heurística
no es adecuada, en este caso la función de heurística que hemos implementado cuenta el número
de conflictos entre las reinas.
 */
    public BusquedaAvara()
    {
        Lista = new ColaDePrioridad();
    }

    public override int CalculoDePrioridad(object nodo_info, object? calculo_heuristica = null)
    {
        var solucion = nodo_info as Solucion ?? throw new ArgumentException("Debe ser Solucion");
        var heur = calculo_heuristica as Func<Solucion, int>;
        
        return heur?.Invoke(solucion) ?? 0; // Ignoramos el coste acumulado.

    }
    public int HeuristicaAvara(Solucion solucion)
    {
    int conflictos = 0;
    int n = solucion.Coords?.Count ?? 0;

    for (int i = 0; i < n; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            var r1 = solucion.Coords![i];
            var r2 = solucion.Coords![j];

            if (r1.Item1 == r2.Item1 || // Comprobamos si se atacan (Misma Fila, Columna o Diagonal)
                r1.Item2 == r2.Item2 || 
                Math.Abs(r1.Item1 - r2.Item1) == Math.Abs(r1.Item2 - r2.Item2))
            {
                conflictos++;
            }
        }
    }
        return conflictos;
    }
}