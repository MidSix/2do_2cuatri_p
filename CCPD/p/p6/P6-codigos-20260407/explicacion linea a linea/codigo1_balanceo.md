# Documentación Detallada - Examen P6

## Módulo 1: codigo1_balanceo.py

```python
1 #! /usr/bin/python```
Interprete shebang que indica Python como ejecutor del script. Permite ejecución directa desde terminal.

```python
2 #```
Comentario de inicio del bloque de copyright y licencia.

```python
3 # Copyright © 2025 by Jonatan Enes (jonatan.enes@udc.es)```
Atribución de autoría con contacto del autor.

```python
4 # Computer Engineering department, Universidade da Coruña, Spain.```
Identificación institucional del autor y origen académico.

```python
5 #```
Continuación del bloque de copyright/licencia.

```python
6 # This file is part of several courses on parallel processing from Universidade da Coruña,```
Declaración de pertenencia a cursos académicos de procesamiento paralelo.

```python
7 # and it can only be used and/or modified by the author, the students or any ```
Restricciones de uso: solo autor, estudiantes o personas autorizadas pueden modificarlo.

```python
8 # explicitly authorized person by the author, inside the context of the subject. ```
Autorización limitada al contexto académico del curso.

```python
9 # Redistribution to a third-party without previous authorization is strictly forbidden.```
Prohibición estricta de redistribución sin autorización previa.

```python
10 # No commercial use is allowed.```
Uso exclusivamente no comercial permitido.

```python
11 #```
Continuación del bloque de restricciones de uso.

```python
12 # This file has only academic purposes and should not be used for any real-world```
Declaración de propósito académico exclusivo, sin garantía para uso real.

```python
13 # scenario, the author holds no accountability for its use or misuse.```
Descargo de responsabilidad sobre posibles usos inadecuados del código.

```python
14 ```
Fin del bloque de copyright y licencia.

```python
15 import random```
Importa módulo `random` para generación de números aleatorios (no usado en este archivo).

```python
16 import time```
Importa módulo `time` para medición de tiempos de ejecución de funciones.

```python
17 from concurrent.futures.process import ProcessPoolExecutor```
Importa `ProcessPoolExecutor` para ejecutar tareas en múltiples procesos CPU simultáneamente.

```python
18 from auxiliar import get_chunks, to_time_miliseconds, sci_not_str, flatten_list_of_lists, validate```
Importa funciones utilitarias del módulo auxiliar: división de datos, conversión de tiempo, notación científica, aplanado y validación.

```python
19 ```
Fin de las importaciones externas.

```python
20 import pandas as pd```
Importa librería `pandas` para manipulación y visualización de datos en tablas formateadas.

```python
21 from tqdm import tqdm```
Importa módulo `tqdm` para barras de progreso visuales durante la ejecución del experimento.

```python
22 pd.set_option('display.max_rows', 40)```
Configura pandas para mostrar máximo 40 filas en DataFrames sin truncar visualmente.

```python
23 pd.set_option('display.max_columns', 500)```
Permite visualizar hasta 500 columnas en tablas de resultados.

```python
24 pd.set_option('display.width', 1000)```
Establece ancho máximo de visualización de 1000 caracteres para mejor legibilidad.

```python
25 ```
Fin de configuración de visualización de pandas.

```python
26 FUNCS = list()```
Inicializa lista vacía `FUNCS` que almacenará referencias a funciones a probar en experimentos.

```python
27 ```
Espacio reservado entre definiciones.

```python
28 N_REPEATS = 2e1```
Define número de repeticiones (20) para pruebas estadísticas y promedios de rendimiento.

```python
29 ```
Fin de variables globales de configuración.

```python
30 def is_prime(num):```
Función que determina si un número es primo mediante división por todos los números menores.

```python
31     flag = False```
Inicializa bandera `flag` en falso para detectar divisores del número.

```python
32     if num > 1:```
Condición necesaria: números primos son mayores que 1.

```python
33         for i in range(2, num):```
Itera desde 2 hasta num-1 buscando divisores del número.

```python
34             if (num % i) == 0:```
Verifica si `i` divide exactamente a `num`, indicando no es primo.

```python
35                 flag = True```
Marca bandera como verdadero al encontrar primer divisor.

