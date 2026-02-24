# 011_computacion_concurrente_paralela_distribuida.md

## Computación Concurrente

La **computación concurrente** se refiere a la ejecución de múltiples cálculos que se solapan en el tiempo. Aunque los cálculos no se ejecutan exactamente al mismo instante, su progreso se entrelaza de tal manera que parecen ocurrir simultáneamente desde la perspectiva lógica. El objetivo principal de la concurrencia es mejorar la *organización* y la *reactividad* de un sistema, permitiendo que un programa maneje múltiples tareas de forma independiente sin bloquearse.

#### Definición:

> La concurrencia es cuando varios procesos **conviven** a la vez, si varios procesos **conviven** a la vez entonces son concurrentes. Sin embargo **convivir** a la vez no implica que ejecuten al mismo tiempo. Por tanto la concurrencia **NO** necesariamente implica paralelismo. 

- La concurrencia es un superconjunto del paralelismo. TODO proceso paralelo por definición se considera concurrente.

**Ejemplo:** Un navegador web que descarga una imagen mientras el usuario sigue navegando por la página. Ambas tareas progresan, aunque el procesador podría estar alternando rápidamente entre ellas (context switching).

## Computación Paralela

La **computación paralela** implica la ejecución simultánea de múltiples tareas o sub-tareas de una única tarea para lograr un resultado más rápido. Requiere de hardware que permita la ejecución en paralelo (múltiples núcleos de CPU, GPUs, etc.). El objetivo fundamental es reducir el *tiempo de ejecución* de un problema dividiéndolo en partes que pueden resolverse al mismo tiempo.

#### Definición 

>El paralelismo ocurre cuando varios procesos **Se ejecutan a la vez**, eso implica el paralelismo, por tanto varios procesos que se **ejecutan a la vez** implican que dichos procesos **existen/conviven** a la vez, por tanto **Paralelismo -> Concurrencia**. Pero como vimos arriba esta implicación NO es bidireccional. 

**Ejemplo:** Un programa de procesamiento de imágenes que divide una imagen en cuatro cuadrantes y asigna cada cuadrante a un núcleo de CPU diferente para su procesamiento simultáneo.

## Computación Distribuida

La **computación distribuida** se basa en un sistema en el que múltiples ordenadores (nodos) trabajan juntos en red para lograr un objetivo común. Estos nodos no comparten memoria ni reloj, sino que se comunican exclusivamente a través de mensajes. El objetivo es proporcionar *escalabilidad*, *tolerancia a fallos* y la capacidad de resolver problemas que son demasiado grandes para un solo ordenador.

**Ejemplo:** Un clúster de servidores web que distribuye las peticiones de los usuarios entre ellos para manejar un alto volumen de tráfico.

## Similitudes y Diferencias

### Similitudes
*   **Gestión de Múltiples Tareas:** Todas buscan manejar y procesar múltiples tareas o componentes de tareas de alguna manera.
*   **Mejora del Rendimiento o la Eficiencia:** Ya sea a través de una mejor organización (concurrencia), mayor velocidad (paralelismo) o escalabilidad/fiabilidad (distribuida).

### Diferencias

| Característica        | Concurrente                                          | Paralela                                             | Distribuida                                          |
| :-------------------- | :--------------------------------------------------- | :--------------------------------------------------- | :--------------------------------------------------- |
| **Objetivo Principal**| Organización, reactividad, manejo de múltiples tareas| Velocidad de ejecución, reducir tiempo de cómputo   | Escalabilidad, tolerancia a fallos, resolución de problemas grandes|
| **Naturaleza**        | Lógica (tareas superpuestas en el tiempo)             | Física (ejecución simultánea real)                   | Geográfica/Lógica (múltiples máquinas en red)       |
| **Recursos**          | Puede usar un solo núcleo de CPU                     | Requiere múltiples unidades de procesamiento (núcleos, GPUs) | Múltiples máquinas independientes, conectadas por red |
| **Comunicación/Coord.**| Comparten recursos, usan mecanismos de sincronización (locks, semáforos) | Comparten memoria, acceso rápido a datos compartidos | Comunicación por mensajes (latencia de red)          |
| **Acoplamiento**      | Alto                                                 | Alto                                                 | Bajo (más autónomas)                                 |

