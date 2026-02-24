# 006 - atop: Monitorización Avanzada y Comportamiento en Entornos Virtualizados (WSL/Docker)

Este documento detalla el uso de la herramienta `atop` para la monitorización de sistemas, explica sus métricas más importantes y aclara su comportamiento cuando se ejecuta en entornos virtualizados como WSL o contenedores Docker, especialmente bajo carga del sistema host.

## 1. Mini-Tutorial: `atop` y Métricas Clave

`atop` es una herramienta avanzada de monitorización de rendimiento en Linux. A diferencia de `top` o `htop`, `atop` muestra una visión más holística y detallada del uso de recursos, incluyendo CPU, memoria, disco y red, con la capacidad de ver el histórico y el consumo por proceso o hilo.

Para ejecutarlo, simplemente escribe `atop` en tu terminal:

```bash
atop
```

Verás una pantalla que se actualiza cada pocos segundos (por defecto 10s) con varias secciones:

### Secciones y Métricas más Importantes:

*   **Línea de Cabecera (arriba):**
    *   **`PRC` (Process Count):** Número total de procesos, ejecutándose, durmiendo, con estado zombie, etc.
    *   **`CPU`:** Uso global de la CPU.
        *   `sys`: Tiempo que la CPU pasa ejecutando tareas del kernel.
        *   `user`: Tiempo que la CPU pasa ejecutando código de usuario (aplicaciones).
        *   `irq`: Tiempo en manejar interrupciones.
        *   `idle`: Tiempo que la CPU está inactiva.
        *   `wait`: Tiempo que la CPU está esperando operaciones de I/O.
    *   **`CPL` (CPU Load):** Carga media del sistema (runqueue) en 1, 5 y 15 minutos.
    *   **`MEM` (Memory):** Uso global de la memoria.
        *   `free`: Memoria libre no usada por nada.
        *   `cache`: Memoria usada para caché de páginas de archivos.
        *   `buff`: Memoria usada para buffers (I/O de disco).
        *   `slab`: Memoria usada por el kernel para estructuras de datos internas.
        *   `swpc`: Cantidad de memoria en swap que está siendo cacheados.

*   **Sección de Discos (DSK):**
    *   **`DSK`:** Estadísticas por cada disco/partición.
    *   `busy`: Porcentaje de tiempo que el disco está ocupado.
    *   `read`/`write`: Cantidad de datos leídos/escritos por segundo.

*   **Sección de Red (NET):**
    *   **`NET`:** Estadísticas por interfaz de red.
    *   `rxpps`/`txpps`: Paquetes recibidos/transmitidos por segundo.
    *   `rxbyt`/`txbyt`: Bytes recibidos/transmitidos por segundo.

*   **Sección de Procesos (abajo):**
    *   Muestra una lista de procesos ordenada por uso de CPU (por defecto).
    *   `PID`: ID del proceso.
    *   `CMD`: Nombre del comando/proceso.
    *   `CPU`: Porcentaje de uso de CPU del proceso.
    *   `MEM`: Porcentaje de uso de memoria del proceso.

### Opciones y Teclas de `atop` (para navegación interactiva):

*   **`g`:** Muestra todas las secciones (CPU, MEM, DSK, NET, PRC).
*   **`m`:** Ordena los procesos por uso de memoria.
*   **`c`:** Ordena los procesos por uso de CPU.
*   **`d`:** Ordena los procesos por actividad de disco.
*   **`q`:** Sale de `atop`.
*   **`i <intervalo>`:** Cambia el intervalo de actualización (ej. `i 2` para cada 2 segundos).
-   `f:` Muestra todas las métricas del atop 

## 2. `atop` en Contenedores/WSL y la Carga del Host

Es crucial entender que `atop` siempre reportará las métricas del sistema operativo donde se ejecuta. Esto tiene implicaciones importantes en entornos virtualizados:

*   **`atop` corre sobre su propio SO:**
    *   Si lo ejecutas en un contenedor Docker, verá los recursos asignados a ese contenedor.
    *   Si lo ejecutas en WSL, verá los recursos asignados a la VM de WSL.
    *   Nunca verá directamente lo que está pasando en el host de Windows.

