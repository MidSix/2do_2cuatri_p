# Diccionarios de Funciones: Action y Func

Este patrón permite eliminar largas cadenas de `if-else` o `switch` almacenando referencias a métodos dentro de un `Dictionary`. En Python esto es trivial debido al tipado dinámico; en C# requiere el uso de **Delegados** (`Action` o `Func`) para definir la firma(los types, tipos) de las funciones almacenadas.

## 1. Concepto: El Delegado
En C#, para guardar una función en una variable (o en un valor de un diccionario), debemos especificar su "firma" (qué recibe y qué devuelve). Usamos dos tipos genéricos estándar:

*   **`Action`**: Para métodos que **NO devuelven valor** (`void`).
*   **`Func<...>`**: Para métodos que **SÍ devuelven valor**.

## 2. Implementación con `Action` (Void)
Ideal para menús de consola o ejecución de comandos simples.

```csharp
// Definición: Diccionario donde la CLAVE es string y el VALOR es una función vacía.
// Dictionary<string (Tipo de la clave), Action (Tipo del valor)>
Dictionary<string, Action> menu = new Dictionary<string, Action>

    { "1", () => Console.WriteLine("Opción Uno") },       // Lambda
    { "2", MiMetodoDefinido },                            // Referencia a método existente
    { "3", () => {                                        // Bloque Lambda multilínea
        Console.WriteLine("Calculando...");
        Console.WriteLine("Hecho."); 
    }}
};

// Ejecución
string opcion = "1";
if (menu.ContainsKey(opcion))
{
    menu[opcion](); // Los paréntesis () invocan la función almacenada
}
```

## 3. Implementación con `Func` (Retorno)
Si necesitas que la función devuelva algo (ej. operaciones matemáticas).
El **último tipo** en `<...>` es siempre el tipo de retorno.

```csharp
// <string, int, int>: Recibe string e int, Devuelve int.
// Aquí: Clave (string), Valor (Función que toma 2 ints y devuelve un int)
Dictionary<string, Func<int, int, int>> operaciones = new Dictionary<string, Func<int, int, int>>
{
    { "suma", (a, b) => a + b },
    { "resta", (a, b) => a - b },
    { "mult", (a, b) => a * b }
};

// Uso
int resultado = operaciones["suma"](5, 3); // Devuelve 8
```

## 4. Restricción de Tipado (Diferencia con Python)
A diferencia de Python, donde un diccionario puede contener funciones con diferentes argumentos, en C# **todas las funciones del diccionario deben compartir la misma firma**.

*   ❌ No puedes mezclar un `Action` (sin parámetros) con un `Action<int>` (con un int) en el mismo diccionario.
*   ✅ Solución: Si necesitas flexibilidad total, tendrías que usar `Dictionary<string, Delegate>` o `object` y hacer casting manual (no recomendado por seguridad de tipos), o un patrón de diseño más complejo (Command Pattern).

## 5. Ventajas
*   **Complejidad Ciclomática**: Reduce estructuras anidadas complejas.
*   **Rendimiento**: El acceso es O(1) en lugar de O(N) secuencial de un `if-else`.
*   **Extensibilidad**: Añadir un caso nuevo es solo añadir una línea al diccionario, no modificar la lógica de control.


# Creating a Dictionary

Import the namespace `System.Collections.Generic` first. Declare with key and value types like this:

```csharp
Dictionary<int, string> countries = new Dictionary<int, string>();
```
- Initialize with data directly:

```csharp
Dictionary<int, string> countries = new Dictionary<int, string>() 
{     
	{1, "USA"},    
	{44, "UK"} 
};
```
- Keys must be unique; duplicates throw exceptions.[source](https://www.geeksforgeeks.org/c-sharp/dictionary-in-c-sharp/)

## Adding Elements

Use `Add(key, value)` for new pairs:
```csharp
countries.Add(33, "France");
```

Or assign via indexer (overwrites if key exists):

```csharp
countries[55] = "India";
```
This keeps code concise for updates.[source](https://www.koderhq.com/tutorial/csharp/dictionary/)

## Accessing Elements

Retrieve by key using indexer:

```csharp
//dictionary_identifier[index];
Console.WriteLine(countries[1]);  // Outputs: USA`
```

Check existence safely with `TryGetValue`:

csharp

`if (countries.TryGetValue(44, out string value)) {     Console.WriteLine(value);  // Outputs: UK }`

Avoids KeyNotFoundException on missing keys.[](https://stackify.com/c-dictionary-how-to-create-one-and-best-practices/)

## Iterating Dictionary

Loop with `foreach` over `KeyValuePair`:

csharp

`foreach (KeyValuePair<int, string> pair in countries) {     Console.WriteLine($"{pair.Key}: {pair.Value}"); }`

Outputs all pairs efficiently.[](https://www.programiz.com/csharp-programming/dictionary)

## Removing Elements

Use `Remove(key)` to delete:

csharp

`countries.Remove(1);`

Clear all with `Clear()` or check count via `Count` property.[](https://zetcode.com/csharp/dictionary/)

## Common Methods

|Method|Purpose|Example Output|
|---|---|---|
|ContainsKey|Check if key exists [](https://www.koderhq.com/tutorial/csharp/dictionary/)​|true/false|
|ContainsValue|Check if value exists [](https://www.koderhq.com/tutorial/csharp/dictionary/)​|true/false|
|Keys|Get all keys as collection [](https://www.programiz.com/csharp-programming/dictionary)​|KeyCollection|
|Values|Get all values as collection [](https://www.programiz.com/csharp-programming/dictionary)​|ValueCollection|

---
**Tags:** #CSharp #Patrones #Diccionarios #Delegados #CleanCode
**Relacionado:** [[004_Python_to_CSharp_Cheatsheet]]