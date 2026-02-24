# 008_colas_thread_safe_y_multiples_prod_cons.md

**Página de referencia en `EnunciadoP2.pdf`:** 17 (Sección 4: "Múltiples productores y consumidores" e "Información" sobre `thread-safe`), 18 (Clases `ProducerThread`, `ConsumerThread` y función `decrease_counter`) y 19 (Funciones `spawn` y `run_experiment`, así como el apartado "Experimentación").

## Colas Thread-Safe para Múltiples Productores y Consumidores

En escenarios más complejos, donde hay múltiples productores y consumidores, la gestión de un búfer compartido con semáforos simples (como en el ejemplo básico del problema productor-consumidor) puede volverse engorrosa y propensa a errores. Las **colas thread-safe** (o "colas seguras para hilos") ofrecen una solución elegante y robusta para este tipo de coordinación.

### ¿Qué es una Cola Thread-Safe?

Una cola thread-safe es una estructura de datos que permite a múltiples hilos o procesos añadir (`put()`) y retirar (`get()`) elementos de forma concurrente sin preocuparse por las condiciones de carrera. Internamente, estas colas utilizan mecanismos de sincronización (como locks y semáforos) para proteger sus operaciones, garantizando la coherencia de los datos.

En Python, el módulo `queue` proporciona la clase `Queue` para hilos y el módulo `multiprocessing` proporciona la clase `Queue` para procesos, ambas son thread-safe.

### Implementación con `multiprocessing.Queue` (`codigo5-MultProdCons.py`)

El `codigo5-MultProdCons.py` utiliza una cola thread-safe (`queue = Queue(QUEUE_SIZE)`) para coordinar a múltiples `ProducerThread` y `ConsumerThread`.

#### Clase `ProducerThread`

```python
class ProducerThread(Thread):
    def run(self):
        global queue, items_pending, OUTPUT
        while True:
            # ... (generación de num, sleep_time) ...
            try:
                queue.put(num, block=QUEUE_BLOCK) # Intenta añadir un ítem a la cola
                # ... (notificación y manejo de Full) ...
            except Full:
                pass # Si la cola está llena y block=False, se ignora
            # ... (sleep y condición de salida) ...
```
El productor simplemente intenta colocar ítems en la cola. Si la cola está llena, el método `put()` se bloqueará hasta que haya espacio (si `block=True`) o lanzará una excepción `Full` (si `block=False` y no hay espacio).

#### Clase `ConsumerThread`

```python
class ConsumerThread(Thread):
    def run(self):
        global queue, items_pending, OUTPUT
        while True:
            # ... (sleep_time) ...
            try:
                num = queue.get(block=QUEUE_BLOCK) # Intenta retirar un ítem de la cola
                decrease_counter() # Decrementar contador global (también thread-safe)
                # ... (notificación) ...
            except Empty:
                pass # Si la cola está vacía y block=False, se ignora
            # ... (sleep y condición de salida) ...
```
El consumidor intenta retirar ítems de la cola. Si la cola está vacía, el método `get()` se bloqueará hasta que haya un ítem disponible (si `block=True`) o lanzará una excepción `Empty` (si `block=False` y la cola está vacía). La función `decrease_counter()` decrementa un contador global `items_pending` que también está protegido por un semáforo (`counter_lock`).

### Ventajas de las Colas Thread-Safe

*   **Simplificación del Código:** La lógica de sincronización compleja (manejo de locks, contadores de ítems/slots) se encapsula dentro de la implementación de la cola, simplificando el código del productor y del consumidor.
*   **Robustez:** Al ser thread-safe, la cola garantiza que las operaciones `put()` y `get()` sean atómicas y que los datos se mantengan coherentes, incluso bajo alta concurrencia.
*   **Facilidad para Múltiples Hilos:** Permite escalar fácilmente el número de productores y consumidores sin introducir nuevos problemas de sincronización manual sobre el búfer.

La Figura 14 en la página 17 del enunciado muestra una representación gráfica de cómo múltiples hilos (productores y consumidores) comparten datos a través de una cola central. Esta estructura es fundamental para los experimentos de las Tareas 12 a 15, donde se varían los parámetros para analizar el comportamiento del sistema.
