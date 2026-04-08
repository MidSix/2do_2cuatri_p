# Documentación Detallada - Examen P6

## Módulo 3: codigo3_dependencias2.py

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
27 def parallel(data, seed_ini, seed_end):```
Función principal que ejecuta procesamiento paralelo con dependencias en extremos del dataset.

```python
28     resultsPar = data```
Inicializa resultados paralelos con copia del dataset original como base de referencia.

```python
29     print("Executing with {0} procs".format(NUM_PROCS))```
Muestra información diagnóstica sobre número de procesos que ejecutarán el procesamiento paralelo.

```python
30 ```
Información básica para verificar configuración antes de iniciar procesamiento intensivo.

```python
31     orig_seed_ini = seed_ini```
Guarda valor inicial del seed izquierdo para restauración periódica y reproducibilidad controlada.

```python
32     orig_seed_end = seed_end```
Guarda valor final del seed derecho para restauración periódica y consistencia entre ciclos.

```python
33 ```
Preserva ambos extremos del seed para mantener consistencia en múltiples iteraciones completas.

```python
34     proc_chunks = get_chunks(len(resultsPar), NUM_PROCS)```
Divide dataset en chunks equitativos según número de procesos disponibles simultáneamente.

```python
35 ```
Prepara división de datos para distribución entre múltiples núcleos procesadores activos.

```python
36 if DEBUG:```
Bloque condicional que solo se ejecuta cuando depuración está activada.

```python
37     print("\nxxxxxxxx DATOS [SPLITTED] in {0} xxxxxxxxx".format(NUM_PROCS))```
Muestra encabezado indicando división de datos en N procesos paralelos activos simultáneamente.

```python
38     for (ini, end) in proc_chunks:```
Itera sobre cada rango definido para cada chunk del dataset dividido previamente.

```python
39         print("{0}".format(["{0:2d}".format(n) for n in data[ini:end]]))```
Imprime visualización formateada de los datos contenidos en cada chunk específico procesado.

```python
40 ```
Visualización detallada para verificar correcta división del dataset inicial entre procesos.

```python
41     print("-----------------------\n")```
Línea divisoria separadora entre visualizaciones de chunks individuales procesados.

```python
42 ```
Fin del bloque de depuración - solo visible cuando DEBUG=True activado explícitamente.

```python
43 with ProcessPoolExecutor(max_workers=NUM_PROCS) as executor:```
Crea pool de procesos con NUM_PROCS trabajadores para ejecución concurrente simultánea.

```python
44     i = 0```
Contador principal que controla número total de iteraciones completas del ciclo paralelo.

```python
45     while i < N_REPEATS:```
Bucle principal que repite el procesamiento completo N_REPEATS veces para promedios estadísticos precisos.

```python
46         futures = list()```
Inicializa lista vacía para almacenar objetos Future de tareas pendientes en procesos.

```python
47         boundaries = list()```
Contenedor especial para almacenar límites de seed que definen dependencias entre chunks.

```python
48 ```
Prepara estructuras específicas para manejar dependencias complejas entre iteraciones paralelas.

```python
49     # 1st iteration```
Comentario indicando configuración especial del primer chunk con dependencia externa izquierda.

```python
50     boundaries.append((orig_seed_ini, resultsPar[proc_chunks[0][1]]))```
Agrega tupla con seed inicial izquierdo y valor final del primer chunk como límites de dependencia.

```python
51 ```
El primer chunk depende del seed externo proporcionado como parámetro de entrada original.

```python
52 ```
Comentario indicando configuración especial de chunks intermedios con dependencias internas completas.

```python
53     # Medium iterations```
Comentario indicando configuración especial del último chunk con dependencia externa derecha.

```python
54     for ini, end in proc_chunks[1:-1]:```
Itera sobre todos los chunks excepto el primero y el último (chunks completamente internos).

```python
55         boundaries.append((resultsPar[ini - 1], resultsPar[end]))```
Agrega tupla con valor final del chunk anterior como seed izquierdo y valor inicial actual como seed derecho.

```python
56 ```
Cada chunk interno depende del resultado exacto del chunk inmediatamente anterior procesado.

```python
57 ```
Comentario indicando configuración especial del último chunk con dependencia externa derecha.

```python
58     # Last iteration```
Comentario indicando que el último chunk tiene dependencia especial desde el extremo derecho.

```python
59     boundaries.append((resultsPar[proc_chunks[-1][0] - 1], orig_seed_end))```
Agrega tupla con valor final del penúltimo chunk como seed izquierdo y seed externo derecho original.

```python
60 ```
El último chunk depende del resultado del penúltimo chunk y del seed externo proporcionado originalmente.

```python
61     for (ini, end), (seed_ini, seed_end) in zip(proc_chunks, boundaries):```
Itera simultáneamente sobre chunks y sus límites de dependencia correspondientes usando zip.

