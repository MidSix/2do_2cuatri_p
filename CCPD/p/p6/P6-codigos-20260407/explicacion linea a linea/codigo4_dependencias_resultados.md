# Documentación Detallada - Examen P6

## Módulo 4: codigo4_dependencias_resultados.py

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
16 from auxiliar import get_chunks, to_time_miliseconds, sci_not_str, flatten_list_of_lists, validate```
Importa funciones utilitarias: división de datos, conversión temporal, notación científica, aplanado y validación.

```python
17 import pandas as pd```
Importa librería `pandas` para visualización estructurada de datos en tablas.

```python
18 ```
Fin de todas las importaciones necesarias para el módulo.

```python
19 pd.set_option('display.max_rows', 20)```
Configura pandas para mostrar máximo 20 filas sin truncamiento visual.

```python
20 pd.set_option('display.max_columns', 500)```
Permite visualizar hasta 500 columnas en tablas de resultados extensas.

```python
21 pd.set_option('display.width', 1000)```
Establece ancho máximo de visualización de 1000 caracteres para mejor legibilidad.

```python
22 ```
Fin de configuración de visualización optimizada para datos extensos.

```python
23 DEBUG = True```
Bandera de depuración activada para mostrar información detallada durante ejecución del experimento.

```python
24 ```
Fin de variables globales de configuración del experimento.

```python
25 def fun(res, num):```
Función matemática: multiplica acumulador por número y aplica módulo 100 más constante 7.

```python
26     res = (res * num) % 100 + 7```
Aplica operación modular con desplazamiento de +7 creando patrón cíclico desplazado en secuencia.

```python
27     return res```
Retorna resultado modificado para uso como acumulador en iteración siguiente del procesamiento.

```python
28 ```
Fin de `fun()` - función matemática con desplazamiento constante que altera patrón cíclico.

```python
29 def sequential(data, seed):```
Función secuencial que procesa dataset linealmente con acumulación dependiente del seed inicial.

```python
30     results = list()```
Inicializa lista vacía para almacenar resultados individuales de cada elemento procesado secuencialmente.

```python
31     previous_num = seed```
Establece valor inicial que se propagará a través de todas las iteraciones del procesamiento secuencial.

```python
32     for n in data:```
Itera sobre cada número del dataset en orden secuencial estricto para procesamiento lineal completo.

```python
33         res = fun(previous_num, n)```
Aplica función matemática con acumulador anterior y valor actual del dataset procesado.

```python
34     results.append(res)```
Guarda resultado individual para construcción de secuencia completa final procesada secuencialmente.

```python
35     previous_num = res```
Actualiza acumulador al resultado obtenido en lugar del valor original, creando dependencia acumulativa.

```python
36 ```
Propagación acumulativa asegura que cada elemento dependa del resultado anterior procesado completamente.

```python
37 return results```
Retorna lista completa de resultados con todas las dependencias aplicadas secuencialmente correctamente.

```python
38 ```
Fin de `sequential()` - procesamiento lineal con acumulación dependiente del resultado anterior.

```python
39 def experiment():```
Función principal que ejecuta medición de tiempo de ejecución secuencial completa.

```python
40     data = [x for x in range(int(N_MIN), int(N_MAX))]```
Genera dataset completo de números enteros desde N_MIN hasta N_MAX-1 inclusive para procesamiento.

```python
41 print("-> N = {0} (from {1} to {2})\n".format(int(N_MAX - N_LEN), sci_not_str(int(N_MIN)), int(N_MAX)))```
Muestra tamaño del dataset con rango completo usando notación científica para valores grandes procesados.

```python
42 start = time.time()```
Registra timestamp inicial para medir tiempo total de ejecución secuencial completa.

```python
43 resultsSeq = data```
Inicializa resultados secuenciales con copia del dataset original como base idéntica a paralela.

```python
44 ```
Punto de partida idéntico entre ejecuciones para comparación justa y precisa de rendimiento.

```python
45 print("Running sequentially")```
Indica inicio de fase secuencial que servirá como línea base de referencia para comparación.

```python
46 SEED = 1```
Establece valor inicial del seed idéntico entre ambas ejecuciones para reproducibilidad exacta.

```python
47 if DEBUG:```
Bloque condicional que muestra datos originales solo cuando depuración está activada explícitamente.

```python
48     print("\nxxxxxxxx DATOS xxxxxxxxx")```
Encabezado indicando visualización del dataset completo original antes de procesamiento intensivo.

```python
49     print("{0}".format(["{0:2d}".format(n) for n in data]))```
Imprime todos los datos formateados para verificación visual completa del dataset procesado.

```python
50     print("")```
Salto de línea adicional para espaciado en salida terminal durante visualización de datos.

```python
51 ```
Permite verificar exactitud del dataset antes de procesamiento intensivo con dependencias acumulativas.

```python
52 i = 0```
Contador interno que controla número total de repeticiones del ciclo secuencial completo procesado.

```python
53 while i < N_REPEATS:```
Bucle principal que repite procesamiento completo para promedios estadísticos precisos y consistentes.

```python
54     resultsSeq = sequential(resultsSeq, SEED)```
Ejecuta función secuencial con resultados acumulados y seed fijo para reproducibilidad exacta del procesamiento.

```python
55 if DEBUG:```
Bloque condicional que muestra resultados intermedios solo cuando depuración está activada explícitamente.

```python
56     print("------ RESULTADO ({0}) ----------".format(i))```
Encabezado indicando número de iteración actual del ciclo secuencial completo procesado.

```python
57     print("{0}".format(["{0:2d}".format(n) for n in resultsSeq]))```
Imprime resultados formateados para verificación visual de cada iteración completa procesada.

```python
58     print("-----------------------\n")```
Línea divisoria separadora entre visualizaciones de resultados individuales procesados secuencialmente.

```python
59 ```
Permite rastrear evolución de resultados a través de múltiples repeticiones completas con dependencias acumulativas.

```python
60 i += 1```
Incrementa contador para próxima iteración completa del ciclo secuencial procesado completamente.

```python
61 end = time.time()```
Registra finalización de todas las repeticiones secuenciales completas con dependencias aplicadas.

```python
62 time_seq = to_time_miliseconds(start, end)```
Convierte diferencia temporal a milisegundos para medición precisa de rendimiento secuencial completo.

```python
63 print("Sequential execution took {0} ms, sum of results is {1}\n".format(time_seq, sum(resultsSeq)))```
Muestra tiempo total secuencial y suma acumulada como verificación adicional de resultados procesados.

```python
64 ```
Establece línea base temporal para comparación directa con ejecución paralela posterior con dependencias acumulativas.

```python
65 ```
Fin de `experiment()` - mide tiempo de ejecución secuencial completa con validación y visualización detallada.

```python
66 if __name__ == '__main__':```
Bloque principal que solo se ejecuta cuando el script es llamado directamente (no importado como módulo).

```python
67     N_MIN, N_MAX = 1e1, 5e1```
Configuración de validación: dataset pequeño para pruebas rápidas y verificación inmediata del algoritmo.

```python
68     N_REPEATS = 2```
Solo 2 repeticiones suficientes para validar corrección del algoritmo rápidamente sin sobrecarga.

```python
69     DEBUG = True```
Depuración activada para visualización detallada durante pruebas de validación del procesamiento secuencial.

```python
70 print("####### VALIDATION EXPERIMENT")```
Encabezado indicando que esta primera ejecución es para validar corrección del algoritmo secuencial.

```python
71     experiment()```
Ejecuta experimento completo con configuración mínima para verificación rápida de funcionalidad secuencial.

```python
72 ```
Prueba inicial confirma que implementación básica funciona correctamente antes de pruebas de rendimiento.

```python
73 ```
Fin del script - ejecuta una sola fase de validación con dataset pequeño y pocas repeticiones para verificación rápida.
