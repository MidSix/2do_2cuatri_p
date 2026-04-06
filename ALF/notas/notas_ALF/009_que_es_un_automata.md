# Autómatas Finitos Deterministas Acíclicos Mínimos (ADFA)
## Notas para ALF - Hashing Perfecto

---

## 1. ¿QUÉ ES UN AUTÓMATA?

Un **autómata** es un modelo matemático o estructura algebraica que se utiliza fundamentalmente para procesar secuencias o cadenas de símbolos con el fin de determinar si dichas cadenas son válidas y pertenecen a un determinado lenguaje formal.

### Definición Formal (5-tupla)
Un autómata finito determinista (AFD) M es una colección de cinco elementos:

```
M = (Q, Σ, s, δ, F)
```

| Elemento         | Descripción                                                                                                                                                                                                                                                                      |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Q**            | Conjunto de estados (representan la "memoria" temporal o las distintas posiciones en las que puede encontrarse el sistema)                                                                                                                                                       |
| **Σ**            | Alfabeto de entrada (conjunto finito de símbolos válidos que componen las palabras que el autómata puede leer)                                                                                                                                                                   |
| **s ∈ Q**        | Estado inicial (punto de partida obligatorio para procesar cualquier cadena)                                                                                                                                                                                                     |
| **δ: Q × Σ → Q** | Función de transición (dicta las reglas exactas sobre cómo el autómata debe saltar de un estado actual a uno nuevo al leer un símbolo específico) - (La función puede ser parcial, es decir en un estado dado no **necesariamente** para cada símbolo debe haber una transición) |
| **F ⊆ Q**        | Conjunto de estados finales o de aceptación (estados que indican que el proceso ha tenido éxito)                                                                                                                                                                                 |
|                  |                                                                                                                                                                                                                                                                                  |

![[Pasted image 20260405140925.png]]
Como podemos ver aquí tenemos de ejemplo un:
- **Automata:** (5-tupla que contiene : Conjunto de Estados -> **Q**, alfabeto -> **Σ**,                       estado inicial -> **s ∈ Q**, función de transición -> **δ: Q × Σ → Q** y conjunto de estados finales         -> **F ⊆ Q**).
- **Finito:** El cardinal **Q** es finito, es decir, tiene un numero finito de elementos, es decir un numero finito de estados.
- **Determinista:** Para cada estado NO hay DOS o mas transiciones de un mismo símbolo.
- **Acíclico:** Esto ocurre cuando NO hay ciclos en el automata, eso quiere decir que NO es posible volver a un estado anterior del Automata(Es decir, un estado que YA ha sido procesado por el automata) desde ninguna función de transición del mismo. 
- **Parcial**: Un automata es parcial cuando NO es completo. Y es completo cuando para TODOS los estados del Automata hay al menos una transición para TODOS los símbolos del alfabeto sobre el que se implementa el Automata.
- **Mínimo:** Un Automata es mínimo cuando todos sus estados son mínimos, esto implica que NO existe ningún estado equivalente a otro dentro del Automata(Si un estado **A** es equivalente a un estado **B** quiere decir que ambos estados NO son mínimos, por tanto el Automata NO tendría SOLO estados mínimos, así que NO seria un Automata mínimo). Dos estados son equivalentes cuando se cumplen las siguientes condiciones:
- **No Numerado:** Que sea numerado quiere decir que cada estado tiene un identificador numérico semántico, como vemos en nuestro ejemplo los estados no tienen ese "identificador" numérico, no hay números asociados a los estados del Automata.
	┌─────────────────────────────────────────────────────┐
	│              CRITERIOS DE EQUIVALENCIA                                   │
	├─────────────────────────────────────────────────────┤
	│                                                                                                 │
	│  1. **Mismo tipo** (ambos finales o ambos no-finales)               │
	│     └─ Estado final ≠ Estado no-final                                        │
	│        (Distinto tipo -> NO equivalentes)                                  │
	│  2. **Misma función de transición para TODOS los**                 │
	│     **símbolos del alfabeto**                                                        │
	│     └─ δ(q₁, a) ≡ δ(q₂, a) para todo a ∈ Σ                                  │
	│           (O sea, ambos llevan al mismo estado)                        │
	│  3. Los destinos alcanzables son equivalentes                        │
	│     └─ Si q₁ ──a──► r₁ y q₂ ──a──► r₂, entonces r₁≡r₂              │
	│                                                                                                 │
	└─────────────────────────────────────────────────────┘