```python
36                 break```
Interrumpe búsqueda de divisores al confirmar que no es primo.

```python
37 ```
Fin del bloque condicional para verificar primos.

```python
38 if flag:```
Si `flag` es verdadero, el número tiene divisor y no es primo.

```python
39     return False```
Retorna `False` indicando que el número no es primo.

```python
40 else:```
Rama alternativa cuando `flag` permanece falso (sin divisores encontrados).

```python
41     return True```
Retorna `True` confirmando que el número es primo.

```python
42 ```
Fin de función `is_prime()` - algoritmo O(n) simple para detección de primalidad.

```python
43 def fun_cheap(items):```
Función computacionalmente ligera: invierte dígitos y suma repetidamente N veces.

```python
44     start = time.time()```
Registra timestamp inicial para medir tiempo de ejecución de la función.

```python
45     results = list()```
Inicializa lista vacía para almacenar resultados individuales de cada elemento procesado.

```python
46     for item in items:```
Itera sobre cada número del conjunto de datos de entrada.

```python
47         i = 0```
Contador interno que controla las N repeticiones del proceso de inversión.

```python
48         result = 0```
Acumula el resultado parcial de la operación modular en cada iteración.

```python
49         while i < N_REPEATS:```
Bucle principal que repite el procesamiento N veces (20) para mayor carga computacional.

```python
50             revs_number = 0```
Inicializa acumulador para construir número invertido desde cero.

```python
51             num = item```
Copia temporal del valor original para manipular sin afectar el dato base.

```python
52             while num > 0:```
Extrae dígitos uno por uno hasta agotar todos los números.

```python
53                 remainder = num % 10```
Obtiene dígito menos significativo mediante operación módulo 10.

```python
54                 revs_number = (revs_number * 10) + remainder```
Construye número invertido desplazando dígitos y sumando nuevo dígito.

```python
55                 num = num // 10```
Elimina último dígito mediante división entera para siguiente iteración.

```python
56 ```
Fin del bucle de extracción de dígitos - número completamente invertido.

```python
57 i += 1```
Incrementa contador de repeticiones para próxima vuelta del proceso completo.

```python
58 result = (result + revs_number) % 7```
Acumula suma de números invertidos módulo 7, creando patrón cíclico.

```python
59 ```
Fin de las N repeticiones del procesamiento interno.

```python
60 results.append(result)```
Guarda resultado final de este elemento en la lista de resultados.

```python
61 end = time.time()```
Registra timestamp final para calcular tiempo total de ejecución.

```python
62 return results, to_time_miliseconds(start, end)```
Retorna lista de resultados y tiempo transcurrido convertido a milisegundos.

```python
63 ```
Fin de `fun_cheap()` - operación rápida con patrón modular predecible.

```python
64 def fun_medium(items):```
Función de complejidad media: filtra números primos del conjunto.

```python
65     start = time.time()```
Inicia cronómetro para medir rendimiento de la función.

```python
66     results = list()```
Prepara contenedor vacío para almacenar solo los números primos encontrados.

```python
67     for num in items:```
Recorre cada número del conjunto de datos de entrada.

```python
68     if is_prime(num):```
Aplica función `is_prime()` para verificar primalidad del número actual.

```python
69         results.append(num)```
Agrega al resultado solo si cumple condición de ser primo.

```python
70 ```
Fin del filtro por primalidad - O(n) con llamada a is_prime().

```python
71 end = time.time()```
Finaliza medición de tiempo para esta función específica.

```python
72 return results, to_time_miliseconds(start, end)```
Devuelve lista filtrada y tiempo de ejecución en milisegundos.

```python
73 ```
Fin de `fun_medium()` - operación de filtrado con verificación matemática.

```python
74 def fun_expensive(items):```
Función computacionalmente costosa: combina primalidad con inversión numérica.

```python
75     start = time.time()```
Registra inicio temporal para medición precisa del rendimiento.

```python
76     results = list()```
Inicializa colección vacía para resultados de números que cumplen múltiples condiciones.

```python
77     for item in items:```
Procesa cada número individualmente con operaciones intensivas.

```python
78     if is_prime(item):```
Primera condición: el número original debe ser primo.

