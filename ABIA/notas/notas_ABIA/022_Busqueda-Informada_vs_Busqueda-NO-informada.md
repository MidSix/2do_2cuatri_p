# Comparativa: Búsqueda Informada vs. No Informada

## Búsqueda No Informada (Búsqueda a Ciegas)

- **Definición:** Este tipo de búsqueda no utiliza ningún conocimiento adicional sobre el problema más allá de la propia definición del grafo (nodos, aristas, estado inicial y final). Exploran el espacio de búsqueda de manera sistemática.
- **Ejemplos:** Búsqueda en Anchura (BFS), Búsqueda en Profundidad (DFS), Algoritmo de Dijkstra.

#### Ventajas
- **Garantía de Solución:** Si existe una solución, algoritmos como BFS la encontrarán.
- **Optimalidad (Condicional):** BFS y Dijkstra garantizan el camino más corto (en grafos no ponderados y ponderados no negativos, respectivamente).

#### Desventajas
- **Ineficiencia:** Son extremadamente lentos en espacios de búsqueda grandes, ya que exploran sin ninguna guía hacia el objetivo.
- **Consumo de Recursos:** Pueden consumir una gran cantidad de memoria (BFS) o tiempo (DFS en ramas muy largas).

## Búsqueda Informada (Búsqueda Heurística)

- **Definición:** Utiliza conocimiento específico del dominio del problema en forma de una **función heurística** ($h(n)$). Esta función estima el coste desde un nodo actual hasta el objetivo, permitiendo guiar la búsqueda hacia los nodos más prometedores.
- **Ejemplos:** A*, Búsqueda Voraz, IDA*.

#### Ventajas
- **Eficiencia:** Son significativamente más rápidos y consumen menos recursos, ya que "podan" grandes partes del árbol de búsqueda que no parecen llevar al objetivo.
- **Escalabilidad:** Permiten resolver problemas mucho más complejos que serían inviables para una búsqueda a ciegas.

#### Desventajas
- **Dependencia de la Heurística:** La calidad de la búsqueda depende directamente de la calidad de la función heurística.
    - Una **mala heurística** puede hacer que el algoritmo sea ineficiente o, en el caso de la búsqueda voraz, que no encuentre la solución óptima.
- **Optimalidad (Condicional):** Para que A* sea óptimo, su heurística debe ser **admisible** (nunca sobreestimar el coste real). Diseñar una buena heurística admisible no siempre es trivial.
