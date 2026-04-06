# Ejercicios de la Práctica 5 (P5) - CCPD

## Resumen General

La P5 se centra en el estudio y ejecución de pipelines usando **pipes** (tuberías) y **queues** (colas), analizando su rendimiento, paralelismo y complejidad algorítmica.

- **Que es un pipeline(CCPD context)**:  Un pipeline es una **arquitectura de procesamiento paralelo donde el trabajo se divide en etapas conectadas en serie**, procesando múltiples elementos simultáneamente.
	- Características Fundamentales:
	- La figura ASCII es **INDEPENDIENTE de la implementación**. Representa la arquitectura lógica, no la implementación.
	- Solo es un diagrama para entender el **paralelismo de flujo**
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Input      │ →│ Etapa1     │ →│ Etapa2    │ →│ Etapa3    │ → Output
│ Elemento A ││ ProcesarA│   │ ProcesarB│    │ ProcesarC│
└─────────┘    └─────────┘    └─────────┘    └─────────┘
                    ↓
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Input      │ →│ Etapa1    │ →│ Etapa2     │ →│ Etapa3    │ → Output
│ Elemento B ││ ProcesarB│    │ ProcesarC│   │ ProcesarD│
└─────────┘    └─────────┘    └─────────┘    └─────────┘
                    ↓
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Input      │ →│ Etapa1     │ →│ Etapa2    │ →│ Etapa3    │ → Output
│ Elemento C ││ ProcesarC│   │ ProcesarD│   │ ProcesarE│
└─────────┘    └─────────┘    └─────────┘    └─────────┘
![[Pasted image 20260325112427.png]]
- **Que es una pipe(CCPD context):** Un pipe es un **mecanismo de comunicación interproceso (IPC (Inter-Process-Comunicator))** que conecta dos extremos para el intercambio de datos.
	Pipe Bidireccional (comunicación duplex)
┌─────────────┐                           ┌─────────────┐
│   Extremo 1    │ ◄─── PIPE ───► │   Extremo 2    │
│   (Writer)        │                            │   (Reader)        │
└─────────────┘                            └─────────────┘

PIPELINE (Arquitectura)
    ↓ usa como base
┌─────────┐     ┌─────────┐    ┌─────────┐
│ Etapa1    │ → │ Etapa2     │ →│ Etapa3    │
└────┬────┘     └────┬────┘    └────┬────┘
      │                       │                      │
      └───PIPE──►    └───PIPE──►   └───PIPE──► (Mecanismo de conexión) PIPE / QUEUE

![[Pasted image 20260325102111.png]]

- **Etapa:** es un **conjunto de funciones `lógicas` que transforman los datos de entrada**, independientemente de cómo se ejecuten(el orden y la forma de ejecución y demás).    **Una etapa = Un bloque de transformación lógica que se aplica a los datos.**
	> Para esta practica en especifico es importante recalcar que cada etapa tiene SOLO UNA función por etapa 
![[Pasted image 20260325104156.png]]

📊 Resumen Visual Completo
Arquitectura Lógica (Misma para Pipes y Queues):
┌─────────┐      ┌─────────┐    ┌─────────┐
│ Input       │ →  │ Etapa1     │ →│ Etapa2    │ → Output
│ Elemento A│   │ ProcesarA │   │ ProcesarB│
└─────────┘      └──────┬───┴   ──────┬───┘
                      ↓                      ↓
                 ┌─────────┐  ┌─────────┐
                 │ PIPE/       │  │   PIPE/     │
                 │ QUEUE    │  │ QUEUE    │
                 └─────────┘  └─────────┘
Implementación con Pipes:
- Conexión: pipe_in.recv() → procesar → pipe_out.send()
- Sincronía: Bloqueante (espera activa)
- Buffer: Mínimo
Implementación con Queues:
- Conexión: queue.get() → procesar → queue.put()  
- Sincronía: No bloqueante (puede continuar)
- Buffer: Configurable (QUEUE_SIZE)

**QUEUE_SIZE y complejidad por etapas -> Relacion:**
![[Pasted image 20260325123407.png]]

