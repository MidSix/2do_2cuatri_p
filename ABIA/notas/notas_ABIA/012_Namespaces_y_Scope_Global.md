# 012 - Namespaces y Scope Global en C#

**Fecha:** 2026-02-03
**Tags:** #csharp #namespaces #scope #arquitectura #analogias

## Concepto
En C#, la organización del código es **lógica**, no física (a diferencia de otros lenguajes donde la estructura de carpetas define los módulos). Esta organización lógica se consigue mediante **Namespaces**.
```csharp
using TGR_1;
/*
    Estamos trayendo el namespace que creamos en el resto de .cs .
    Sin traer el namespace, aunque podemos comunicarnos con el resto de
    .cs al estar en el mismo proyecto tendriamos que hacerlo
    antecediendo el nombre del namespace. La lista nos quedaria asi:
    List<TGR_1.Student> students = new List<TGR_1.Student>();. Ahora.
    los modulso .cs al estar en el mismo workspace con el mismo proyecto
    se agregan a un namespace global, entonces no es necesario crear un
    namespace propio para tus modulos. Pero es recomendable y mas seguro
    hacer esto, Por que? Todos los paquetes externos viven en el
    namespace global, eso quiere decir que si por mala suerte
    instalaste un paquete ruso de la deepweb que uno de sus
    metodos/clases se llama igual a una de las que tienes en tus modulos
    pues surge una incompatibilidad y no compilara el programa.
    Para evitar esto es un estandar en la industria crear un namespace
    especifico para tus proyectos que vivan independientes al global y
    dejar el global solo para los paquetes de terceros, de esta forma
    se reducen los fallos de dependencias. Ya gemini me acostumbro
    a hablar con analogias, puedes pensar en un scope propio fuera del
    global del workspace como workspace(estamos en la misma LAN,
    estamos conectados, pero se creo una subred[scope propio] que nos
    separa).
*/
```
### Analogía de Redes (VLANs / Subredes)
Podemos entender los namespaces utilizando conceptos de redes:

1.  **Namespace Global (La LAN Plana):**
    *   Es el espacio por defecto donde vive el código si no se especifica nada.
    *   **Analogía:** Una red local donde todos los dispositivos están conectados al mismo switch sin segmentar. Todos se ven directamente por su nombre.
    *   **Comportamiento en C#:** Si tienes una clase `Student` sin namespace y un `Program.cs` sin namespace, ambos están en el "Global Namespace" y se ven sin necesidad de `using`.
    *   **Riesgo:** Colisiones de nombres (dos clases `Student` romperían el programa) y desorganización en proyectos grandes.

2.  **Namespaces Declarados (Las VLANs/Subredes):**
    *   Cuando envuelves código en `namespace MiProyecto.Logica { ... }`, estás aislando ese código en su propia "subred".
    *   **Analogía:** Mover dispositivos a una VLAN específica (ej. VLAN 10). Los dispositivos fuera de esa VLAN no pueden verlos directamente.

3.  **La directiva `using` (El Enrutamiento):**
    *   Para que el código en el espacio Global (o en otro namespace) vea una clase dentro de un namespace específico, necesitas importarlo.
    *   **Analogía:** Configurar una ruta o un puente que permite el tráfico desde la red actual hacia la subred destino. `using TGR_1;` le dice al compilador: "Si no encuentras el nombre aquí, búscalo también en la subred TGR_1".

## Top-Level Statements
En las versiones modernas de C# (.NET 6+), el archivo `Program.cs` suele usar **Top-Level Statements** (código directo sin `class Program` ni `Main`).
*   **Por defecto:** Este código reside en el **Namespace Global**.
*   **Consecuencia:** Si tus clases (`Student.cs`) tienen un namespace definido (`namespace TGR_1`), el `Program.cs` no las verá automáticamente a menos que uses `using TGR_1;` o muevas el `Program.cs` al mismo namespace (usando `namespace TGR_1;` al inicio del archivo).

## Buenas Prácticas
Aunque usar el espacio global es cómodo para scripts rápidos, el estándar industrial ("Filosofía del Archivador") dicta que **todo código debe pertenecer a un namespace explícito** (generalmente coincidiendo con el nombre del Proyecto) para evitar conflictos al integrar librerías de terceros.