```python
79         revs_number = 0```
Prepara acumulador para inversión numérica del valor primario.

```python
80         num = item```
Copia del valor para manipulación sin alterar referencia original.

```python
81     while num > 0:```
Descompone número en dígitos individuales mediante módulo y división entera.

```python
82         remainder = num % 10```
Extrae último dígito para reordenamiento posterior.

```python
83         revs_number = (revs_number * 10) + remainder```
Reconstruye número con dígitos en orden inverso.

```python
84         num = num // 10```
Elimina dígito procesado para siguiente iteración de extracción.

```python
85 ```
Número completamente invertido listo para comparación y verificación adicional.

```python
86 if item == revs_number:```
Verifica si el número es palíndromo numérico (igual a su inversión).

```python
87     results.append(item)```
Agrega al resultado números que son primos y palíndromos simultáneamente.

```python
88 if is_prime(revs_number):```
Verifica si el número invertido también es primo (primo reversible).

```python
89     results.append(revs_number)```
Agrega la inversión si cumple condición de primalidad adicional.

```python
90 ```
Ambas condiciones pueden agregar hasta dos valores al resultado final.

```python
91 end = time.time()```
Finaliza medición temporal para esta función intensiva.

```python
92 return results, to_time_miliseconds(start, end)```
Retorna lista de resultados y tiempo computacional en milisegundos.

```python
93 ```
Fin de `fun_expensive()` - operación más pesada con múltiples verificaciones.

```python
94 def fun_par_unordered(data, proc_chunks, resultsPar):```
Función paralela sin orden garantizado: procesa chunks en cualquier secuencia.

```python
95     with ProcessPoolExecutor(max_workers=N_PROC) as executor:```
Crea ejecutor de procesos con N_PROC trabajadores para ejecución concurrente.

```python
96         total_runtime = 0```
Acumula tiempo total de ejecución de todas las funciones procesadas.

```python
97         start = time.time()```
Registra inicio temporal del procesamiento paralelo completo.

```python
98         futures = list()```
Contenedor para objetos Future que representan tareas pendientes de completar.

```python
99     for ini, end in proc_chunks:```
Itera sobre cada división de datos precalculada en chunks.

```python
100         for fun in FUNCS:```
Para cada chunk, ejecuta todas las funciones definidas en FUNCS.

```python
101             futures.append((fun.__name__, executor.submit(fun, data[ini:end])))```
Envía cada función con su chunk correspondiente al pool de procesos.

```python
102 ```
Todas las tareas se envían simultáneamente sin orden de procesamiento garantizado.

```python
103 for fun_name, f in futures:```
Recorre resultados completados en cualquier orden de llegada.

```python
104     result, runtime = f.result()```
Obtiene resultado y tiempo individual de cada tarea terminada.

```python
105     resultsPar[fun_name].append(result)```
Agrega resultados a diccionario por nombre de función correspondiente.

```python
106     total_runtime += runtime```
Suma tiempos individuales para cálculo posterior de eficiencia.

```python
107 ```
Procesamiento termina cuando todas las tareas están completas.

```python
108 end = time.time()```
Registra finalización del procesamiento paralelo completo.

```python
109 time_granted = N_PROC * to_time_miliseconds(start, end)```
Calcula tiempo teórico ideal si todos los procesos trabajaran sin sobrecarga.

```python
110 time_efficiency = "{0} %".format(int(100 * (total_runtime / time_granted)))```
Calcula eficiencia: mayor que 100% indica sobrecarga de comunicación.

```python
111 return resultsPar, time_efficiency```
Retorna diccionario de resultados y porcentaje de eficiencia calculada.

```python
112 ```
Fin de `fun_par_unordered()` - paralelización sin sincronización estricta.

```python
113 def chk_par_unordered(data, proc_chunks, resultsPar):```
Función de comprobación paralela sin orden: estructura similar a fun_par_unordered.

```python
114     with ProcessPoolExecutor(max_workers=N_PROC) as executor:```
Inicializa pool de procesos con N_PROC trabajadores disponibles.

```python
115         total_runtime = 0```
Acumulador para tiempo total de ejecución de todas las funciones.

```python
116         start = time.time()```
Marca inicio temporal del proceso de comprobación paralelo.

