> [!PDF|yellow] [[EnunciadoP2.pdf#page=1&selection=104,0,106,80&color=yellow|EnunciadoP2, p.1]]
> >  locks

- Se encargan de la coherencia y coordinación. Sin ellos implementar programas concurrentes seria muy inviable, entre otras cosas debido a las condiciones de carrera(razon por la que el resultado de multiples procesos dependientes puede generar diferentes respuestas en cada ejecucion)
- **Objetivos:** Locks, variables compartidas, productores(generadores de datos) y consumidores(procesadores de datos) 

> [!PDF|yellow] [[EnunciadoP2.pdf#page=3&selection=17,36,17,86&color=yellow|EnunciadoP2, p.3]]
> >  tienen sus recursos y flujo de ejecución propios.

- Esos recursos son la PC(point counter) / registros y un Stack(Pila)


> [!PDF|yellow] [[EnunciadoP2.pdf#page=6&selection=57,0,57,86&color=yellow|EnunciadoP2, p.6]]
> > Figura 2: Secuencia de lectura y escritura de una variable por parte de diversos hilos

- Es una figura que ilustra la "condición de carrera", es decir, muestra como varios hilos trabajando sobre una misma variable global pueden producir fallos, NO es un escenario de implementación de un lock (tipo de variable semáforo que SOLO deja pasar un hilo a la vez) sino una representación grafica de lo que ocurre SIN ellos. 

Recuadro Azul -> Memoria principal(MEM). "La RAM"
Recuadro Rojo -> Memoria privada/local:
	P MEM (Process Memory)
	T MEM  (Thread Memory)

- Usualmente el concepto de memoria local/privada se trata de la cache. Que cache?
	- La L1 y L2. Estas caches son por núcleo y privadas, los núcleos no pueden ver las L2/L1 de otros, solo las de ellos. Por lo cual P MEM se encuentra aquí. En especifico, al ser una sola variable lo que se esta leyendo y el bloque de código por tanto es minúsculo, **se tiene que encontrar en la cache L1**, la mas rápida y con tamaño mas pequeño de todas, esta a su vez tiene 2 divisiones. la L1i(Instructions) y la L1d(Data), como V no son una secuencia de instrucciones sino el contenido de una variable, una "Data" entonces se debe encontrar muy específicamente en la **Memoria Cache L1d** 

>La L3 se trata de "La cache del procesador". Aquella cache que contiene al resto de caches. Es esta la memoria que permite la comunicación entre cores, ya que la comunicación entre cores via Caches L2/L1 NO son posibles, al ser caches privadas de cada core.


> [!PDF|yellow] [[EnunciadoP2.pdf#page=6&selection=62,1,64,1&color=yellow|EnunciadoP2, p.6]]
> > operación atómica 

- Son operaciones que aplican un constraint(limitación) concurrente, pueden frenar el paralelismo/concurrencia de forma momentánea en secuencias de instrucciones que requieren un orden. Esto se hace para evitar las **Condiciones de carrera** y asegurar la coherencia de los datos. Y Los Locks se implementan mediante instrucciones atómicas a nivel de hardware (como Compare-and-Swap). Estas instrucciones actúan como un vínculo entre el hardware y el software. Conceptos Clave: 

1. Atomicidad: Una operación atómica es indivisible. El procesador garantiza que los pasos de "Lectura-Modificación-Escritura" se ejecuten como uno solo, sin que ningún otro hilo pueda interferir en medio. 
2. Constraint Concurrente: Las instrucciones atómicas fuerzan un orden. Si múltiples hilos intentan acceder a la vez, el hardware los obliga a pasar de uno en uno, eliminando el paralelismo en ese punto crítico para evitar el caos. 
3. Bloqueo de **Linea de Caché(la dirección especifica con la que se opera)**: A nivel de silicio, el núcleo que ejecuta la instrucción atómica "secuestra" la dirección de memoria, impidiendo que otros núcleos lean o escriban ese dato hasta que la operación termine. En resumen: La instrucción atómica es la herramienta de hardware que permite construir el "muro" del Lock en el software, asegurando que solo un hilo sea el "dueño" del recurso en un momento dado.

> En los años 90's era otra paranoia pero ahora mismo funciona así xd, hace décadas lo que se 
> hacia era un **Bus locking** bloqueaban el bus que permite comunicación cache RAM y el concepto de caches L1,2,3 también era distinto entonces las lecturas de hilos sobre cache L1d que seria ahora pues parece que se hacían sobre la RAM entonces al bloquearla pues no podían hacer operaciones sobre esa dirección de memoria, pero era super ineficiente porque por hacer un x = x + 1 te bloqueas todo xd. Bueno, tecnología vieja básicamente. Ahora lo que se hace es bloquear la Linea de cache especifica con la que esta trabajando un hilo de un proceso para que otros hilos del proceso no puedan usarla sin que termine el anterior, sin embargo los otros hilos pueden hacer otras cosas, por lo que guay.


> [!PDF|yellow] [[EnunciadoP2.pdf#page=7&selection=4,0,4,89&color=yellow|EnunciadoP2, p.7]]
> > Figura 3: Explicación gráfica comparando el efecto de usar o no una variable de tipo lock


### En resumen

- **`X[n]`** es simplemente una forma de decir "la variable X con valor n". Es decir, **NO** es una indexación, aquí en el esquema, la nomenclatura `[]` tiene un significado distinto, alberga simplemente el valor de la variable X luego de haberle hecho una operacion atomica, ya sea LOAD, ADD o STORE.
- **LOCK_ACQ(LOCK_ACQUIRE)** es la instrucción atómica que actúa como barrera. Solo deja pasar a un hilo, obligando a los demás a esperar a que el valor de la Cache del proceso sea actualizado realmente.
- Cada vez que un LOCK es adquirido por un hilo hemos de percatarnos que la columna que representa el valor de la L pasa de ser 1(disponible) a 0(NO disponible).
- El gráfico demuestra que gracias al Lock, las operaciones que antes se solapaban y se "pisaban" (escenario izquierda), ahora se ejecutan una **detrás** de otra (escenario derecha).


> [!PDF|yellow] [[EnunciadoP2.pdf#page=7&selection=6,0,6,106&color=yellow|EnunciadoP2, p.7]]
> > Figura 4: Explicación gráfica del funcionamiento de una instrucción atómica usada para implementar un lock


### En resumen

- En general esta es bastante fácil de ver. Un hilo, en este caso el 3, manda un LOCK_ACQ, que simplemente es una función que retorna un bool al hilo digamos. Si la variable "L" del LOCK:     L != 0, o sea, esta disponible, entonces entra, resta uno a la variable, hace lo que tiene que hacer, y cuando la libera suma uno a L porque se fue, no tiene mas xd. Y se recalca la diferencia entre LOCK y semáforo, pues un LOCK es un tipo de semáforo donde los hilos que pueden entrar dejan de ser "plural, y solo es uno" entra ese y se bloquea la Linea de cache, eso es todo.

> [!PDF|yellow] [[EnunciadoP2.pdf#page=9&selection=74,14,74,32&color=yellow|EnunciadoP2, p.9]]
> >  la cuenta parcial

-> La cuenta parcial de un hilo es el numero de veces que el hilo tendría que realizar una cuenta, en este caso es sumar 1, por tanto si la cuenta parcial de un hilo es sumar 10, como lo hace de uno en uno pues el hilo haría la operación sumar diez veces. 




Aquí tienes la resolución detallada de cada tarea basada en el código y los resultados de los experimentos realizados.

---


**1. ¿Afecta el ratio de productores a consumidores? ¿Por qué?** **Sí, afecta directamente al rendimiento.**

- **Explicación:** En el experimento **EXP 1**, observamos que con el mismo número de ítems (100), el tiempo varía según el ratio. Si tienes 5 productores y 10 consumidores (Ratio 1:2), el tiempo es de **8190 ms**, similar a tener 5 de cada uno (**8157 ms**).
    
- **Por qué:** El sistema está limitado por el componente más lento o menos numeroso. Si los productores no generan datos lo suficientemente rápido, los consumidores extra se quedan inactivos esperando. Si los consumidores son pocos, la cola se llena y los productores se detienen. El equilibrio ideal ocurre cuando la tasa de producción iguala a la de consumo.
    

**2. ¿Cómo evolucionan los tiempos cuando se aumentan de forma equilibrada?** **El tiempo disminuye drásticamente (mejora el rendimiento).**

- **Explicación:** Al pasar de 10 productores y 10 consumidores (**4433 ms**) a 100 de cada uno (**791 ms**), el tiempo de ejecución cae casi un 82%.
    
- **Por qué:** Al haber más hilos trabajando en paralelo, la probabilidad de que la cola esté vacía o llena disminuye, y se procesan más ítems simultáneamente, aprovechando mejor la capacidad de cómputo del procesador.
    

---


**¿Qué efecto tienen las esperas mínimas y máximas de los consumidores y los productores?** **Actúan como un freno directo al sistema: a mayor tiempo de "sleep", mayor tiempo de ejecución total.**

- **Explicación:** En el **EXP 2**, cuando tanto productores como consumidores tienen esperas bajas (250-500 ms), el tiempo es de **1978 ms**. Si duplicamos la espera de ambos (500-1000 ms), el tiempo sube a **3779 ms**.
    
- **Por qué:** El `time.sleep` simula el tiempo de procesamiento real de una tarea. Si un trabajador tarda más en "fabricar" o "comer", el flujo de la cola se ralentiza. Los resultados muestran que el tiempo total es casi proporcional al aumento de los retardos.
    

---

**¿Tiene efecto el tamaño de la cola?** **Sí, un tamaño mayor permite un flujo más fluido y reduce los bloqueos.**

- **Explicación:** En el **EXP 3**, con una cola de tamaño 1, el tiempo es de **16365 ms**. Al aumentar la cola a tamaño 10, el tiempo baja a **8767 ms**.
    
- **Por qué:** Una cola pequeña provoca que los hilos se bloqueen constantemente (el productor no puede poner si está llena, el consumidor no puede quitar si está vacía). Una cola más grande actúa como un **amortiguador (buffer)**, permitiendo que los productores sigan trabajando aunque los consumidores tengan un ligero retraso momentáneo, y viceversa.
    

---


**¿Cómo aumentan dichos tiempos a medida que el número de ítems se incrementa?** **Aumentan de forma lineal.**

- **Explicación:** En el **EXP 4**, procesar 100 ítems tarda **1205 ms**; 200 ítems tardan **1980 ms**; y 400 ítems tardan **3499 ms**.
    
- **Por qué:** Dado que la infraestructura (número de hilos y retardos) es constante, el tiempo total es directamente proporcional a la cantidad de trabajo. Si duplicas la carga de trabajo, el sistema tardará aproximadamente el doble de tiempo en vaciar la lista de tareas pendientes.
    
