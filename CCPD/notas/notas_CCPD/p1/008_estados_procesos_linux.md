# 008 - Estados de los Procesos en Linux

Los procesos en sistemas operativos tipo Unix (como Linux) pueden estar en varios estados. Estos estados te dan una idea de qué está haciendo el proceso y por qué no está usando la CPU o está atascado. Los verás en la columna `ST` de herramientas como `atop` o `ps`.

Aquí están los estados más comunes:

1.  **`R` (Running / Runnable - En ejecución / Ejecutable):**
    *   El proceso está actualmente ejecutándose en un núcleo de la CPU o está listo para ejecutarse y está esperando en la cola del planificador de tareas para que se le asigne un tiempo de CPU.
    *   Significa que está activo y haciendo trabajo (o listo para hacerlo).

2.  **`S` (Interruptible Sleep - Suspendido Interrumpible):**
    *   El proceso está "durmiendo", es decir, esperando que ocurra algún evento (por ejemplo, que termine una operación de E/S, que se libere un recurso, que haya datos disponibles en una conexión de red, o un temporizador).
    *   Puede ser despertado por una señal. Este es el estado más común para procesos inactivos o esperando.

3.  **`D` (Uninterruptible Sleep - Suspendido Ininterrumpible):**
    *   El proceso está "durmiendo" y **no puede ser interrumpido por señales**.
    *   Este estado suele indicar que el proceso está esperando una operación de E/S de bajo nivel (por ejemplo, en un disco o red) y no puede ser interrumpido hasta que esa operación se complete.
    *   Un proceso en estado `D` es muy difícil de matar y a menudo puede ser un síntoma de problemas de hardware o drivers.

4.  **`Z` (Zombie):**
    *   El proceso ha terminado su ejecución, pero su proceso padre aún no ha leído su estado de salida.
    *   No consume recursos de CPU ni memoria (más allá de la entrada en la tabla de procesos) y **no puede ser matado**.

5.  **`T` (Stopped - Detenido):**
    *   El proceso ha sido detenido. Esto puede ocurrir porque ha recibido una señal `SIGSTOP` o `SIGTSTP` (como cuando pulsas `Ctrl+Z` en la terminal) o porque está siendo depurado por un debugger.
    *   Un proceso en este estado no consume CPU y puede ser reanudado con una señal `SIGCONT`.

6.  **`X` (Dead - Muerto):**
    *   Este estado es muy breve y normalmente no lo verás. Indica que el proceso está a punto de ser completamente eliminado de la memoria.

Además de estos, a veces puedes ver modificadores o letras adicionales que proporcionan más información, como:

*   `<`: Proceso de alta prioridad.
*   `N`: Proceso de baja prioridad (valor `nice` alto).
*   `L`: Páginas de memoria bloqueadas en RAM (por ejemplo, para aplicaciones en tiempo real).
*   `s`: El proceso es un líder de sesión.
*   `+`: El proceso está en el grupo de procesos en primer plano.

Los más importantes para la monitorización de rendimiento y resolución de problemas son `R`, `S`, `D` y `Z`.

---
[[006_atop_monitorizacion_y_entornos_virtualizados]]
[[007_interpretacion_avanzada_atop]]
