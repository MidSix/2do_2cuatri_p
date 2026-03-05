# Operadores para Null en C#

null operators
En C#, el manejo de nulos es más estricto que en otros lenguajes (como Python). Para evitar el famoso `NullReferenceException`, existen varios operadores específicos.

---

## 1. Tipos Nullables (`Tipo?`)
Permite que un tipo de valor (como `int`, `bool`, `double`) acepte el valor `null`. Por defecto, los tipos de valor no son nulables.

- **Código:**
```csharp
int? edad = null;
Console.WriteLine(edad == null ? "No asignada" : edad.ToString());
```
- **Salida:** `No asignada`

---

## 2. Operador ternario (`?`)
Elegir entre a o b según una condición ` cond ? a : b `
- **Código:**
```csharp
Console.WriteLine(longitud == null ? "Nulo" : longitud.ToString());
```
- **Salida:** `Nulo`

## 3.Null-conditional
 Acceder a algo solo si a existe.  `a?.b`,    `a?[b]`. 
 - **Código**
```csharp
string nombre = null;
int? longitud = nombre?.Length;
```

---

## 4. Operador Null-Coalescing (`??`)
Devuelve el valor del operando izquierdo si no es nulo; de lo contrario, devuelve el operando derecho (un valor por defecto).

- **Código:**
```csharp
string entrada = null;
string resultado = entrada ?? "Valor por defecto";
Console.WriteLine(resultado);
```
- **Salida:** `Valor por defecto`

---

## 5. Asignación Null-Coalescing (`??=`)
Asigna el valor del operando derecho al izquierdo solo si el izquierdo es nulo.

- **Código:**
```csharp
List<string> nombres = null;
nombres ??= new List<string>(); // Si es null, inicializa la lista
nombres.Add("Sebastian");
Console.WriteLine(nombres.Count);
```
- **Salida:** `1`

---

## 6. Operador Null-Forgiving (`!`)
Es una instrucción al compilador: "Sé que esto parece que podría ser nulo, pero te aseguro que no lo será en tiempo de ejecución". No tiene efecto en ejecución, solo silencia avisos del compilador.

- **Código:**
```csharp
string? texto = ObtenerNombreDeBD(); 
Console.WriteLine(texto!.Length); // Forzamos al compilador a ignorar el posible nulo
```
- **Nota:** Si `texto` resulta ser nulo en ejecución, lanzará un error. Úsalo con precaución.

---

## 7. Operador de Acceso a Índice Condicional (`?[]`)
Similar a `?.`, pero para colecciones o arrays. Accede al índice solo si la colección no es nula.

- **Código:**
```csharp
int[] numeros = null;
int? primerElemento = numeros?[0];
Console.WriteLine(primerElemento == null ? "Array nulo" : primerElemento.ToString());
```
- **Salida:** `Array nulo`
