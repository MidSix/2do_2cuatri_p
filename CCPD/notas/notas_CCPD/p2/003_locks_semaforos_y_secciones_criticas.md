# 003_locks_semaforos_y_secciones_criticas.md

**Página de referencia en `EnunciadoP2.pdf`:** 6 (Sección 2: "Locks y operaciones atómicas", introducción a semáforos y locks), 7 (Figuras 3 y 4, explicación gráfica de locks) y 8 (Sección 2.1: "Conteo básico con variable compartida e hilos", método `safe` de `codigo1-ThreadCount.py`).

## Locks, Semáforos y Secciones Críticas

Para resolver los problemas de coherencia y las condiciones de carrera que surgen al acceder a variables compartidas, se utilizan mecanismos de sincronización como **locks** y **semáforos**. Estos permiten controlar el acceso a las **secciones críticas** del código.

### Sección Crítica

Una **sección crítica** es un segmento de código que accede a un recurso compartido (como una variable, una estructura de datos o un dispositivo) y que no debe ser ejecutado por más de un hilo a la vez para mantener la coherencia de los datos.

### Locks (Cerraduras / Mutexes)

Un **lock** (o mutex, del inglés *mutual exclusion*) es una herramienta de sincronización que asegura que solo un hilo pueda ejecutar una sección crítica de código en un momento dado. Funciona como una cerradura:
*   Un hilo que desea entrar en la sección crítica debe primero "adquirir" (acquire) el lock.
*   Si el lock está disponible, el hilo lo toma y entra en la sección crítica.
*   Si el lock ya está tomado por otro hilo, el hilo que intenta adquirirlo se bloquea y espera hasta que el lock sea liberado.
*   Una vez que el hilo termina su trabajo en la sección crítica, debe "liberar" (release) el lock para que otros hilos puedan adquirirlo.

En Python, `threading.Lock` o un `threading.Semaphore(1)` (un semáforo con valor inicial 1) se comportan como un lock.

### Semáforos

Un **semáforo** es una herramienta de sincronización más general que un lock. Un semáforo mantiene un contador interno.
*   Cuando un hilo llama a `acquire()` en un semáforo, su contador se decrementa. Si el contador llega a un valor negativo, el hilo se bloquea.
*   Cuando un hilo llama a `release()` en un semáforo, su contador se incrementa. Si hay hilos bloqueados esperando por este semáforo, uno de ellos es desbloqueado.

La diferencia clave con un lock es que un semáforo puede permitir el acceso a un número predefinido de hilos a una sección (si el valor inicial es mayor que 1). Un semáforo con un valor inicial de 1 se comporta como un lock binario.

#### `threading.Semaphore` en Python

En Python, `threading.Semaphore` permite crear semáforos. El valor pasado al constructor define el número máximo de hilos que pueden adquirir el semáforo concurrentemente.

### Aplicación (Método `safe` en `codigo1-ThreadCount.py`)

El `codigo1-ThreadCount.py` utiliza la sección crítica protegida por un semáforo (`self.__count_access`) en el método `safe` para garantizar la coherencia:

```python
def safe(count, n):
    while n > 0:
        count.lock_count()   # Adquirir el lock (entra en sección crítica)
        c = count.get_count()
        c = count.add_to_count(c, 1)
        count.set_count(c)
        count.unlock_count() # Liberar el lock (sale de sección crítica)
        n -= 1
```

En este caso, `count.lock_count()` adquiere el semáforo y `count.unlock_count()` lo libera. Esto asegura que solo un hilo a la vez pueda ejecutar las operaciones de lectura, modificación y escritura del contador, evitando así las condiciones de carrera y garantizando que el contador llegue al valor esperado, tal como se verifica en la Tarea 2 del enunciado. La Figura 5 de la página 8 muestra esta diferencia entre el acceso seguro (`safe`) y no seguro (`unsafe`).
