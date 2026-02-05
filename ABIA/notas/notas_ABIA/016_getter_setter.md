# 016_Propiedades_Full_vs_Auto_y_Validacion.md

## Concepto: De Auto-Properties a Full Properties
En C#, cuando escribes `public int Age { get; set; }`, el compilador genera "mágicamente" un campo privado para guardar el dato. Esto es genial para prototipar, pero **impide validar** datos porque no tienes control sobre la asignación.

### Sintaxis por defecto (Auto-Implemented Properties)
Si no necesitas validación, C# permite escribirlo en una sola línea. Es el equivalente a declarar un atributo público en Python, pero manteniendo la estructura de propiedad por si quieres cambiarla en el futuro sin romper el código que usa la clase.

```csharp
// Solo lectura (Solo Getter)
public string Species { get; } = "Human";

// Lectura y Escritura (Getter y Setter por defecto)
public int Age { get; set; }
```

Para validar (ej. que la edad no sea negativa), debes pasar a **Full Properties**. Esto requiere declarar explícitamente un **Backing Field** (la variable privada real).

---

## Comparativa: Python vs C#

### 1. El concepto de "Backing Field"
Ambos lenguajes necesitan un lugar privado donde guardar el dato real. La propiedad pública es solo el "portero" o la interfaz.

*   **Python:** Se usa la convención del guion bajo `_variable`.
*   **C#:** Se declara explícitamente `private _variable;`.

### 2. Sintaxis de Validación

#### 🐍 Python (Decoradores)
Python separa el getter y el setter en funciones distintas decoradas.

```python
class Student:
    def __init__(self, age):
        self._age = age  # "Backing field" (convención)

    # GETTER
    @property
    def age(self):
        return self._age

    # SETTER
    @age.setter
    def age(self, value):
        # La validación ocurre aquí
        if value < 0:
            raise ValueError("La edad no puede ser negativa")
        self._age = value # Asignación al campo privado
```

#### #️⃣ C# (Bloques Get/Set)
C# agrupa todo dentro de la propiedad. Utiliza la palabra clave reservada **`value`** (equivalente al argumento `value` del setter de Python) que representa el dato que están intentando asignar.

```csharp
public class Student
{
    // 1. Backing Field (Privado, donde vive el dato real)
    private int _age; 

    // 2. Propiedad Pública (El portero)
    public int Age 
    {
        get 
        { 
            return _age; 
        }
        set 
        {
            // La variable "value" es mágica/reservada: trae el dato entrante.
            if (value < 0) 
            {
                throw new ArgumentException("La edad no puede ser negativa");
            }
            _age = value; // Si pasa el filtro, guardamos en el campo privado
        }
    }
}
```

---

## Puntos Clave para la Transición

1.  **La palabra clave `value`:** En C# no declaras el argumento del setter (como `def age(self, value)`). Simplemente usas `value` dentro del bloque `set`; C# ya sabe que es el dato entrante.
2.  **Recursividad Infinita (El error clásico):** 
    *   ❌ `set { Age = value; }` -> Esto llama al setter a sí mismo infinitamente -> **StackOverflow**.
    *   ✅ `set { _age = value; }` -> Esto guarda el dato en la variable privada.
3.  **Convención de Nombres:**
    *   Propiedad Pública: `PascalCase` (`Age`).
    *   Campo Privado: `camelCase` con guion bajo (`_age`).

### 1. Asignar al Campo (`_name = name`)
*   **Qué hace:** Escribe directamente en la memoria.
*   **Consecuencia:** **Sáltate el setter**. No hay validación.
*   **Uso:** Solo cuando el dato viene de una fuente ya validada (ej. base de datos) y quieres velocidad.

### 2. Asignar a la Propiedad (`Name = name`)
*   **Qué hace:** Llama al bloque `set { ... }`.
*   **Consecuencia:** **Ejecuta la validación**. Si el nombre es un número, lanzará la excepción incluso desde el constructor.
*   **Uso:** **Recomendado** para asegurar la integridad del objeto desde el segundo cero.

---

## La palabra clave `value`
Es el error más común al empezar en C#. 
*   En el `set`, `value` representa lo que el usuario envió (ej. `estudiante.Name = "Pepe"`, entonces `value` vale `"Pepe"`).
*   Si usas el nombre de la propiedad (`Name`) dentro de su propio `set`, estarás leyendo el valor antiguo, no el nuevo.