*   **Impacto Indirecto de la Carga del Host (Ej. Jugando en Windows):**
    Si tu sistema host (Windows) está bajo una carga intensa (ej. jugando a un juego exigente como Stellar Blade), el impacto en el rendimiento de tu entorno WSL/Docker será indirecto pero significativo:
    *   **Consumo de CPU:** El planificador de Windows priorizará el juego. Los procesos dentro del contenedor/WSL seguirán mostrando un porcentaje de uso de CPU basado en su *parte asignada* de los recursos. Sin embargo, ese porcentaje representará una porción más pequeña de los recursos físicos de la CPU, ya que el host está priorizando otras tareas. Esto resultará en que las tareas dentro del contenedor/WSL se ejecutarán más lentamente.
    *   **Consumo de Memoria:** Si el juego en Windows consume una gran cantidad de RAM física, Windows podría reducir dinámicamente la memoria asignada a la VM de WSL 2. En este caso, `atop` en WSL o el contenedor podría mostrar una disminución en `MemAvailable` o incluso en `MemTotal` (para WSL), o un aumento en la actividad de `swap` dentro del ambiente virtualizado.

*   **Visibilidad de la Carga:**
    *   No verás directamente el consumo de recursos del juego de Windows en el `atop` del contenedor/WSL.
    *   La degradación del rendimiento en el entorno virtualizado se manifestará en `atop` como tiempos de ejecución más largos para las tareas internas, posibles aumentos en `sys` o `wait` de la CPU, o cambios en la disponibilidad de memoria.

Esta abstracción de recursos es fundamental para que el sistema host mantenga la estabilidad y la capacidad de respuesta, gestionando los recursos de forma dinámica entre sus propios procesos y los entornos virtualizados que aloja.

## 3. Distinción Conceptual: Memoria Libre, Memoria Disponible y Swap

Es fundamental comprender la diferencia entre estos conceptos, especialmente al interpretar las métricas de herramientas como `atop` o `cat /proc/meminfo`:

*   **`MemFree` (Memoria Libre):**
    *   Representa la cantidad de memoria RAM que está **completamente vacía y no está siendo utilizada para nada** por el sistema operativo o las aplicaciones. Es memoria ociosa, lista para ser usada de inmediato.

*   **`MemAvailable` (Memoria Disponible):**
    *   Es la cantidad de memoria RAM que puede ser utilizada por nuevas aplicaciones o procesos **sin necesidad de que el sistema recurra a la memoria de intercambio (swap)**.
    *   Incluye la `MemFree` **más** una parte de la memoria que el sistema utiliza para **cachés de disco (ej. `Cached`, `Buffers`, `SReclaimable`)**, pero que es fácilmente liberable. El sistema operativo puede descartar esta caché (ya que los datos originales están en disco) al instante si una aplicación necesita esa RAM, sin tener que escribir nada a disco.
    *   **Es la métrica más precisa** para evaluar cuánta memoria RAM tienes realmente disponible para iniciar nuevas aplicaciones o para que las existentes se expandan.

*   **Swap (Memoria de Intercambio o Memoria Virtual):**
    *   La memoria swap es un espacio en el disco duro (partición o archivo) que el sistema operativo utiliza como una **extensión de la RAM física** cuando esta se agota.
    *   Cuando el sistema necesita más RAM de la que está `MemAvailable` (es decir, ya ha agotado `MemFree` y ha reclamado todas las cachés liberables), empieza a mover páginas de memoria **menos utilizadas o menos críticas** de la RAM física al espacio de swap en el disco.
    *   Este proceso libera RAM física para procesos más activos, pero introduce una **penalización de rendimiento muy severa**, ya que el acceso al disco es muchísimas veces más lento que el acceso a la RAM.
    *   El swap **no es un mecanismo para "prestar memoria para mejorar el rendimiento"**, sino una medida de emergencia para evitar que el sistema se bloquee por falta de memoria física, a costa de una degradación del rendimiento.

Comprender esta distinción es clave para diagnosticar correctamente los problemas de rendimiento relacionados con la memoria en un sistema Linux.

---
[[008_estados_procesos_linux]]