```python
62         futures.append(executor.submit(sequential, resultsPar[ini:end], seed_ini, seed_end))```
Envía cada chunk con sus límites específicos de seed a proceso paralelo para procesamiento dependiente.

```python
63 ```
Cada proceso recibe información precisa sobre qué valores deben usarse como entradas externas.

```python
64     resultsPar = list()```
Inicializa lista vacía para acumular resultados individuales de cada proceso completado.

```python
65     for f in futures:```
Recorre todos los objetos Future representando tareas terminadas en procesos paralelos simultáneos.

```python
66         resultsPar.append(f.result())```
Obtiene resultado individual de cada tarea y lo agrega a lista acumuladora principal.

```python
67 ```
Recolecta resultados de todos los procesos antes de continuar con siguiente iteración completa.

```python
68 resultsPar = flatten_list_of_lists(resultsPar)```
Aplana estructura anidada resultante de múltiples listas concatenadas procesadas en paralelo simultáneamente.

```python
69 ```
Estructura final lista para comparación directa con resultados secuenciales esperados.

```python
70 if DEBUG:```
Bloque condicional que muestra resultados detallados solo cuando depuración está activada explícitamente.

```python
71     print("------ RESULTADOS ({1}) - SPLITTED in {0} ----------".format(NUM_PROCS, i))```
Encabezado indicando número de iteración y división en procesos paralelos activos simultáneamente.

```python
72     for (ini, end) in proc_chunks:```
Itera sobre cada rango definido para visualización chunk por chunk procesada.

```python
73         print("{0}".format(["{0:2d}".format(n) for n in resultsPar[ini:end]]))```
Imprime resultados formateados de cada chunk procesado en paralelo simultáneamente.

```python
74     print("-----------------------\n")```
Línea divisoria separadora entre visualizaciones de resultados individuales procesados.

```python
75 ```
Permite verificar que resultados paralelos coinciden con división esperada del dataset procesado.

```python
76 i += 1```
Incrementa contador principal para próxima iteración completa del ciclo paralelo simultáneo.

```python
77 return resultsPar```
Retorna lista final de resultados procesados en paralelo con todas las dependencias aplicadas correctamente.

```python
78 ```
Fin de `parallel()` - núcleo del algoritmo con dependencias en extremos y entre chunks internos.

```python
79 def fun(prev_n, num, next_n):```
Función matemática que depende de tres valores: anterior, actual y siguiente para cálculo modular.

```python
80     res = (prev_n + num + next_n) % 100```
Suma tres valores y aplica módulo 100 creando patrón cíclico con dependencia tridimensional.

```python
81     return res```
Retorna resultado modificado para uso como valor anterior en iteración siguiente del procesamiento.

```python
82 ```
Fin de `fun()` - función matemática con dependencia de tres valores adyacentes simultáneamente.

```python
83 def sequential(data, seed_ini, seed_end):```
Función secuencial que procesa dataset linealmente con dependencias en extremos y entre elementos.

```python
84     results = list()```
Inicializa lista vacía para almacenar resultados individuales de cada elemento procesado secuencialmente.

```python
85 ```
Punto de partida idéntico a la versión paralela para comparación directa de resultados.

```python
86     # 1st iteration```
Comentario indicando tratamiento especial del primer elemento con dependencia externa izquierda.

```python
87     previous_num = seed_ini```
Establece valor inicial desde el extremo izquierdo proporcionado como parámetro externo original.

```python
88     n = data[0]```
Obtiene primer elemento del dataset para procesamiento inicial con dependencias externas.

```python
89     next_num = data[1]```
Obtiene segundo elemento necesario para calcular resultado del primer elemento procesado.

```python
90     results.append(fun(previous_num, n, next_num))```
Aplica función matemática con tres valores: seed externo izquierdo, primer dato y segundo dato.

```python
91 ```
El primer resultado depende de valor externo proporcionado y dos elementos del dataset inicial.

```python
92     # Medium iterations```
Comentario indicando procesamiento estándar de elementos intermedios completamente internos.

```python
93     for i in range(1, len(data) - 1):```
Itera sobre todos los elementos excepto el primero y el último (elementos completamente internos).

```python
94         previous_num = n```
Actualiza valor anterior al elemento procesado en iteración inmediatamente anterior.

```python
95     n = data[i]```
Obtiene elemento actual del dataset para procesamiento con dependencias de ambos lados.

```python
96     next_num = data[i + 1]```
Obtiene siguiente elemento necesario para calcular resultado del elemento actual procesado.

```python
97     res = fun(previous_num, n, next_n)```
Aplica función matemática con tres valores: anterior procesado, actual y siguiente adyacente.

```python
98     results.append(res)```
Guarda resultado individual para construcción de secuencia completa final procesada secuencialmente.