```python
117     for fun in FUNCS:```
Itera sobre cada función definida para procesamiento en chunks.

```python
118         for ini, end in proc_chunks:```
Para cada función, divide datos en chunks y envía a procesos paralelos.

```python
119             futures.append((fun.__name__, executor.submit(fun, data[ini:end])))```
Submite cada combinación función-chunk al pool de ejecución.

```python
120 ```
Orden de envío diferente: todas funciones primero, luego todos chunks.

```python
121 for fun_name, f in futures:```
Recoge resultados completados independientemente del orden de llegada.

```python
122     result, runtime = f.result()```
Extrae resultado y tiempo individual de cada tarea finalizada.

```python
123     resultsPar[fun_name].append(result)```
Organiza resultados en diccionario agrupado por nombre de función.

```python
124     total_runtime += runtime```
Acumula tiempos para cálculo posterior de eficiencia del sistema.

```python
125 ```
Termina cuando todas las tareas asignadas están completamente procesadas.

```python
126 end = time.time()```
Registra finalización completa del procesamiento paralelo.

```python
127 time_granted = N_PROC * to_time_miliseconds(start, end)```
Calcula tiempo ideal teórico sin considerar sobrecarga de comunicación.

```python
128 time_efficiency = "{0} %".format(int(100 * (total_runtime / time_granted)))```
Convierte relación tiempos a porcentaje para evaluar eficiencia real.

```python
129 return resultsPar, time_efficiency```
Devuelve resultados organizados y métrica de rendimiento obtenida.

```python
130 ```
Fin de `chk_par_unordered()` - variante de comprobación sin orden estricto.

```python
131 def fun_par_ordered(data, proc_chunks, resultsPar):```
Función paralela con orden garantizado: procesa chunks secuencialmente.

```python
132     with ProcessPoolExecutor(max_workers=N_PROC) as executor:```
Crea ejecutor de procesos para ejecución concurrente controlada.

```python
133         total_runtime = 0```
Inicializa acumulador para tiempo total de todas las funciones procesadas.

```python
134         start = time.time()```
Registra timestamp inicial del procesamiento ordenado completo.

```python
135     for ini, end in proc_chunks:```
Procesa cada chunk en secuencia estricta para reproducibilidad.

```python
136         futures = list()```
Inicializa lista de tareas pendientes dentro de cada chunk procesado.

```python
137         for fun in FUNCS:```
Para cada chunk, envía todas las funciones al pool de ejecución.

```python
138             futures.append((fun.__name__, executor.submit(fun, data[ini:end])))```
Submite cada función con su porción correspondiente del dataset.

```python
139 ```
Todas las tareas de un chunk se envían antes de pasar al siguiente.

```python
140 for fun_name, f in futures:```
Recoge resultados completados dentro del mismo chunk procesado.

```python
141     result, runtime = f.result()```
Obtiene resultado y tiempo individual de cada tarea terminada.

```python
142     resultsPar[fun_name].append(result)```
Agrega resultados al diccionario organizado por nombre de función.

```python
143     total_runtime += runtime```
Suma tiempos para cálculo posterior de eficiencia del sistema.

```python
144 ```
Completa todas las funciones antes de avanzar al siguiente chunk.

```python
145 end = time.time()```
Registra finalización del procesamiento ordenado completo.

```python
146 time_granted = N_PROC * to_time_miliseconds(start, end)```
Calcula tiempo teórico ideal sin sobrecarga de comunicación entre procesos.

```python
147 time_efficiency = "{0} %".format(int(100 * (total_runtime / time_granted)))```
Convierte relación tiempos a porcentaje para evaluar eficiencia real.

```python
148 return resultsPar, time_efficiency```
Retorna diccionario de resultados y métrica de rendimiento calculada.

```python
149 ```
Fin de `fun_par_ordered()` - paralelización con secuencia estricta garantizada.

```python
150 def chk_par_ordered(data, proc_chunks, resultsPar):```
Función de comprobación paralela ordenada: estructura similar a fun_par_ordered.

```python
151     with ProcessPoolExecutor(max_workers=N_PROC) as executor:```
Crea pool de procesos para ejecución concurrente controlada.

