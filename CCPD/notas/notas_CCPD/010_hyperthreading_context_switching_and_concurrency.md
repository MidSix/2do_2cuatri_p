# 010 - Hyper-threading (SMT), Context Switching y la Ejecución de Procesos

Esta nota profundiza en la relación entre el hardware de la CPU (especialmente Hyper-threading o SMT), la concurrencia, el paralelismo y los diferentes tipos de cambios de contexto, basándose en la comprensión de los estados de los procesos.

## 1. Concurrencia vs. Paralelismo (Revisado)

*   **Concurrencia:** Múltiples tareas haciendo progreso durante el mismo período de tiempo, a menudo intercalando su ejecución en una única unidad de procesamiento. Es la ilusión de simultaneidad.
*   **Paralelismo:** Múltiples tareas ejecutándose verdaderamente de forma simultánea en múltiples unidades de procesamiento dedicadas. Es la simultaneidad real.

## 2. Hyper-threading (SMT) y los "Hilos Lógicos"

Hyper-threading (Intel) o Simultaneous Multi-threading (SMT en AMD y otros) es una tecnología que permite que un **único núcleo físico de CPU** se presente al sistema operativo como **dos (o más) "hilos lógicos" o "hardware threads"**.

*   **¿Cómo funciona?** Un núcleo físico con Hyper-threading duplica ciertas partes de su arquitectura que almacenan el estado de un programa, como los **registros de la CPU** y el **contador de programa (Program Counter)**. Sin embargo, ambos hilos lógicos **comparten las unidades de ejecución físicas** (ALUs, FPUs, etc.) y las **cachés** (L1, L2, L3) del núcleo.

*   **Propósito:** El objetivo es mejorar la utilización del núcleo físico. Si un hilo lógico se detiene (ej. esperando datos de la memoria tras un fallo de caché), el núcleo puede inmediatamente ejecutar instrucciones del otro hilo lógico que comparte ese mismo núcleo, manteniendo sus unidades de ejecución ocupadas.

## 3. Tipos de "Context Switching" y su Coste

La distinción clave está en el coste y el mecanismo del cambio de contexto:

### a) Cambio de Contexto de Software (Tradicional / entre Procesos/Hilos de Software)

*   **Mecanismo:** Gestionado por el **sistema operativo**. Cuando el SO decide cambiar de un proceso/hilo a otro, debe:
    1.  Guardar el estado completo del proceso/hilo actual (todos sus registros de CPU, puntero de pila, puntero de instrucción, estado de la unidad de coma flotante, etc.) en la memoria RAM.
    2.  Cargar el estado completo del siguiente proceso/hilo a ejecutar desde la RAM.
*   **Coste:** Es una operación **costosa y lenta** porque implica accesos a la memoria principal (RAM), que es mucho más lenta que los registros de la CPU. Además, al cargar un nuevo contexto, a menudo se invalidan las cachés existentes, lo que puede llevar a fallos de caché (`cache misses`) iniciales.
*   **Ocurre:** Cuando el sistema alterna entre procesos o hilos de software que comparten un **mismo núcleo físico** (en ejecución concurrente), o entre procesos/hilos asignados a diferentes núcleos.

### b) Cambio de Contexto a Nivel de Hardware (Hyper-threading / entre Hilos Lógicos)

*   **Mecanismo:** Gestionado directamente por el **hardware de la CPU**. Como el núcleo duplica los registros y el contador de programa para cada hilo lógico, los estados de ambos hilos ya están presentes en el propio núcleo. El cambio entre ellos es una operación interna del hardware.
*   **Coste:** Es **inmensamente más rápido y menos costoso** que un cambio de contexto de software. No implica accesos a la RAM para guardar/cargar estados de los registros principales. El núcleo simplemente "alterna" entre los conjuntos de registros duplicados de los hilos lógicos.
*   **Beneficio de la Caché:** Al compartir las cachés L1/L2/L3, un cambio entre hilos lógicos en el mismo núcleo **no invalida la caché**. Ambos hilos pueden beneficiarse de los datos ya presentes en la caché, reduciendo los `cache misses`.
*   **Ocurre:** Dentro de un **único núcleo físico con Hyper-threading** cuando alterna la ejecución entre sus hilos lógicos. No se busca un paralelismo puro entre ellos, sino una **concurrencia muy eficiente** que maximice la utilización de las unidades de ejecución compartidas.

## 4. Reafirmando el Comportamiento de `stress -c N`

Volviendo a tu situación con 8 núcleos lógicos (4 físicos con HT):

*   **`stress -c N` con `N <= 4 (núcleos físicos)`:** Cada proceso de `stress` puede ser asignado a un núcleo físico diferente, probablemente utilizando un solo hilo lógico por core, logrando **paralelismo real** entre ellos. El `user` time aumenta eficientemente en relación con el `real` time.
*   **`stress -c N` con `4 < N <= 8 (núcleos lógicos)`:** Aquí es donde tu punto es crucial. Si lanzas, por ejemplo, `stress -c 5`:
    *   Cuatro de esos procesos se ejecutarán en paralelo en cuatro núcleos físicos distintos (un hilo lógico por núcleo).
    *   El quinto proceso de `stress` será asignado a uno de los núcleos físicos ya ocupados. Dentro de ese núcleo físico, los dos hilos lógicos (el proceso de `stress` original y el quinto) ejecutarán sus instrucciones de forma **concurrente** mediante el cambio de contexto a nivel de hardware.
    *   Aunque esta concurrencia es eficiente gracias a Hyper-threading, **no es paralelismo puro** para esas dos tareas que comparten el mismo núcleo físico. Introducirá una pequeña penalización en la ejecución `real` de esas tareas en ese core específico, en comparación con tener un core físico completamente dedicado.
*   **`stress -c N` con `N > 8 (núcleos lógicos)`:** Como discutimos previamente, el sistema se ve forzado a realizar una gran cantidad de **cambios de contexto de software** entre todos los procesos de `stress` para turnarse en los 8 hilos lógicos disponibles. La sobrecarga del sistema operativo se vuelve dominante, ralentizando el `real` time y haciendo que el `sys` time aumente.

Tu comprensión de que `N <= núcleos lógicos` no garantiza que *todas* las tareas se ejecuten en paralelismo puro (debido a la naturaleza concurrente de los hilos lógicos dentro de un mismo núcleo físico con HT) es absolutamente correcta. El "patrón" que se rompe con `N > núcleos lógicos` se refiere al punto en que la sobrecarga de la gestión de la concurrencia por software supera con creces los beneficios del paralelismo o la concurrencia por hardware.

---
[[006_atop_monitorizacion_y_entornos_virtualizados]]
[[007_interpretacion_avanzada_atop]]
[[008_estados_procesos_linux]]
[[009_comportamiento_stress_command]]
