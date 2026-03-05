# 009_parametros_diseno_sistemas_concurrentes.md

**Página de referencia en `EnunciadoP2.pdf`:** 19 (apartado "Experimentación" y descripción de variables), 20 (Tareas 12-15) y 21 (Figuras con resultados de EXP 1-4).

## Parámetros Clave en el Diseño y Experimentación de Sistemas Concurrentes

El rendimiento y el comportamiento de un sistema concurrente son complejos y dependen de múltiples factores. La Práctica 2, especialmente con el `codigo5-MultProdCons.py`, explora cómo varios parámetros influyen en la eficiencia y la sincronización de un sistema productor-consumidor con múltiples hilos.

Comprender el impacto de estos parámetros es crucial para diseñar y optimizar aplicaciones concurrentes.

### Parámetros Fundamentales y su Impacto:

1.  **`NUM_CONSUMERS` y `NUM_PRODUCERS` (Número de Consumidores y Productores)**
    *   **Descripción:** Definen el grado de concurrencia de cada tipo de rol en el sistema.
    *   **Impacto:**
        *   **Relación Productor/Consumidor (Tarea 12 / EXP 1):** Un desequilibrio significativo (e.g., muchos productores y pocos consumidores, o viceversa) puede llevar a la cola a llenarse rápidamente (si hay más producción) o vaciarse constantemente (si hay más consumo). Esto puede causar bloqueos frecuentes en los hilos que esperan por espacio o ítems, o incluso inanición si el desequilibrio es extremo y algunos hilos nunca obtienen acceso.
        *   **Aumento Equilibrado:** Un aumento equilibrado de productores y consumidores puede mejorar el rendimiento general hasta cierto punto, siempre que haya suficientes recursos de CPU y la contención en la cola no sea excesiva.

2.  **`ITEMS_TO_PROCESS` (Número Total de Ítems a Procesar)**
    *   **Descripción:** Determina la carga de trabajo total y, por ende, la duración del experimento.
    *   **Impacto (Tarea 15 / EXP 4):** Aumentar el número de ítems a procesar generalmente aumenta el tiempo total de ejecución, ya que hay más trabajo que realizar. La relación entre el aumento de ítems y el tiempo puede ser lineal o no lineal, dependiendo de cómo interactúen los demás parámetros (e.g., si la contención o los tiempos de espera dominan).

3.  **`QUEUE_SIZE` (Tamaño de la Cola Compartida)**
    *   **Descripción:** Define la capacidad del búfer compartido entre productores y consumidores.
    *   **Impacto (Tarea 14 / EXP 3):**
        *   **Cola Pequeña:** Aumenta la contención. Los productores se bloquearán más a menudo si la cola se llena, y los consumidores si se vacía. Esto puede llevar a un peor rendimiento debido a los constantes bloqueos y desbloqueos.
        *   **Cola Grande:** Reduce la contención y el tiempo de espera, permitiendo que productores y consumidores operen de forma más independiente durante más tiempo. Sin embargo, un tamaño excesivamente grande puede consumir más memoria sin proporcionar mejoras de rendimiento adicionales más allá de cierto punto. Una cola de tamaño 0 puede ser un caso especial que simula un "pipeline" muy estricto o puede significar una cola "infinita" en algunos contextos (aunque en `multiprocessing.Queue` un tamaño 0 significa tamaño "infinito" si no se especifica explícitamente).

4.  **`MIN_SLEEP_PRODUCER`, `MAX_SLEEP_PRODUCER`, `MIN_SLEEP_CONSUMER`, `MAX_SLEEP_CONSUMER` (Tiempos de Espera)**
    *   **Descripción:** Estos parámetros introducen latencia artificial en las operaciones de producción y consumo, simulando el tiempo que un hilo "trabaja" o "espera" en una aplicación real.
    *   **Impacto (Tarea 13 / EXP 2):**
        *   **Tiempos de Espera Largos:** Aumentan el tiempo total de ejecución y magnifican el impacto de la sincronización. Pequeñas diferencias en los tiempos de espera entre productores y consumidores pueden crear cuellos de botella y desequilibrios.
        *   **Tiempos de Espera Cortos:** Los hilos operan más rápido, lo que puede aumentar la contención si la `QUEUE_SIZE` es pequeña, pero también puede llevar a un uso más eficiente de los recursos si los demás parámetros están bien ajustados.

### Consideraciones Adicionales

*   **`OUTPUT`:** Una variable booleana que controla la verbosidad de la salida de los hilos. Desactivarla (`OUTPUT = False`) es útil para experimentos a gran escala para evitar la sobrecarga de I/O, tal como se hace en el `codigo5-MultProdCons.py` para los experimentos de las Tareas 12-15.
*   **Variables Globales:** La "Experimentación" del enunciado (página 19) subraya el papel crítico de las variables globales para configurar los experimentos. Es esencial entender qué variables globales (`QUEUE_SIZE`, `ITEMS_TO_PROCESS`, etc.) se están modificando para cada experimento y cómo afectan el resultado.

Analizando las interacciones entre estos parámetros, se pueden identificar cuellos de botella, optimizar el rendimiento y comprender mejor el comportamiento de los sistemas concurrentes bajo diferentes cargas y configuraciones.
