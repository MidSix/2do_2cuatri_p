# Operadores Ternarios y Coalescencia Nula (C# vs Python)

En C#, el manejo de condiciones en una línea y valores nulos es más estricto y tiene operadores dedicados, a diferencia de Python que suele reutilizar palabras clave o evaluación de "truthiness".

## 1. El Operador Ternario (`? :`)

Permite realizar una asignación condicional en una sola línea.

### Sintaxis C#
```csharp
condicion ? valor_si_cierto : valor_si_falso;
```

### Sintaxis Python
```python
valor_si_cierto if condicion else valor_si_falso
```

### Ejemplo Práctico
Supongamos que queremos asignar una ruta por defecto si el usuario no escribe nada.

**En C#:**
```csharp
// string.IsNullOrWhiteSpace comprueba si es null, vacío o solo espacios
string target = string.IsNullOrWhiteSpace(input) ? defaultPath : input;
```

**En Python:**
```python
# En Python dependemos de que un string vacío sea "False"
target = input if input and not input.isspace() else default_path
```

---

## 2. El Operador de Coalescencia Nula (`??`)

Este operador es específico para manejar `null`. Si el valor de la izquierda es `null`, devuelve el de la derecha. Si no, devuelve el de la izquierda.

### Sintaxis C#
```csharp
variable = posible_nulo ?? valor_fallback;
```

### Sintaxis Python (Equivalente aproximado con `or`)
En Python no existe un operador exclusivo para `None`, se usa `or` aprovechando que `None` es falsy.
```python
variable = posible_nulo or valor_fallback
```
*Cuidado*: En Python, `0` o `False` también activarían el `or`. En C#, `??` **SOLO** salta si es estrictamente `null`.

### Ejemplo
Leer de la consola de forma segura (Console.ReadLine puede devolver null).

**En C#:**
```csharp
string name = Console.ReadLine() ?? "SinNombre";
```

**En Python:**
```python
name = input() or "SinNombre"
```

---

## 3. Tipos Nullable (`?`)

En C# (con `Nullable: enable` en el .csproj), las variables por defecto **no pueden ser nulas**. Debes marcar explícitamente que aceptas nulos.

*   `string` -> No puede ser null (debe tener un valor).
*   `string?` -> Puede ser string o null.
*   `int` -> No puede ser null (si no se asigna, es 0).
*   `int?` -> Puede ser un número o null (útil para bases de datos).

**Ejemplo:**
```csharp
string? input = Console.ReadLine(); // Puede devolver null
// string input = Console.ReadLine(); // Warning: Posible asignación de null
```