```python
152         total_runtime = 0```
Inicializa acumulador para tiempo total de todas las funciones procesadas.

```python
153         start = time.time()```
Registra inicio temporal del proceso de comprobación ordenado.

```python
154     for fun in FUNCS:```
Itera sobre cada función definida para procesamiento en chunks.

```python
155         futures = list()```
Prepara lista de tareas pendientes dentro de cada chunk procesado.

```python
156         for ini, end in proc_chunks:```
Para cada función, divide datos en chunks y envía secuencialmente.

```python
157             futures.append((fun.__name__, executor.submit(fun, data[ini:end])))```
Submite cada combinación función-chunk al pool de ejecución.

```python
158 ```
Orden inverso: todas funciones primero, luego todos chunks secuencialmente.

```python
159 for fun_name, f in futures:```
Recoge resultados completados independientemente del orden de llegada.

```python
160     result, runtime = f.result()```
Extrae resultado y tiempo individual de cada tarea finalizada.

```python
161     resultsPar[fun_name].append(result)```
Organiza resultados en diccionario agrupado por nombre de función.

```python
162     total_runtime += runtime```
Acumula tiempos para cálculo posterior de eficiencia del sistema.

```python
163 ```
Termina cuando todas las tareas asignadas están completamente procesadas.

```python
164 end = time.time()```
Registra finalización completa del procesamiento paralelo ordenado.

```python
165 time_granted = N_PROC * to_time_miliseconds(start, end)```
Calcula tiempo ideal teórico si todos los procesos trabajaran sin sobrecarga.

```python
166 time_efficiency = "{0} %".format(int(100 * (total_runtime / time_granted)))```
Convierte relación tiempos a porcentaje para evaluar eficiencia real.

```python
167 return resultsPar, time_efficiency```
Devuelve resultados organizados y métrica de rendimiento obtenida.

```python
168 ```
Fin de `chk_par_ordered()` - variante de comprobación con orden estricto.

```python
169 def parallel_processing(data, parallel_funct):```
Función orquestadora: delega a función específica y normaliza resultados.

```python
170     resultsPar = dict()```
Inicializa diccionario vacío para almacenar resultados por nombre de función.

```python
171     for fun in FUNCS:```
Prepara estructura inicial con lista vacía para cada función definida.

```python
172         resultsPar[fun.__name__] = list()```
Asegura que cada función tenga su contenedor de resultados listo.

```python
173 ```
Estructura base preparada antes de llamar a la función paralela específica.

```python
174     proc_chunks = get_chunks(len(data), NUM_CHUNKS)```
Divide dataset en chunks equitativos según número de procesos definido.

```python
175 ```
Prepara división de datos para distribución entre procesos paralelos.

```python
176     resultsPar, time_efficiency = parallel_funct(data, proc_chunks, resultsPar)```
Ejecuta función específica (ordenada/desordenada) con datos y chunks preparados.

```python
177 ```
Delega procesamiento a implementación específica de paralelización deseada.

```python
178     for k in resultsPar:```
Itera sobre cada función procesada para normalizar resultados finales.

```python
179         resultsPar[k] = flatten_list_of_lists(resultsPar[k])```
Aplana listas anidadas resultantes de múltiples chunks concatenados.

```python
180         resultsPar[k].sort()```
Ordena resultados para garantizar consistencia entre ejecuciones secuenciales y paralelas.

```python
181 ```
Normalización asegura comparabilidad exacta con ejecución secuencial.

```python
182 return resultsPar, time_efficiency```
Retorna diccionario normalizado de resultados y métrica de eficiencia.

```python
183 ```
Fin de `parallel_processing()` - orquestador central que unifica diferentes estrategias.

```python
184 def save_config():```
Función auxiliar: captura configuración actual del sistema para reproducibilidad.

```python
185     d = dict()```
Inicializa diccionario vacío para almacenar parámetros de configuración actuales.

```python
186     d["N_FUNCS"] = len(FUNCS)```
Guarda número total de funciones definidas en el experimento actual.

```python
187     d["N_CHUNKS"] = NUM_CHUNKS```
Registra número de chunks para división del dataset en esta ejecución.

```python
188     d["N_PROC"] = N_PROC```
Almacena número de repeticiones configurado para pruebas estadísticas.

