### El engaño del `==` en C# vs Python

En Python, cuando tú escribes `a == b`, por debajo Python llama al método mágico `a.__eq__(b)`. Es decir, el `==` comprueba si el **contenido** (el valor) es igual. Para comprobar si son exactamente el mismo objeto en memoria, en Python usas `a is b`.

En C# (para las clases), ¡es exactamente al revés por defecto!:

- El operador **`==`** en C# comprueba la **igualdad de referencia**. Es decir, mira si ambas variables apuntan _exactamente al mismo espacio en memoria_. (Es el equivalente a usar `is` en Python).
- El método **`.Equals()`** está diseñado para comprobar la **igualdad de valor** (¿tienen los mismos datos por dentro, aunque sean objetos distintos en memoria?).

### ⚠️ El gran matiz: Tipos de Referencia vs Tipos de Valor

Hay una razón por la que C# hace esto. En C#, los datos se dividen estrictamente en dos mundos:

- **Tipos de Referencia (`class`):** Como tu `Facto`. Aquí C# dice: _"No sé qué hace a dos 'Factos' iguales, no me la voy a jugar comparando todos sus campos porque podría ser lentísimo. Ante la duda, solo diré que son iguales si son exactamente el mismo objeto en memoria"_.
- **Tipos de Valor (`struct`, `int`, `float`, `bool` y también los `string`):** Para estos datos básicos, **el `==` en C# SÍ compara por valor**. C# sabe perfectamente cómo comparar dos números o dos textos letra por letra.


En el nivel más absoluto, primitivo y general de C# (hablando de la raíz del lenguaje, `System.Object`), **`==` y `.Equals()` hacen exactamente lo mismo: ambos comparan de la misma manera y eso depende del tipo.**

Para entenderlos en su estado más puro, vamos a definirlos y ver cómo C# los aplica al universo de datos:

### 1. ¿Qué son exactamente?

- **`==` (Igualdad):** Es un **operador**. Esto significa que el compilador de C# decide cómo usarlo _en tiempo de compilación_ basándose en el tipo de variable que estás declarando.
- **`.Equals()`:** Es un **método virtual**. Absolutamente todo en C# nace con este método porque viene pegado en el "ADN" base del lenguaje (`System.Object`). Al ser un método, se ejecuta _en tiempo de ejecución_ basándose en lo que realmente es el objeto en ese momento.

### 2. ¿Qué hacen y cómo comparan por defecto?

C# divide todo el universo de datos nativos en dos grandes reinos desde la fábrica. El comportamiento predeterminado de `==` y `.Equals()` depende exclusivamente de a qué reino pertenezca el dato:

**Reino A: Tipos de Valor (Números `int`, `float`, booleanos `bool`, `structs`)** En este reino, el comportamiento por defecto es comparar por **VALOR**.

- `==` mira si el valor es matemáticamente el mismo (ej. `5 == 5`).
- `.Equals()` hace exactamente lo mismo (ej. `5.Equals(5)`).
- _Conclusión:_ Ambos miran el contenido crudo.

**Reino B: Tipos de Referencia (Cualquier objeto, listas genéricas, diccionarios, etc.)** En este reino, el comportamiento por defecto de la fábrica es comparar por **REFERENCIA**.

- `==` mira si ambas variables apuntan exactamente al mismo cajón de memoria.
- `.Equals()` hace exactamente lo mismo, mira si es el mismo cajón de memoria.
- _Conclusión:_ Ambos ignoran el contenido y miran la dirección de memoria.

### El Resumen Definitivo

En el escenario más general posible, **`==` y `.Equals()` son clones que hacen lo mismo**. O los dos miran el valor (para números), o los dos miran la memoria (para objetos).

La única razón por la que en programación avanzada parecen cosas distintas, es porque el lenguaje te permite "hackear" el método `.Equals()` para que empiece a mirar valores en el Reino B, dejando al pobre operador `==` intacto mirando la memoria.

_(Nota: La única gran excepción de fábrica es el texto, los `strings`. Pertenecen al Reino B (memoria), pero los creadores de C# los modificaron desde el día 1 para que tanto `==` como `.Equals()` comparen por VALOR (letra por letra) porque era lo que todo el mundo esperaba)._