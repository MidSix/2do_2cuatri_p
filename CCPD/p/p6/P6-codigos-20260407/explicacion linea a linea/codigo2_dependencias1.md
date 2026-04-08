# Documentación Detallada - Examen P6

## Módulo 2: codigo2_dependencias1.py

```python
1 #! /usr/bin/python```
Shebang que indica Python como interpretador para ejecución directa del script.

```python
2 #```
Inicio de bloque de copyright y licencia académica.

```python
3 # Copyright © 2025 by Jonatan Enes (jonatan.enes@udc.es)```
Atribución de autoría con contacto institucional del autor.

```python
4 # Computer Engineering department, Universidade da Coruña, Spain.```
Identificación del departamento académico y origen geográfico del autor.

```python
5 #```
Continuación del bloque legal de uso del código fuente.

```python
6 # This file is part of several courses on parallel processing from Universidade da Coruña,```
Declaración de pertenencia a material educativo de procesamiento paralelo.

```python
7 # and it can only be used and/or modified by the author, the students or any ```
Restricción de uso: autor, estudiantes o personas explícitamente autorizadas.

```python
8 # explicitly authorized person by the author, inside the context of the subject. ```
Limitación al contexto académico del curso específico correspondiente.

```python
9 # Redistribution to a third-party without previous authorization is strictly forbidden.```
Prohibición absoluta de redistribución sin autorización previa explícita.

```python
10 # No commercial use is allowed.```
Uso exclusivamente no comercial permitido bajo licencia académica.

```python
11 #```
Continuación del bloque de restricciones legales y éticas.

```python
12 # This file has only academic purposes and should not be used for any real-world```
Declaración de propósito académico exclusivo sin garantía para aplicaciones reales.

```python
13 # scenario, the author holds no accountability for its use or misuse.```
Descargo de responsabilidad sobre posibles usos inadecuados del código.

```python
14 ```
Fin del bloque completo de copyright y licencia académica.

```python
15 import time```
Importa módulo `time` para medición precisa de tiempos de ejecución.

```python
16 from concurrent.futures.process import ProcessPoolExecutor```
Importa ejecutor de procesos para paralelización mediante múltiples núcleos CPU.

```python
17 from auxiliar import get_chunks, to_time_miliseconds, sci_not_str, flatten_list_of_lists, validate```
Importa funciones utilitarias: división de datos, conversión temporal, notación científica, aplanado y validación.

```python
18 import pandas as pd```
Importa librería `pandas` para visualización estructurada de datos en tablas.

```python
19 ```
Fin de todas las importaciones necesarias para el módulo.

```python
20 pd.set_option('display.max_rows', 20)```
Configura pandas para mostrar máximo 20 filas sin truncamiento visual.

```python
21 pd.set_option('display.max_columns', 500)```
Permite visualizar hasta 500 columnas en tablas de resultados extensas.

```python
22 pd.set_option('display.width', 1000)```
Establece ancho máximo de visualización de 1000 caracteres para mejor legibilidad.

```python
23 ```
Fin de configuración de visualización optimizada para datos extensos.

```python
24 N_PROC = 4```
Variable global que define número de procesos paralelos por defecto (4 núcleos).

```python
25 DEBUG = True```
Bandera de depuración activada para mostrar información detallada durante ejecución.

```python
26 ```
Fin de variables globales de configuración del experimento.

```python
27 def parallel(data, seed):```
Función principal que ejecuta procesamiento secuencial en paralelo con dependencia entre iteraciones.

```python
28     resultsPar = data```
Inicializa resultados paralelos con copia del dataset original como base de referencia.

```python
29     orig_seed = seed```
Guarda valor inicial del seed para restauración periódica y reproducibilidad controlada.

```python
30 ```
Preserva estado inicial para ciclos completos de procesamiento paralelo.

```python
31     proc_chunks = get_chunks(len(data), NUM_PROCS)```
Divide dataset en chunks equitativos según número de procesos disponibles.

```python
32 ```
Prepara división de datos para distribución entre múltiples núcleos procesadores.

```python
33 if DEBUG:```
Bloque condicional que solo se ejecuta cuando depuración está activada.

```python
34     print("\nxxxxxxxx DATOS [SPLITTED] in {0} xxxxxxxxx".format(NUM_PROCS))```
Muestra encabezado indicando división de datos en N procesos paralelos.

