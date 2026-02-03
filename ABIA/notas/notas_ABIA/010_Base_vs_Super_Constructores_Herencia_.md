# Constructores en Herencia: `base` (C#) vs `super` (Python)

Esta nota profundiza en la mecánica de inicialización de objetos cuando existe herencia, un punto donde C# es mucho más estricto que Python.

## 1. El Modelo Mental: "Rellenar la Ficha"

Una confusión común es pensar que al llamar al padre podemos elegir que atributos. **Esto es falso**.
Por el simple hecho de heredar (`: Padre`), la clase Hija **YA TIENE** todos los atributos del padre.

**¿Entonces para qué llamamos al constructor?**
Imagina que la clase Padre es una "Ficha de Registro" con campos obligatorios (ej: Nombre).
1.  **Herencia:** Te da la ficha en blanco.
2.  **Constructor (`base` / `super`):** Es el momento de **escribir** en esos campos obligatorios.

> **Regla de Oro:** Si el Padre exige un dato en su constructor, el Hijo tiene la **obligación** de proporcionárselo. De lo contrario.

## 2. Sintaxis y Momento de Ejecución

La gran diferencia no es *qué* hacen, sino *cuándo* y *dónde* se escribe.

### Python: `super()` (Dentro)
En Python, la llamada es explícita **dentro** del cuerpo del método. Es flexible (demasiado), si se te olvida, el programa arranca pero fallará luego.

```python
class Hija(Padre):
    def __init__(self, dato_hija, dato_padre):
        # 1. Puedes ejecutar código antes del padre (raro, pero posible)
        print("Iniciando...")
        
        # 2. Llamada explícita
        super().__init__(dato_padre) 
        
        # 3. Resto de inicialización
        self.dato_hija = dato_hija
```

### C#: `: base()` (En la Firma)
En C#, la llamada se hace en la **declaración** del constructor. C# garantiza que el Padre esté listo **antes** de que se ejecute una sola línea de código del Hijo.

```csharp
public class Hija : Padre
{
    //                                         Firma del Constructor
    //                                              ↓↓↓↓↓↓↓↓
    public Hija(string datoHija, string datoPadre) : base(datoPadre)
    {
        // Cuando entras aquí, el Padre YA está construido.
        this.DatoHija = datoHija;
    }
}
```

> **Base()** llama al constructor del padre al igual que super,  el atributo que aparece dentro de los parentesis es el atributo que el constructor del padre necesita para inicializarce, sin el no puede inicializarce y obviamente no podra pasarle los datos al hijo
## 3. Estrategias de "Paso de Datos"

Si el Padre requiere un argumento (ej. `Nombre`), el Hijo tiene dos formas de cumplir:

### A. El Intermediario (Pasamanos)
El hijo no sabe el dato, así que se lo pide al usuario (`Main`) y se lo pasa inmediatamente al padre.

```csharp
// El usuario hace: new Hija("Pepe");
public Hija(string nombre) : base(nombre) 
{ 
    // Hija recibe "Pepe" -> Se lo pasa a Padre -> Padre lo guarda.
}
```

### B. El Inventor (Hardcode)
El hijo no pide el dato, pero como el padre lo exige, el hijo se lo "inventa" o fija un valor predeterminado.

```csharp
// El usuario hace: new Hija();
public Hija() : base("Nombre Predeterminado") 
{ 
    // Hija no pide nada, pero satisface al Padre con un literal.
}
```

## 4. Argumentos Opcionales

Si el constructor del Padre tiene argumentos opcionales (valores por defecto), la "obligación" de llamar a `base` se relaja.

```csharp
public class Padre {
    // Nombre es opcional
    public Padre(string nombre = "Anónimo") { ... }
}

public class Hija : Padre {
    // VÁLIDO: No escribimos ": base(...)"
    // C# entiende implícitamente ": base()" que usa "Anónimo"
    public Hija() { ... } 
}
```

---
**Tags:** #CSharp #Python #POO #Herencia #Constructores #BuenasPracticas
**Relacionado:** [[004_Python_to_CSharp_Cheatsheet]] (Sintaxis básica), [[005_Metodos,Clases_CSharp]] (Anatomía clases)