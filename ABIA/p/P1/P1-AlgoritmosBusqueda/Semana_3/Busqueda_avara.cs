/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/
using n_reinas;
//Uso esa clase para hacer override del calculo de prioridad, ya que el algoritmo A*
// con heurística avara solo se basa en la heurística para decidir qué nodo expandir.
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

Podemos definir "optimo" como la solucion que permite disponer a las reinas en el tablero
con el menor numero de movimientos posible. De esta manera,
una solución subóptima sería aquella que, aunque resuelve el problema de colocar las reinas sin conflictos,
requiere más movimientos que la solución óptima. Asegurarse que la solucion
sea la optima no es gratis, A* necesita expandir mas nodos para garantizar la optimalidad 
por ello vemos como el algoritmo voraz es capaz de manejar tableros de mayor tamaño que A*,
si capamos los nodos a expandir.
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
    
}