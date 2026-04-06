# Relación Biunívoca - Explicación del Notebook ALF

## Definición Matemática General

En matemáticas, una **relación biunívoca** (también conocida como función biyectiva) es una función matemática que cumple con ser simultáneamente:

### 1. Inyectiva
- A cada elemento del conjunto de origen le corresponde una imagen distinta
- Matemáticamente: si f(x) = f(y), entonces x = y

### 2. Sobreyectiva
- Todos los elementos del conjunto de llegada (codominio) son la imagen de algún elemento del conjunto de origen

---

## Propiedad Fundamental

> **Una de las propiedades más importantes** de establecer una función biyectiva es que:
>
> 1. ✅ Garantiza que su relación inversa (f⁻¹) también es una función matemáticamente válida
> 2. ✅ Los dos conjuntos que se están relacionando tienen exactamente la misma **cardinalidad** (el mismo número de elementos)

---

## Aplicación en la Práctica 2

### Contexto del Hashing Perfecto ([[021_hashing]]) con Autómatas

El objetivo del autómata numerado es crear una correspondencia matemática exacta (**biunívoca**) entre dos conjuntos de la misma cardinalidad:

| Conjunto A                                                     | Conjunto B                                         |
| -------------------------------------------------------------- | -------------------------------------------------- |
| Palabras del diccionario (lenguaje reconocido por el autómata) | Índices numéricos enteros (1 al total de palabras) |

---

## Implementación a través de los Algoritmos

Que es el hashing -> [[021_hashing]]

### Hashing Directo: `Palabra_a_Indice`
- **Actúa como la función f(x)**
- Dado un elemento del conjunto de palabras, el algoritmo:
  - Recorre el autómata letra por letra
  - Suma los pesos de indexación de las ramas lexicográficamente descartadas
  - Devuelve un índice único
- **Garantías por la biunivocidad:**
  - ❌ No existen colisiones (ningún par de palabras devuelve el mismo número)
  - ✅ La función cubre todos los números desde el 1 hasta el total del diccionario

### Hashing Inverso: `Indice_a_Palabra`
- **Actúa como la función inversa f⁻¹(y)**
- Dado un valor numérico (índice), el algoritmo:
  - Recorre el autómata descontando del índice los pesos de los estados que se van descartando en orden alfabético
  - Reconstruye de manera exacta e unívoca la palabra original
- **La existencia y validez de f⁻¹ queda garantizada** por la biyectividad de la función original

---

## Por Qué Funciona: Los Pesos de Indexación

> **Gracias a la biyectividad matemática que otorgan los pesos de indexación** (que equivalen al cardinal del "lenguaje derecho" de cada estado), es posible comprimir diccionarios masivos con cientos de miles de entradas.

### Mecanismo:
1. Las palabras se transforman en su posición relativa (índice)
2. Los índices pueden ser decodificados a la palabra original de forma instantánea
3. Logrando una representación **extremadamente compacta y eficiente**

---

## Resumen Visual

```
Conjunto A (Palabras) ───────┐
                             │ f(x)
                             ▼
                    [Autómata Numerado]
                             │
                             ▼
Conjunto B (Índices 1..N) ────┘

La relación es BIUNIVOCAMENTE:
• Una palabra → Un índice único (inyectiva)
• Un índice → Una palabra única (sorbitiva)
• f(x) = y ⟺ f⁻¹(y) = x  (inversa existe y es válida)
```

---

*Fuente: Notebook ALF - Práctica 2 sobre Autómatas Finitos Deterministas Acíclicos Mínimos*
