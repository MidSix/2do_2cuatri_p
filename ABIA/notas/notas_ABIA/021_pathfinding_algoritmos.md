# Algoritmos de Pathfinding en IA

Los algoritmos de pathfinding o búsqueda de caminos son fundamentales en la Inteligencia Artificial para encontrar la ruta óptima o eficiente entre dos puntos en un grafo o mapa.

- Estos algoritmos se encajan conceptualmente dentro de [[022_Busqueda-Informada_vs_Busqueda-NO-informada]] 

## 1. Búsqueda en Anchura (Breadth-First Search - BFS)
- **Tipo:** Búsqueda no informada.
- **Concepto:** Explora todos los nodos en el nivel actual antes de pasar al siguiente nivel.
- **Ventaja:** Garantiza el camino más corto si todas las aristas tienen el mismo peso.
- **Desventaja:** Alto consumo de memoria (exponencial).

## 2. Búsqueda en Profundidad (Depth-First Search - DFS)
- **Tipo:** Búsqueda no informada.
- **Concepto:** Sigue un camino hasta el final antes de retroceder.
- **Uso:** Útil para juegos donde se requiere explorar todas las posibilidades, pero **no** garantiza el camino más corto.

## 3. Algoritmo de Dijkstra
- **Tipo:** Búsqueda no informada.
- **Concepto:** Una versión ponderada de BFS. Mantiene una lista de distancias acumuladas desde el origen y siempre elige el nodo con la menor distancia.
- **Ventaja:** Encuentra siempre el camino más corto en grafos con pesos no negativos.
- **Limitación:** Explora en todas las direcciones sin guía hacia el objetivo (no usa heurística).

## 4. Búsqueda Voraz (Greedy Best-First Search)
- **Tipo:** Búsqueda informada.
- **Concepto:** Utiliza una **función heurística** $h(n)$ para estimar la distancia al objetivo.
- **Comportamiento:** "Salta" hacia el nodo que parece estar más cerca de la meta.
- **Riesgo:** Puede quedar atrapado en mínimos locales o callejones sin salida si no hay obstáculos directos. No garantiza el camino más corto.

## 5. Algoritmo A* (A-Star)
- **Tipo:** Búsqueda informada.
- **Concepto:** Combina Dijkstra y Búsqueda Voraz. Utiliza la función: $f(n) = g(n) + h(n)$
    - $g(n)$: Coste real acumulado desde el inicio.
    - $h(n)$: Estimación heurística hasta el objetivo.
- **Propiedad:** Es **óptimo y completo** si la heurística es admisible (nunca sobreestima el coste real). Es el estándar de la industria.

## 6. Algoritmo IDA* (Iterative Deepening A*)
- **Tipo:** Búsqueda informada.
- **Concepto:** Combina la eficiencia de espacio de DFS con la optimalidad de A*.
- **Uso:** Muy útil cuando la memoria es limitada y el grafo es muy grande.

## 7. D* (Dynamic A*) / Lite
- **Tipo:** Búsqueda informada.
- **Concepto:** Versiones de A* que pueden recalcular rutas en tiempo real cuando el entorno cambia (obstáculos que aparecen o se mueven).

--- 
## Closer look:
#### Algoritmo A* (A-Star):
-  [Video](https://www.youtube.com/watch?v=hQa9JTtq4Ok) muy goty
- A* cuenta con diversos usos como en Google Maps o en videojuegos, lo cierto es que en cualquier caso, para 2 dimensiones nosotros pasamos el "mundo" a una cuadricula, dicha cuadricula estara representanda por `Cuadradado verde -> nodo/estado inicio` `cuadrado negro -> obstaculos/ausencia de nodos` y `cuadrado rojo -> meta.`        Pero NO podemos operar tampoco con una cuadricula asi que hemos de pasarlo a un grafo que sera aquello que usaremos para llevar a cabo nuestra busqueda.
- `Mundo_Real(2D) --> Cuadricula --> Grafo` 

>Cuadricula --> Grafo: Representacion grafica. El grafo presentado es no dirigido.                       Si pensamos que representa los posibles movimientos de un NPC, significa que puede moverse hacia adelante y tambien regresar sobre sus pasos

- **nodos**: Los posibles estados a los que puede acceder un objeto.
- **aristas**: La conexion que permite pasar de un estado a otro
- **Pesos_de_cada_aristas:** El costo de cambiar de un estado a otro
![[cuadricula_to_grafo.png]] 