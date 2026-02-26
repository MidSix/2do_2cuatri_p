# 017 - Comparativa: Clases y Métodos Abstract vs. Static (C# vs. Python)

Esta nota clarifica las diferencias fundamentales entre las palabras clave `abstract` y `static` aplicadas a clases y métodos en C# y cómo se mapean a Python, dado que sus propósitos son distintos y a menudo generan confusión.

---

## 1. Tabla Comparativa Rápida

| Característica            | Clase Abstracta                                | Clase Estática                                          |
| :------------------------ | :--------------------------------------------- | :------------------------------------------------------ |
| **¿Se puede instanciar?** | No                                             | No                                                      |
| **¿Se puede heredar?**    | Sí (diseñada para ser heredada)                | No                                                      |
| **Propósito Principal**   | Definir una plantilla/contrato para subclases. | Agrupar funcionalidades de utilidad sin estado.         |
| **Contenido**             | Métodos abstractos y concretos, propiedades.   | Sólo miembros estáticos (métodos, propiedades, campos). |

---

## 2. Clases y Métodos Abstractos

*   **Propósito:** Las clases abstractas definen una interfaz común y/o una implementación parcial para un conjunto de clases relacionadas. Funcionan como un "contrato" o una "plantilla" que las clases hijas deben seguir. Los métodos abstractos fuerzan a las subclases a proporcionar su propia implementación.

*   **Características Clave:**
    *   **No se pueden instanciar:** No puedes crear un objeto directamente de una clase abstracta (`new MiClaseAbstracta()` fallaría).
    *   **Se diseñan para ser heredadas:** Son la base de una jerarquía de herencia.
    *   **Pueden contener métodos abstractos:** Métodos declarados sin implementación (sin cuerpo) que las subclases *concretas* deben implementar.
    *   **Pueden contener métodos y propiedades concretas:** Lógica común que todas las subclases pueden compartir.
    *   **Obligación de implementación:** Una subclase que no sea abstracta (una clase concreta) debe implementar todos los métodos abstractos de su clase padre abstracta. Si una subclase es también abstracta, puede posponer la implementación a sus propios descendientes.

*   **Implementación en C#:**
    ```csharp
    public abstract class Shape
    {
        public abstract double GetArea(); // Método abstracto
        public void DisplayMessage() // Método concreto
        {
            Console.WriteLine("Esto es una forma.");
        }
    }

    public class Circle : Shape
    {
        public double Radius { get; set; }
        public override double GetArea() // Implementación obligatoria
        {
            return Math.PI * Radius * Radius;
        }
    }
    ```

*   **Implementación en Python:** Utiliza el módulo `abc` (Abstract Base Classes).
    ```python
    from abc import ABC, abstractmethod

    class Shape(ABC): # Hereda de ABC
        @abstractmethod # Decorador para método abstracto
        def get_area(self):
            pass # No tiene implementación

        def display_message(self): # Método concreto
            print("Esto es una forma.")

    class Circle(Shape):
        def __init__(self, radius):
            self.radius = radius

        def get_area(self): # Implementación obligatoria
            return 3.14159 * self.radius ** 2
    ```

---

## 3. Clases y Métodos Estáticos

> A diferencia de las clases abstractas que Sí existen en python. Las clases estáticas NO existen en **python**. SOLO existen métodos estáticos pero no clases.


*   **Propósito:** Las clases y métodos estáticos agrupan funcionalidades que no necesitan un estado de instancia para operar. Son útiles para funciones de utilidad, helpers, o configuraciones globales.

*   **Características Clave:**
    *   **No se pueden instanciar:** Accedes a sus miembros directamente a través del nombre de la clase (`MiClaseEstatica.MiMetodoEstatico()`).
    *   **No se pueden heredar:** No puedes extender una clase estática.
    *   **Todos sus miembros son estáticos:** Una clase estática solo puede contener métodos, propiedades y campos estáticos.

*   **Implementación en C#:**
    ```csharp
    public static class MathUtils
    {
        public static double PI = 3.14159; // Campo estático

        public static double Add(double a, double b) // Método estático
        {
            return a + b;
        }

        public static double CalculateCircumference(double radius) // Método estático
        {
            return 2 * PI * radius;
        }
    }

    // Uso:
    double sum = MathUtils.Add(5, 3);
    double circumference = MathUtils.CalculateCircumference(10);
    ```

*   **Implementación en Python:**
    *   **No existen `clases estáticas` dedicadas** como en C#. En su lugar, se suele usar un módulo (archivo `.py`) con funciones globales, o una clase normal que solo contenga métodos estáticos.
    *   **Métodos Estáticos:** Se definen dentro de una clase usando el decorador `@staticmethod`. No reciben el argumento `self`.
    ```python
    class MathUtils:
        PI = 3.14159 # Variable de clase, accesible como MathUtils.PI

        @staticmethod
        def add(a, b): # Método estático, no recibe 'self'
            return a + b

        @staticmethod
        def calculate_circumference(radius): # Método estático
            return 2 * MathUtils.PI * radius # Accede a la variable de clase

    # Uso:
    suma = MathUtils.add(5, 3)
    circunferencia = MathUtils.calculate_circumference(10)
    ```

---

**Conclusión:**
Aunque tanto las clases abstractas como las estáticas no se pueden instanciar directamente, sus roles son fundamentalmente opuestos: las `abstract` son para la **herencia y la polimorfismo**, estableciendo contratos para el diseño orientado a objetos; mientras que las `static` son para la **utilidad y la organización de funciones**, sin relación con instancias o jerarquías.
