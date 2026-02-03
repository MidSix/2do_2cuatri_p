# Guía de Contenidos: Ejercicios 1, 2 y 3 (Práctica 1)

Esta nota resume los prerrequisitos teóricos y el enfoque recomendado para abordar los primeros tres ejercicios de la Práctica 1.

## Ejercicio 1: Introducción a Julia y Preprocesamiento
*   **Enfoque:** Tutorial práctico de programación matricial.
*   **¿Necesito Teoría?** **NO.**
    *   El PDF del enunciado es autocontenido. Explica las fórmulas matemáticas necesarias para la normalización (Min-Max, Z-Score) y la codificación de variables categóricas.
    *   La segunda mitad del documento sirve como manual de referencia de Julia (`size`, `mean`, `convert`, broadcasting).
*   **Objetivo:** Familiarizarse con la sintaxis de Julia y la manipulación de datos, no profundizar en ML.

## Ejercicio 2: Entrenamiento de RRNNAA (Redes Neuronales)
*   **Enfoque:** Introducción a la librería `Flux` (Deep Learning en Julia).
*   **¿Necesito Teoría?** **Opcional (Recomendado Tema 2.3).**
    *   El PDF explica *cómo* implementar el código (`Chain`, `Dense`, `Flux.train!`), pero asume cierta familiaridad con conceptos básicos:
        *   ¿Qué es una capa densa (totalmente conectada)?
        *   ¿Qué es una función de activación (sigmoide vs. identidad)?
        *   ¿Qué es One-Hot-Encoding?
    *   **Referencia Teórica:** Si estos términos te suenan a chino, consulta `Teoría/Tema 2/Tema 2.3 - Redes de Neuronas Artificiales.pdf`.

## Ejercicio 3: Sobreentrenamiento y Validación
*   **Enfoque:** Metodología experimental y visualización de datos.
*   **¿Necesito Teoría?** **NO.**
    *   El documento explica detalladamente y desde cero los conceptos clave:
        *   **Hold-Out:** Partición de datos en Entrenamiento, Validación y Test.
        *   **Early Stopping (Parada Temprana):** Técnica de regularización para evitar el sobreajuste.
    *   Incluye un tutorial final sobre la librería `Plots.jl` para generar las gráficas de curvas de aprendizaje.

---
**Resumen de Acción:**
1.  Ataca el **Ej. 1** y **Ej. 3** directamente con el enunciado en mano.
2.  Para el **Ej. 2**, ten abierto el **Tema 2.3** por si necesitas aclarar qué hace una "neurona" conceptualmente.

---
**Tags:** #FAA #Practica1 #Julia #Flux #RRNNAA #GuiaEstudio