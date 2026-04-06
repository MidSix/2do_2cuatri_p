# Práctica 2: Autómatas Finitos Deterministas Acíclicos Mínimos para Hashing Perfecto

## 1. Fundamentos Teóricos Completos

### Definición de AFD (Autómata Finito Determinista)
Un AFD se define mediante la **5-tupla**:
```
A = (Q, Σ, δ, q₀, F)
```

| Componente | Descripción |
|------------|-------------|
| **Q** | Conjunto finito de estados (vértices del grafo) |
| **Σ** | Alfabeto de símbolos (etiquetas de transiciones) |
| **δ** | Función de transición: δ: Q × Σ → Q. Notación: q.a ≡ δ(q,a) |
| **q₀** | Estado inicial |
| **F** | Subconjunto de estados finales (círculos dobles) |

### Lenguaje Reconocido
```
L(A) = { w | al aplicar transiciones sucesivas q₀.w se alcanza un estado ∈ F }
```

### Propiedades Especiales
| Término | Definición |
|---------|------------|
| **Acíclico** | El grafo no contiene ciclos (conjunto finito de palabras) |
| **Mínimo** | No existe otro autómata con menos estados o transiciones que reconozca el mismo lenguaje |

### Numeración (Pesos de Indexación)
- Cada estado tiene un **peso numérico** asignado
- El peso representa el **cardinal del "lenguaje derecho"** de dicho estado
- Es decir: número de palabras/subpalabras que se pueden formar leyendo desde ese estado hasta cualquier estado final siguiendo transiciones válidas

---

## 2. Algoritmos y Métodos

### Algoritmo A: Palabra → Índice (Hashing Directo)

**Objetivo**: Transformar una palabra en un índice numérico único sumando los pesos de las ramas descartadas lexicográficamente antes de tomar una transición válida.

```
1. Inicializar:
   Indice = 1
   Estado_Actual = Estado_Inicial

2. Para cada letra Palabra[i] en la palabra:
   a) Si la transición es válida:
      - Recorrer caracteres c desde primera letra del alfabeto hasta predecesor de Palabra[i]
      - Por cada transición válida con c desde Estado_Actual:
        Sumar a Indice el valor de Estado_Actual[c].Número (peso del estado destino)
   b) Avanzar el estado: Estado_Actual = Estado_Actual[Palabra[i]]
   c) Si la transición NO es válida en algún punto → retornar "palabra desconocida"

3. Al terminar la palabra:
   - Si Estado_Actual ES final → devolver Indice
   - Si NO es final → retornar "palabra desconocida"
```

### Algoritmo B: Índice → Palabra (Hashing Inverso)

**Objetivo**: Reconstruir la palabra original a partir de su índice.

```
1. Inicializar:
   Estado_Actual = Estado_Inicial
   Número = Indice
   Palabra = Palabra_Vacía
   i = 1

2. Repetir hasta que Número == 0:
   a) Iterar caracteres c posibles en orden alfabético
   b) Si hay transición válida para c:
      Estado_Auxiliar = Estado_Actual[c]
   c) Si Número > Estado_Auxiliar.Número:
      Restar caminos descartados: Número = Número - Estado_Auxiliar.Número
   d) Si NO (el índice pertenece a esta rama):
      - Concatenar c a la Palabra
      - Avanzar Estado_Actual = Estado_Auxiliar
      - Si el nuevo estado ES final:
        Número = Número - 1
      - Romper bucle de caracteres y volver a iterar bloque general

3. Retornar la Palabra formada
```

---

## 3. Fórmulas y Ecuaciones

### Peso del Estado Inicial
$$\text{Peso}(q_0) = |L(A)|$$
Donde $|L(A)|$ es el número total de palabras en el diccionario.

### Cálculo del Índice
Dado una palabra $w = w_1 w_2 \dots w_n$:

$$\text{Indice}(w) = 1 + \sum_{i=1}^{n} \sum_{c < w_i} \text{Peso}(\delta(q_{i-1}, c))$$

Donde $q_{i-1}$ es el estado alcanzado al leer el prefijo hasta $w_{i-1}$.

### Nota Importante sobre Fin de Palabra
El carácter de fin de palabra `\0` se utiliza implícitamente tras la última letra. Esto garantiza que todos los autómatas tengan un único estado final, simplificando las implementaciones (caso base del peso = 1).

---

## 4. Estructura Binaria de los Archivos

### Formato General del Vector
El archivo binario consiste en un **vector dividido en celdas de 4 bytes**:

```
Celda 0 (4 bytes):    Número total de celdas del vector
Celda 1 a N:          Estados y transiciones
```