- **Que es un worker?** -> Un worker **es un proceso o hilo** que ejecuta la función de procesamiento dentro del pool(se encarga de procesar datos).

📊 Resumen Visual Final
┌─────────────────────────────────────────────────────────────┐
│                    PARALELISMO EN PIPELINES                                              │
├─────────────────────────────────────────────────────────────┤
│                                                                                                               │
│  NIVEL 1: FLUJO (Pipeline Parallelism)                                                   │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                                         │ 
│  │ Etapa1     │ →│ Etapa2    │ →│ Etapa3     │                                        │
│  │(4 W)        │    │(4 W)        │    │(4 W)        │                                        │
│  └────┬────┘    └────┬────┴──────┬───── ┘                                        │
│           │                      │                     │                                                    │
│           ▼                     ▼                   ▼                                                   │
│           [A]                   [B]                   [C]                                                 │
│                                                                                                                │
│  Elementos A, B, C en ETAPAS DIFERENTES simultáneamente               │
│                                                                                                                │
├─────────────────────────────────────────────────────────────┤
│                                                                                                               │
│  NIVEL 2: PROCESAMIENTO (Pooling)                                                   │
│  Etapa1: Worker1│Worker2│Worker3│Worker4                                     │
│                   [A] │         [B]   │      [C]   │      [D]                                          │
│                                                                                                                 │
│  Múltiples workers procesando en paralelo dentro de la etapa             │
│                                                                                                                │
├─────────────────────────────────────────────────────────────┤
│                                                                                                               │
│  NIVEL 3: TAREAS (Batching)                                                                 │
│  Worker recibe [A,B,C,D] en lugar de A                                                 │
│                                                                                                               │
│  Menor overhead, mejor utilización                                                      │
│                                                                                                               │
└─────────────────────────────────────────────────────────────┘
## Tarea 1 – Estudio del código basado en pipes

### Enunciado

Analiza el resto de la función run_pipeline para comprender más en detalle la construcción del pipeline, especialmente el orden de las funciones a ejecutar en las tareas centrales, así como la manera en la que se realiza la 'conexión' de los 'pipes'.

### Teoría Necesaria

#### 1. Pipes y el Sistema Operativo

Las tuberías de Python usan los mecanismos nativos del SO para comunicaciones entre procesos:

- **Comunicaciones bloqueantes**: Si un proceso emisor quiere enviar, espera a que el receptor lea; si un receptor quiere leer, se bloquea hasta recibir
- **Diseño DAG (Grafo Acíclico Dirigido)**: El pipeline es un camino crítico donde la etapa más lenta determina el tiempo total

#### 2. Conexión de Pipes en Pipelines

# Estructura básica del pipeline:

Generador → Pipe1 → Etapa1 → Pipe2 → Etapa2 → Pipe3 → Etapa3 → Consumer

**Construcción paso a paso:**

1. Se define un **generador** que introduce datos iniciales en la primera tubería
2. Se crean las **etapas centrales**: cada proceso recibe pipe_in (de donde lee) y pipe_out (por donde envía)
3. El flujo termina en un **consumidor** que recoge los resultados finales

### Código de Referencia

def pipe_stage(pipe_in, pipe_out, funct):

_, input_pipe = pipe_in

output_pipe, _ = pipe_out

start = time.time()

try:

while True:

item = input_pipe.recv() # Bloqueante: espera a recibir

result = funct(item)

if result:

output_pipe.send(result) # Bloqueante: espera a enviar

except EOFError:

end = time.time()

print(f"Stage '{funct.__name__}' finished after {to_time_miliseconds(start, end)} ms")

output_pipe.close()

## Tarea 2 – Ejecución del código basado en pipes

### Enunciado

Ejecuta el 'código1_pipes':

- ¿Es el resultado final el mismo usando pipelines que ejecutando de forma secuencial? (test de validación)
- Con un rango de datos de 10 a 2e5, ¿Tarda lo mismo la versión secuencial que la paralela con hilos? ¿Y con procesos hay ganancia?
- ¿Si ambas versiones paralelas tardan lo mismo o incluso más, a qué crees que se debe?
- ¿Tardan lo mismo todas las funciones, o algunas son más rápidas?

