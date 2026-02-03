# Fase de Construcción vs. Modelo de Scripting

**Fecha:** 2026-02-01
**Etiquetas:** #arquitectura_software #compilacion #scripting #csharp #julia #python

## Concepto Clave
La necesidad de un "Archivo de Proyecto" (como `.csproj`) **no depende** estrictamente de si un lenguaje es Compilado Ahead-Of-Time (AOT) o Just-In-Time (JIT). Depende de la **Filosofía de Construcción (Build Workflow)** elegida por el ecosistema del lenguaje.

## 1. Modelo de "Fase de Construcción" (Build Phase)
*   **Ejemplos:** C# (.NET), Java, C++, Rust, C.
*   **Características:**
    *  Requiere generar un **artefacto intermedio** o final en disco (`.dll`, `.exe`, `.class`) **antes** de poder ejecutar cualquier lógica. -> Es decir: En el intento de ejecutar el codigo se crearan archivos finales como .exe e intermedios como .dll que son los que se ejecutaran. Cuando compilas en C te devuelve un archivo .exe justo en el mismo directorio en donde se encuentra el codigo que compilaste(con configuraciones por defecto), sin embargo lenguages como C# o Java son mas ordenados, SI generan estos archivos pero no los liberan justo en tu espacio de trabajo sino dentro del directorio bin/Debug/net10.0 (Aqui como podras adivinar depende de la version del framework que tengas, si tienes la version 8 pues sera net8.0 y no net10.0) y ahi estaran.  
    
    *   Es un proceso "Todo o Nada": El compilador necesita un inventario completo (el archivo de proyecto) para validar y enlazar todos los símbolos. Si falta una pieza, no se genera el artefacto.
    
    *   **C# es el caso clave:** A pesar de ejecutarse via JIT (CLR), exige esta fase de construcción previa para empaquetar el CIL (Common Intermediate Language).

## 2. Modelo de "Scripting" (Ejecución Directa)
*   **Ejemplos:** Python, Julia, JavaScript.
*   **Características:**
    *   El entorno de ejecución (runtime) ingiere directamente el **código fuente**. NO genera archivos intermedios, ademas de cache, para la ejecucion del codigo.
    *   Las dependencias se resuelven de forma dinámica o secuencial durante la ejecución (via `import` o `include`).
    *   **Julia es el caso clave:** Es un lenguaje compilado (JIT de alto rendimiento), pero su flujo de trabajo es de scripting. No necesita un `.csproj` para correr varios archivos porque los compila en memoria a medida que los descubre, sin exigir un empaquetado previo en disco.

## Conclusión
La distinción real no es "Compilado vs. Interpretado", sino **"Empaquetado Previo vs. Ingesta Directa"** Build-lenguage vs scripting-language.

- Ambos modelos de ejecucion generan archivos temporales para acelerar posteriores ejecuciones. Python los genera en el Pycache y C# en el directorio obj (object - intermediate) por ejemplo. La diferencia real radica en si generan archivos intermedios o finales NECESARIOS para la ejecucion del codigo (ten en cuenta que el cache NO es necesario para la ejecucion del codigo, si eliminas el directorio con la cache el programa tras ejecutarse simplemente lo volvera a generar, mientras que si eliminas archivos necesarios para la ejecucion el programa simplemente no podra ejecutarse). Los que tienen modelo scripting NO los generan mientras que los que tienen modelo build SI los generan.