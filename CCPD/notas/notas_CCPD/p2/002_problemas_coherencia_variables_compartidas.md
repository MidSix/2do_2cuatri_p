# 002_problemas_coherencia_variables_compartidas.md

**Página de referencia en `EnunciadoP2.pdf`:** 6 (Sección 2: "Locks y operaciones atómicas", introducción a problemas de coherencia) y 8 (Sección 2.1: "Conteo básico con variable compartida e hilos" y "Tarea 2 - Conteo básico, tiempos y validación").

## Problemas de Coherencia en Variables Compartidas (Condiciones de Carrera)

Cuando múltiples hilos de ejecución acceden y modifican una misma variable compartida sin ningún tipo de coordinación, pueden surgir problemas de **coherencia de datos**. Estos problemas son una manifestación de las **condiciones de carrera** (race conditions).

### ¿Qué es una Condición de Carrera?

Una condición de carrera ocurre cuando la salida de un programa depende del orden o la temporización de eventos incontrolables, como la secuencia en que los hilos acceden a un recurso compartido. Si el resultado final del programa es inconsistente o impredecible debido a que la ejecución de los hilos se entrelaza de una manera no determinista, estamos ante una condición de carrera.

### El Problema de la No-Coherencia (`codigo1-ThreadCount.py` `unsafe`)

El `codigo1-ThreadCount.py` ilustra este problema con un contador (`CountContainer`) que es incrementado por varios hilos. El método `unsafe` realiza la siguiente secuencia de operaciones:

1.  `c = count.get_count()`: Un hilo lee el valor actual del contador.
2.  `c = count.add_to_count(c, 1)`: El hilo incrementa su copia local del valor.
3.  `count.set_count(c)`: El hilo escribe el nuevo valor de vuelta al contador compartido.

Si dos hilos (`Hilo A` y `Hilo B`) ejecutan `unsafe` concurrentemente, puede ocurrir la siguiente secuencia de eventos, llevando a un resultado incorrecto:

*   `Hilo A` lee `count` (ej. `0`).
*   `Hilo B` lee `count` (ej. `0`).
*   `Hilo A` incrementa su copia a `1`.
*   `Hilo B` incrementa su copia a `1`.
*   `Hilo A` escribe `1` a `count`.
*   `Hilo B` escribe `1` a `count`.

Aunque ambos hilos intentaron incrementar el contador, el valor final es `1` en lugar del `2` esperado. Uno de los incrementos se "pierde" porque el segundo hilo sobrescribe el valor del primero basándose en un valor inicial obsoleto.

### Impacto en la Práctica

Este tipo de problemas es difícil de depurar porque no siempre se manifiesta. Depende de la temporización precisa de la ejecución de los hilos, que puede variar en cada ejecución del programa. Los sistemas operativos pueden alternar la ejecución de hilos en cualquier momento, haciendo que el orden de las operaciones sea impredecible.

La consecuencia es que, en escenarios donde la exactitud del conteo o el estado de una variable compartida es crítico, el uso de mecanismos de sincronización es indispensable para garantizar la coherencia y la corrección del programa. La Tarea 2 del enunciado pide observar y entender esta inconsistencia.
