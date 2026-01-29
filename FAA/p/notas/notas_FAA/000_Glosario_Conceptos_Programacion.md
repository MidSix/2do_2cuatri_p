# Glosario de Conceptos de Programación
[+3h_Julia](https://www.youtube.com/watch?v=KlorfxsdWDw)
Definiciones claras y concisas de términos fundamentales para el ingeniero de software.

## Expresión vs. Sentencia

*   **Expresión (Expression):** Todo código que, al ejecutarse, **produce y devuelve un valor útil**.
    *   *Prueba:* ¿Puedo asignarlo a una variable? `x = (mi_expresion)`. Si funciona, es una expresión (asignar "None" o "nothing" en julia, no cuenta ya que no son utiles de por si).
    *   *Ejemplos:* `2 + 2`, `funcion()`, `lista[0]`.
    *   *En Julia:* `if`, `for`, `begin`, `try` son expresiones (devuelven el valor de la última línea ejecutada).

*   **Sentencia (Statement):** Una instrucción u **orden** que realiza una acción (cambio de estado, control de flujo) pero **no devuelve ningún valor útil** por sí misma.
    *   *Ejemplos en Python:* `if x: ...`, `import math`, `class MiClase: ...`. No puedes hacer `x = import math`.

## REPL (Read-Eval-Print Loop)

Es el **Bucle de Lectura-Evaluación-Impresión**, comúnmente conocido como **"consola interactiva"** o "shell interactivo". Es el entorno donde escribes código línea a línea y obtienes respuesta inmediata.
*   **En Python:** Al ejecutar `python` en la terminal (prompt `>>>`).
*   **En Julia:** Al ejecutar `julia` (prompt `julia>`). Es mucho más potente y tiene "modos" que se activan con teclas especiales:
    *   `?` -> Modo Ayuda (Documentación) "Escribes nombre de funciones y te da su doc".
    *   `]` -> Modo Paquetes (`pkg>`).
    *   `;` -> Modo Shell (comandos del sistema).

## Compilación y Rendimiento: JIT vs. AOT

Entender cómo se ejecuta el código es vital para escribir Julia eficiente.

### 1. Tipos de Ejecución
*   **AOT (Ahead-Of-Time - C/C++):** El código se compila a binario (`.exe`) **antes** de ejecutarse. Si hay un error, no compila. Es rapidísimo pero rígido.
*   **Interpretado (Python):** Un programa lee y ejecuta línea a línea. Si hay un error en la línea 100, las 99 anteriores ya se ejecutaron. Es flexible pero lento.
*   **JIT (Just-In-Time - Julia):** Híbrido. Se siente como interpretado (ejecutas script), pero **compila cada función a código máquina justo antes de usarla**.

### 2. La Trampa del Global Scope
Julia necesita conocer los tipos de datos para optimizar.
*   **En Funciones:** El compilador deduce que `i` es entero y genera código máquina puro (Velocidad C).
*   **En Global Scope:** Una variable global puede cambiar de tipo en cualquier momento. El compilador añade chequeos de seguridad en cada paso (Velocidad Python).

**El impacto es brutal:**
Un mismo bucle sumatorio de 1 a 100 millones:
*   **Global Scope:** `0.455583 seconds` (Velocidad Python). Millones de asignaciones de memoria.
*   **Función (1ª vez):** `0.001267 seconds` (Incluye tiempo de compilación).
*   **Función (2ª vez):** `0.000001 seconds` (Velocidad C/C++). **¡450,000 veces más rápido!**

### 3. Herramientas de Medición (Benchmarking)
*   **`@time`**: Macro básico nativo. Mide tiempo y memoria.
    ```julia
    #Definicion de funcion:
    @time function nombre_funcion(variables::el_tipo)
	    contenido
	end
	#Llamada a la funcion
    @time mi_funcion()
    
    #Al hacer esto imprira el tiempo que tomo en ejecutar y compilar esa
    #funcion
    ```
*   **`BenchmarkTools.jl`**: Estándar profesional. Ejecuta la función miles de veces para dar una media precisa.
    ```julia
    using BenchmarkTools
    @btime mi_funcion()
    ```

---
**Tags:** #Programacion #Conceptos #Glosario #IngenieriaSoftware
**Relacionado:** [[004_Python_to_Julia_Cheatsheet]]