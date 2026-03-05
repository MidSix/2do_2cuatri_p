## Contexto: ¿Por qué C#?

**Python** → _Scripting & AI Glue_ | Prototipado rápido, Scripts de automatización, Ciencia de Datos.
**C#** → _Enterprise & Systems_ | Desarrollo de aplicaciones robustas, Motores de Videojuegos (Unity), Backends de alto rendimiento (.NET).

# Python to C#: La Vía Robusta (Cheatsheet)

Esta guía asume que dominas Python y traduce esos conceptos a C# (versión moderna .NET 8+).
## ⚠️ La Diferencia #1: Estructura y Tipado
*   **Python:** Interpretado, tipado dinámico, indentación define bloques. Puedes escribir código "suelto".
*   **C#:** Compilado, tipado estático, llaves `{}` definen bloques. Todo código debe vivir dentro de una **Clase** y un **Método**. (En pyhon se dice: Todo es un objeto, aqui se puede decir: Todo en una clase y dentro de un metodo).

>C# y Java exigen que el codigo se organice SIEMPRE dentro de una clase y un metodo para obligar la organizacion del codigo. NO fue creado con enfoque hacia programas diminutos sino para programas empresariales gigantezcos de miles y miles o incluso millones de lineas de codigo donde poder ubicar rapidamente bloques de codigo y evitarse dolores de cabeza con los scopes es fundamental. Sigue una filosofia de archivadores si se quiere establecer alguna analogia -> Basicamente es mas lento y tedioso de escribir pero ofrece mayor seguridad de mantenimiento, visto el uso y el por que de este lenguaje parece probable que haga falta aprenderlo si se desea trabajar en multinacionales, puede que quizas no estos exactamente pero si sus variantes mas modernas como Kotlin, asi que renta aprenderlos. En resumen:
>Cuanto mas dinero hay en juego, mas estricto y ordenado suele ser el lenguaje exigido

## 1. Sintaxis Básica y Bloques

| Concepto                  | Python 🐍                                           | C# (Moderno) #️⃣                                                                     |
| :------------------------ | :-------------------------------------------------- | :----------------------------------------------------------------------------------- |
| **Bloques**               | Indentación obligatoria.                            | Llaves `{ ... }` (La indentación es estética pero recomendada).                      |
| **Fin de línea**          | Salto de línea.                                     | **Punto y coma `;`** (Obligatorio).                                                  |
| **Imprimir**              | `print("Hola")`                                     | `Console.WriteLine("Hola");`                                                         |
| **Leer teclado**          | `input()`                                           | `Console.ReadLine();`                                                                |
| **Interpolación**         | `f"Valor: {x}"`                                     | `$"Valor: {x}"` ($ va afuera).                                                       |
| **Variables**             | `x = 10` (Dinámico)                                 | `int x = 10;` o `var x = 10;` (Inferencia de tipos).                                 |
| **Booleanos**             | `True`, `False`                                     | `true`, `false` (minúscula) same as Julia.                                           |
| **Nulo**                  | `None`                                              | `null`                                                                               |
| **Operador AND**          | `and`                                               | `&&`                                                                                 |
| **Operador OR**           | `or`                                                | **\|\|**                                                                             |
| **Operador NOT**          | `not`                                               | `!`                                                                                  |
| **Coments single-line**   | `# comment`                                         | `// comment`                                                                         |
| **Coments multi-line**    | `"""comment"""`                                     | `/* comment */`                                                                      |
| **Convertir a int**       | `int()`                                             | `int.Parse("10")` o `Convert.ToInt32("10")`                                          |
| **Convertir a float**     | `float()`                                           | `float.Parse("10.5")` , `double.Parse("10.5")`                                       |
| **Longitud**              | `len(lista)`                                        | `lista.Count` o `array.Length`                                                       |
| **Obtener Tipo**          | `type(x)`                                           | `x.GetType()`                                                                        |
| **Cargar un modulo**      | `import pandas`                                     | **Automático** (si está en el `.csproj`)                                             |
| **1-Usar atajo**          | `import pandas as pd`                               | `using Newtonsoft.Json;` (No permite alias tipo `as pd`, solo acorta el prefijo).    |
| **2-Si borras la línea**  | El código falla (`NameError`).                      | El código funciona (si usas el nombre completo).                                     |
| **Instanciar clase**      | micoche  = Coche()                                  | **Coche** miCoche = **new** Coche();                                                 |
| **operador incremento**   | **intentos += 1**                                   | **intentos += 1**. Tienes: ++intentos y intentos++ pero xd. usa `+= `y ya.           |
| **Comparacion**           | `==`                                                | `==`                                                                                 |
| **Diferente**             | `!=`                                                | `!=`                                                                                 |
| **Mayor / Menor**         | `>`, `<`                                            | `>`, `<`                                                                             |
| **Mayor o igual**         | `>=`                                                | `>=`                                                                                 |
| **Division entera**       | `//`                                                | `/`                                                                                  |
| **Division**              | `/`                                                 | `/`                                                                                  |
| **Modulo**                | `%`                                                 | `%`                                                                                  |
| **Truncar decimales a 2** | `{valor:.2f}`                                       | `{valor:F2}`                                                                         |
| **Argumentos opcionales** | def x (y = 5):                                      | int x(int y = 5){ ... }zv                                                            |
| **LAMBDA**                | lambda argumentos: expresion                        | (argumentos) => expresion \|                 (argumentos) => {secuencia-expresiones} |
| **Op. Coalescencia nula** | `No hay pero ->resultado = p if x else y`           | `int resultado = null ?? 4 `                                                         |
| **Ternarios**             | valor_si_verdadero if condicion else valor_si_falso | condicion ? valor_si_verdadero : valor_si_falso                                      |


