# 012_hilos_software_hardware_y_context_switching.md

## Proceso vs. Hilo (de Software)

Es fundamental distinguir entre un **proceso** y un **hilo (de software)**:

*   Un **proceso** es una instancia de un programa en ejecución. Cada proceso tiene su propio espacio de direcciones de memoria virtual, recursos del sistema (archivos abiertos, sockets, etc.) y al menos un hilo de ejecución. Los procesos son entidades relativamente pesadas y la comunicación entre ellos requiere mecanismos específicos (IPC - Inter-Process Communication). Un proceso puede crear otros procesos (procesos hijos) mediante operaciones como `fork()` o `exec()`.

*   Un **hilo de software** (o "thread", " lightweight process" - LWP) es la unidad más pequeña de ejecución que puede ser programada por el sistema operativo. Un hilo reside *dentro* de un proceso, y todos los hilos de un mismo proceso comparten su espacio de direcciones de memoria, recursos y código. Los hilos son más ligeros que los procesos y el cambio entre hilos dentro del mismo proceso es más rápido que el cambio entre procesos diferentes.

Por lo tanto, es crucial entender que:
*   Cuando un proceso *crea* otro **proceso** (un "proceso hijo"), está generando una entidad de ejecución *independiente y separada*. Este nuevo proceso hijo tendrá su *propio* espacio de memoria virtual y recursos, y contendrá al menos un hilo de software (su hilo principal) para ejecutar su código. Los procesos hijos son entidades "pesadas" y distintas del padre.
*   Cuando un proceso *crea* un **hilo** (de software), está generando una unidad de ejecución *dentro de sí mismo*. Este nuevo hilo compartirá el espacio de memoria y los recursos del proceso padre. Los hilos son "ligeros" y están inherentemente ligados a su proceso padre.

En resumen, no es correcto decir que a los hijos de un proceso se les llama hilos. A los hijos de un proceso se les llama **procesos hijos**, y cada uno de ellos tendrá sus propios hilos de software.

## Hilos de Software vs. Hilos de Hardware

La distinción entre hilos de software y hilos de hardware es crucial para entender cómo los procesadores modernos manejan la ejecución:

1.  **Hilos de Software (Software Threads):**
    *   Son las unidades de ejecución que crea y gestiona el **sistema operativo** (SO).
    *   Son lo que los programadores usualmente entienden por "hilo" (ej., hilos Pthreads, hilos de Java, hilos de .NET).
    *   Un hilo de software contiene el estado de ejecución de un programa: el contador de programa (Program Counter - PC), los registros de la CPU, la pila de ejecución, y otros datos específicos del hilo.
    *   El SO es responsable de mapear estos hilos de software a los hilos de hardware disponibles para su ejecución.

2.  **Hilos de Hardware (Hardware Threads / Hilos Físicos / Hilos de CPU):**
    *   Son componentes físicos o lógicos dentro del **hardware del procesador** (CPU) que permiten mantener un estado de ejecución independiente.
    *   Cada hilo de hardware tiene su propio conjunto de registros de CPU, contador de programa (PC), y en algunos casos, su propia caché L1 o partes de ella.
    *   La tecnología más conocida que implementa múltiples hilos de hardware por núcleo es **Simultaneous Multi-threading (SMT)**, comercialmente conocida como **Intel Hyper-Threading**.

## Intel i3-12100f: 4 Núcleos / 8 Hilos (de Hardware)

Para el ejemplo del i3-12100f (4 núcleos, 8 hilos), significa que el procesador tiene 4 **núcleos físicos**. Gracias a la tecnología Hyper-Threading, cada uno de esos 4 núcleos físicos puede manejar **2 hilos de hardware**.

Esto **no significa** que cada núcleo puede ejecutar 2 *procesos* completos simultáneamente en el sentido estricto, ni que ejecuta 2 hilos de software *a la vez* en el mismo instante. Significa que cada núcleo físico puede presentar al sistema operativo como si tuviera dos unidades de ejecución lógicas (dos hilos de hardware).

Un núcleo con SMT (Hyper-Threading) funciona alternando muy rápidamente entre las instrucciones de dos hilos de software diferentes. Cuando un hilo de software se detiene temporalmente (por ejemplo, esperando datos de memoria o una operación de I/O), el núcleo puede cambiar instantáneamente la ejecución al otro hilo de software asociado a su segundo hilo de hardware, en lugar de quedarse inactivo. Esto mejora la *utilización* del núcleo y, por ende, el rendimiento general para cargas de trabajo concurrentes, aunque no duplica la capacidad de cómputo real.

## Context Switching (SO) vs. Hardware Thread Switching

La explicación de su profesor sobre "hilos del CPU como punteros que no guardan el estado" se refiere probablemente a la eficiencia del hardware al cambiar entre los dos hilos de hardware *dentro del mismo núcleo físico*, lo cual es diferente al **context switching** gestionado por el sistema operativo.

*   **Context Switching (a nivel de SO):** Es un proceso costoso. Cuando el SO decide cambiar la ejecución de un hilo de software a otro (ya sea en el mismo núcleo o en otro):
    1.  Guarda todo el estado del hilo de software actual (registros de CPU, contador de programa, estado del FPU, etc.) en la memoria.
    2.  Carga el estado del nuevo hilo de software desde la memoria a los registros de la CPU.
    Este proceso lleva tiempo (cientos o miles de ciclos de reloj) porque implica accesos a memoria y manipulación de datos en el kernel del SO. Es una operación del software.

*   **Hardware Thread Switching (por SMT/Hyper-Threading):** Un hilo de hardware (logical processor) *sí* mantiene su propio estado arquitectónico (registros, PC). El cambio entre los dos hilos de hardware que comparte un núcleo físico es muchísimo más rápido que un context switching de SO. No hay una "guardado completo en memoria" en el mismo sentido que el SO, ya que el hardware está diseñado para tener múltiples bancos de registros o duplicar las partes críticas del estado para cada hilo de hardware. El núcleo puede decidir en cada ciclo de reloj de qué hilo de hardware tomar la siguiente instrucción, sin la intervención del SO. Esto permite que el núcleo "esconda" la latencia de un hilo ejecutando instrucciones del otro. No es un *context switching* en el sentido tradicional de la palabra, porque el hardware tiene la capacidad de cambiar de hilo sin necesidad de una costosa operación de salvado/restauración de un bloque grande de memoria.

En resumen, los hilos de hardware son la capacidad del procesador para mantener y alternar rápidamente entre múltiples estados de ejecución, lo que el SO puede aprovechar para ejecutar más hilos de software de forma concurrente en un solo núcleo físico, mejorando la eficiencia sin incurrir en el costo total de un context switching de SO tradicional.
