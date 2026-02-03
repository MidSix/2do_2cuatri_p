# Convenciones de Nombres (Naming Conventions) en C#

A diferencia de Python, que utiliza `snake_case` de forma extensiva, C# adopta un estándar más estricto basado en la capitalización para distinguir el ámbito (scope) y el tipo de los elementos.

## Los 3 Estilos Principales

1.  **PascalCase**: La primera letra de **cada palabra** es mayúscula.
    *   Ejemplo: `CalculateMeanGrade`, `StudentList`.
2.  **camelCase**: La primera letra es minúscula, las siguientes palabras inician con mayúscula.
    *   Ejemplo: `totalGrade`, `studentName`.
3.  **snake_case** (Python): Todo minúsculas separado por guiones bajos.
    *   Ejemplo: `calculate_mean_grade`. **NO SE USA EN C#** (salvo en nombres de constantes privadas a veces, pero no es estándar).

## Reglas de Oro en C#

| Elemento               | Convención                   | Ejemplo C#                | Equivalente Python |
| :--------------------- | :--------------------------- | :------------------------ | :----------------- |
| **Clase / Struct**     | **PascalCase**               | `class Student`           | `class Student`    |
| **Método**             | **PascalCase**               | `void Calculate()`        | `def calculate():` |
| **Propiedad** (Public) | **PascalCase**               | `public int Age { get; }` | `self.age`         |
| **Variable Local**     | **camelCase**                | `int totalCount = 0;`     | `total_count = 0`  |
| **Parámetro**          | **camelCase**                | `void Add(int newId)`     | `def add(new_id):` |
| **Interface**          | **PascalCase** (Prefijo 'I') | `interface IDisposable`   | -                  |
| **Nombrar modulos**    | **PascalCase**               | `StudentUtils.cs`         | `student_utils.py` |

## ¿Por qué este cambio?

En C#, la convención comunica información semántica sobre el código:

*   Si empieza con **Mayúscula** (PascalCase), sabes que es algo "público" o una definición de tipo (una Clase, un Método que puedes llamar, una Propiedad).
*   Si empieza con **minúscula** (camelCase), sabes que es algo "interno" o temporal (una variable dentro de una función, un argumento que se está pasando).

### Ejemplo Comparativo

**Python:**
```python
class StudentUtils:
    def calculate_mean(self, student_list):
        total_sum = 0
        # ...
```

**C#:**
```csharp
class StudentUtils
{
    public void CalculateMean(List<Student> studentList)
    {
        int totalSum = 0;
        // ...
    }
}
```
