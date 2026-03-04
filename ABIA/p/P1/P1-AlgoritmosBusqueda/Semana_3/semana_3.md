# Semana 3: Búsqueda Informada (A* y Búsqueda Avara)

En esta tercera semana de la práctica, se han implementado dos algoritmos de búsqueda informada para resolver el problema de las n-reinas: **Búsqueda A* Mejorada** y **Búsqueda Avara (Greedy)**. El objetivo es comparar cómo la introducción de una heurística afecta drásticamente a la eficiencia de la búsqueda.

## 1. Implementación de Algoritmos

Se han realizado las siguientes modificaciones y adiciones respecto a las semanas anteriores:

- **Heurística de Conflictos:** Se ha implementado la función `CalculoHeuristica` en `Ejecucion3.cs`, la cual cuenta el número total de pares de reinas que se atacan entre sí (en filas, columnas o diagonales). Un estado con 0 conflictos representa una solución válida.
- **Búsqueda Avara (`BusquedaAvara`):** Se ha creado una nueva clase que hereda de `AlgoritmoDeBusqueda`. Esta búsqueda es "avara" o "voraz" porque el cálculo de la prioridad ignora completamente el coste acumulado (`g(n)`), basándose únicamente en el valor de la heurística (`h(n)`): `f(n) = h(n)`.
- **A* Mejorada:** Utiliza la misma clase base pero con el cálculo de prioridad estándar `f(n) = g(n) + h(n)`.

## 2. Resultados Obtenidos

Se ha ejecutado el programa incrementando el número de reinas hasta superar el límite de 15.000 nodos evaluados.

### Búsqueda A* Mejorada

| Número de Reinas | Nodos Expandidos |
|------------------|------------------|
| 4                | 32               |
| 5                | 197              |
| 6                | 4.102            |
| 7                | 82.678           |

*El límite de 15.000 se alcanzó con **7 reinas**.*

### Búsqueda Avara (Greedy)

| Número de Reinas | Nodos Expandidos |
|------------------|------------------|
| 4                | 13               |
| 8                | 171              |
| 12               | 1.393            |
| 16               | 2.427            |
| 20               | 9.451            |
| 24               | 3.961            |
| 26               | 15.813           |

*El límite de 15.000 se alcanzó con **26 reinas**.*

*(Nota: Los resultados de la Búsqueda Avara muestran variabilidad debido a que el algoritmo no garantiza la ruta más corta, sino que busca llegar rápido al objetivo).*

## 3. Análisis Comparativo: El "Coste" de la Optimalidad

Tras los experimentos, hemos analizado por qué la Búsqueda Avara es capaz de manejar tableros mucho más grandes que A* bajo el mismo límite de 15.000 nodos:

- **A* y la Búsqueda de la Solución Óptima:** En el problema de las $n$-reinas, definimos como **solución óptima** aquella que alcanza el estado sin conflictos con el **menor número de movimientos de reinas** posible. Para garantizar esto, A* utiliza el coste acumulado $g(n)$. Como cada movimiento suma $1$ al coste: si avanza mucho en profundidad, el valor de $g(n)$ sube lo suficiente como para que el algoritmo decida "frenar" y volver a revisar niveles superiores para asegurarse de que no se ha saltado un camino más corto.

- **La búsqueda Avara:** Por otro lado al ignorar por completo el coste acumulado ($g(n)$), la Búsqueda Avara deja de preocuparse por si el camino es el más corto. Su única obsesión es reducir los conflictos ($h(n)$) en el siguiente paso. Al no tener el coste $g(n)$ que le obliga a mirar hacia atrás, el algoritmo profundiza rápidamente en el árbol de búsqueda. Aunque la solución encontrada pueda ser **subóptima** (requerir más movimientos de los estrictamente necesarios), esta agresividad le permite resolver tableros de hasta **26 reinas** revisando menos de 15.000 nodos. Mientras que A* al asegurar optimalidad requiere revisar mas nodos. Aun así, si bien no es optima, si es completa pues por grande que sean el numero de configuraciones del tablero, siguen siendo finitos. Y al implementar un control de duplicados evitamos los bucles. Tambien con la cola de prioridad podemos hacer backtrack en caso de llegar a un nodo no meta y sin hijos. Por tanto nuestra implementación de Avara es completa mas no necesariamente optima pues no lo asegura.

## 4. Conclusión Final

**Asegurar la optimalidad no es gratis**: el esfuerzo que realiza A* para garantizar que hemos llegado a la solución con el mínimo número de movimientos posibles se traduce en una explosión de nodos expandidos(analizar muchas soluciones/configuraciones de reinas en el tablero), esto garantiza la optimalidad pero ralentiza las evaluaciones, mientras que avara con la implementación actual asegura soluciones a una velocidad mucho mayor, solo que estas no necesariamente son optimas. En la naturaleza de este problema NO nos interesa conseguir soluciones optimas sino simplemente **soluciones validas**, nos basta con poder configurar n reinas en un tablero nxn sin que estas se ataquen entre si, son esas las condiciones del problema, no necesitamos que la configuración se lleve a cabo moviendo el menor numero de reinas posibles en el proceso. Por eso para este problema la implementación de Avara resulta mejor que A*. 