### Teoría Necesaria

#### 1. Ejecución Secuencial vs Paralela

AspectoSecuencialPipeline ParaleloProcesoÚnico proceso aplica todas las funciones consecutivamenteFunciones en procesos diferentes simultáneamenteDatosUn elemento procesado completo antes del siguienteDatos fluyen a través de etapas

#### 2. Factores que Afectan el Rendimiento

- **Coste de cada función**: No todas tienen la misma complejidad
- **Comunicaciones bloqueantes**: Las tuberías obligan a esperar
- **Datos y orden de etapas**: Influyen en la mejora obtenida

### Preguntas Clave para Análisis

1. **Validación**: Comparar resultados entre secuencial y paralelo
2. **Rendimiento con hilos vs procesos**: Los procesos pueden tener mejor ganancia al evitar el GIL (Global Interpreter Lock)
3. **Diferencias de tiempo por función**: Las funciones más complejas tardan más

## Tarea 3 – Estudio del código basado en queues

### Enunciado

Analiza el resto del 'código2_queues'. Estudia en particular la función queue_stage_parallel, que implementa la ejecución de una etapa con paralelismo basado en Pooling.

### Teoría Necesaria

#### 1. Diferencias Clave: Pipes vs Queues

CaracterísticaPipes (Tuberías)Queues (Colas)BloqueantesSÍ - emisor espera a receptorNO - se puede introducir y continuarAlmacenamientoBuffer mínimoCapacidad para múltiples elementosMulti-accesoEmisor único → Receptor únicoAcceso seguro de varios procesos/hilos

#### 2. Pooling y Paralelismo Múltiple

**Pooling**: Crear y reutilizar un conjunto de workers en lugar de crearlos/destruirlos continuamente.

def queue_stage_parallel(queue_in, queue_out, funct, n_workers=4):

"""

Ejecuta una etapa con paralelismo basado en Pooling.

- Crea un pool de n_workers procesos/hilos

- Cada worker procesa items del queue_in y envía a queue_out

- Los workers se reutilizan para múltiples tareas

"""

from multiprocessing import Pool

  

with Pool(processes=n_workers) as pool:

# Envía lotes de datos a los workers

results = pool.map(funct, data)

for result in results:

queue_out.send(result)

#### 3. Variables Clave del Pooling

VariableDescripciónEfectoPOOL_WORKERSNúmero de workers en el poolPocos → cuello de botella; Muchos → overhead/ociosidadQUEUE_SIZETamaño máximo de las colas entre etapasPequeño → bloqueos frecuentes; Grande → alto uso de memoriaBATCH_SIZENúmero de elementos por tarea (lote)Pequeño → alta gestión, workers siempre activos; Grande → menos gestión, posibles esperas

### Consideraciones de Pooling

- **Overhead**: Crear/destruir procesos tiene coste; el pooling lo amortiza con muchas tareas
- **Process oversubscription**: Tener más workers que núcleos físicos NO es perjudicial - los tiempos ociosos se aprovechan por otras etapas

## Tarea 4 – Ejecución del código basado en queues, validación

### Enunciado

Ejecuta el 'código2_queues' con las secciones descomentadas para validar el pipeline usando resultados de la ejecución secuencial.

### Teoría Necesaria

#### 1. Tipos de Paralelismo Implementables

ConfiguraciónDescripciónsequentialEjecución secuencial de funciones sobre la listaparallelEtapas en paralelo, ejecución interna secuencialparallel_multi_threadsEtapas + Pooling con hilos dentro de cada etapaparallel_multi_processEtapas + Pooling con procesos dentro de cada etapa

#### 2. Validación del Pipeline

La validación compara:

- **Resultado final**: Debe ser idéntico entre todas las configuraciones
- **Tiempo de ejecución**: Varía según el grado de paralelismo aplicado

## Tarea 5 – Ejecución del código basado en queues, experimentación

