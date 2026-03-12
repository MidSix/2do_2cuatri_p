
# 009 - Comportamiento del Comando `stress` y la Gestión de Procesos Hijos

Cuando se utiliza el comando `stress` (o `stress-ng`) con la opción `-c N` (o `--cpu N`) para generar carga de CPU en un sistema, es importante entender cómo se estructura y gestiona el proceso.

No se lanzan `N` procesos de `stress` completamente independientes, sino que opera de la siguiente manera:

1.  **Proceso Padre de `stress`:** Se inicia un único proceso principal de `stress`. Este es el proceso "padre" y su PID es el que verás inicialmente asociado al comando `stress`. Por ejemplo, en el caso `stress: info: [172] dispatching hogs: 4 cpu, ...`, el PID 172 es el del proceso padre.

2.  **Procesos Hijos (Workers):** El proceso padre de `stress` es el encargado de **crear y gestionar `N` procesos hijos** (a menudo llamados "workers" o "hogs") que son los que realmente realizan el trabajo de estresar la CPU. Estos hijos son los que ejecutarán los bucles intensivos para consumir ciclos de procesador. Cada uno tendrá su propio PID, distinto del padre.

### ¿Por qué al matar uno se cierran todos?

Si terminas uno de los procesos hijos (o incluso el propio proceso padre), es muy probable que toda la operación de `stress` se detenga, y el resto de los procesos hijos sean cerrados. Esto ocurre por las siguientes razones:

*   **Gestión del Proceso Padre:** El proceso padre de `stress` actúa como un **coordinador**. Está diseñado para monitorear a sus hijos y asegurar que la tarea de estrés se complete según lo previsto.
*   **Detección de Fallo/Terminación:** Cuando uno de los procesos hijos es terminado (por ejemplo, al enviarle una señal `SIGTERM` o `SIGKILL`), el proceso padre detecta esta terminación inesperada.
*   **Limpieza Coordinada:** Al detectar que la tarea de estrés ya no puede continuar de forma completa (porque le falta uno de sus "hijos"), el proceso padre suele iniciar un proceso de **limpieza coordinada**. Esto implica enviar señales de terminación a los procesos hijos restantes y luego finalizar él mismo.

**Ejemplo de la salida observada:**

```
ubuntu@ContenedorParalelismo:~$ stress -c 4
stress: info: [172] dispatching hogs: 4 cpu, 0 io, 0 vm, 0 hdd
stress: FAIL: [172] (425) <-- worker 174 got signal 15
stress: WARN: [172] (427) now reaping child worker processes
stress: FAIL: [172] (461) failed run completed in 30s
ubuntu@ContenedorParalelismo:~$"
```

En este caso:
*   `[172]` es el PID del proceso padre de `stress`.
*   `worker 174` es el PID de uno de los procesos hijos que recibió `SIGTERM` (Signal 15).
*   Tras la terminación del `worker 174`, el proceso padre `[172]` emite una advertencia (`WARN`) y procede a "recolectar" (`reaping`) a sus demás procesos hijos, lo que resulta en la terminación de toda la operación de `stress`.

Esta comportamiento es parte del diseño de `stress` para asegurar que las operaciones de estrés sean gestionadas como una unidad.

---
[[006_atop_monitorizacion_y_entornos_virtualizados]]
[[007_interpretacion_avanzada_atop]]
[[008_estados_procesos_[]()linux]]
