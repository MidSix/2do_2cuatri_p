---
id: ejecucion-compilacion-csharp
aliases: [Entry Point, Main, Build Action, csproj]
tags:
  - ABIA
  - C_sharp
  - arquitectura
created: 2026-02-01
---

# 007 - Ejecución Monolítica: Proyecto vs. Archivo

En C#, la unidad mínima de ejecución y compilación **no es el archivo**, es el **Proyecto**. Esto define el comportamiento del lenguaje y el flujo de ejecución. Es decir, si tienes 3 modulos .cs en tu directorio, NO podras ejecutarlos por separado como scripts(cosa que si puedes hacer en python), NO puedes hacer esto porque la unidad de ejecucion en C# es el ejecutable resultante de unir TODOS los .cs, todos los modulos c_sharp de un mismo proyecto en un ejecutable que SIEMPRE empieza por el modulo que tenga la clase que contenga el metodo Main. De esta forma, si desde el metodo Main no llamas a los metodos del resto de tus modulos, pues no se ejecutaran.

## 1. La Unidad de Compilación (Assembly)
A diferencia de Python, donde el intérprete lee un archivo `.py` específico línea por línea, el compilador de C# (Roslyn) opera sobre el **Proyecto**.

En .NET moderno, el archivo `.csproj` tiene una regla implícita: **"Compila todos los archivos `*.cs` que encuentres en esta carpeta y subcarpetas"** / Basicamente implementa un filtro que permite ubicar solo los modulos .cs e incluirlos en la compilacion(antiguamente se listaban los archivos de tu programa que se iban a compilar uno a uno en el .csproj pero vieron que era un coñazo e implementaron este filtro para que por defecto se compile todos los .cs sin tener que escribirlos explicitamente, actualmente se dieron cuenta que era mas eficiente en lugar de listar todos los que quieres compilar, listar manualmente en el .csproj SOLO los que no quieres compilar, es en principio el unico caso en donde verias el nombre de tus archivos en el .csproj, solo para especificar que no quieres compilar un archivo).

*   **Consecuencia:** El compilador genera un único bloque binario (Assembly) con *todo* el código que encuentra. No es posible ejecutar un archivo `.cs` aisladamente.
*   **Visibilidad:** Todos los archivos del proyecto se "ven" entre sí automáticamente sin necesidad de importarse, porque acaban mezclados en el mismo binario final.
*   **Nota Técnica:** En versiones antiguas de .NET, los archivos sí se listaban uno a uno en el `.csproj`. Ahora la inclusión es automática por defecto.

## 2. El Determinismo del `Main`
Como el resultado es un único binario, el sistema operativo necesita un punto de entrada único y determinista.
*   El Runtime busca el método estático `static void Main(string[] args)`.
*   Cualquier código que no sea llamado directa o indirectamente desde `Main` es **código muerto** (se compila, ocupa espacio, pero nunca se ejecuta).
*   **Error de Múltiples Mains:** Si tienes dos archivos con `Main` en el mismo proyecto, el compilador falla porque no sabe cuál es el punto de entrada (salvo que lo fuerces en la configuración).

## 3. Cómo excluir archivos (Build Action)
Dado que C# intenta compilar todo lo que hay en la carpeta, si quieres guardar un archivo de "borrador" o "código viejo" sin que rompa la compilación, debes excluirlo explícitamente. No basta con no llamarlo.

Esto se hace modificando el archivo `.csproj` o las propiedades del archivo.

### Método: Cambiar la "Acción de Compilación"
Técnicamente, cambias el archivo de `Compile` a `None`.

**En el `.csproj`:**
```xml
<ItemGroup>
  <!-- Esto le dice al compilador: "Ignora este archivo" -->
  <Compile Remove="CodigoViejo.cs" />
  <None Include="CodigoViejo.cs" />
</ItemGroup>
```

Al hacer esto, el archivo existe físicamente en el disco, pero para el compilador es como si fuera un archivo de texto plano o una imagen; no intenta convertirlo en código ejecutable.

- \<Compile Remove="CodigoViejo.cs" /> Es la unica linea obligatoria, remueve del proceso de compilacion al modulo especificado

- \<None Include="CodigoViejo.cs" />  Es un metadato para el IDE, es recomendable escribirlo para hacerle saber a las herramientras de codificacion que dicho archivo no sera compilado, pero no es necesario, se puede borrar, pero mejor no xd.

---
**Resumen Técnico:**
*   **Python:** Ejecución por archivo. Multiples entry points posibles.
*   **C#:** Ejecución por Proyecto. Single entry point (`Main`). Todo o nada.

**Relacionado:**
*   [[005_Anatomia_Metodo_CSharp|Anatomía del Main]]