```python
35     for (ini, end) in proc_chunks:```
Itera sobre cada rango definido para cada chunk del dataset dividido.

```python
36         print("{0}".format(["{0:2d}".format(n) for n in data[ini:end]]))```
Imprime visualización formateada de los datos contenidos en cada chunk específico.

```python
37 ```
Visualización detallada para verificar correcta división del dataset inicial.

```python
38     print("-----------------------\n")```
Línea divisoria separadora entre visualizaciones de chunks individuales.

```python
39 ```
Fin del bloque de depuración - solo visible cuando DEBUG=True activado.

```python
40 i = 0```
Contador principal que controla número total de iteraciones completas del ciclo paralelo.

```python
41 with ProcessPoolExecutor(max_workers=NUM_PROCS) as executor:```
Crea pool de procesos con NUM_PROCS trabajadores para ejecución concurrente.

```python
42     while i < N_REPEATS:```
Bucle principal que repite el procesamiento completo N_REPEATS veces para promedios estadísticos.

```python
43         futures = list()```
Inicializa lista vacía para almacenar objetos Future de tareas pendientes.

```python
44 ```
Prepara contenedor antes de enviar tareas a los procesos paralelos.

```python
45     for ini, end in proc_chunks:```
Itera sobre cada chunk del dataset dividido previamente en rangos definidos.

```python
46         futures.append(executor.submit(sequential, resultsPar[ini:end], seed))```
Envía cada chunk con su seed actual a proceso paralelo para procesamiento secuencial.

```python
47         seed = resultsPar[end - 1]```
Actualiza seed usando último resultado del chunk anterior para crear dependencia entre iteraciones.

```python
48 ```
La dependencia se establece mediante el valor de salida de un chunk como entrada del siguiente.

```python
49     resultsPar = list()```
Inicializa lista vacía para acumular resultados individuales de cada proceso completado.

```python
50     for f in futures:```
Recorre todos los objetos Future representando tareas terminadas en procesos paralelos.

```python
51         resultsPar.append(f.result())```
Obtiene resultado individual de cada tarea y lo agrega a lista acumuladora.

```python
52 ```
Recolecta resultados de todos los procesos antes de continuar con siguiente iteración.

```python
53 resultsPar = flatten_list_of_lists(resultsPar)```
Aplana estructura anidada resultante de múltiples listas concatenadas en paralelo.

```python
54 seed = orig_seed```
Restaura seed original al final de cada ciclo completo para reproducibilidad controlada.

```python
55 ```
Ciclo cerrado permite repetir procesamiento con estado inicial consistente.

```python
56 if DEBUG:```
Bloque condicional que muestra resultados detallados solo cuando depuración está activada.

```python
57     print("------ RESULTADOS ({1}) - SPLITTED in {0} ----------".format(NUM_PROCS, i))```
Encabezado indicando número de iteración y división en procesos paralelos activos.

```python
58     for (ini, end) in proc_chunks:```
Itera sobre cada rango definido para visualización chunk por chunk.

```python
59         print("{0}".format(["{0:2d}".format(n) for n in resultsPar[ini:end]]))```
Imprime resultados formateados de cada chunk procesado en paralelo.

```python
60     print("-----------------------\n")```
Línea divisoria separadora entre visualizaciones de resultados individuales.

```python
61 ```
Permite verificar que resultados paralelos coinciden con división esperada del dataset.

```python
62 i += 1```
Incrementa contador principal para próxima iteración completa del ciclo paralelo.

```python
63 return resultsPar```
Retorna lista final de resultados procesados en paralelo con todas las dependencias aplicadas.

```python
64 ```
Fin de `parallel()` - núcleo del algoritmo con dependencia entre chunks e iteraciones.

```python
65 def fun(res, num):```
Función matemática simple: multiplica acumulador por número y aplica módulo 100.

```python
66     res = (res * num) % 100```
Aplica operación modular que crea patrón cíclico en secuencia de resultados.

```python
67     return res```
Retorna resultado modificado para uso como acumulador en iteración siguiente.

```python
68 ```
Fin de `fun()` - función matemática determinista con comportamiento periódico.

