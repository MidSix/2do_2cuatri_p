# 001_diferencias_hilos_procesos_p2.md

> [!PDF|yellow] [[EnunciadoP2.pdf#page=3&selection=13,0,13,33&color=yellow|EnunciadoP2, p.3]]
> > Diferencia entre Hilos y Procesos
> 
> 


**Página de referencia en `EnunciadoP2.pdf`:** 3 (Sección 1: "Diferencia entre Hilos y Procesos" y "Tarea 1 - Compartición de variables en procesos e hilo")

## Procesos vs. Hilos: Manejo de Variables y Memoria

En la computación concurrente, la elección entre usar **procesos** o **hilos (de software)** tiene implicaciones significativas en cómo se gestionan y comparten los datos.

### Procesos

*   **Aislamiento de Memoria:** Cada proceso posee su propio espacio de direcciones de memoria virtual, completamente aislado de otros procesos. Esto proporciona robustez y seguridad, ya que un error en un proceso no afecta directamente la memoria de otro.
*   **Copias de Variables:** Cuando un proceso padre crea un proceso hijo (mediante `fork()` o similar), el hijo recibe una *copia* del espacio de memoria del padre. Esto significa que las variables del padre son duplicadas para el hijo; cualquier modificación que el hijo haga a sus variables no afectará las del padre, y viceversa.
*   **Compartición Explícita:** Para que los procesos compartan información, deben usar mecanismos de comunicación explícitos como memoria compartida, pipes, sockets o colas de mensajes. La "memoria compartida" es una región de memoria especial que el sistema operativo permite que múltiples procesos accedan.

### Hilos (de Software)

*   **Memoria Compartida por Defecto:** Todos los hilos dentro del mismo proceso comparten el mismo espacio de direcciones de memoria virtual. Esto significa que las variables globales y los objetos en el heap son accesibles y modificables por *todos* los hilos del proceso.
*   **Referencias Directas:** Un cambio realizado por un hilo en una variable compartida es inmediatamente visible para los demás hilos del mismo proceso. Esto facilita la comunicación, pero introduce desafíos en la coherencia de los datos.
*   **Problemas de Coherencia:** La facilidad de compartir memoria implica que, si múltiples hilos acceden y modifican la misma variable sin coordinación, pueden surgir **condiciones de carrera** (race conditions) y otros problemas de coherencia, llevando a resultados impredecibles e incorrectos.

> [!PDF|yellow] [[EnunciadoP2.pdf#page=3&selection=16,84,17,26&color=yellow|EnunciadoP2, p.3]]
> > los hilos son entidades que viven dentro de un proceso
> 

* ---> Los hilos de software son entidades que **viven** dentro de procesos. Por tanto, los procesos son el superconjunto de los hilos. Un hilo no puede vivir de forma independiente a un proceso.

### Conclusión (Tarea 1 en `codigo0-ProcesosVsHilos.py`)

El `codigo0-ProcesosVsHilos.py` ilustra estas diferencias:

*   **Escenario 1 (Procesos sin memoria compartida):** Los procesos hijos no ven los cambios de los demás en una variable, ya que cada uno trabaja sobre su propia copia.
*   **Escenario 2 (Hilos):** Todos los hilos ven y modifican la misma variable, lo que puede llevar a resultados inconsistentes si no hay sincronización adecuada.
*   **Escenario 3 (Procesos con memoria compartida explícita):** Los procesos hijos pueden compartir la misma variable si se configura explícitamente una región de memoria compartida.

Esta práctica enfatiza que la gestión de variables compartidas es una consideración crítica al diseñar programas concurrentes con hilos.
- Ejemplo de ejecución de la tarea 1 para el código 0.
-> **Entity:** No es mas que el PID(Process ID) del proceso. Recalco que del proceso.
	fíjate que los hilos al vivir dentro de un proceso cuando se busca el PID de ellos te devolverá el PID del proceso que los alberga.
-> Cada "-------------" Significa que los 2 procesos o hilos ya modificaron la variable global. Y este
	proceso se lleva a cabo tantas veces como entidades(procesos o hilos) haya. En el código del profesor hay 2 entidades, por eso se llevan a cabo 2 iteraciones donde en cada una, las 2 entidades de forma secuencial modifican la variable global.

![[Pasted image 20260225111531.png]]

