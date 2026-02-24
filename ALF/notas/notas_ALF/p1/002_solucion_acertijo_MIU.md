# Solución al Ejercicio 3 de la Práctica 1: El Sistema MIU

## 1. El Acertijo MU: ¿Se puede producir la cadena `MU`?

La respuesta corta es **no, no se puede**.

La clave para resolver este acertijo es encontrar un **invariante**: una propiedad que es cierta para el axioma inicial (`MI`) y que se conserva como cierta después de aplicar cualquiera de las reglas de producción.

En este caso, el invariante es el **número de letras 'I'** en los teoremas.

### Análisis del Invariante

1.  **Axioma `MI`**: Empezamos con **1** letra 'I'.
2.  **Efecto de las reglas sobre el número de 'I's**:
    *   **Regla 1 (`xI` → `xIU`):** No cambia el número de 'I's.
    *   **Regla 2 (`Mx` → `Mxx`):** Duplica el número de 'I's. Si había `N` letras 'I', ahora habrá `2 * N`.
    *   **Regla 3 (`III` → `U`):** Reduce el número de 'I's en 3. Si había `N`, ahora habrá `N - 3`.
    *   **Regla 4 (`UU` → `_`):** No cambia el número de 'I's.

### La Prueba (Módulo 3)

La propiedad clave es que **el número de letras 'I' en un teorema nunca puede ser un múltiplo de 3**.

*   El axioma `MI` tiene 1 'I', y `1 mod 3 = 1`.
*   La **Regla 2** (duplicar) nunca producirá un múltiplo de 3 si no partía de uno.
    *   Si `N mod 3 = 1`, entonces `2N mod 3 = 2`.
    *   Si `N mod 3 = 2`, entonces `2N mod 3 = 4 mod 3 = 1`.
*   La **Regla 3** (restar 3) no altera el resultado de la operación módulo 3. `(N - 3) mod 3` es lo mismo que `N mod 3`.

**Conclusión:**
Partimos de un número de 'I's (1) que no es múltiplo de 3. Ninguna de las reglas puede transformar la cantidad de 'I's en un múltiplo de 3.

El teorema objetivo, **`MU`**, tiene **0** letras 'I'. Como 0 es un múltiplo de 3, y hemos demostrado que el sistema nunca puede generar un teorema con un número de 'I's que sea múltiplo de 3, podemos concluir que **`MU` no es un teorema del sistema MIU.**

---

## 2. El Procedimiento de Decisión para el Sistema MIU

Un **procedimiento de decisión** es un algoritmo que, para cualquier cadena, determina en tiempo finito si pertenece o no al lenguaje (es decir, si es un teorema).

**Opinión y Análisis:**

Para el sistema MIU, mi opinión es que **no existe un procedimiento de decisión** (el sistema es **indecidible**).

*   **Búsqueda Infinita:** Un programa puede generar teoremas de forma indefinida (búsqueda hacia adelante). Si una cadena *es* un teorema, la encontraremos. Pero si *no lo es*, el programa no tiene un criterio claro para detenerse y concluir "no".
*   **Contraste con sistemas decidibles:** En sistemas más simples (como el `mg~` del ejercicio 2), donde las reglas solo alargan las cadenas, el procedimiento es simple: si generas teoremas más largos que tu objetivo y no lo has encontrado, nunca lo harás.
*   **La complejidad del MIU:** Las reglas 3 y 4, que acortan las cadenas, rompen esta lógica. Una cadena muy larga podría, teóricamente, convertirse en una más corta. Esto impide podar el árbol de búsqueda y nos obliga a una exploración potencialmente infinita.

Este problema está relacionado con conceptos profundos de la teoría de la computación, como el **problema de la parada**, que demuestra que es imposible crear un algoritmo general para saber si un programa cualquiera se detendrá o no. El sistema MIU es un ejemplo clásico que ilustra esta indecidibilidad.

Por lo tanto, aunque se puede implementar un programa que *enumere* teoremas, no se puede implementar uno que *decida* la pertenencia para todos los casos posibles de forma garantizada.