```python
69 def sequential(data, seed):```
Función secuencial que procesa dataset linealmente con acumulación dependiente del seed.

```python
70     results = list()```
Inicializa lista vacía para almacenar resultados individuales de cada elemento procesado.

```python
71     previous_num = seed```
Establece valor inicial que se propagará a través de todas las iteraciones del procesamiento.

```python
72     for n in data:```
Itera sobre cada número del dataset en orden secuencial estricto.

```python
73         res = fun(previous_num, n)```
Aplica función matemática con acumulador anterior y valor actual del dataset.

```python
74         results.append(res)```
Guarda resultado individual para construcción de secuencia completa final.

```python
75     previous_num = n```
Actualiza acumulador al valor actual del dataset para propagación en iteraciones siguientes.

```python
76 ```
Propagación secuencial asegura que cada elemento dependa del anterior procesado.

```python
77 return results```
Retorna lista completa de resultados con todas las dependencias aplicadas secuencialmente.

```python
78 ```
Fin de `sequential()` - procesamiento lineal con acumulación dependiente.

```python
79 def experiment():```
Función principal que ejecuta comparación entre ejecución secuencial y paralela.

```python
80     data = [x for x in range(int(N_MIN), int(N_MAX))]```
Genera dataset completo de números enteros desde N_MIN hasta N_MAX-1 inclusive.

```python
81 print("-> N = {0} (from {1} to {2})\n".format(int(N_MAX - N_LEN), sci_not_str(int(N_MIN)), int(N_MAX)))```
Muestra tamaño del dataset con rango completo usando notación científica para valores grandes.

```python
82 start = time.time()```
Registra timestamp inicial para medir tiempo total de ejecución secuencial.

```python
83 resultsSeq = data```
Inicializa resultados secuenciales con copia del dataset original como base.

```python
84 ```
Punto de partida idéntico entre ejecuciones secuencial y paralela para comparación justa.

```python
85 print("Running sequentially")```
Indica inicio de fase secuencial que servirá como línea base de referencia.

```python
86 SEED = 1```
Establece valor inicial del seed idéntico entre ambas ejecuciones para reproducibilidad.

```python
87 if DEBUG:```
Bloque condicional que muestra datos originales solo cuando depuración está activada.

```python
88     print("\nxxxxxxxx DATOS xxxxxxxxx")```
Encabezado indicando visualización del dataset completo original.

```python
89     print("{0}".format(["{0:2d}".format(n) for n in data]))```
Imprime todos los datos formateados para verificación visual completa.

```python
90     print("")```
Salto de línea adicional para espaciado en salida terminal.

```python
91 ```
Permite verificar exactitud del dataset antes de procesamiento intensivo.

```python
92 i = 0```
Contador interno que controla número total de repeticiones del ciclo secuencial.

```python
93 while i < N_REPEATS:```
Bucle principal que repite procesamiento completo para promedios estadísticos precisos.

```python
94     resultsSeq = sequential(resultsSeq, SEED)```
Ejecuta función secuencial con resultados acumulados y seed inicial fijo.

```python
95 if DEBUG:```
Bloque condicional que muestra resultados intermedios solo cuando depuración está activada.

```python
96     print("------ RESULTADO ({0}) ----------".format(i))```
Encabezado indicando número de iteración actual del ciclo secuencial completo.

```python
97     print("{0}".format(["{0:2d}".format(n) for n in resultsSeq]))```
Imprime resultados formateados para verificación visual de cada iteración.

```python
98     print("-----------------------\n")```
Línea divisoria separadora entre visualizaciones de resultados individuales.

```python
99 ```
Permite rastrear evolución de resultados a través de múltiples repeticiones completas.

```python
100 i += 1```
Incrementa contador para próxima iteración completa del ciclo secuencial.

```python
101 end = time.time()```
Registra finalización de todas las repeticiones secuenciales completas.

```python
102 time_seq = to_time_miliseconds(start, end)```
Convierte diferencia temporal a milisegundos para medición precisa de rendimiento.

```python
103 print("Sequential execution took {0} ms, sum of results is {1}\n".format(time_seq, sum(resultsSeq)))```
Muestra tiempo total secuencial y suma acumulada como verificación adicional de resultados.

```python
104 ```
Establece línea base temporal para comparación directa con ejecución paralela posterior.