La notación δ(q, a) es equivalente a q.a. Esta notación es transitiva, eso quiere decir que cumple la propiedad matemática de transitividad: Una relación $R$ es transitiva si: $(a R b \land b R c) \implies (a R c)$. O sea, si decimos que w NO es un símbolo sino es un palabra. La notación q_0.w. también es valida, y simplemente te dice si partiendo del estado inicial la palabra w puede llegar a un estado final, si puede -> La palabra es aceptada, si no puede -> La palabra es rechazada.


> [!PDF|yellow] [[p2.pdf#page=1&selection=196,1,197,51&color=yellow|p2, p.1]]
> > os autómatas finitos deterministas acíclicos mínimos constituyen la estructura más compacta posible para reconocer conjuntos finitos de palabras

- **Reconocer conjuntos finitos palabras:** Con eso quiere decir que son excelentes para "determinar" si una palabra o un conjunto de ellas pertenece a un lenguaje.
┌─────────────────────────────────────────────────────┐
│              RECONOCER UN LENGUAJE                                      │
├─────────────────────────────────────────────────────┤
│                                                                                                 │
│  Entrada: Palabra w                                                                  │
│                                                                                                 │
│  Proceso:                                                                                  │
│    • Seguir transiciones desde q₀                                             │
│    • Si se atora → RECHAZAR                                                   │
│    • Si termina en F(conjunto estados finales) → ACEPTAR      │
│                                                                                                  │
│  Salida:                                                                                      │
│    • w ∈ L(A)   si q₀.w ∈ F (reconocido)                                     │
│    • w ∉ L(A)   si q₀.w ∉ F o se atora                                          │
│                                                                                                  │
│  En tu proyecto:                                                                        │
│    • L = diccionario de palabras                                                │
│    • Reconocer = determinar si palabra está en L                    │
└─────────────────────────────────────────────────────┘

> [!PDF|yellow] [[p2.pdf#page=1&selection=197,58,197,77&color=yellow|p2, p.1]]
> > ratios de compresión

- Son simplemente una division de la siguiente forma
$$\text{Ratio de Compresión} = \frac{\text{Tamaño del diccionario crudo}}{\text{Tamaño del autómata compacto}}$$
Por ejemplo. Si un diccionario pesa 4 MiB guardado en disco y con un Automata pesa 150 KiB -> 4000 KiB / 150 KiB -> 26.7, O sea, la compresión por automata en lugar de guardarlo en disco es un 26.7 veces mejor,  si hacemos el inverso: 150 KiB / 4000 KiB -> 0.0375 equivalentemente 3.75%, el diccionario implementado con un Automata ocupa 3.75% el espacio de aquel implementado guardando palabra por palabra en el disco.
### Funcionamiento Básico
1. El autómata se sitúa en el estado inicial
2. Comienza a leer la palabra símbolo por símbolo
3. Con cada símbolo procesado, consulta su función de transición y avanza al siguiente estado correspondiente
4. **Si al terminar de procesar toda la cadena el autómata se encuentra posicionado en uno de sus estados finales → la palabra es aceptada**
5. De lo contrario → la palabra es rechazada

---

## 2. ¿QUÉ IMPLICA QUE SEA FINITO?

### Implicación Fundamental (Implicación teórica)
Que un autómata sea **finito** implica fundamentalmente que **la cantidad de memoria disponible para aceptar o rechazar una cadena de entrada es estrictamente limitada(memoria = estados, es decir, el conjunto de estados "Q" es finito)**. Por tanto la memoria de un Automata finito se ve reducida exclusivamente a:
- Recordar en qué estado se encuentra el modelo en el paso actual(Esto no permite un recuento de los estados anteriores)
- Leer el símbolo correspondiente de la cadena de entrada

### Importancia y Consecuencias

| Aspecto                     | Implicación                                                                                                                                                                                                                                                           |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Capacidad computacional** | No puede procesar estructuras que exijan llevar la cuenta de un número arbitrario de eventos pasados                                                                                                                                                                  |
| **Lenguajes no regulares**  | No puede aceptar lenguajes como {aⁿbⁿ \| n ≥ 0} porque al comenzar a analizar las "bes", cualquier autómata finito es completamente incapaz de retener en memoria la información sobre cuántas "aes" exactas se acaban de leer                                        |
| **Lema del Bombeo**         | Si el lenguaje que acepta es infinito, obligatoriamente tendrá que aceptar cadenas con una longitud mayor al número de estados. Esto provoca que, al procesar dicha cadena larga, el autómata repita irremediablemente al menos un estado, estableciendo así un ciclo |
| **Terminación garantizada** | La propiedad finita asegura que procesos abstractos de construcción de autómatas lleguen siempre a un fin (ej: convertir AFN → AFD termina porque el número de estados es finito)                                                                                     |

### Reflejo en la Definición Formal (Implicación practica)
> La propiedad de "finitud" se refleja directamente en dos componentes principales:
- **Q** se define explícitamente como un conjunto **finito** de estados
- **Σ** es también un conjunto **finito** (y no vacío) de símbolos

---

## 3. ¿QUÉ IMPLICA QUE SEA DETERMINISTA?

### Implicación Fundamental
Que un autómata sea **determinista** implica que su comportamiento es totalmente predecible: para cada estado en el que se encuentre y para cada símbolo del alfabeto que lea, existe **exactamente un único estado de destino**.

Matemáticamente: δ: Q × Σ → Q (debe estar completamente especificada para cualquier combinación posible)

### Diferencias Principales con AFN (No Determinista)

| Característica | AFD (Determinista) | AFN (No Determinista) |
|----------------|-------------------|---------------------|
| **Función de transición** | δ: Q × Σ → Q (único destino) | ∆: Q × Σ → 2Q (múltiples destinos) |
| **Múltiples caminos** | No permite | Permite que, desde un mismo estado y leyendo el mismo símbolo, pueda transitar a varios estados diferentes |
| **Transiciones espontáneas** | No tiene | Puede incluir ε-transiciones (cambiar de estado sin consumir ningún símbolo) |
| **Modelo de aceptación** | Sigue una única ruta lineal; decide al terminar | Explora conceptualmente todos los caminos en paralelo; acepta si AL MENOS UNO termina en estado final |

### Importancia para la Implementación Práctica

#### 1. Velocidad y Eficiencia (O(n))
- Se puede implementar **directamente mediante una matriz o tabla de transiciones** donde el estado actual y el carácter leído sirven como índices exactos del siguiente casillero
- Procesar una palabra es un simple bucle que tarda tiempo directamente proporcional a la longitud de la palabra (tiempo lineal)
- Sin necesidad de manejar memoria adicional, recursividad múltiple o algoritmos de backtracking

#### 2. Viabilidad Algorítmica para Hashing Perfecto
Como se implementa en la Práctica 2, el determinismo es esencial para construir arquitecturas algorítmicas complejas como los **Autómatas Finitos Deterministas Acíclicos Mínimos Numerados** para hacer hashing perfecto:
- Que el camino sea único y determinista garantiza que al sumar los "pesos de las ramas descartadas", se obtenga una clave numérica inmutable, unívoca y exacta para cada palabra

#### 3. Paso Final en Todo Compilador/Analizador
Aunque construir un modelo inicial suele ser más fácil pensando en un AFN (o usando Expresión Regular), para llevarlo a un programa real siempre se recurre al **Teorema de Equivalencia**, que asegura que cualquier AFN puede ser convertido algorítmicamente en un AFD.

### Teorema de Equivalencia
> Dado un AFN M, siempre existe un AFD M' tal que L(M) = L(M')

- Q' = 2^Q (puede llegar a tener hasta 2^|Q| estados)
- El proceso termina porque el número de estados del AFN es finito

---

## 4. ¿QUÉ IMPLICA QUE SEA ACÍCLICO?

### Implicación Fundamental
Que un autómata sea **acíclico** implica que **su grafo subyacente no contiene ciclos**. Es decir, no existe ninguna ruta de transiciones que permita salir de un determinado estado y volver de nuevo a él tras leer una serie de símbolos.

### Consecuencias Críticas en Estructura y Funcionamiento

| Propiedad | Explicación |
|-----------|-------------|
| **Lenguajes finitos** | Al carecer de ciclos, el autómata es estructuralmente incapaz de repetir secuencias de caracteres de forma indefinida (proceso conocido como "bombeo" en los autómatas con lazos). Por consiguiente, un autómata acíclico **solo puede reconocer un conjunto finito de palabras** |
| **Compacidad extrema en memoria** | Cuando un autómata acíclico es a su vez determinista y mínimo (ADFA), constituye **la estructura más compacta posible que se puede diseñar para reconocer conjuntos masivos pero finitos de palabras** (como diccionarios completos de un idioma). Se consiguen ratios de compresión excelentes al unificar los prefijos y sufijos comunes sin generar ambigüedades |
| **Tiempos estrictamente lineales** | La ausencia de ciclos y el determinismo garantizan que no existan bucles infinitos ni necesidad de evaluar múltiples caminos. Los tiempos de reconocimiento son **estrictamente lineales con respecto a la longitud de la palabra**, proporcionando respuestas inmediatas independientemente del tamaño de la base de datos |
| **Posibilidad de aplicar Hashing Perfecto** | La estructura acíclica permite contar matemáticamente el número exacto de sufijos válidos que se pueden leer desde cualquier estado hasta el final (el cardinal del lenguaje derecho). Al ser finito, se pueden asignar **pesos de indexación fijos a los estados o transiciones**, lo que permite construir el mecanismo de hashing para mapear unívocamente palabras con números relativos y viceversa |

### Cardinal del Lenguaje Derecho
En un autómata acíclico, desde cualquier estado se puede calcular:
- **Cardinal del lenguaje derecho** = número exacto de palabras/subpalabras que puedes leer desde dicho estado hasta algún estado final, siguiendo transiciones válidas

---

## 5. ¿QUÉ IMPLICA QUE SEA MÍNIMO?

### Implicación Fundamental
Que un autómata sea **mínimo** implica que constituye la estructura lógica y en memoria más optimizada posible para procesar y reconocer un conjunto de cadenas determinado.

### Definición Formal
Matemáticamente, un Autómata Finito Determinista (AFD) M se considera mínimo cuando:

> **No existe ningún otro AFD M' que tenga menos estados o menos arcos (transiciones) y que acepte exactamente el mismo lenguaje** (L(M') = L(M))

Para lograr llegar a esta estructura, los algoritmos de minimización analizan el grafo, identifican clases de estados que son funcionalmente equivalentes y los fusionan, manteniendo únicamente un único estado representante por cada clase.

### Ejemplo de Minimización
```
AFD no mínimo: 4 estados, 7 arcos → AFD mínimo: 2 estados, 3 arcos
```
Los algoritmos identifican clases de estados equivalentes y, para cada clase, mantienen únicamente su estado representante.

### Importancia para la Implementación de Funciones Hash (Hashing Perfecto)

En aplicaciones como la de tu práctica (hashing biunívoco de diccionarios a través de ADFA), la propiedad de que el autómata sea mínimo es absolutamente vital:

#### 1. Compacidad Extrema para Diccionarios Masivos
Los autómatas finitos deterministas acíclicos mínimos constituyen **la estructura más compacta posible** para reconocer conjuntos finitos de palabras. Al minimizarse, se unifican de forma óptima todos los prefijos y sufijos comunes que comparten las palabras del diccionario, lo que arroja unos ratios de compresión excelentes sin generar ambigüedad.

#### 2. Base Matemática para la Correspondencia Biunívoca
El *hashing perfecto* directo e inverso se basa en asignar un "peso de indexación" fijo a cada estado o transición, el cual representa matemáticamente el cardinal de su lenguaje derecho (cuántas terminaciones válidas restan hasta el final).

**Si el autómata no fuera mínimo**, existirían estados y ramas redundantes, lo cual:
- Duplicaría los caminos para llegar a las mismas terminaciones
- Corrompería los conteos de los lenguajes derechos
- Destruiría por completo la relación unívoca exacta (1 a N) entre la palabra y su número de índice

#### 3. Eficiencia Algorítmica Garantizada
Una estructura libre de redundancias permite que las funciones de *hashing* y *unhashing* no desperdicien cálculos. En un autómata mínimo, los tiempos de procesamiento, cálculo numérico y reconocimiento **son siempre estrictamente lineales con respecto a la longitud de la palabra procesada**, logrando un rendimiento óptimo independientemente de lo inmenso que sea el diccionario.

---

## RELACIÓN JERÁRQUICA PARA TU IMPLEMENTACIÓN

```
Autómata → Finito → Determinista → Acíclico → Mínimo
    ↓           ↓              ↓            ↓          ↓
Memoria     Predicible     Sin ciclos   Óptimo    Biunívoco
limitada    comportamiento  finitos     compacto   hashing
```

### Propiedad por Propiedad:
| Autómata                                         | Finito | Determinista | Acíclico | Mínimo |
| ------------------------------------------------ | ------ | ------------ | -------- | ------ |
| Memoria limitada a estado actual y símbolo leído | ✓      | ✓            | ✓        | ✓      |
| Comportamiento totalmente predecible             | ✓      | ✓            | ✓        | ✓      |
| Sin bucles infinitos ni evaluación múltiple      | ✓      | ✓            | ✓        | ✓      |
| Estructura más compacta posible                  | ✓      | ✓            | ✓        | ✓      |
| Correspondencia 1:N exacta para hashing          | ✓      | ✓            | ✓        | ✓      |

---

## RESUMEN PARA IMPLEMENTACIÓN DE FUNCIÓN HASH

Para crear tu función hash que devuelva el hash deseado, necesitas implementar un **ADFA (Autómata Finito Determinista Acíclico Mínimo)** porque:

1. **Finito** → Algoritmos terminan garantizado (no hay bucles infinitos)
2. **Determinista** → Camino único para hashing consistente y reproducible
3. **Acíclico** → Solo palabras finitas, pesos calculables de forma exacta
4. **Mínimo** → Máxima eficiencia y correspondencia 1:N exacta (biunívoca)

### Algoritmo de Hashing Perfecto (Resumen)
```
PALABRA_A_INDICE:
    índice = 1
    para cada estado en el autómata:
        índice += peso_de_estados_destino_precendentes_no_usadas
    Si se alcanza un estado final → índice es la clave numérica de la palabra
    Si no → palabra no está en el diccionario
```

### Algoritmo Inverso (Resumen)
```
INDICE_A_PALABRA:
    para cada transición posible desde el estado inicial:
        restar peso de las palabras que irían antes que la buscada
    Deducir letra por letra usando etiquetas de transiciones
```

---

## REFERENCIAS CLAVE
- Teorema de Equivalencia: AFN ↔ AFD (cualquier AFN puede convertirse en un AFD)
- Lema del Bombeo: Caracteriza los lenguajes regulares
- Cardinal del lenguaje derecho: Base matemática para hashing perfecto
- Minimización: Identifica y fusiona estados equivalentes
