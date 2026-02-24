# Práctica: Algoritmos de Búsqueda - Problema de las N-Reinas (C#)

**Asignatura:** Inteligencia Artificial / Programación
**Grupo:** G1.1 - Jueves
**Autores:**
* Xoel Sánchez Dacoba
* Sebastián David Moreno Expósito

---

## 1. Introducción y Objetivos

El objetivo principal de esta práctica ha sido la implementación de un motor de búsqueda en el espacio de estados para resolver el problema de las **N-Reinas**, migrando la lógica original desde **Python** a **C# (.NET)**.

El reto técnico consistió en adaptar un código basado en tipado dinámico y "métodos mágicos" de Python a un lenguaje fuertemente tipado como C#, haciendo uso de estructuras de datos eficientes, interfaces y delegados.

## 2. Estructura del Proyecto

El código se ha organizado en varios ficheros `.cs` para respetar el principio de responsabilidad única y facilitar la modularidad.

### 2.1. Representación del Estado (`Solucion.cs`)
Esta clase modela un estado del tablero. En lugar de usar una matriz, se utiliza una lista de tuplas `(Fila, Columna)`.
* **Sobrecarga de Operadores:** Se han implementado manualmente los operadores de comparación (`==`, `!=`, `<`, `>`) y los métodos `Equals` y `GetHashCode`. Esto replica el comportamiento de `__eq__` y `__lt__` de Python, permitiendo que la Cola de Prioridad ordene las soluciones automáticamente.
* **Formato de Salida:** Se sobrescribió `ToString()` para mostrar las coordenadas en el formato `Fila-Columna`.

### 2.2. Gestión de Candidatos (`ListaCandidatos.cs`)
Se definió la interfaz `IListaCandidatos` para desacoplar el algoritmo de búsqueda de la estructura de datos subyacente.
* **Cola de Prioridad:** La clase `ColaDePrioridad` implementa esta interfaz usando `PriorityQueue<Solucion, int>` (nativo de .NET 6) junto con un `Dictionary<string, Solucion>`.
* **Eficiencia:** El diccionario permite búsquedas y "borrados lógicos" en tiempo constante $O(1)$, marcando los nodos obsoletos con un coste `REMOVED_COST` (-1), una técnica idéntica a la usada en la versión de referencia de Python (`heapq`).

### 2.3. Motor de Búsqueda (`Algoritmos_Busqueda.cs`)
Contiene la lógica genérica de búsqueda.
* **Delegados (`Func<>`):** Para pasar funciones como parámetros (cálculo de coste, generación de vecinos, criterio de parada), se utilizaron delegados genéricos en lugar de pasar objetos dinámicos.
* **Clase `AEstrella`:** Hereda del motor base e implementa el cálculo de prioridad $f(n) = g(n) + h(n)$.

### 2.4. Ejecución y Lógica del Problema (`Ejecucion.cs`)
Contiene el `Main` y la definición específica del problema de las N-Reinas:
* **Generación de Vecinos:** Se iteran las columnas y se mueve la reina una fila hacia abajo (módulo N), generando exactamente un vecino por reina.
* **Criterio de Parada:** Verifica que no existan conflictos en filas, columnas ni diagonales.

## 3. Decisiones de Diseño y Migración

Durante la portabilidad de Python a C# se tomaron las siguientes decisiones técnicas:

1.  **Tipado Estático:** Se sustituyó el uso de `Duck Typing` por tipos explícitos y Genéricos (`List<Tuple<int, int>>`), lo que añade seguridad en tiempo de compilación.
2.  **Manejo de Nulos:** Se implementó lógica defensiva contra `NullReferenceException` utilizando operadores modernos de C# como `?.` (null-conditional) y `??` (null-coalescing), especialmente en la sobrecarga de operadores.
3.  **Inmutabilidad:** Las tuplas de coordenadas se tratan como objetos inmutables para evitar efectos colaterales al generar nuevos estados vecinos.

## 4. Resultados y Ejecución

El algoritmo se ha probado con **N=4** reinas.

### Comparativa de Rendimiento
* **Python:** Explora 126 nodos.
* **C#:** Explora 107 nodos.

**Análisis:** Ambos encuentran una solución válida y óptima. La diferencia en el número de nodos se debe a la implementación interna de las estructuras de prioridad (`heapq` vs `PriorityQueue`) y cómo desempatan nodos con el mismo coste. La solución encontrada es:

```text
Solución encontrada: 2-0 0-1 3-2 1-3
Número de nodos expandidos: 107