# 005_interbloqueo_deadlock_concurrencia.md

**Página de referencia en `EnunciadoP2.pdf`:** 12 (Sección 3.2: "Deadlock software", Tarea 9) y 13 (Figuras 9 y 10).

## Interbloqueo (Deadlock) en Programas Concurrentes

Un **interbloqueo** o **deadlock** es una situación en la que dos o más procesos o hilos de un sistema concurrente quedan bloqueados indefinidamente, esperando cada uno por un recurso que otro de los procesos o hilos bloqueados tiene tomado. Es un "abrazo mortal" que impide el avance de cualquiera de las entidades involucradas.

### Condiciones para que ocurra un Deadlock

Para que un deadlock ocurra, deben darse simultáneamente cuatro condiciones (condiciones de Coffman):

1.  **Exclusión Mutua:** Al menos un recurso debe ser no compartible, es decir, solo un proceso/hilo puede usarlo a la vez (por ejemplo, un lock).
2.  **Retención y Espera (Hold and Wait):** Un proceso/hilo debe estar reteniendo al menos un recurso mientras espera adquirir recursos adicionales que están siendo retenidos por otros procesos/hilos.
3.  **No Apropiación (No Preemption):** Un recurso no puede ser quitado por la fuerza a un proceso/hilo que lo tiene. Solo el proceso/hilo que lo retiene puede liberarlo voluntariamente.
4.  **Espera Circular (Circular Wait):** Debe existir una cadena cerrada de procesos/hilos, donde cada uno espera por un recurso retenido por el siguiente proceso/hilo en la cadena.

### Demostración de Deadlock (Tarea 9 y `codigo2-ProdCons.py`)

La Tarea 9 del `EnunciadoP2.pdf` propone un escenario para provocar un deadlock modificando el `codigo2-ProdCons.py`. Originalmente, los semáforos `item_ready` y `item_consumed` se inicializan a `0` y `1` respectivamente.

Si ambos semáforos se inicializan a `0`:
*   `item_ready = threading.Semaphore(0)`
*   `item_consumed = threading.Semaphore(0)`

Consideremos la ejecución:

1.  El **productor** intenta adquirir `item_consumed`. Como su valor inicial es `0`, el productor se **bloquea** esperando a que `item_consumed` sea liberado.
2.  El **consumidor** intenta adquirir `item_ready`. Como su valor inicial es `0`, el consumidor también se **bloquea** esperando a que `item_ready` sea liberado.

En este punto, ambos hilos están bloqueados:
*   El productor espera por `item_consumed`, que nunca será liberado (porque el consumidor está bloqueado y no puede liberarlo).
*   El consumidor espera por `item_ready`, que nunca será liberado (porque el productor está bloqueado y no puede liberarlo).

Se ha formado una espera circular y se cumplen todas las condiciones de deadlock. El programa se "congelará" y no avanzará. La Figura 9 en la página 13 ilustra esta situación con el diagrama de estados, mostrando cómo tanto el productor como el consumidor quedan esperando indefinidamente. La Figura 10 muestra la salida de una ejecución en este estado, donde los mensajes indican que ambos hilos están en estado de espera.

### Prevención y Resolución

La prevención de deadlocks generalmente implica romper una o más de las cuatro condiciones de Coffman. Por ejemplo, asegurándose de que los recursos se adquieran en un orden predefinido (para romper la espera circular) o asignando todos los recursos necesarios a un proceso/hilo antes de que comience a ejecutarse (para romper la retención y espera). Sin embargo, en muchos sistemas complejos, la detección y recuperación de deadlocks puede ser necesaria.