### Estructura de un Estado
| Posición | Tamaño | Contenido |
|----------|--------|-----------|
| Byte 0 | 1 byte | Número de transiciones que salen del estado |
| Bytes 1-3 | 3 bytes | Peso de indexación (inicialmente en cero) |

### Estructura de una Transición
| Posición | Tamaño | Contenido |
|----------|--------|-----------|
| Byte 0 | 1 byte | Carácter de la transición |
| Bytes 1-3 | 3 bytes | Celda destino (índice en el vector) |

### Conveniencias Técnicas Cruciales
```
Celda "0" (4 bytes):    Estado FINAL - ocupa solo 1 celda, sin transiciones
Celda "2" (8 bytes):    Estado INICIAL - inmediatamente después del final
```

---

## 5. Procedimientos Detallados de Implementación

### Parte 1: Asignar Pesos (siw.py)

**Objetivo**: Crear el programa `siw.py` (State Indexing Weights) que:
- Abra un archivo .bin sin pesos
- Recorra recursivamente el autómata calculando el peso de cada estado
- Volque el autómata modificado a un archivo de salida (tinyw.bin, etc.)

#### Algoritmo para Calcular Pesos (Recursivo)
```python
Definición Base:
  Peso(Estado_Final) = 1

Definición Recursiva:
  Peso(Estado_S) = Σ Peso(Estado_Destino) para todas las transiciones de S
```

#### Validación (Caso Base)
- ✅ El estado final (único, celda 0) tiene peso **1**
- ✅ El peso de cualquier otro estado es la suma de los pesos de los estados destino de todas sus transiciones

### Parte 2: Diccionario e Indexación (nadfa.py)

El programa implementará tres comportamientos:

| Opción | Descripción |
|--------|-------------|
| `-d <fichero.bin>` | Recorrido recursivo imprimiendo TODAS las palabras aceptadas |
| `-i <fichero.bin>` | Hashing directo: leer palabra de entrada → devolver índice asociado |
| `-w <fichero.bin>` | Hashing inverso: leer índice de entrada → devolver palabra |

---

## 6. Requisitos Previos

### Conocimientos Técnicos Necesarios
1. ✅ **Lectura/escritura de formatos binarios en Python 3**
   - Uso de estructuras (struct)
   - Operaciones con bytes
   - Operaciones a nivel de bit para desempaquetar celdas de 4 bytes

2. ✅ **Manejo de entrada/salida estándar para pipelines**
   - Pipes en Unix/Linux
   - Redirección de flujo (`|`, `<`, `>`) 

3. ✅ **Recorridos en grafos**
   - Algoritmos de recursividad como DFS
   - Traversing de árboles y grafos acíclicos

---

## 7. Ejemplos Ilustrativos

### Verbo "discount" y Variaciones (16 palabras)

| Palabra | Índice |
|---------|--------|
| discount | 1 |
| remount | 13 |
| remounted | 14 |

#### Pesos de Estado:
- **Estado inicial**: peso = 16 (total de formas)
- **Estado final**: peso = 1

### Hashing Directo - Ejemplo Paso a Paso
**Buscando "discount":**
```
1. Letra 'd': primera transición disponible → índice = 1
2. Como es el primer carácter y la única opción, no hay ramas descartadas
3. Resultado: índice = 1
```

**Buscando "remount" (índice 13):**
```
El algoritmo suma los pesos de todas las ramas lexicográficamente anteriores
hasta llegar a la transición 'r', acumulando un total de 13.
```

### Hashing Inverso - Ejemplo
**Índice 14 → Palabra:**
```
1. Número = 14 > 0, comenzar búsqueda desde estado inicial
2. Iterar caracteres en orden: 'a', 'b', ..., 'r'
3. Al llegar a 'r': Número (14) > peso de ramas anteriores
4. Restar pesos descartados, seguir rama 'r'
5. Continuar hasta encontrar la palabra exacta
6. Resultado: "remounted"
```

---

## 8. Posibles Errores y Soluciones

| Error | Causa Probable | Solución |
|-------|----------------|----------|
| Excepciones con estructura binaria | Lectura incorrecta de bytes | Usar `struct.unpack()` con corrimientos de bits o módulos de estructuración binaria. Las celdas destino son **índices**, no punteros en crudo |
| Palabra no encontrada (-i) | Transición inválida durante recorrido | Imprimir exactamente: `unknown` |
| Índice fuera de rango (-w) | Número < 1 o > total de palabras | Imprimir exactamente: `index out of bounds` |
| Fichero no existente | Ruta incorrecta o archivo borrado | Mostrar mensaje de error adecuado, evitar crasheos |
| Formato incorrecto | Archivo dañado o versión incompatible | Validar cabecera del archivo antes de procesar |

---

## 9. Criterios de Éxito (Validación)

### Comandos de Verificación con Pipes y `cmp`

