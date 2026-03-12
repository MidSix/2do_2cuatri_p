# Alfabeto, Palabra y Lenguaje

A la hora de trabajar con autómatas y lenguajes formales, es crucial diferenciar tres conceptos básicos:

1. **Alfabeto ($\Sigma$):** Es un conjunto de símbolos y este **siempre debe ser finito** (por ejemplo, el abecedario español, o el alfabeto binario $\Sigma = \{0, 1\}$).
2. **Palabra o cadena ($w$):** Es una secuencia formada por símbolos pertenecientes a un alfabeto. Las palabras **siempre tienen una longitud finita** (no existen palabras formadas por infinitos símbolos).
3. **Lenguaje ($L$):** Es, por definición, un conjunto de palabras. Dado que simplemente agrupa palabras, puede estar formado por un número finito de ellas (lenguaje finito) o por infinitas palabras (lenguaje de tamaño infinito).

**Ejemplo:**
Imagina que tenemos el alfabeto binario $\Sigma = \{0, 1\}$. 
Si definimos un lenguaje $L$ como "todas las cadenas formadas exclusivamente por unos", el lenguaje sería:
$L = \{1, 11, 111, 1111, 11111, \dots\}$

Como se puede observar:
- Cada cadena individualmente ($1$, $11$, $111$, etc.) tiene una longitud finita (termina en algún momento).
- El lenguaje en sí ($L$) contiene una cantidad infinita de cadenas, por lo que es un lenguaje infinito.
