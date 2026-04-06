A continuación, te proporciono la teoría completa y los detalles técnicos exhaustivos basados estrictamente en el material proporcionado para que puedas desarrollar la **Práctica 2: Autómatas finitos deterministas acíclicos mínimos numerados**, sin necesidad de consultar fuentes adicionales.

1. Fundamentos teóricos completos

La práctica se basa en el uso de **Autómatas Finitos Deterministas Acíclicos Mínimos (ADFA)** para implementar un mecanismo de _hashing_ perfecto, estableciendo una relación biunívoca entre las palabras de un diccionario y un valor numérico (índice).

- **Autómata Finito Determinista (AFD):** Se define mediante la 5-tupla A=(Q,Σ,δ,q0​,F), donde:
    - Q: Conjunto finito de estados (vértices del grafo).
    - Σ: Alfabeto de símbolos (etiquetas de transiciones).
    - δ: Función de transición δ:Q×Σ→Q. La notación q.a equivale a δ(q,a).
    - q0​: Estado inicial.
    - F: Subconjunto de estados finales (se representan con círculos dobles).
- **Lenguaje reconocido** L(A)**:** Conjunto de palabras w para las cuales al aplicar transiciones sucesivas q0​.w se alcanza un estado perteneciente a F.
- **Acíclico y Mínimo:** El grafo del autómata no contiene ciclos (conjunto finito de palabras) y no existe otro autómata con menos estados o transiciones que reconozca el mismo lenguaje.
- **Numeración (Pesos de Indexación):** Para lograr el _hashing_, se asigna un **peso numérico** a cada estado. Este peso representa el cardinal del "lenguaje derecho" de dicho estado, es decir, **el número de palabras o subpalabras que se pueden formar leyendo desde ese estado hasta cualquier estado final** siguiendo transiciones válidas.

2. Métodos y algoritmos

Para el cálculo del _hashing_ directo (palabra a índice) e inverso (índice a palabra), se emplean dos algoritmos detallados a continuación:

**Algoritmo A:** **Palabra_a_Indice** **(Hashing directo)** Este método transforma una palabra en un índice numérico único sumando los pesos de las ramas descartadas lexicográficamente antes de tomar una transición válida.

1. Se inicializa `Indice = 1` y `Estado_Actual = Estado_Inicial`.
2. Para cada letra `Palabra[i]` en la palabra:
    - Si la transición es válida, se recorren los caracteres `c` desde la primera letra del alfabeto hasta el predecesor de `Palabra[i]`.
    - Por cada transición válida con `c` desde el `Estado_Actual`, se suma a `Indice` el valor de `Estado_Actual[c].Número` (el peso del estado destino).
    - Se avanza el estado: `Estado_Actual = Estado_Actual[Palabra[i]]`.
    - Si la transición no es válida en algún punto, se retorna **"palabra desconocida"**.
3. Al terminar la palabra, si `Estado_Actual` es final, se devuelve el `Indice`. Si no, se retorna "palabra desconocida".

**Algoritmo B:** **Indice_a_Palabra** **(Hashing inverso)**

1. Se inicializa `Estado_Actual = Estado_Inicial`, `Número = Indice`, `Palabra = Palabra_Vacía`, y un contador `i = 1`.
2. Se repite el siguiente bloque hasta que `Número == 0`:
    - Se iteran los caracteres `c` posibles en orden alfabético.
    - Si hay transición válida para `c`, sea `Estado_Auxiliar = Estado_Actual[c]`.
    - Si `Número > Estado_Auxiliar.Número`, se restan esos caminos descartados: `Número = Número - Estado_Auxiliar.Número`.
    - Si no (el índice pertenece a esta rama), se concatena `c` a la `Palabra`, se avanza `Estado_Actual = Estado_Auxiliar`. Si el nuevo estado es final, se decremente el número: `Número = Número - 1`. Se rompe el bucle de caracteres y se vuelve a iterar el bloque general.
3. Retorna la `Palabra` formada.

4. Fórmulas y ecuaciones

Las fórmulas subyacentes se aplican lógicamente en los algoritmos anteriores:

- **Peso del Estado Inicial (**q0​**):** Peso(q0​)=∣L(A)∣, es decir, el número total de palabras en el diccionario.
- **Cálculo del Índice:** Dado w=w1​w2​...wn​: Indice(w)=1+∑i=1n​∑c<wi​​Peso(δ(qi−1​,c)) donde qi−1​ es el estado alcanzado al leer el prefijo hasta wi−1​.
- El **carácter de fin de palabra** **\0** se utiliza implícitamente tras la última letra de la palabra. Esto garantiza que todos los autómatas tengan **un único estado final**, simplificando las implementaciones (caso base del peso = 1).

4. Procedimientos detallados

A. Preparación inicial

Trabajarás con diccionarios de prueba ya compilados que carecen de los pesos precalculados: `tiny.bin`, `small.bin`, `medium.bin` y `large.bin`. La estructura física (binaria) en la que se leen los datos consiste en un vector dividido en **celdas de 4 bytes**:

1. La primera celda almacena el número total de celdas del vector.
2. Tras esto vienen los estados. **La representación de un estado en el vector** incluye:
    - **1 celda inicial:** 1 byte para el número de transiciones que salen de él, y 3 bytes para su peso de indexación (inicialmente en cero).
    - **Celdas subsecuentes:** 1 celda por cada transición. Contienen 1 byte para el carácter de la transición y 3 bytes para la celda destino.
3. Conveniencias técnicas cruciales:
    - El estado final está en la primera posición de los estados (celda "0") y ocupa solo 1 celda (no tiene transiciones).
    - El **estado inicial** está siempre inmediatamente después del final (en la posición de 2 x 4 bytes tras el inicio).

B. Pasos intermedios y C. Criterios de validación

**Parte 1: Asignar Pesos (****siw.py****)**

- **Procedimiento:** Crear el programa `siw.py` (State Indexing Weights). Debe abrir un archivo `.bin` sin pesos, recorrer recursivamente el autómata calculando el peso de cada estado, y volcar el autómata modificado a un archivo de salida (`tinyw.bin`, etc.).
- **Validación (Caso Base):** El estado final (único, de la celda 0) tiene peso 1. El peso de cualquier otro estado es la suma de los pesos de los estados destino de todas sus transiciones.

**Parte 2: Diccionario e Indexación (****nadfa.py****)** El programa implementará tres comportamientos (usando el fichero con pesos precalculados generado en el paso anterior):

- **-d <fichero.bin>**: Realizar recorrido recursivo por el autómata imprimiendo **todas las palabras aceptadas**.
- **-i <fichero.bin>**: Leer en bucle de la entrada estándar y devolver el índice asociado (hashing directo, según Algoritmo A).
- **-w <fichero.bin>**: Leer en bucle un índice de la entrada estándar y devolver la palabra (hashing inverso, según Algoritmo B).

5. Requisitos previos

- Conocimientos sólidos en lectura/escritura de **formatos binarios en Python 3** (uso de estructuras, bytes y operaciones a nivel de bit para desempaquetar las celdas de 4 bytes en porciones de 1 y 3 bytes).
- Manejo de entrada/salida estándar para _pipelines_ (pipes) en Unix.
- Comprensión de recorridos en grafos (algoritmos de recursividad como DFS para recorrer y calcular pesos).

6. Ejemplos ilustrativos

Un ejemplo usado en el material es el verbo _discount_, _dismount_, _recount_ y _remount_, que con sus variaciones forman 16 palabras.

- **Pesos de estado:** El estado inicial tiene peso 16 (total de formas). El estado final tiene peso 1.
- **Hashing Directo:** Si buscamos "discount", el algoritmo sigue las transiciones de la letra 'd' y como es el primer carácter, el índice es 1. La palabra "remount" devuelve el índice 13.
- **Hashing Inverso:** Si enviamos índice `14`, la salida debe ser `remounted`.

7. Posibles errores y soluciones

- **Excepciones con la estructura Binaria:** Asegúrate de extraer correctamente el dato de 4 bytes en "1 byte de info" y "3 bytes de destino/peso" utilizando corrimientos de bits o módulos de estructuración binaria (ej. biblioteca `struct` en Python). Las celdas destino son índices _de celdas en el vector_, no punteros en crudo.
- **Gestión de Errores de Flujo:**
    - Si se da una palabra no presente en el diccionario con la opción `-i`, se debe imprimir exactamente **unknown**.
    - Si se proporciona un índice numérico fuera del rango válido (<1 o >total) con la opción `-w`, se debe imprimir **index out of bounds**.
    - Gestionar adecuadamente ficheros no existentes o formatos incorrectos (evitar crasheos de Python, mostrar mensaje de error adecuado).

8. Criterios de éxito

Para verificar que tu práctica está correctamente implementada, debes poder encadenar mediante _pipes_ en la terminal tus programas y usar la utilidad `cmp` de Unix sin recibir diferencias de salida:

```
# Validar el volcado completo de palabras
$ python3 nadfa.py -d largew.bin > out.txt
$ cmp large.txt out.txt

# Validar el ciclo completo de Hashing y Unhashing
$ cat large.txt | python3 nadfa.py -i largew.bin | python3 nadfa.py -w largew.bin > out.txt
$ cmp large.txt out.txt
```

_Si ambos comandos no devuelven error y el fichero temporal_ _out.txt_ _es idéntico a los originales de texto, el hashing es un éxito matemático y funcional absoluto_.

**Parte Opcional (Pesos en transiciones en lugar de estados):** Adicionalmente puedes implementar `tiw.py` y `nadfa2.py`. La teoría indica que colocar los pesos de indexación en la propia transición (en lugar de en los estados) aumenta el tamaño del autómata en disco porque siempre hay más transiciones que estados. Sin embargo, la ventaja es que el procesamiento es mucho más rápido porque el cálculo del índice evita sumar recursivamente los pesos de las ramas predecesoras; simplemente suma el peso almacenado directamente en la transición tomada. El criterio de éxito aquí es generar un fichero `opcional.txt` documentando el porcentaje de crecimiento en memoria y la aceleración en tiempos de ejecución