```python
105 print("Running in parallel with {0} processes".format(NUM_PROCS))```
Indica inicio de fase paralela con número específico de procesos activos simultáneamente.

```python
106 start = time.time()```
Registra timestamp inicial para medir tiempo total de ejecución paralela completa.

```python
107 resultsPar = parallel(data, SEED)```
Ejecuta función principal con dataset original y seed idéntico a ejecución secuencial.

```python
108 end = time.time()```
Registra finalización de todas las repeticiones paralelas completas.

```python
109 time_par = to_time_miliseconds(start, end)```
Convierte diferencia temporal a milisegundos para medición precisa de rendimiento paralelo.

```python
110 print("Parallel execution took {0} ms, sum of results is {1}\n".format(time_par, sum(resultsPar)))```
Muestra tiempo total paralelo y suma acumulada para verificación de consistencia básica.

```python
111 ```
Establece métrica temporal paralela para comparación directa contra línea base secuencial.

```python
112 print("Speedup is {0:2f}".format(time_seq/time_par))```
Calcula y muestra speedup como ratio de tiempo secuencial entre paréntesis paralelo.

```python
113 ```
Métrica fundamental para evaluar ganancia de rendimiento obtenida con paralelización.

```python
114 valid, message = validate(resultsSeq, resultsPar)```\nAplica función de validación que compara exhaustivamente ambos conjuntos de resultados.

```python
115 if not valid:```
Bloque condicional que se activa cuando validación detecta discrepancias entre resultados.

```python
116     print("Results ARE NOT equal")```
Alerta inmediata indicando que resultados no coinciden exactamente entre ambas ejecuciones.

```python
117     print(message)```
Muestra mensaje descriptivo específico de la discrepancia detectada por validación.

```python
118 else:```
Rama alternativa cuando validación confirma consistencia total entre resultados.

```python
119     print("Results ARE equal\n\n")```
Confirmación positiva indicando que ambas ejecuciones produjeron resultados idénticos.

```python
120 ```
Validación crítica asegura corrección del algoritmo antes de confiar en métricas de rendimiento.

```python
121 ```
Fin de `experiment()` - compara exhaustivamente ejecución secuencial contra paralela con validación completa.

```python
122 if __name__ == '__main__':```
Bloque principal que solo se ejecuta cuando el script es llamado directamente (no importado).

```python
273     N_MIN, N_MAX = 1e1, 5e1```
Configuración de validación: dataset pequeño para pruebas rápidas y verificación inmediata.

```python
274     N_REPEATS = 2```
Solo 2 repeticiones suficientes para validar corrección del algoritmo rápidamente.

```python
275     NUM_PROCS = 4```
Usa 4 procesos paralelos para demostrar funcionamiento básico de la implementación.

```python
276     DEBUG = True```
Depuración activada para visualización detallada durante pruebas de validación.

```python
277 print("####### VALIDATION EXPERIMENT")```
Encabezado indicando que esta primera ejecución es para validar corrección del algoritmo.

```python
278     experiment()```
Ejecuta experimento completo con configuración mínima para verificación rápida de funcionalidad.

```python
129 ```
Prueba inicial confirma que implementación básica funciona correctamente antes de pruebas de rendimiento.

```python
130     N_MIN, N_MAX = 1e1, 5e6```
Configuración de rendimiento: dataset masivo para medición precisa de escalabilidad y velocidad.

```python
131     N_REPEATS = 400```
Muchas repeticiones necesarias para promedios estadísticos significativos con dataset grande.

```python
132     NUM_PROCS = 8```
Usa 8 procesos para aprovechar hardware disponible y demostrar escalabilidad real.

```python
133     DEBUG = False```
Depuración desactivada para evitar saturación de salida durante pruebas de rendimiento intensivas.

```python
134 print("####### PERFORMANCE EXPERIMENT")```
Encabezado indicando que esta segunda ejecución es para medir rendimiento real con dataset grande.

```python
135     experiment()```
Ejecuta experimento completo con configuración optimizada para medición precisa de velocidad y speedup.

```python
136 ```
Prueba final evalúa comportamiento con carga real y dataset masivo para métricas significativas.

```python
137 ```
Fin del script - ejecuta dos fases: validación rápida seguida de prueba de rendimiento exhaustiva.