```python
99 ```
Cada elemento interno depende del anterior procesado y del siguiente elemento adyacente en el dataset.

```python
100     # Last iteration```
Comentario indicando tratamiento especial del último elemento con dependencia externa derecha.

```python
101     previous_num = n```
Actualiza valor anterior al penúltimo elemento procesado en iteración inmediatamente anterior.

```python
102     n = data[-1]```
Obtiene último elemento del dataset para procesamiento final con dependencias externas.

```python
103     next_num = seed_end```
Usa valor externo proporcionado como parámetro derecho en lugar de elemento siguiente inexistente.

```python
104     results.append(fun(previous_num, n, next_num))```
Aplica función matemática con tres valores: anterior procesado, último dato y seed externo derecho.

```python
105 ```
El último resultado depende del penúltimo elemento procesado y del valor externo proporcionado originalmente.

```python
106 return results```
Retorna lista completa de resultados con todas las dependencias aplicadas secuencialmente correctamente.

```python
107 ```
Fin de `sequential()` - procesamiento lineal con dependencias en extremos y entre elementos adyacentes.

```python
108 def experiment():```
Función principal que ejecuta comparación entre ejecución secuencial y paralela con dependencias complejas.

```python
109     data = [x for x in range(int(N_MIN), int(N_MAX))]```
Genera dataset completo de números enteros desde N_MIN hasta N_MAX-1 inclusive para procesamiento.

```python
110 print("-> N = {0} (from {1} to {2})\n".format(int(N_MAX - N_LEN), sci_not_str(int(N_MIN)), int(N_MAX)))```
Muestra tamaño del dataset con rango completo usando notación científica para valores grandes procesados.

```python
111 start = time.time()```
Registra timestamp inicial para medir tiempo total de ejecución secuencial completa.

```python
112 resultsSeq = data```
Inicializa resultados secuenciales con copia del dataset original como base idéntica a paralela.

```python
113 ```
Punto de partida idéntico entre ejecuciones para comparación justa y precisa de rendimiento.

```python
114 print("Running sequentially")```
Indica inicio de fase secuencial que servirá como línea base de referencia para comparación.

```python
115 SEED_1, SEED_2 = 3, 7```
Establece valores iniciales y finales del seed diferentes entre ambos extremos del dataset procesado.

```python
116 if DEBUG:```
Bloque condicional que muestra datos originales solo cuando depuración está activada explícitamente.

```python
117     print("\nxxxxxxxx DATOS xxxxxxxxx")```
Encabezado indicando visualización del dataset completo original antes de procesamiento intensivo.

```python
118     print("{0}".format(["{0:2d}".format(n) for n in data]))```
Imprime todos los datos formateados para verificación visual completa del dataset procesado.

```python
119     print("")```
Salto de línea adicional para espaciado en salida terminal durante visualización de datos.

```python
120 ```
Permite verificar exactitud del dataset antes de procesamiento intensivo con dependencias complejas.

```python
121 i = 0```
Contador interno que controla número total de repeticiones del ciclo secuencial completo procesado.

```python
122 while i < N_REPEATS:```
Bucle principal que repite procesamiento completo para promedios estadísticos precisos y consistentes.

```python
123     resultsSeq = sequential(resultsSeq, SEED_1, SEED_2)```
Ejecuta función secuencial con resultados acumulados y ambos seeds fijos para reproducibilidad exacta.

```python
124 if DEBUG:```
Bloque condicional que muestra resultados intermedios solo cuando depuración está activada explícitamente.

```python
125     print("------ RESULTADO ({0}) ----------".format(i))```
Encabezado indicando número de iteración actual del ciclo secuencial completo procesado.

```python
126     print("{0}".format(["{0:2d}".format(n) for n in resultsSeq]))```
Imprime resultados formateados para verificación visual de cada iteración completa procesada.

```python
127     print("-----------------------\n")```
Línea divisoria separadora entre visualizaciones de resultados individuales procesados secuencialmente.

```python
128 ```
Permite rastrear evolución de resultados a través de múltiples repeticiones completas con dependencias.

```python
129 i += 1```
Incrementa contador para próxima iteración completa del ciclo secuencial procesado completamente.

```python
130 end = time.time()```
Registra finalización de todas las repeticiones secuenciales completas con dependencias aplicadas.

```python
131 time_seq = to_time_miliseconds(start, end)```
Convierte diferencia temporal a milisegundos para medición precisa de rendimiento secuencial completo.

```python
132 print("Sequential execution took {0} ms, sum of results is {1}\n".format(time_seq, sum(resultsSeq)))```
Muestra tiempo total secuencial y suma acumulada como verificación adicional de resultados procesados.

```python
133 ```
Establece línea base temporal para comparación directa con ejecución paralela posterior con dependencias.