```python
189     return d```
Retorna diccionario con snapshot completo de configuración actual.

```python
190 ```
Fin de `save_config()` - útil para guardar estado entre diferentes combinaciones.

```python
191 def get_data_ranged(min, max):```
Generador simple: crea lista de números enteros en rango especificado.

```python
192     return [x for x in range(int(min), int(max))]```
Comprehension que genera secuencia completa desde min hasta max-1 inclusive.

```python
193 ```
Fin de `get_data_ranged()` - utilidad básica para creación de datasets numéricos.

```python
194 def pretty_print_df(df, split_strings):```
Formateador visual: inserta separadores entre secciones del DataFrame.

```python
195     df_string = df.to_string()```
Convierte DataFrame a representación string para manipulación posterior.

```python
196     num_dashes = 102```
Define longitud de línea de separador visual (102 caracteres).

```python
197     for split in split_strings:```
Itera sobre cada marcador de sección definido para insertar separadores.

```python
198         df_string = df_string.replace("\n{0}".format(split), '\n' + '-' * num_dashes + "\n{0}".format(split))```
Inserta línea de guiones antes y después de cada marcador de sección.

```python
199 ```
Mejora legibilidad visual de tablas grandes en salida terminal.

```python
200 return df_string```
Retorna string formateado con separadores visuales insertados.

```python
201 ```
Fin de `pretty_print_df()` - mejora presentación de resultados tabulares.

```python
202 ALL_FUNCS = [fun_cheap, fun_medium, fun_expensive]```
Define lista completa de funciones para experimentos con diferentes complejidades.

```python
203 ALL_EXPENSIVE_FUNCS = [fun_expensive, fun_expensive, fun_expensive, fun_expensive]```
Crea lista con múltiples instancias de la función más costosa para mayor carga.

```python
204 ```
Permite comparar rendimiento entre conjuntos balanceados y sesgados hacia operaciones intensivas.

```python
205 def experiment():```
Función principal: ejecuta todos los experimentos con configuración actual.

```python
206     global NUM_CHUNKS, N_PROC, FUNCS```
Accede a variables globales para modificar configuración durante ejecución.

```python
207     print("RUNNING EXPERIMENTS WITH {0} FUNCTIONS: {1}".format(len(FUNCS), [f.__name__ for f in FUNCS]))```
Muestra información inicial sobre funciones que serán probadas en experimentos.

```python
208 ```
Información de diagnóstico para verificar configuración antes de comenzar pruebas.

```python
209     data = get_data_ranged(int(N_BASE), int(N_BASE) + N_LEN)```
Genera dataset completo desde N_BASE hasta N_BASE+N_LEN según parámetros globales.

```python
210 ```
Crea el conjunto de datos base que será procesado en todas las pruebas.

```python
211 print("####### N = {0} (from {1} to {2}) #######\n".format(int(N_LEN), int(N_BASE), int(N_BASE + N_LEN)))```
Muestra tamaño del dataset con rango completo para referencia durante ejecución.

```python
212 ```
Salida de diagnóstico sobre dimensiones del dataset actual.

```python
213 print("Running sequentially")```
Indica inicio de fase secuencial como línea base de comparación.

```python
214     resultsSeq = dict()```
Inicializa diccionario vacío para almacenar resultados de ejecución secuencial.

```python
215     sstart = time.time()```
Registra timestamp inicial para medir tiempo total de ejecución secuencial.

```python
216     for fun in FUNCS:```
Itera sobre cada función definida para medición de rendimiento individual.

```python
217         if fun.__name__ not in resultsSeq:```
Verifica si ya existe entrada para esta función en el diccionario de resultados.

```python
218             resultsSeq[fun.__name__] = list()```
Crea lista vacía inicial para almacenar múltiples llamadas a la misma función.

```python
219         result, runtime = fun(data)```
Ejecuta función con dataset completo y captura resultados más tiempo de ejecución.

```python
220         resultsSeq[fun.__name__].append(result)```
Agrega resultado individual a la lista correspondiente por nombre de función.

```python
221         print("Function {0} finished after {1} ms".format(fun.__name__, runtime))```
Muestra tiempo de ejecución individual para cada función procesada secuencialmente.