### Enunciado

Descomenta y ejecuta los experimentos para ver el papel de las variables en modular el paralelismo:

- ¿Observas diferentes tiempos entre etapas? ¿A qué se debe?
- ¿Qué etapa es cuello de botella?
- ¿Hay ganancia secuencial vs paralelo simple?
- ¿Todas las funciones se benefician del paralelismo?
- ¿Diferencia entre ejecución interna secuencial vs paralela de etapas?
- Efecto de POOL_WORKERS, QUEUE_SIZE, BATCH_SIZE

### Teoría Necesaria

#### 1. Cuello de Botella (Bottleneck)

**Definición**: La tarea que consume más tiempo y determina el rendimiento global del pipeline.

- **En escenarios bloqueantes (pipes)**: El cuello de botella bloquea al resto, haciendo que todos tengan tiempos iguales o mayores
- **En escenarios no bloqueantes (queues)**: Indica dónde optimizar; mejorar otra etapa no reduce el tiempo total si hay esperas

#### 2. Factores que Causan Diferencias entre Etapas

1. **Complejidad algorítmica**: Funciones como is_prime son más costosas que filter_evens
2. **Orden de las funciones**: Afecta cuántos datos llegan a cada etapa (ej: filtrar pares antes que primos reduce carga)
3. **Datos de entrada**: Una lista desordenada vs pre-filtrada afecta el trabajo de cada etapa

#### 3. Ganancia del Paralelismo

ComparaciónEsperadoSecuencial vs paralelo simpleSÍ hay ganancia (etapas simultáneas)Hilos vs procesos en PoolingProcesos pueden tener mejor ganancia (evitan GIL)Paralelismo interno de etapasDepende de la complejidad de cada función

#### 4. Efecto de las Variables

**POOL_WORKERS:**

- Aumentar: Reduce cuello de botella pero aumenta overhead y puede dejar workers ociosos
- Optimal: Cerca del número de núcleos físicos, considerando que no todas las funciones paralelizan bien

**QUEUE_SIZE:**

- Pequeño (< 10): Alta probabilidad de bloqueos cuando se llena
- Grande (> 1000): Alto uso de memoria, posible agotamiento con datos infinitos
- Optimal: Depende del volumen de datos y latencia de comunicación

**BATCH_SIZE:**

- Pequeño (1-5): Workers siempre activos pero alta sobrecarga de gestión
- Grande (100+): Menor sobrecarga pero workers pueden esperar a acumular lote
- Optimal: Balance entre utilización y overhead; típicamente 10-50 para datos numéricos

## Tarea 6 – Complejidad algorítmica de las funciones

### Enunciado

Analiza las funciones del código2 e intenta ordenarlas por complejidad. Verifica:

- filter_divisible_by → O(1)
- is_prime → O(sqrt(n))
- checksum → O(n)
- filter_evens → O(1)
- is_emirp → O(n)

### Teoría Necesaria

#### 1. Notación Big-O Explicada

ComplejidadSignificadoEjemploO(1)Tiempo constante, independiente del tamaño de entradaAcceso a array por índiceO(log n)LogarítmicoBúsqueda binariaO(n)LinealRecorrer una lista una vezO(sqrt(n))Raíz cuadradaVerificar primalidad simple

#### 2. Análisis de Cada Función

**filter_divisible_by(x, n) → O(1)**

def filter_divisible_by(item, n):

"""

Devuelve item si es divisible por n, None en otro caso.

  

Complejidad: O(1)

- Una sola operación de módulo: item % n

- No depende del tamaño de item (solo su valor numérico)

"""

return item if item % n == 0 else None

**Por qué O(1):** El operador % es una operación aritmética básica que se ejecuta en tiempo constante, independientemente del valor de item.

**is_prime(n) → O(sqrt(n))**

def is_prime(num):

"""

Comprueba si un número es primo.

  

Complejidad: O(sqrt(n))

- Solo necesita verificar divisores hasta sqrt(n)

- Si n tiene un divisor mayor que sqrt(n), también tendría uno menor

"""