## 2. El "Boilerplate" Obligatorio
En Python puedes crear un archivo `script.py` y escribir `print("Hola")`. En C#, necesitas una estructura mínima (aunque .NET moderno permite *Top-level statements*, es vital entender la estructura clásica).

**Python:**
```python
# script.py
print("Hola Mundo")
```

**C# (Clásico/Estructurado):**
```csharp
// Program.cs
using System; // Importar namespace | Si tienes "<ImplicitUsings>enable</ImplicitUsings>" configurado en tu .csproj entonces el compilador escribira "using System" importando el espacio de nombres de System por ti sin necesidad de tener que escribirlo tu, por eso de tener configurado con esa marca el .csproj y escribiendo using System en tu .cs el linter te saltara un warning diciendo que no es necesario pues porque no lo es xd.

namespace MiProyecto
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hola Mundo");
        }
    }
}
```

## 3. Control de Flujo

### Condicionales
**Python:**
```python
if x > 0:
    print("Positivo")
elif x < 0:
    print("Negativo")
else:
    print("Cero")
```

**C#:**
```csharp
if (x > 0) 
{
    Console.WriteLine("Positivo");
}
else if (x < 0) // Nota: else if separado
{
    Console.WriteLine("Negativo");
}
else
{
    Console.WriteLine("Cero");
}
```

### Bucles
**Python:**
```python
# Rango 0 a 9
for i in range(10):
    print(i)

# Iterar lista
for item in lista:
    print(item)

while condicion:
	cuerpo
```

**C#:**
```csharp
// Rango 0 a 9
for (int i = 0; i < 10; i++) 
{
    Console.WriteLine(i);
}

// Iterar colección (El equivalente directo a 'for x in y')
foreach (var item in lista)
{
    Console.WriteLine(item);
}

while (condicion)
{
	cuerpo
}
```

## 4. Colecciones (Arrays vs Listas)

En Python, las listas son dinámicas. En C#, hay diferencia entre **Array** (fijo) y **List** (dinámica).