```python
222 ```
Medición línea por línea establece baseline para comparación con paralelización.

```python
223 for k in resultsSeq:```
Itera sobre todas las funciones procesadas secuencialmente.

```python
224     resultsSeq[k] = flatten_list_of_lists(resultsSeq[k])```
Aplana listas anidadas resultantes de múltiples repeticiones por función.

```python
225     resultsSeq[k].sort()```
Ordena resultados para garantizar consistencia en comparación con ejecución paralela.

```python
226 ```
Normalización asegura comparabilidad exacta entre ejecuciones secuenciales y paralelas.

```python
227 eend = time.time()```
Registra finalización de toda la fase secuencial completa.

```python
228 print("SEQ execution took {0} ms".format(to_time_miliseconds(sstart, eend)))```
Muestra tiempo total acumulado de ejecución completamente secuencial.

```python
229 print("-" * 40)```
Separador visual entre fases del experimento para mejor legibilidad.

```python
230 print("\n")```
Salto de línea adicional para espaciado en salida terminal.

```python
231 print("Running parallel arrangements")```
Indica inicio de fase paralela con diferentes configuraciones de chunks y procesos.

```python
232     all_measurements = list()```
Contenedor principal para tiempos de todas las combinaciones de configuración probadas.

```python
233     all_efficiencies = list()```
Almacena métricas de eficiencia calculadas para cada combinación de parámetros.

```python
234     with tqdm(total=len(NUM_CHUNKS_OPTS) * len(N_PROC_OPTS) * 4) as pbar:```
Inicializa barra de progreso que muestra avance durante múltiples combinaciones de prueba.

```python
235         for NUM_CHUNKS in NUM_CHUNKS_OPTS:```
Itera sobre cada opción de número de chunks definida para división del dataset.

```python
236             for N_PROC in N_PROC_OPTS:```
Para cada configuración de chunks, prueba diferentes números de procesos paralelos.

```python
237                 times = save_config()```
Guarda snapshot de configuración actual antes de ejecutar combinaciones específicas.

```python
238                 times_efficiency = save_config()```
Copia adicional para almacenar métricas de eficiencia por separado.

```python
239                 for par_fun in [chk_par_ordered, fun_par_ordered, chk_par_unordered, fun_par_unordered]:```
Ejecuta las cuatro variantes de procesamiento paralelo con diferentes estrategias.

```python
240                     start = time.time()```
Registra inicio temporal para medir tiempo específico de cada estrategia paralela.

```python
241                     resultsPar, t_efficiency = parallel_processing(data, par_fun)```
Ejecuta función orquestadora con estrategia específica y captura resultados más eficiencia.

```python
242                     for k in resultsSeq:```
Verifica consistencia comparando resultados paralelos contra baseline secuencial.

```python
243                         if not validate(resultsSeq[k], resultsPar[k]):```
Aplica función de validación para detectar discrepancias entre ejecuciones.

```python
244                             print("!!!! RESULTS NOT EQUAL for {0} !!!!".format(par_fun.__name__))```
Alerta inmediata si resultados no coinciden exactamente con ejecución secuencial.

```python
245                             break```
Interrumpe verificación actual al detectar inconsistencia en algún resultado.

```python
246 ```
Validación crítica asegura corrección de algoritmo antes de medir rendimiento.

```python
247                     end = time.time()```
Registra finalización del procesamiento paralelo con estrategia específica.

```python
248                     times[par_fun.__name__] = to_time_miliseconds(start, end)```
Guarda tiempo de ejecución en snapshot de configuración para referencia posterior.

```python
249                     times_efficiency[par_fun.__name__] = t_efficiency```
Almacena métrica de eficiencia calculada por estrategia paralela específica.

```python
250                     pbar.update(1)```
Avanza barra de progreso para reflejar avance en combinaciones probadas.

```python
251 ```
Completa todas las estrategias con cada combinación de chunks y procesos.

```python
252 all_measurements.append(times)```
Agrega snapshot completo de tiempos a colección principal de mediciones.

```python
253 all_efficiencies.append(times_efficiency)```
Guarda métricas de eficiencia para análisis posterior de rendimiento relativo.

