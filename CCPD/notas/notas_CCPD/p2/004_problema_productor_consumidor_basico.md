# 004_problema_productor_consumidor_basico.md

**Página de referencia en `EnunciadoP2.pdf`:** 10 (Sección 3.1: "Escenario base y locks", Tareas 5-7) y 11 (Tarea 8 y Figura 7).

## El Problema Clásico del Productor-Consumidor

El problema del productor-consumidor es un problema clásico de sincronización en computación concurrente. Describe dos tipos de procesos o hilos:
*   **Productores:** Generan datos o "ítems" y los colocan en un búfer o cola compartida.
*   **Consumidores:** Toman datos o "ítems" del búfer o cola compartida y los procesan.

El desafío principal es la coordinación entre productores y consumidores para asegurar que:
1.  Los productores no intenten añadir ítems a un búfer lleno.
2.  Los consumidores no intenten retirar ítems de un búfer vacío.
3.  El acceso al búfer compartido esté sincronizado para evitar condiciones de carrera.

### Implementación Básica con Semáforos (`codigo2-ProdCons.py`)

El `codigo2-ProdCons.py` presenta una implementación básica de este problema utilizando dos semáforos para la coordinación de un único productor y un único consumidor.

*   **`item_ready = threading.Semaphore(0)`**: Este semáforo controla el acceso a los ítems producidos. Se inicializa a `0` porque, al principio, no hay ningún ítem listo para ser consumido. El consumidor intentará adquirirlo y se bloqueará si no hay ítems. El productor lo liberará después de producir un ítem.
*   **`item_consumed = threading.Semaphore(1)`**: Este semáforo controla la "ranura" disponible en el búfer (implícitamente, asumiendo un búfer de tamaño 1 para esta versión básica). Se inicializa a `1` porque, al principio, hay una ranura disponible para que el productor coloque un ítem. El productor intentará adquirirlo y se bloqueará si no hay ranuras disponibles. El consumidor lo liberará después de consumir un ítem.

#### Función `producer()`

```python
def producer():
    global item, ITEMS_CONSUMED
    while True:
        producer_notify("Waiting to produce a new item")
        item_consumed.acquire()  # Esperar a que haya una ranura disponible
        producer_notify("Producing an item")
        item = random.randint(0, 1000) # Producir un ítem
        producer_notify("Produced item number {0}".format(item))
        item_ready.release()     # Señalizar que hay un ítem listo
        if ITEMS_CONSUMED: # Condición de salida
            break
```
El productor espera por `item_consumed` antes de producir, asegurando que siempre haya espacio. Una vez producido, libera `item_ready` para notificar al consumidor.

#### Función `consumer()`

```python
def consumer():
    global item, ITEMS_CONSUMED
    items_consumed = 0
    while True:
        consumer_notify("Waiting for new items")
        item_ready.acquire()     # Esperar a que haya un ítem listo
        consumer_notify("consuming item")
        time.sleep(SLEEP_TIME)   # Simular tiempo de consumo
        items_consumed += 1
        consumer_notify("Consumed item number {0}".format(item))
        item_consumed.release()  # Señalizar que se ha consumido un ítem (ranura libre)
        if items_consumed >= ITEMS_TO_CONSUME: # Condición de salida
            ITEMS_CONSUMED = True
            break
```
El consumidor espera por `item_ready` antes de consumir, asegurando que siempre haya un ítem disponible. Una vez consumido, libera `item_consumed` para notificar al productor.

La Figura 7 en la página 11 del enunciado ilustra gráficamente la secuencia de eventos, mostrando cómo los semáforos (`Acquire`/`Release`) coordinan el flujo de ítems entre el productor y el consumidor.
