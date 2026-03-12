# Relaciones y Funciones en Autómatas

En la asignatura de Autómatas y Lenguajes Formales (ALF), entender cómo se relacionan los conjuntos es fundamental para definir las transiciones de los estados.

> Nosotros podemos **clasificar** las funciones en atendiendo tanto al conjunto de salida(Total, parcial) como al conjunto de llegada(Inyectiva, Sobreyectiva y Biyectiva).
## 1. Conceptos Básicos
Sea una relación $f$ del conjunto $A$ (salida/dominio) al conjunto $B$ (llegada/codominio).

### ¿Es Función o no?
*   **Función:** Para cada elemento $x \in A$, existe **como máximo una** imagen $y \in B$. No puede haber "un origen con dos destinos".
    *   *Ejemplo No Función:* $f = \{(1, a), (1, b)\}$. El 1 tiene dos destinos. **No es función**.

### Tipos de Funciones (según el conjunto de SALIDA $A$)
*   **Función Total:** **TODOS** los elementos de $A$ tienen una flecha asignada. El autómata siempre sabe qué hacer.
*   **Función Parcial:** **ALGUNOS** elementos de $A$ no tienen flecha. El autómata podría "bloquearse" en ciertos estados con ciertas entradas.

## 2. Clasificación Avanzada (según el conjunto de LLEGADA $B$)
Estas propiedades definen la "calidad" del emparejamiento:

| Tipo | Regla Mnemotécnica | Descripción |
| :--- | :--- | :--- |
| **Inyectiva** | "1 a 1" | No hay dos elementos de $A$ que apunten al mismo elemento de $B$. |
| **Sobreyectiva** | "No sobra nada" | Todos los elementos de $B$ tienen al menos una flecha que les llega. |
| **Biyectiva** | "Perfecta" | Es Inyectiva y Sobreyectiva a la vez. Emparejamiento perfecto sin que sobre nada en ningún lado. |

---
*Nota: En los ejercicios de teoría de conjuntos, una función puede ser Total pero no Sobreyectiva (si sobran elementos en B), o Total pero no Inyectiva (si dos de A van al mismo de B).*