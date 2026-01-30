# Multiple Dispatch en Julia

El **Multiple Dispatch** (Despacho Múltiple) es el paradigma central de Julia. Determina qué implementación de una función (qué "método") se ejecuta basándose en los tipos de **todos** sus argumentos.
## Crear una funcion en Julia
- Al crear una funcion en Julia se crea lo que se conoce como "funcion generica", esto se traduce a que una funcion crea una especie de coleccion que permite albergar multiples definiciones de la misma funcion, para referenciar estas multiples definiciones de una misma funcion generica es necesario el nombre de la funcion y el discriminador (Los argumentos de la funcion) una mista funcion con mismo identificador pero que espere parametros distintos se convierten en 2 implementaciones de la misma funcion, en el lenguaje tecnico de Julia no se les llama "multiples deficiones o multiples implementaciones de una misma funcion" sino "metodos" de la funcion.

- TODA funcion en Julia se entiende como una "funcion generica" -> es conceptualmente una unica funcion, pero consiste en varias definiciones(metodos). Es decir, es una funcion con multiples definiciones.

- En Julia el termino "method" significa algo completamente distinto a lo que significa en lenguajes con programacion orientada a objetos, en ellos el termino "method" hace alusion a un comportamiento ligado a un objeto, propio de un tipo de objeto. Sin embargo en Julia el termino "method" consiste en su lugar en una forma de llamar a una de las posibles definiciones de una funcion.
## Diferencia con otros modelos
1. **Single Dispatch (POO Clásica - Python/Java):** El comportamiento depende solo del objeto que "posee" el método (`objeto.metodo()`). El resto de argumentos son tratados de forma pasiva dentro de la función (requiriendo `if/isinstance`).
2. **Redefinición (Python):** En Python, definir una función con el mismo nombre que una anterior **sobrescribe** la referencia. La versión antigua desaparece.
3. **Multiple Dispatch (Julia):** Definir una función con el mismo nombre pero distintos tipos de argumentos **añade** un nuevo método a la función genérica.

## La "Clave Primaria" de una Función
En Julia, la identidad única de una ejecución no es solo el nombre de la función, sino la combinación de:
`Nombre de la función` + `Tipos de todos los argumentos`.

## Ventajas
- **Rendimiento:** El compilador genera código máquina especializado para cada combinación de tipos.
- **Extensibilidad:** Se pueden añadir nuevos comportamientos para nuevos tipos de datos sin modificar el código original (soluciona el "Problema de la Expresión").
- **Código Limpio:** Elimina la necesidad de condicionales de tipo (`if x isa Int`) dentro de las funciones.

---
**Tags:** #Julia #FAA #MultipleDispatch #Polimorfismo
**Relacionado:** [[001_Lenguajes_Dinamicos_y_Problema_Dos_Lenguajes]]