| Concepto           | Python 🐍                    | C# #️⃣                                                                       |
| :----------------- | :--------------------------- | :--------------------------------------------------------------------------- |
| **Lista Dinámica** | `lista = [1, 2, 3]` - list() | `List<int> lista = [1, 2, 3];`                                               |
| **Array Fijo**     | (No nativo, usas listas)     | `int[] array = new int[size];` `array[0] = elem1`; `array[1] = elem2` ...    |
| **Añadir**         | `lista.append(4)`            | `lista.Add(4);` (Solo en List, no en Array)                                  |
| **Longitud**       | `len(lista)`                 | `lista.Count` (Listas) o `array.Length` (Arrays). **Propiedad, no función**. |
| **Acceso**         | `lista[0]`                   | `lista[0]`                                                                   |
| **Diccionario**    | `d = {"a": 1}`               | `var d = new Dictionary<string, int> { {"a", 1} };`                          |
| **Array Fijo v2**  | (No nativo, usas listas)     | `type[] name_array = {elem1,elem2,elem3};`                                   |
| **Lista vacia**    | `lista = []`                 | `public List<tipo> name = new List<tipo>();`                                 |

## 5. Funciones

**Python:**
```python
def suma(a, b):
    return a + b
```

**C#:**
```csharp
// Debes especificar tipos (o usar templates/generics)
// 'public' y 'static' son modificadores de acceso y contexto
public static int Suma(int a, int b) 
{
    return a + b;
}
```

### Funciones Anonimas (Lambda Expressions)
Similar a los one-liners de Julia o lambdas de Python.

**C#:**
```csharp
Func<int, int, int> suma = (a, b) => a + b;
(a, b) => a + b; //Si no la quieres guardar en una variable.
(a, b) => {a + b;a - b;a * b;}; //secuencia de instrucciones.
```

## 6. LINQ (La Joya de C#)
Lo que en Python haces con *List Comprehensions*, en C# se hace con **LINQ** (Language Integrated Query). Es SQL para objetos.

**Python:**
```python
cuadrados = [x**2 for x in lista if x > 5]
```

**C#:**
```csharp
using System.Linq;

// Sintaxis de Métodos (Lambda) - La más usada
var cuadrados = lista.Where(x => x > 5).Select(x => x * x).ToList();

// O Sintaxis de Query (SQL-like)
var cuadrados = from x in lista
                where x > 5
                select x * x;
```

## 7. Clases y Objetos (OOP)

C# es puramente orientado a objetos.

**Python:**
```python
class Persona:
    def __init__(self, nombre):
        self.nombre = nombre
    
    def saludar(self):
        print(f"Hola {self.nombre}")
```

**C#:**
```csharp
public class Persona
{
    // Propiedad (Getter y Setter automático)
    public string Nombre { get; set; }

    // Constructor
    public static void Persona(string nombre)
    {
        Nombre = nombre; // No necesitas 'self', el ámbito se resuelve solo (o usa 'this')
    }

    public void Saludar()
    {
        Console.WriteLine($"Hola {Nombre}");
    }
}
```

## 8. Manejo de Excepciones (Try/Catch/Finally)

El concepto es idéntico, pero la sintaxis cambia. En lugar de `except`, C# usa `catch` "igual que Julia by the way".

| Concepto              | Python 🐍                | C# #️⃣                        |
| :-------------------- | :----------------------- | :---------------------------- |
| **Bloque de intento** | `try:`                   | `try { ... }`                 |
| **Captura de error**  | `except Exception as e:` | `catch (Exception e) { ... }` |
| **Ejecución final**   | `finally:`               | `finally { ... }`             |

**Python:**
```python
try:
    resultado = 10 / 0
except ZeroDivisionError as e:
    print(f"Error específico: {e}")
except Exception as e:
    print(f"Ocurrió un error general: {e}")
finally:
    print("Esta línea se ejecuta siempre.")
```

