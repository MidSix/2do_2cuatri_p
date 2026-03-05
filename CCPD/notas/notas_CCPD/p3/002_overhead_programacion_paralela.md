# Overhead en Programación Paralela (P3)

## Definición
El **Overhead** (sobrecarga) es el tiempo que el sistema (hardware y software) dedica a realizar tareas necesarias para la ejecución de un programa, pero que **no forman parte del cálculo útil** (la tarea en sí).

En el contexto de la Práctica 3 con Python, el overhead incluye:
1. **Creación de recursos:** El tiempo que tarda el Sistema Operativo en "engendrar" un nuevo Proceso o Hilo.
2. **Comunicación Inter-Procesos (IPC):** El tiempo necesario para mover datos entre la memoria del programa principal y la memoria de los procesos hijos.
3. **Gestión de colas:** El trabajo del `PoolExecutor` para decidir qué trabajador toma cada tarea.
4. **Context Switching:** El esfuerzo de la CPU para cambiar de un proceso a otro.

---

## Análisis Empírico (Basado en `codigo1.py`)

### 1. El Paradox de las Tareas Ligeras (`1e3`)
En tu experimento, para 1,000 iteraciones, los resultados fueron:
* **SEQ:** 0ms
* **PRO_2:** 9ms

**¿Por qué gana el secuencial?** 
Porque el **tiempo de overhead** (los 9ms de crear procesos y repartir tareas) es mayor que el **tiempo de cómputo** (los <1ms de hacer las sumas). Paralelizar aquí es "matar moscas a cañonazos".

### 2. El Desastre de `PRO_per_task`
Este es el ejemplo máximo de overhead. Mientras que `PRO_2` (con Pooling) tarda **13ms**, `PRO_per_task_2` tarda **20ms**.
* **Causa:** En cada tarea, el sistema debe destruir el proceso anterior y crear uno nuevo de cero. El hardware pasa más tiempo "gestionando personal" que "trabajando en la obra".

### 3. Procesos vs Hilos
* **Procesos (PRO):** Tienen un overhead **alto**. Son independientes y requieren copiar memoria.
* **Hilos (THR):** Tienen un overhead **bajo**. Comparten memoria y son rápidos de crear.

> **Lección Clave:** El paralelismo solo es eficiente cuando el tiempo de ejecución de la tarea es significativamente mayor que el tiempo de overhead necesario para gestionarla.
