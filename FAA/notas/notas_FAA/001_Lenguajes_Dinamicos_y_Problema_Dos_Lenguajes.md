# Lenguajes Dinámicos y el Problema de los Dos Lenguajes

Un **lenguaje dinámico** realiza comprobaciones (como el tipado) en tiempo de ejecución en lugar de en compilación (esto se traduce a que NO es necesario sintacticamente declarar los tipos, no te dara un error de sintaxis si no los declaras aunque sea buena practica si declararlos, Python y Julia, ambos son dinamicos). Esto favorece la flexibilidad y el prototipado rápido, pero históricamente penaliza el rendimiento.

## El Problema de los Dos Lenguajes
Tradicionalmente, el flujo de trabajo en ciencia de datos e ingeniería consistía en:
1. **Fase de prototipado:** Uso de lenguajes dinámicos y "lentos" (Python, R, MATLAB) por su facilidad de escritura.
2. **Fase de producción:** Reescribir el código crítico en lenguajes estáticos y "rápidos" (C, C++, Fortran) para obtener rendimiento.

Esto genera una brecha de mantenimiento, errores de traducción y duplicación de esfuerzo.

## La Propuesta de Julia
Hay dos tipos de lenguajes -> Estaticos y dinamicos, Julia es dinamico.
Julia busca resolver este dilema siendo un lenguaje con **sintaxis dinámica** (fácil de escribir, sin declaraciones obligatorias de tipos) pero con **rendimiento de lenguaje estático**. 
- Lo logra mediante **compilación JIT (Just-In-Time)** agresiva usando LLVM.
- El código se compila a código máquina específico para los tipos de datos en el momento de la primera ejecución.

---
**Tags:** #Julia #FAA #Programacion #LenguajesDinamicos
**Relacionado:** [[002_Multiple_Dispatch_Julia]]