```python
254 ```
Acumula datos completos para visualización final en tablas formateadas.

```python
255 print("\n")```
Salto de línea adicional antes de mostrar resultados finales organizados.

```python
256 print("~" * 40)```
Encabezado decorativo para tabla de tiempos paralelos con separadores visuales.

```python
257 print("|" + " " * 7 + "Parallel times (ms)" + " " * 12 + "|")```
Encabezado centrado de columna principal mostrando métrica de tiempo en milisegundos.

```python
258 print("~" * 102)```
Línea divisoria completa para separar encabezado del contenido de datos.

```python
259 print(pretty_print_df(pd.DataFrame(all_measurements), [i * len(N_PROC_OPTS) for i in range(0, len(NUM_CHUNKS_OPTS))]))```
Convierte mediciones a DataFrame y aplica formateo visual con separadores entre secciones.

```python
260 print("~" * 102)```
Cierre de línea divisoria para completar estructura tabular decorada.

```python
261 print("\n")```
Espaciado adicional después de tabla de tiempos para separación visual.

```python
262 print("~" * 45)```
Encabezado decorativo para tabla de eficiencia con separadores visuales.

```python
263 print("|" + " " * 5 + "Parallel % of time in execution" + " " * 7 + "|")```
Encabezado centrado de columna mostrando porcentaje de tiempo en ejecución real.

```python
264 print("~" * 102)```
Línea divisoria completa para separar encabezado del contenido de datos.

```python
265 print(pretty_print_df(pd.DataFrame(all_efficiencies), [i * len(N_PROC_OPTS) for i in range(0, len(NUM_CHUNKS_OPTS))]))```
Convierte eficiencias a DataFrame y aplica formateo visual con separadores entre secciones.

```python
266 print("~" * 102)```
Cierre de línea divisoria para completar estructura tabular decorada.

```python
267 print("\n")```
Espaciado final después de todas las visualizaciones de resultados.

```python
268 ```
Fin de `experiment()` - ejecuta exhaustivamente todas combinaciones con validación y métricas.

```python
269 if __name__ == '__main__':```
Bloque principal que solo se ejecuta cuando el script es llamado directamente (no importado).

```python
270     global NUM_CHUNKS, N_PROC```
Accede a variables globales para configuración específica de ejecución.

```python
271 ```
Comienzo del bloque de configuración predeterminada para experimentos.

```python
272     # N_BASE, N_LEN = (1e5, 3000)```
Configuración comentada: dataset grande con muchas repeticiones (no activa por defecto).

```python
273     # NUM_CHUNKS_OPTS = [4, 10, 20, 80]```
Opciones de chunks comentadas para división más granular del dataset.

```python
274     # N_PROC_OPTS = [2, 3, 4, 8, 12, 16]```
Opciones de procesos comentadas para mayor paralelismo en hardware disponible.

```python
275 ```
Configuraciones alternativas disponibles pero desactivadas por defecto.

```python
276     N_BASE, N_LEN = (1e2, 3000)```
Configuración activa: dataset pequeño para pruebas rápidas y desarrollo.

```python
277     NUM_CHUNKS_OPTS = [4, 20]```
Opciones activas de chunks para división del dataset en esta ejecución.

```python
278     N_PROC_OPTS = [2, 3, 4]```
Opciones activas de procesos paralelos según hardware disponible localmente.

```python
279 ```
Configuración balanceada entre velocidad de prueba y cobertura significativa.

```python
280     FUNCS = ALL_FUNCS```
Selecciona conjunto completo de funciones con diferentes niveles de complejidad.

```python
281     experiment()```
Ejecuta primera serie de experimentos con configuración balanceada inicial.

```python
282 ```
Prueba inicial con dataset pequeño y funciones variadas para validación rápida.

```python
283     FUNCS = ALL_EXPENSIVE_FUNCS
```
Cambia a conjunto sesgado hacia operaciones computacionalmente intensivas.

```python
284     experiment()
```
Ejecuta segunda serie de experimentos con funciones más costosas para estrés testing.

```python
285 
```
Prueba adicional evalúa comportamiento bajo carga computacional mayor.

```python
286 
```
Fin del script - ejecuta dos series completas de experimentos con diferentes configuraciones.



