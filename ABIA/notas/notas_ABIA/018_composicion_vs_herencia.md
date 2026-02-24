# 018 - Composición vs. Herencia ("Tiene-un" vs. "Es-un")

En la Programación Orientada a Objetos, la herencia y la composición son dos mecanismos fundamentales para establecer relaciones entre clases. Aunque ambos permiten la reutilización de código, modelan relaciones conceptualmente diferentes y entender cuándo usar cada uno es crucial para un buen diseño de software.

La regla principal es:
- **Herencia**: Modela una relación **"Es-un"** (IS-A).
- **Composición**: Modela una relación **"Tiene-un"** (HAS-A).

---

## 1. Herencia (Relación "Es-un")

La herencia se usa cuando una clase es una **versión especializada** de otra. La clase hija hereda los atributos y métodos de la clase padre y puede añadir o modificar funcionalidades.

**Ejemplo Lógico**: Un `Perro` **es un** `Animal`. Tiene sentido que `Perro` herede de `Animal`, ya que compartirá características fundamentales (como tener un nombre o comer) pero añadirá otras específicas (ladrar).

### Ejemplo en C\#

```csharp
using System;

// Clase Padre
public class Animal
{
    public string Name { get; set; }

    public Animal(string name)
    {
        this.Name = name;
    }

    public void Eat()
    {
        Console.WriteLine($"{Name} está comiendo.");
    }
}

// Clase Hija
public class Dog : Animal
{
    public Dog(string name) : base(name) // Llama al constructor del padre
    {
    }

    public void Bark()
    {
        Console.WriteLine("¡Guau! ¡Guau!");
    }
}

public class Program
{
    public static void Main()
    {
        Dog myDog = new Dog("Fido");
        myDog.Eat();   // Método heredado de Animal
        myDog.Bark();  // Método propio de Dog
    }
}
```

### Ejemplo en Python

```python
# Clase Padre
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} está comiendo.")

# Clase Hija
class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)  # Llama al constructor del padre

    def bark(self):
        print("¡Guau! ¡Guau!")

# --- Uso ---
my_dog = Dog("Fido")
my_dog.eat()   # Método heredado de Animal
my_dog.bark()  # Método propio de Dog
```

### Salida del Código (para ambos ejemplos)

```
Fido está comiendo.
¡Guau! ¡Guau!
```

---

## 2. Composición (Relación "Tiene-un")

La composición se usa para construir objetos complejos a partir de otros objetos más simples. En lugar de que una clase *sea* otra, una clase *contiene* a otra para delegarle funcionalidad. Es más flexible que la herencia.

**Ejemplo Lógico**: Un `Coche` **no es** un `Motor`, pero **tiene un** `Motor`. No tendría sentido que `Coche` heredara de `Motor`. En su lugar, el objeto `Coche` contiene un objeto `Motor` y lo utiliza cuando es necesario.

### Ejemplo en C\#

```csharp
using System;

// Clase Componente
public class Engine
{
    public void Start()
    {
        Console.WriteLine("Motor encendido. ¡Vroom!");
    }
}

// Clase Contenedora
public class Car
{
    private Engine _engine; // El Car "tiene un" Engine
    public string Brand { get; set; }

    public Car(string brand)
    {
        this.Brand = brand;
        this._engine = new Engine(); // Se crea la instancia del componente
    }

    public void StartCar()
    {
        Console.WriteLine($"Arrancando el coche {Brand}...");
        _engine.Start(); // Delega la acción al componente
    }
}

public class Program
{
    public static void Main()
    {
        Car myCar = new Car("Toyota");
        myCar.StartCar();
    }
}
```

### Ejemplo en Python

```python
# Clase Componente
class Engine:
    def start(self):
        print("Motor encendido. ¡Vroom!")

# Clase Contenedora
class Car:
    def __init__(self, brand):
        self.brand = brand
        self.engine = Engine()  # El Car "tiene un" Engine

    def start_car(self):
        print(f"Arrancando el coche {self.brand}...")
        self.engine.start()  # Delega la acción al componente

# --- Uso ---
my_car = Car("Toyota")
my_car.start_car()
```

### Salida del Código (para ambos ejemplos)

```
Arrancando el coche Toyota...
Motor encendido. ¡Vroom!
```

---

## Conclusión: ¿Cuándo Usar Cada Una?

| Criterio             | Herencia ("Es-un")                                                                  | Composición ("Tiene-un")                                                                    |
| :------------------- | :---------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------ |
| **Tipo de Relación** | Fuerte y acoplada. La subclase depende de la superclase.                            | Débil y flexible. El contenedor no depende de la implementación del componente.             |
| **Flexibilidad**     | Rígida. Cambios en el padre afectan a toda la jerarquía.                            | Alta. Puedes cambiar el componente en tiempo de ejecución.                                  |
| **Prueba Lógica**    | ¿ClaseB **es una** ClaseA?                                                          | ¿ClaseA **tiene una** ClaseB?                                                               |
| **Recomendación**    | Usar con moderación, cuando la relación "es-un" es clara y la jerarquía es estable. | **Preferir siempre que sea posible.** Es más flexible y conduce a un código más mantenible. |
