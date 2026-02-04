# Cache vs. Artefactos Necesarios (Build vs. Scripting)

**Fecha:** 2026-02-01
**Etiquetas:** #compilacion #python #csharp #arquitectura_software #optimizacion

## La Distinción Fundamental
La diferencia entre un modelo de **Scripting** (Python, Julia) y un modelo de **Construcción** (C#, Java, C) **no** es si generan archivos temporales, ambos lo hacen

### 1. Archivos de Caché (Opcionales)
Ambos modelos generan archivos para acelerar ejecuciones posteriores.
- **Python:** Genera `__pycache__` (`.pyc`).
- **C#:** Genera directorio `obj/`.
- **Característica:** Son **desechables**. Si eliminas estos directorios, el programa simplemente los regenerará en la siguiente ejecución sin fallar. No son bloqueantes.

### 2. Archivos de Artefacto (Necesarios)
Aquí radica la diferencia del modelo de Construcción.
- **Modelo Scripting (Python):** La "fuente de la verdad" para la ejecución es el código fuente (`.py`). No existe un archivo intermedio obligatorio independiente del fuente.
- **Modelo Build (C#):** La ejecución **depende** de la existencia de un artefacto final (`bin/` -> `.dll` / `.exe`).
    - Si borras el directorio `bin/`, el runtime no puede ejecutar el programa directamente; **exige** un paso previo de reconstrucción.
    - El código fuente (`.cs`) no es ejecutable por sí mismo; es solo el plano para crear el artefacto ejecutable.

## Resumen
- **Scripting:** Source Code -> Ejecución (Cache es un bonus).
- **Build:** Source Code -> **Artefacto Obligatorio** -> Ejecución (Cache es ayuda para crear el artefacto).
