# 007 - Interpretación Avanzada de atop: Hilos, Frecuencia y Estados de Procesos

## ¿Qué es atop?

`atop` es una herramienta de monitorización de rendimiento de sistema en Linux que ofrece una visión detallada y en tiempo real del estado de los recursos (CPU, memoria, disco, red) y de los procesos activos. Es especialmente útil para analizar el comportamiento del sistema y detectar cuellos de botella.

## Interpretación de la CPU en atop

### Líneas `CPU` (mayúsculas) vs. `cpu` (minúsculas)

*   **`CPU` (mayúsculas):** Muestra el uso agregado de todos los núcleos/hilos lógicos de la CPU del sistema en su conjunto. Proporciona un resumen global de cómo se está utilizando la capacidad total de procesamiento.
*   **`cpu` (minúsculas, ej. `cpu0`, `cpu1`):** Estas líneas representan los hilos lógicos individuales de tu procesador (también conocidos como núcleos lógicos o "logical cores"). Si tu CPU tiene tecnologías como Hyper-threading, verás más líneas `cpu` de las que tienes núcleos físicos. El sistema operativo utiliza estos hilos de hardware para ejecutar las tareas.

### Visualización de la Frecuencia de la CPU

Para ver la frecuencia de ejecución actual de cada hilo lógico de la CPU:

1.  Abre `atop` en tu terminal.
2.  **Pulsa la tecla `f`** (minúscula) mientras `atop` se está ejecutando.

Esto hará que las líneas `cpu` individuales cambien para mostrar la frecuencia actual de cada núcleo lógico, generalmente expresada en **MHz**. Pulsar `f` repetidamente ciclará por diferentes vistas (uso en %, ciclos de reloj, frecuencia).

*Nota:* Si ves `---` o no aparece la frecuencia, podría ser que el sistema o la versión de `atop` no estén exponiendo esa información específica.

## Interpretación de la Memoria en atop

En `atop`, hay varias métricas relacionadas con la memoria que son cruciales para entender el uso de recursos de los procesos:

*   **`VGROW`**: Muestra el crecimiento de la memoria virtual del proceso (Virtual Memory Grow). Indica cuánto ha aumentado el tamaño de la memoria virtual asignada a un proceso.
*   **`RGROW`**: Muestra el crecimiento de la memoria residente (RAM) del proceso (Resident Memory Grow). Refleja cuánto ha aumentado la cantidad de memoria física (RAM) utilizada por un proceso.

## Hilos (Threads) en atop

Es fundamental diferenciar entre los "hilos de hardware" (los `cpu` lógicos) y los "hilos de software" (los hilos de ejecución creados por los procesos).

### `NTHR` (Number of Threads) en la lista de procesos

En la sección inferior de `atop`, donde se listan los procesos, la columna `NTHR` te indica el **número de hilos de software** que está utilizando cada proceso específico.

*   Un proceso sencillo puede tener `NTHR` igual a `1`.
*   Aplicaciones más complejas (navegadores web, servidores de bases de datos) pueden tener decenas o cientos de hilos (`NTHR` >> 1).

### Línea `PRC` (Process and Kernel activity summary)

La línea `PRC` ofrece un resumen de la actividad del planificador de tareas del sistema, mostrando estadísticas globales sobre los hilos de los procesos:

*   **`#trun` (threads running):** Es la abreviatura de **"threads running"**. Indica el número de hilos de software que están actualmente en ejecución en una CPU o que están listos para ser ejecutados inmediatamente. Estos hilos están consumiendo activamente recursos de CPU o esperando ser programados en el siguiente ciclo de reloj.
*   **`#tslpi` (threads in sleep, interruptible):** Es la abreviatura de **"threads in sleep, interruptible"**. Representa el número de hilos de software que están en estado de espera o "dormidos", pero que pueden ser "despertados" por una señal o un evento. Ejemplos comunes incluyen hilos esperando operaciones de I/O (lectura de disco, respuesta de red) o entrada de usuario. Estos hilos no están consumiendo CPU mientras están en este estado.

### Hilos de CPU vs. Hilos de Proceso

*   **Hilos de CPU (hardware):** Son los núcleos lógicos del procesador que el sistema operativo puede utilizar para ejecutar instrucciones. Los recursos de cómputo físicos.
*   **Hilos de Proceso (software):** Son unidades de ejecución dentro de un proceso. El planificador del sistema operativo asigna estos hilos de software a los hilos de CPU disponibles para su ejecución. No se asignan "cores" directamente a tareas, sino los hilos de software a los hilos de CPU.
---
[[008_estados_procesos_linux]]
