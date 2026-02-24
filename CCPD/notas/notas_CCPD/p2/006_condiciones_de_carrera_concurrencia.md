# 006_condiciones_de_carrera_concurrencia.md

> [!PDF|red] [[EnunciadoP2.pdf#page=13&selection=20,0,20,20&color=red|EnunciadoP2, p.13]]
> > Condición de carrera


**Página de referencia en `EnunciadoP2.pdf`:** 13 (Sección 3.3: "Condición de carrera", Tarea 10) y 14 (Figura 11 y `codigo3-ProdConsRace.py`).

## Condiciones de Carrera y No-Determinismo

Las **condiciones de carrera** ocurren cuando la corrección del resultado de un programa concurrente depende de la secuencia o temporización particular de las operaciones de múltiples hilos que acceden a recursos compartidos. El resultado es no determinista; puede variar de una ejecución a otra, incluso con la misma entrada.

### ¿Cómo se Manifiestan?

A diferencia del deadlock, que bloquea el sistema, una condición de carrera puede no siempre causar un fallo evidente. A menudo, se traduce en un resultado incorrecto o inconsistente que es difícil de detectar y reproducir debido a su naturaleza dependiente del tiempo.

### Escenario de Carrera en Productores-Consumidores (`codigo3-ProdConsRace.py`)

El `codigo3-ProdConsRace.py` presenta un escenario donde un productor y un consumidor compiten por un único lock (`item_ready`) para acceder a un recurso. El enunciado (página 14) describe este escenario como "hilos voraces" (greedy threads):

*   **Productor:** Intenta producir un ítem y adquirir el lock.
*   **Consumidor:** Intenta consumir un ítem y adquirir el lock.

A diferencia del `codigo2-ProdCons.py` donde se usaban dos semáforos para una coordinación estricta (item listo vs. ranura disponible), aquí ambos hilos compiten por el *mismo* lock (`item_ready = threading.Semaphore(1)`). El problema surge porque:

1.  El productor, al adquirir `item_ready`, produce un ítem y luego lo libera.
2.  El consumidor, al adquirir `item_ready`, consume el ítem (previamente producido) y luego lo libera.

La condición de carrera aquí se da por la **adquisición del lock**. No hay una garantía de qué hilo (productor o consumidor) ganará el lock en un momento dado, lo que puede llevar a una secuencia de eventos ineficiente o con resultados inesperados si no se controla adecuadamente la cantidad de ítems producidos/consumidos.

Aunque el lock evita que ambos hilos accedan a la sección crítica *simultáneamente*, no hay una coordinación sobre *cuándo* deben producir y *cuándo* deben consumir. Por ejemplo:
*   Si el productor adquiere el lock varias veces seguidas sin que el consumidor lo haga, podría producir ítems que sobrescriben los anteriores (si el búfer es de tamaño 1 como en esta simplificación).
*   Si el consumidor adquiere el lock varias veces seguidas sin que el productor lo haga, intentaría consumir ítems inexistentes (aunque en este código la variable `item` se mantiene, lo que se consume es el *valor actual*).

La Figura 11 en la página 14 ilustra la configuración de lock que genera esta condición de carrera, y el texto explica cómo la ejecución puede "saltar" de un hilo a otro sin aparente orden, debido a la gestión del SO y la competición por el lock. El resultado será que ambos hilos "ganarán" el lock un número similar de veces, pero la eficiencia del proceso podría no ser óptima y el comportamiento es no determinista.

### Diferencia con el problema de coherencia anterior

Mientras que el problema de coherencia en `codigo1-ThreadCount.py` (sin locks) era sobre la *corrección* del valor final de una variable, aquí (con un único lock) el problema es más sobre la *eficiencia* y el *orden no determinista* de las operaciones en un escenario de productor-consumidor simplificado. El lock asegura la atomicidad de la operación en sí (producir o consumir), pero no la coordinación lógica de que un ítem producido debe ser consumido antes de que se produzca otro.
