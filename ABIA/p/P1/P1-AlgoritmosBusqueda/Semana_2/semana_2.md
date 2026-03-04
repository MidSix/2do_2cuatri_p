# Semana 2: Búsqueda no Informada

En esta segunda semana de la práctica, se han implementado dos algoritmos de búsqueda no informada: **Búsqueda en Anchura (BFS)** y **Búsqueda en Profundidad (DFS)**. El objetivo es comparar su eficiencia en el problema de las n-reinas en términos de nodos expandidos/evaluados.

## 1. Implementación de Algoritmos

Se ha extendido la estructura base de la Semana 1 para incorporar estos nuevos métodos:

- **Cola (FIFO):** Implementada para la búsqueda en anchura, asegurando que se exploren los nodos nivel por nivel.
- **Cola (LIFO):** Implementada para la búsqueda en profundidad, explorando ramas completas antes de retroceder.
- **BusquedaEnAnchura / BusquedaEnProfundidad:** Clases que heredan de `AlgoritmoDeBusqueda` y configuran la lista de candidatos correspondiente.

## 2. Resultados Obtenidos

Se ha ejecutado el programa empezando con `n = 4` y aumentando el número de reinas hasta que el número de nodos evaluados superase los 15.000.

### Búsqueda en Anchura (BFS)

| Número de Reinas | Nodos Evaluados |
|------------------|-----------------|
| 4                | 126             |
| 5                | 1.400           |
| 6                | 22.239          |

*El límite de 15.000 se alcanzó con **6 reinas**.*

### Búsqueda en Profundidad (DFS)

| Número de Reinas | Nodos Evaluados |
|------------------|-----------------|
| 4                | 31              |
| 5                | 71              |
| 6                | 4.114           |
| 7                | 18.698          |

*El límite de 15.000 se alcanzó con **7 reinas**.*

## 3. Análisis Comparativo

- **Eficiencia en Nodos:** En este problema específico y con el estado inicial planteado, DFS ha demostrado ser más eficiente en términos de memoria y tiempo de búsqueda inicial para encontrar una solución válida. BFS explora exhaustivamente todos los estados a la misma profundidad, lo que provoca una explosión combinatoria mucho más rápida (alcanza el límite de 15.000 nodos con solo 6 reinas).
- **Consumo de Memoria:** Aunque no se ha medido explícitamente el uso de RAM, teóricamente BFS es mucho más costoso ya que debe mantener en la cola todos los nodos de un nivel para pasar al siguiente, mientras que DFS solo mantiene la ruta actual.
- **Conclusión:** Para el problema de las n-reinas, donde la profundidad de la solución es conocida y no hay ciclos infinitos (gracias a la gestión de nodos visitados), DFS es una opción más adecuada que BFS cuando no se dispone de una heurística (búsqueda no informada).
