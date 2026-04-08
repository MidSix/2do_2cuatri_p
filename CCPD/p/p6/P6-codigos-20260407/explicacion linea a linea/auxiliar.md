# Documentación Detallada - Examen P6

## Módulo 5: auxiliar.py (Módulo Utilitario)

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
15 def to_time_miliseconds(start, end):```
Función conversora: transforma diferencia temporal a milisegundos para medición precisa de rendimiento.

```python
16     return int(1000 * (end - start))```
Multiplica diferencia en segundos por 1000 y convierte a entero para obtener milisegundos exactos.

```python
17 ```
Fin de `to_time_miliseconds()` - utilidad esencial para métricas de tiempo consistentes entre módulos.

```python
18 def validate(*args):```
Función de validación exhaustiva: compara múltiples conjuntos de datos elemento por elemento.

```python
19     length = len(args[0])```
Obtiene longitud del primer conjunto como referencia para comparación de tamaños consistentes.

```python
20     for res in args[1:]:```
Itera sobre cada conjunto adicional para verificar consistencia de tamaño con el primero.

```python
21         if len(res) != length:```
Detecta discrepancias en longitud que invalidan comparabilidad entre conjuntos de datos.

```python
22             return False, "size mismatch"```
Retorna inmediatamente indicando error de tamaño sin continuar comparación innecesaria.

```python
23         length = len(res)```
Actualiza referencia de longitud cuando todos los tamaños son consistentes entre conjuntos.

```python
24 ```
Primera fase valida que todos los conjuntos tienen exactamente el mismo número de elementos.

```python
25     length = len(args[0])```
Reinicia longitud de referencia para comparar valores individuales elemento por elemento.

```python
26     for i in range(0, length):```
Itera sobre cada índice para comparación exhaustiva de todos los elementos correspondientes.

```python
27         value = args[0][i]```
Obtiene valor de referencia del primer conjunto en posición actual para comparación precisa.

```python
28     for res in args[1:]:```
Para cada elemento, verifica que todos los conjuntos adicionales tengan el mismo valor exacto.

```python
29         if value != res[i]:```
Detecta discrepancias en valores que invalidan equivalencia completa entre resultados.

```python
30             return False, "value mismatch"```
Retorna inmediatamente indicando error de valor sin continuar comparación innecesaria.

```python
31     return True, ""```
Si completa todas las verificaciones sin errores, confirma equivalencia total con mensaje vacío.

```python
32 ```
Validación doble asegura tanto tamaño idéntico como valores exactos en cada posición correspondiente.

```python
33 def get_chunks(n, num_chunks):```
Función de división: calcula y devuelve rangos equitativos para distribución entre procesos paralelos.

```python
34     chunksize = n // num_chunks```
Calcula tamaño base de cada chunk mediante división entera para distribución lo más equitativa posible.

```python
35     proc_chunks = []```
Inicializa lista vacía para almacenar tuplas con rangos de inicio y fin de cada chunk procesado.

```python
36     for i_proc in range(num_chunks):```
Itera sobre cada proceso asignando un rango específico de datos para procesamiento paralelo.

```python
37         chunkstart = i_proc * chunksize```
Calcula índice de inicio del chunk actual multiplicando número de proceso por tamaño base.

```python
38     if i_proc < num_chunks - 1:```
Condición especial para todos los chunks excepto el último que necesita tratamiento diferente.

```python
39         chunkend = (i_proc + 1) * chunksize```
Calcula índice de fin del chunk actual como siguiente inicio para distribución equitativa.

```python
40     else:```
Rama alternativa exclusiva para el último chunk que debe cubrir todo lo restante sin truncamiento.

```python
41         chunkend = n```
Establece fin en longitud total del dataset para incluir todos los elementos restantes correctamente.

```python
42     proc_chunks.append((chunkstart, chunkend))```
Agrega tupla con rango actual a lista de chunks para distribución entre procesos paralelos.

```python
43 ```
El último chunk puede ser ligeramente más grande para garantizar cobertura completa del dataset.

```python
44 return proc_chunks```
Retorna lista completa de rangos para uso en división y procesamiento paralelo distribuido.

```python
45 ```
Fin de `get_chunks()` - esencial para distribución equitativa de carga entre múltiples núcleos procesadores.

```python
46 def flatten_list_of_lists(l):```
Función de aplanado: convierte estructura anidada en lista lineal simple para procesamiento uniforme.

```python
47     # Read this like "for each sublist in l, give sublist, and for each item in sublist, give item"```
Comentario explicativo que describe comportamiento del comprehension anidado de forma intuitiva.

```python
48     return [item for sublist in l for item in sublist]```
Comprehension anidado que extrae cada elemento individual de todas las sublists en orden secuencial.

```python
49 ```
Estructura resultante lista para comparación directa con resultados secuenciales sin anidación.

```python
50 def sci_not_str(num):```
Función de formateo: convierte números a notación científica string para visualización compacta de valores grandes.

```python
51     if type(num) != int:```
Verifica si el número es flotante o decimal para aplicar formato con decimales significativos.

```python
52         return "{:1.2e}".format(num)```
Formatea número flotante con 2 decimales en notación científica con ancho mínimo de 1 carácter.

```python
53     else:```
Rama alternativa exclusiva para números enteros que requieren formato sin decimales innecesarios.

```python
54         return "{:1.0e}".format(num).replace("+0", "")```
Formatea número entero con 0 decimales, elimina signo + redundante del exponente positivo.

```python
55 ```
Elimina el prefijo "+" de exponentes positivos para formato más limpio y consistente visualmente.

```python
56 return resultsPar, time_efficiency```
Retorna diccionario normalizado de resultados y métrica de eficiencia calculada correctamente.

```python
57 ```
Fin de `sci_not_str()` - útil para mostrar tamaños grandes de dataset en formato compacto legible.
