# Explicación Exhaustiva - Práctica 3 (Pooling)

## Tarea 1: Análisis del código y sus secciones

El objetivo de esta tarea es entender cómo se estructura un programa que compara la ejecución secuencial con la paralela usando **Pooling**.

> [!PDF|yellow] [[EnunciadoP3.pdf#page=3&selection=51,0,57,33&color=yellow|EnunciadoP3, p.3]]
> > Finalmente, hay que tener en cuenta que en el aspecto técnico, la técnica de Pooling permite el aprovechamiento de recursos al re-usar procesos o hilos, en vez de crearlos y destruirlos constantemente. Esta diferencia será la base de la existencia de esta técnica.

   -  Los procesos/hilos NO se destruyen al terminar una tarea, simplemente se quedan esperando a que les llegue nuevas tareas via una cola. Por que? El comportamiento por defecto de un proceso/hilo es eliminarse tras terminar su trabajo, esta funcionalidad es vital para evitar **procesos zombies**, es decir, tener cientos de procesos abiertos que no están haciendo nada.
# Tarea 1: Análisis del código y sus secciones
### 1. Resolución del Problema (La "Carga")
El corazón del cálculo está en la función `evaluate_item`.
```python
def evaluate_item(number, count):
    y = 0
    for i in range(0, count):
        y = y + int((y * 5.5) / 1e8) + i % (number + 10)
    return y
```
*   **¿Qué hace?**: Es una tarea puramente **CPU-bound** (intensiva en cómputo). No tiene `sleeps` ni accesos a disco/red. Hace cálculos matemáticos repetitivos.
*   **Parámetro `count`**: Determina la "pesadez" de cada tarea. A mayor `count`, más iteraciones.
*   **Importancia para el examen**: El profesor puede preguntar: *"Si cambiamos la operación por un `time.sleep(1)`, ¿seguiría siendo CPU-bound?"*. La respuesta es **No**, sería I/O-bound (o bloqueante), y ahí los hilos (threads) sí podrían ser eficientes a pesar del GIL.

### 2. Gestión del Paralelismo (Pooling)
Aquí es donde usamos la librería `concurrent.futures`.

#### A. Creación del Pool
```python
with PoolType(max_workers=workers_num) as executor:
```
*   **`PoolType`**: Puede ser `ProcessPoolExecutor` (procesos) o `ThreadPoolExecutor` (hilos).
*   **`max_workers`**: El número de "obreros" (procesos o hilos) que creamos de antemano.
*   **La cláusula `with`**: Es vital. Garantiza que, al terminar el bloque, el pool se cierre y se liberen los recursos (limpieza automática).

#### B. Envío de tareas (Submit)
```python
futures = list()
for item in tasks_list:
    futures.append(executor.submit(evaluate_item, item, count))
```
*   **`executor.submit(...)`**: Lanza la función al pool. **No espera** a que termine. Devuelve un objeto **Future**.
*   **¿Qué es un Future?**: Es una "promesa". Representa un cálculo que se está realizando en segundo plano.

#### C. Recogida de resultados
```python
result_items = list()
for f in futures:
    result_items.append(f.result())
```
*   **`f.result()`**: Aquí es donde el programa **se bloquea** y espera a que esa tarea específica termine para obtener el valor.

### 3. Gestión Experimental y Configuración
Se encuentra principalmente en el bloque `if __name__ == "__main__":`.
*   **Variables de control**: `NUM_TASKS` (cuántas tareas), `N_WORKERS_LIST` (lista de cuántos procesos/hilos probar), `COUNT_INI/MAX` (rango de dificultad de la tarea).
*   **`measurements`**: Un diccionario donde guardamos los tiempos para luego compararlos.
*   **¿Por qué `pools` es una lista?**: Para permitir la **iteración automática** sobre diferentes tipos de paralelismo (procesos e hilos). Esto facilita la **comparación de rendimiento** en un solo ciclo de ejecución sin duplicar código.

---
# Tarea 2

### Teoría Clave para el Test (Variantes)

1.  **¿Por qué usar Pooling en vez de crear procesos a mano?**: 
    *   Crear un proceso es "caro" (consume tiempo y memoria). 
    *   **Pooling** crea los procesos una sola vez y los **reutiliza**. Si tienes 10,000 tareas y un pool de 4 procesos, los 4 procesos irán cogiendo tareas de la cola según queden libres.
2.  **GIL (Global Interpreter Lock)**:
    *   Python tiene un candado que impide que dos hilos ejecuten código Python a la vez en el mismo proceso.
    *   **Resultado**: En tareas de cálculo (como esta), los `hilos` (THR) tardarán **lo mismo o más** que la ejecución secuencial (SEQ). Para paralelismo real en cálculo, necesitamos `procesos` (PRO).
3.  **Escenario de "Sobrecarga" (Overhead)**:
    *   Si las tareas son muy cortas (ej. `count=10`), el tiempo que tarda Python en gestionar el Pool es mayor que el ahorro del paralelismo. Podrías ver que SEQ es más rápido que PRO.


# Tarea 2: VALIDITY TEST

> ctrl + click izquierdo para verla completo.
> -> Salida de "VALIDITY TEST"
![[Pasted image 20260304123635.png]]
 1. **La Configuración (Inputs)**
* **NUM_LIST_LEN** -> 5: Significa que tenemos 5 tareas totales por hacer.
* **N_WORKERS_LIST** -> [2, 4]: El experimento probará a usar 2 trabajadores y luego 4. **De que tipo?** tanto procesos como hilos. 2 hilos/2procesos y 4hilos/4procesos. **Por que?** Para comparar los resultados de aplicar paralelismo sobre uno u otro usando pooling.
* **COUNT_INI** (1e3) y COUNT_MAX (1e4): Indica que primero haremos las 5 tareas con una dificultad de 1,000 iteraciones cada una, y luego las repetiremos con 10,000 iteraciones (10 veces más pesadas).
> Fíjese que en la respuesta solo hay PRO_per_task, y no THR_per_task. Esto esta hecho así por motivos pedagógicos. La idea de el output final es demostrar la importancia de aplicar pooling cuando es necesario para no estar creando y destruyendo procesos de forma constante, podemos ver como entre dar procesos a cada tarea, es decir, creando y destruyendo o aplicando pooling hay un empeoramiento de al rededor del 50% de tiempo, es decir, tarda casi la mitad mas de tiempo solo por no aplicar pooling.
-   1. ¿Cómo se generan las tareas?
-   En el archivo codigo1.py, dentro de la función run_experiment, verás esta línea:
-    1 tasks_list = [x for x in range(1, NUM_TASKS + 1)]
-    * Si NUM_TASKS (que en la consola sale como NUM_LIST_LEN) es 5, entonces tasks_listes:
-    * [1, 2, 3, 4, 5].
-   1. ¿Qué se le pasa a la función?
-   Cuando el programa empieza a ejecutar las tareas (ya sea de forma secuencial o paralela), hace esto:
-    * Tarea 1: Llama a evaluate_item(1, count)
-    * Tarea 2: Llama a evaluate_item(2, count)
-    * Tarea 3: Llama a evaluate_item(3, count)
-    * Tarea 4: Llama a evaluate_item(4, count)
-    * Tarea 5: Llama a evaluate_item(5, count)
### Conceptos Fundamentales (Analogías para el Test)

#### ¿Qué es un Pool y el procedimiento Pooling?
Imagina un restaurante con 4 cocineros fijos (**Pool**). 
*   **Sin Pooling**: Cada vez que llega un pedido, contratas a un cocinero, hace el plato y lo despides. El tiempo perdido en papeleo (contratación/despido) es enorme (**Overhead**).
*   **Con Pooling**: Los 4 cocineros están siempre allí. Van cogiendo pedidos de una cola conforme se liberan. Es mucho más eficiente porque **reutilizan** el recurso (el cocinero).

---

### Análisis de Resultados: "VALIDITY TEST" (Caso de Examen)

Si el profesor muestra una tabla de tiempos como esta:

| N | SEQ | PRO_2 | PRO_4 | THR_2 | THR_4 | PRO_per_task_2 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1e3** | 0 | 9 | 11 | 1 | 1 | **16** |

#### Puntos clave para razonar:
1.  **Validación**: Si los "RESULTS" (las listas de números) son iguales en todos los métodos, el programa es **correcto**.
2.  **Overhead (Sobrecarga)**: ¿Por qué SEQ (0ms) es más rápido que PRO_2 (9ms)? Porque la tarea es tan pequeña (1e3) que tardas más en crear los procesos que en calcular. El paralelismo tiene un "coste de gestión".
3.  **Ventaja del Pooling**: ¿Por qué PRO_2 (9ms) es más rápido que PRO_per_task_2 (16ms)? Porque el Pooling **reutiliza** procesos, mientras que el "per_task" crea y destruye uno nuevo por cada tarea, lo que es mucho más costoso.
4.  **Hilos vs Procesos (GIL)**: En este código, los hilos (THR) parecen rápidos porque son "ligeros" de crear, pero en tareas muy pesadas el **GIL de Python** les impedirá ganar a los procesos (PRO).

## Tarea 2: Ejecución del código, prueba de validación

### 1. El concepto de Escenario Base (Baseline)
En esta práctica, la ejecución **SEQ (Secuencial)** es tu "Baseline". Es la verdad absoluta. Si el paralelismo da un resultado distinto a SEQ, el programa no vale (está "invalidado").

### 2. ¿Qué es la prueba de validación?
Es comparar la lista de salida de los métodos paralelos con la lista de salida del método secuencial. 
*   **Importancia**: Asegura la **integridad de los datos**. Al dividir tareas, es fácil cometer errores de concurrencia que alteren el resultado final.

### 3. Escalabilidad (Pequeña escala vs Gran escala)
*   **Razonamiento**: Antes de lanzar un cálculo de 3 días en un superordenador, validas con una carga pequeña (1e3, 5 tareas) que el algoritmo funciona bien en paralelo. Si falla en pequeño, fallará en grande.

---

## Tarea 3: Ejecución del código, justificación del uso de Pools 

En esta tarea comparamos el paralelismo con Pooling (`PRO_x`) frente al paralelismo sin Pooling (`PRO_per_task_x`).

### 1. El coste de creación/destrucción
*   **`PRO_per_task`**: Crea un proceso nuevo para cada tarea y lo destruye al terminar. Para 2,000 tareas, se realizan 2,000 operaciones de `fork()`/`spawn`.
*   **Efecto**: El tiempo total se dispara porque el Sistema Operativo (SO) gasta más tiempo gestionando la vida de los procesos que haciendo el cálculo real.

### 2. Consumo de recursos y límites del SO
*   **Cambio de contexto (Context Switch)**: Al tener muchos procesos naciendo y muriendo, el procesador gasta ciclos cambiando de una tarea a otra.
*   **Límite de procesos**: Si lanzamos demasiados procesos simultáneos, podemos saturar el límite de procesos del SO (`ulimit`). El Pooling protege el sistema al mantener un número **fijo y controlado** de trabajadores.

### 3. Agrupación de tareas
*   **4 procesos vs 8 procesos**: Usar más procesos en el Pool (8 en vez de 4) no siempre es mejor si las tareas son cortas, ya que el coste de organizar a 8 personas es mayor que el de organizar a 4.

**Comparación de Escala (Examen):**
*   **Test de Validez (Pequeña escala)**: Con solo 5 tareas (`NUM_LIST_LEN=5`), se crean 5 procesos en total. El tiempo de gestión es despreciable.
*   **Experimento Tarea 3 (Gran escala)**: Con 2,000 tareas, el método `PRO_per_task` crea y destruye **2,000 procesos**. 
*   **Resultado**: Mientras que con Pooling (`PRO_x`) tardamos ~350ms, sin Pooling (`PRO_per_task`) tardamos ~6,000ms. Esto demuestra que el coste de creación/destrucción se **acumula** linealmente con el número de tareas, convirtiéndose en el cuello de botella principal.
> El método de pooling 

---

### Teoría Clave para el Test (Variantes)

1.  **¿Por qué usar Pooling en vez de crear procesos a mano?**: 
    *   Crear un proceso es "caro" (consume tiempo y memoria). 
    *   **Pooling** crea los procesos una sola vez y los **reutiliza**.
2.  **GIL (Global Interpreter Lock)**:
    *   Python tiene un andado que impide que dos hilos ejecuten código Python a la vez en el mismo proceso.
3.  **Escenario de "Sobrecarga" (Overhead)**:
    *   Si las tareas son muy cortas, el tiempo de gestión del Pool supera al ahorro del paralelismo.

> [!PDF|yellow] [[EnunciadoP3.pdf#page=6&selection=16,0,17,15&color=yellow|EnunciadoP3, p.6]]
> > Dentro del método que crea y destruye procesos, ¿hay diferencias entre agrupar tareas y usar 4 procesos u 8?

- Si. Si nuestro procesador es capaz de llevar a cabo 8 procesos en paralelo notaremos una mejoría usando paralelismo de 8 en lugar de 4 o de 2. 