**C#:**
```csharp
try
{
    // Código que podría fallar
    int resultado = 10 / int.Parse("0"); 
}
catch (DivideByZeroException e)
{
    // Captura un tipo de error específico
    Console.WriteLine($"Error específico: {e.Message}");
}
catch (FormatException e)
{
    // Captura otro tipo de error específico
     Console.WriteLine($"Error de formato: {e.Message}");
}
catch (Exception e) // 'Exception' es la clase base para todos los errores
{
    // Captura cualquier otro error no manejado arriba
    Console.WriteLine($"Ocurrió un error general: {e.Message}");
}
finally
{
    // Este bloque se ejecuta siempre, haya error o no.
    // Ideal para limpiar recursos (cerrar archivos, conexiones, etc.)
    Console.WriteLine("Esta línea se ejecuta siempre.");
}
```

## 9. Programación Orientada a Objetos (POO) Avanzada

| Concepto               | Python 🐍                   | C# #️⃣                                      |
| :--------------------- | :-------------------------- | :------------------------------------------ |
| **Instanciación**      | `obj = MiClase()`           | `MiClase obj = new MiClase();`              |
| **Herencia**           | `class Hija(Padre):`        | `class Hija : Padre { ... }`                |
| **Llamar al Padre**    | `super().__init__()`        | `: base()` (en la firma del constructor)    |
| **Polimorfismo**       | Dinámico (Duck Typing)      | `virtual` (en padre) y `override` (en hijo) |
| **Abstracción (G/S)**  | `@property` / `@x.setter`   | `{ get; set; }` (Propiedades automáticas)   |
| **Métodos Abstractos** | `@abstractmethod`           | `abstract void Metodo();`                   |
| **Herencia Múltiple**  | Soportada: `class C(A, B):` | **No soportada** (se usan Interfaces)       |

### Ejemplo de Herencia y Polimorfismo

**Python:**
```python
class Animal:
    def hablar(self):
        pass

class Perro(Animal):
    def hablar(self):
        print("Guau")
```

**C#:**
```csharp
public class Animal 
{
    // 'virtual' permite que los hijos sobrescriban el método
    public virtual void Hablar() 
    {
        Console.WriteLine("Sonido genérico");
    }
}

public class Perro : Animal 
{
    // 'override' indica que estamos rediniendo el comportamiento
    public override void Hablar() 
    {
        Console.WriteLine("Guau");
    }
}
```

### Ejemplo de Getters y Setters (Propiedades)

En C# no solemos usar métodos `get_nombre()` y `set_nombre()`. Usamos **Propiedades**, al igual que en python desde la >v2.2.

- **Pragmaticamente**: Estas propiedades basicamente permiten **acceder** y **modificar** un atributo de un objeto sin necesidad de escribir los parentesis -> "()", mi_objeto.metodo() y mi_objeto.propiedad. Ambas pueden albergar el codigo que implemente el concepto de getter y setter pero una forma es mas comoda que otra (la que implica escribir menos basicamente).

- **Matiz semantico de propiedades vs metodos**:
   1. Propiedad (`.propiedad`): Se usa para lo que el objeto ES o TIENE (Estado).
       * Ejemplo: persona.Nombre, lista.Count (Longitud).
       * Sensación: "Dame este dato rápido".
   2. Método (`.metodo()`): Se usa para lo que el objeto HACE (Comportamiento) o si la operación es costosa.
       * Ejemplo: persona.Caminar(), lista.Sort() (Ordenar cuesta trabajo a la CPU).
       * Sensación: "Ejecuta esta acción".

**Python:**
```python
class Cuenta:
    def __init__(self):
        self._saldo = 0

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        if valor >= 0:
            self._saldo = valor
```

**C#:**
```csharp
public class Cuenta
{
    private decimal _saldo;

    public decimal Saldo
    {
        get { return _saldo; }
        set 
        { 
            if (value >= 0) _saldo = value; // 'value' es una palabra reservada
        }
    }
}
```

---
**Tags:** #CSharp #Python #Cheatsheet #Sintaxis #ABIA #POO
**Relacionado:** [[900university/2do_curso/2do_cuatri/FAA/notas/notas_FAA/004_Python_to_Julia_Cheatsheet|Python to Julia Cheatsheet]]