## Concurrente vs. Secuencial: ¿Sinónimos?

No, **computación concurrente y computación secuencial NO son sinónimos**.

*   **Computación Secuencial:** Las instrucciones se ejecutan una tras otra, en un orden predefinido y sin solapamiento en el tiempo. Cada tarea debe completarse antes de que la siguiente pueda comenzar. Es el modelo de ejecución más simple y directo.

*   **Computación Concurrente:** Como se explicó, las tareas progresan *aparentemente* al mismo tiempo, entrelazándose lógicamente. Un sistema concurrente puede estar ejecutándose en un solo núcleo de CPU, alternando entre las tareas rápidamente.

### ¿Por qué no son sinónimos?

La clave está en la **superposición en el tiempo**. En la computación secuencial, no hay superposición; todo es estrictamente uno después de otro. En la concurrente, sí hay superposición lógica, incluso si la ejecución física real es por turnos (lo que se conoce como *multitarea preemptiva* o *context switching* en un solo procesador).

La concurrencia se enfoca en *manejar muchas cosas a la vez* (gestión lógica), mientras que la secuencialidad se enfoca en *hacer una cosa cada vez*. El paralelismo, por otro lado, se enfoca en *hacer muchas cosas simultáneamente* (ejecución física). Un programa concurrente puede ejecutarse en paralelo si hay recursos físicos disponibles, pero no es un requisito. Un programa paralelo siempre es concurrente.

## Context Switching: ¿Exclusivo de la Concurrencia?

El **context switching** (cambio de contexto) es el proceso mediante el cual un procesador almacena el estado de un proceso o hilo y restaura el estado de otro proceso o hilo, permitiendo que la ejecución del segundo proceso o hilo continúe desde el punto donde fue suspendido. Este mecanismo es fundamental para la **multitarea** y la **concurrencia** en sistemas operativos.

### ¿Es específico de la computación concurrente?

Sí, el context switching está intrínsecamente ligado a la computación concurrente, especialmente cuando el número de tareas (hilos/procesos) activas supera el número de unidades de procesamiento (núcleos de CPU) disponibles. En un entorno concurrente con recursos limitados, el sistema operativo utiliza el context switching para dar la ilusión de ejecución simultánea, alternando rápidamente el uso del CPU entre las diferentes tareas. Sin el context switching, una tarea bloquearía completamente al procesador hasta su finalización, impidiendo la concurrencia.

### ¿No hay context switching en la computación paralela?

En la **computación paralela verdadera**, donde cada tarea o sub-tarea se ejecuta en una unidad de procesamiento independiente y dedicada (por ejemplo, un hilo en un núcleo de CPU diferente), el *context switching entre esas tareas específicamente paralelizadas* se minimiza drásticamente o incluso puede ser inexistente durante su ejecución simultánea. Esto se debe a que cada tarea tiene su propio recurso físico y no necesita compartir el tiempo del procesador con otras tareas paralelas del mismo problema.

Sin embargo, esto no significa que no haya *ningún* context switching en un sistema que esté ejecutando procesos paralelos. Un sistema operativo es un entorno complejo que gestiona muchos procesos y tareas concurrentes, no solo las que el usuario ha diseñado para ser paralelas.
*   **A nivel de sistema:** El sistema operativo aún puede realizar context switching entre el conjunto de procesos paralelos y otros procesos del sistema (como servicios del SO, programas en segundo plano, etc.) que están compitiendo por los recursos generales del sistema.
*   **Sub-tareas o hilos dentro de un proceso paralelo:** Si un proceso paralelo crea más hilos de los que el hardware puede ejecutar simultáneamente (por ejemplo, 10 hilos en un CPU de 4 núcleos), entonces sí habrá context switching entre esos hilos para compartir los 4 núcleos disponibles.

En resumen:
*   El context switching es un mecanismo clave para la **concurrencia**, permitiendo que múltiples tareas compartan un número limitado de recursos de procesamiento.
*   En el **paralelismo verdadero**, el objetivo es evitar el context switching entre las tareas paralelizadas, asignando a cada una su propio recurso de procesamiento para una ejecución genuinamente simultánea y más rápida. No obstante, el context switching puede ocurrir en otros niveles del sistema o si hay más tareas que recursos disponibles incluso dentro de un esquema "paralelo".