if num < 2:

return False

if num == 2:

return True

if num % 2 == 0:

return False

  

# Solo verificar impares hasta sqrt(num)

i = 3

while i * i <= num: # Equivalente a i <= sqrt(num)

if num % i == 0:

return False

i += 2

return True

**Por qué O(sqrt(n)):**

- Si n es compuesto, tiene al menos un factor primo ≤ √n
- Verificamos divisores impares: 3, 5, 7, ..., hasta √n
- Número de iteraciones ≈ (√n - 1) / 2 = O(√n)

**checksum(data) → O(n)**

def checksum(items):

"""

Calcula una suma checksum de todos los items.

  

Complejidad: O(n)

- Debe procesar cada elemento exactamente una vez

- n = número de elementos en la lista

"""

total = 0

for item in items: # Recorre TODOS los elementos

if item:

total += item

return total

**Por qué O(n):** El bucle for itera sobre cada elemento de la lista una vez. Si hay n elementos, se ejecuta n veces.

**filter_evens(x) → O(1)**

def filter_evens(item):

"""

Devuelve item si es par, None en otro caso.

  

Complejidad: O(1)

- Una sola operación de módulo con 2

"""

return item if item % 2 == 0 else None

**Por qué O(1):** Similar a filter_divisible_by, es una operación aritmética básica.

**is_emirp(n) → O(n)**

def is_emirp(num):

"""

Un emírprimo es un número primo que se lee igual al revés (ej: 131).

  

Complejidad: O(n) donde n = valor del número

- Primero verifica si es primo: O(sqrt(n))

- Luego convierte a string y verifica palíndromo: O(d) donde d = dígitos

- Para números grandes, la conversión y comparación de string puede ser O(n)

"""

if not is_prime(num):

return False

  

s_num = str(num)

s_reversed = s_num[::-1]

return s_num == s_reversed

**Por qué O(n):**

- La conversión a string tiene complejidad proporcional al número de dígitos
- Para un número N con d dígitos: d ≈ log₁₀(N)
- En términos del valor numérico, esto se considera O(log N) o aproximadamente O(n) para análisis simplificado

### Resumen de Complejidades

FunciónComplejidadOperación Dominantefilter_divisible_byO(1)Módulo %filter_evensO(1)Módulo %is_primeO(√n)Bucle hasta √nchecksumO(n)Recorrido completois_emirpO(n)Conversión string + comparación

## Preguntas de Análisis para la P5

### Tarea 2 - Preguntas

1. **Validación**: ¿El resultado es idéntico? → SÍ, el pipeline procesa los mismos datos con las mismas funciones
2. **Hilos vs Procesos**: Los procesos suelen tener mejor ganancia al evitar el GIL de Python
3. **Por qué igual o más lento**: Overhead de creación de procesos, comunicación por pipes bloqueantes
4. **Diferencias entre funciones**: Las más complejas (is_prime, checksum) tardan más

### Tarea 5 - Preguntas

1. **Tiempos diferentes entre etapas**: SÍ, debido a la diferente complejidad algorítmica de cada función
2. **Cuello de botella**: Generalmente is_emirp o checksum (mayor complejidad)
3. **Ganancia secuencial vs paralelo**: SÍ hay ganancia por ejecución simultánea de etapas
4. **No todas se benefician**: Funciones O(1) tienen poco que ganar del paralelismo interno
5. **Ejecución interna**: El paralelismo dentro de etapas ayuda más a funciones complejas
6. **Variables**: Cada una modula el balance entre rendimiento y recursos usados

## Conclusiones Clave

1. **Pipes vs Queues**: Las queues son más flexibles (no bloqueantes) pero consumen más memoria
2. **Cuello de botella**: La etapa más lenta determina el tiempo total en pipelines bloqueantes
3. **Paralelismo efectivo**: Depende del balance entre complejidad de funciones y overhead de comunicación
4. **Configuración óptima**: Requiere experimentación con POOL_WORKERS, QUEUE_SIZE y BATCH_SIZE según los datos específicos