---
id: contexto-importaciones-csharp
aliases: [Namespaces, using vs import, NuGet]
tags:
  - ABIA
  - C_sharp
  - arquitectura
created: 2026-02-01
---

# 006 - Contexto e Importaciones: ¿Dónde está mi `import`?

Al venir de Python, es normal buscar la instrucción `import numpy` y sorprenderse al no encontrarla. En C#, el concepto de "traer código de fuera" se divide en dos pasos separados mientras que en python todo se resuelve en una sola linea y por tanto visualmente en un solo paso.

## 1. El mito del `import`
En Python, `import math` hace dos cosas a la vez:
1.  Busca el archivo en el disco.
2.  Lo carga en memoria para que lo uses.

**En C#, no existe una instrucción de código que "cargue" un paquete.** El código ya está cargado por el compilador antes de que empiece a ejecutarse la primera línea.

## 2. Los dos pasos de "C#"

### Paso A: La Referencia
*   **¿Qué es?** Es decirle al proyecto: "Necesito este paquete externo".
*   **¿Dónde se hace?** No en el código `.cs`, sino en el archivo de proyecto `.csproj` (o vía comando `dotnet add package`).
*   **Analogía:** Es comprar el libro y ponerlo en la estantería de tu biblioteca.
*   **Herramienta:** **NuGet** (es el `pip` de C#).

### Paso B: El `using` (El Atajo / Post-it)
*   **¿Qué es?** Es decirle al compilador: "No quiero escribir el nombre completo cada vez". Es el que importa el namespace del modulo.
*   **Efecto:**
    *   **Sin using:** Debes escribir `Newtonsoft.Json.JsonConvert.SerializeObject(...)`.
    *   **Con using:** Escribes `JsonConvert.SerializeObject(...)`.

> **Diferencia Clave:** Si borras el `using`, el código sigue funcionando (si escribes la ruta completa). Si borras la referencia al paquete, el código explota porque no lo encuentra.

## 3. ¿Por qué `using System;` es innecesario?
Si ves que tu IDE te marca `using System;` en gris (innecesario), es por lo que permite la evolución de C# (.NET 6+) con los global usings declarados en el .csproj.

### Global Usings
Microsoft decidió que escribir `using System;` en los 500 archivos de un proyecto era perder el tiempo. Ahora, el archivo `.csproj` suele tener activada la opción `<ImplicitUsings>enable</ImplicitUsings>`.

Esto significa que el compilador **inyecta automáticamente** los namespaces más comunes (`System`, `System.Linq`, `System.Collections.Generic`) en todos tus archivos, aunque tú no los veas.

## Resumen Comparativo

| Acción                 | Python 🐍                      | C# #️⃣                                                                                        |
| :--------------------- | :----------------------------- | :-------------------------------------------------------------------------------------------- |
| **Instalar paquete**   | `pip install pandas`           | `dotnet add package Newtonsoft.Json`                                                          |
| **Cargar en script**   | `import pandas`                | **Automático** (si está en el `.csproj`).                                                     |
| **Usar atajo**         | `import pandas as pd`          | `using Newtonsoft.Json;` (No permite alias tipo `as pd` globalmente, solo acorta el prefijo). |
| **Si borras la línea** | El código falla (`NameError`). | El código funciona (si usas el nombre completo).                                              |
|                        |                                |                                                                                               |
Es en .csproj donde los modulos se referencian, NO en los modulos .cs individuales. El conjunto de paquetes por defecto se referencian en \<Project Sdk="Microsoft.NET.Sdk">

---
**Tags:** #CSharp #Arquitectura #NuGet
**Relacionado:** [[005_Metodos,Clases_CSharp|Anatomía de un Método]]