```python
134 print("Running in parallel with {0} processes".format(NUM_PROCS))```
Indica inicio de fase paralela con número específico de procesos activos simultáneamente procesando.

```python
135 start = time.time()```
Registra timestamp inicial para medir tiempo total de ejecución paralela completa con dependencias.

```python
136 resultsPar = parallel(data, SEED_1, SEED_2)```
Ejecuta función principal con dataset original y ambos seeds idénticos a ejecución secuencial procesada.

```python
137 end = time.time()```
Registra finalización de todas las repeticiones paralelas completas con dependencias aplicadas correctamente.

```python
138 time_par = to_time_miliseconds(start, end)```
Convierte diferencia temporal a milisegundos para medición precisa de rendimiento paralelo completo.

```python
139 print("Parallel execution took {0} ms, sum of results is {1}\n".format(time_par, sum(resultsPar)))```
Muestra tiempo total paralelo y suma acumulada para verificación de consistencia básica procesada.

```python
140 ```
Establece métrica temporal paralela para comparación directa contra línea base secuencial con dependencias.

```python
141 print("Speedup is {0:2f}".format(time_seq/time_par))```
Calcula y muestra speedup como ratio de tiempo secuencial entre paréntesis paralelo procesado.

```python
142 ```
Métrica fundamental para evaluar ganancia de rendimiento obtenida con paralelización de dependencias complejas.

```python
143 valid, message = validate(resultsSeq, resultsPar)```
Aplica función de validación que compara exhaustivamente ambos conjuntos de resultados procesados.

```python
144 if not valid:```
Bloque condicional que se activa cuando validación detecta discrepancias entre resultados procesados.

```python
145     print("Results ARE NOT equal")```
Alerta inmediata indicando que resultados no coinciden exactamente entre ambas ejecuciones procesadas.

```python
146     print(message)```
Muestra mensaje descriptivo específico de la discrepancia detectada por validación de dependencias.

```python
147 else:```
Rama alternativa cuando validación confirma consistencia total entre resultados procesados correctamente.

```python
148     print("Results ARE equal\n\n")```
Confirmación positiva indicando que ambas ejecuciones produjeron resultados idénticos con dependencias aplicadas.

```python
149 ```
Validación crítica asegura corrección del algoritmo de dependencias antes de confiar en métricas de rendimiento.

```python
150 ```
Fin de `experiment()` - compara exhaustivamente ejecución secuencial contra paralela con validación completa de dependencias.

```python
151 if __name__ == '__main__':```
Bloque principal que solo se ejecuta cuando el script es llamado directamente (no importado como módulo).

```python
149     N_MIN, N_MAX = 1e1, 5e1```
Configuración de validación: dataset pequeño para pruebas rápidas y verificación inmediata de dependencias.

```python
150     N_REPEATS = 2```
Solo 2 repeticiones suficientes para validar corrección del algoritmo de dependencias rápidamente.

```python
151     NUM_PROCS = 4```
Usa 4 procesos paralelos para demostrar funcionamiento básico de la implementación con dependencias.

```python
152     DEBUG = True```
Depuración activada para visualización detallada durante pruebas de validación de dependencias complejas.

```python
153 print("####### VALIDATION EXPERIMENT")```
Encabezado indicando que esta primera ejecución es para validar corrección del algoritmo de dependencias.

```python
154     experiment()```
Ejecuta experimento completo con configuración mínima para verificación rápida de funcionalidad de dependencias.

```python
155 ```
Prueba inicial confirma que implementación básica de dependencias funciona correctamente antes de pruebas de rendimiento.

```python
156     N_MIN, N_MAX = 1e1, 5e6```
Configuración de rendimiento: dataset masivo para medición precisa de escalabilidad y velocidad con dependencias.

```python
157     N_REPEATS = 400```
Muchas repeticiones necesarias para promedios estadísticos significativos con dataset grande y dependencias complejas.

```python
158     NUM_PROCS = 8```
Usa 8 procesos para aprovechar hardware disponible y demostrar escalabilidad real de dependencias paralelas.

```python
159     DEBUG = False```
Depuración desactivada para evitar saturación de salida durante pruebas de rendimiento intensivas con dependencias.

```python
160 print("####### PERFORMANCE EXPERIMENT")```
Encabezado indicando que esta segunda ejecución es para medir rendimiento real con dataset grande y dependencias.

```python
161     experiment()```
Ejecuta experimento completo con configuración optimizada para medición precisa de velocidad y speedup con dependencias.

```python
162 ```
Prueba final evalúa comportamiento con carga real y dataset masivo para métricas significativas de dependencias paralelas.

```python
163 ```
Fin del script - ejecuta dos fases: validación rápida seguida de prueba de rendimiento exhaustiva con dependencias complejas.
