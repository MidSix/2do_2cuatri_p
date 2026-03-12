# Propiedades Matemáticas de las Operaciones con Lenguajes

En la asignatura de ALF, es vital conocer qué reglas de álgebra podemos aplicar y cuáles están terminantemente prohibidas al manipular Expresiones Regulares y Lenguajes.

## 1. Unión ($\cup$)
La unión es la operación más "liberal" y se comporta de forma similar a la suma lógica.

*   **Conmutativa:** $R \cup S = S \cup R$ (El orden de los caminos no importa).
*   **Asociativa:** $(R \cup S) \cup T = R \cup (S \cup T)$ (Se pueden agrupar como quieras).
*   **Idempotente:** $R \cup R = R$ (La unión es inclusiva; tener el mismo camino dos veces no añade nada).
*   **Elemento Neutro:** $R \cup \emptyset = R$ (Unir con el conjunto vacío no añade palabras).
*   **Subconjuntos:** Si $S \subseteq R \implies R \cup S = R$ (Si un saco ya contiene al otro, la unión es el saco grande).

## 2. Concatenación ($\cdot$)
Es la operación más "rígida". **Cuidado: El orden es sagrado.**

*   **NO CONMUTATIVA:** $RS \neq SR$ (En general). Ejemplo: $ab \neq ba$.
*   **Asociativa:** $(RS)T = R(ST)$ (Se puede escribir $RST$ sin paréntesis).
*   **Elemento Neutro ($\epsilon$):** $R \cdot \epsilon = \epsilon \cdot R = R$ (La palabra vacía es el "1" de la concatenación).
*   **Elemento Nulo ($\emptyset$):** $R \cdot \emptyset = \emptyset \cdot R = \emptyset$ (Si concatenas con el vacío, el resultado es el vacío. Es como multiplicar por 0).

## 3. Distribución
La concatenación se distribuye respecto a la unión (como en el álgebra normal).

*   **Por la izquierda:** $R(S \cup T) = RS \cup RT$
*   **Por la derecha:** $(S \cup T)R = SR \cup TR$

## 4. Cierre de Kleene (*)
El asterisco tiene sus propias reglas especiales para simplificación.

*   **Idempotencia del Cierre:** $(R^*)^* = R^*$ (Cerrar lo que ya está cerrado no añade nada).
*   **Cierre del Vacío:** $\emptyset^* = \{\epsilon\}$ (Al menos puedes elegir no elegir nada).
*   **Cierre de la Palabra Vacía:** $\epsilon^* = \epsilon$.
*   **Relación con Positivo:** $R R^* = R^* R = R^+$
*   **Redundancia de $\epsilon$:** $(\epsilon \cup R)^* = R^*$ (El asterisco ya incluye la opción de no elegir nada).

---
**Resumen para el examen:** 
Si ves un ejercicio de simplificación, puedes mover bloques de una unión de sitio, pero **NUNCA** muevas bloques que estén pegados por concatenación. Si cambias $ab$ por $ba$, habrás cambiado el lenguaje.
