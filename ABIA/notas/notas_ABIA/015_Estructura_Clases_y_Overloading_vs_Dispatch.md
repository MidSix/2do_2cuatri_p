# 015 - Estructura de Clases, Atributos y Overloading vs Dispatch

Este documento consolida las diferencias arquitectónicas clave entre lenguajes dinámicos (Python/Julia) y estáticos (C#) respecto a la definición de clases y el polimorfismo.

## 1. Definición de Atributos: El "Layout" de Memoria

En C# (y C++/Java), la clase actúa como una definición rígida de la estructura en memoria. A diferencia de Python, no se pueden añadir propiedades "al vuelo".

### Ubicación y Ámbito
Los atributos (datos) **deben** declararse a nivel de clase, fuera de cualquier método.

| Tipo de Atributo     | Sintaxis C# (Nivel de Clase)  | Equivalente Python                    | Comportamiento                                                                                     |
| :------------------- | :---------------------------- | :------------------------------------ | :------------------------------------------------------------------------------------------------- |
| **Instancia**        | `public int Edad;`            | `self.edad = ...` (en `__init__`)     | Cada objeto (`new`) tiene su propia copia independiente de esta variable.                          |
| **Clase (Estático)** | `public static int Contador;` | Variable definida fuera de `__init__` | Existe una única copia compartida por todas las instancias y se accede vía `NombreClase.Contador`. |

**Nota:** Declarar una variable dentro del constructor (`public Classroom() { int x; }`) la convierte en una **variable local** temporal, no en un atributo del objeto.

>En general declarar CUALQUIER variable dentro de CUALQUIER metodo NO la convertira en un atributo sino en una variable temporal que no le pertenece al objeto ni a la clase, es decir, desde fuera no se podra acceder a ella. Los modificadores de acceso (Public,Private,Internal,etc) SOLO son para los miembros de clase(Atributos y metodos) por lo que una variable declarada en un metodo NO es un miebro de clase al no ser atributo, no podrias aplicar sobre ella esos modificadores de acceso, simplemente seria una variable local interna independiente a la clase y a sus instanciaciones.
## 2. Ámbito y Variables Locales

En C#, la ubicación de la declaración determina la naturaleza de la variable de forma absoluta:

1.  **Atributos (Miembros de Clase):** Se declaran fuera de los métodos. Son los únicos que aceptan modificadores de acceso (`public`, `private`, `internal`, etc.).
2.  **Variables Locales:** Se declaran **dentro** de un método. 
    *   **No pertenecen al objeto ni a la clase.** Son temporales y mueren al llegar a la llave de cierre `}` del método.
    *   **No admiten modificadores de acceso:** Intentar poner `public` a una variable dentro de un método provoca un error de compilación.
    *   **Invisibilidad:** Desde fuera del método es físicamente imposible acceder a ellas.

## 3. Constructores y Sobrecarga (Overloading)

### Reglas de Constructores
1.  **Nombre:** Debe ser **idéntico** al de la clase.
2.  **Retorno:** No tienen tipo de retorno (ni `void`).
3.  **Función:** Inicializar los atributos ya declarados en la estructura de la clase.

### Sobrecarga (Overloading)
Capacidad de definir múltiples métodos (o constructores) con el mismo nombre pero **diferente firma** (parámetros).
C# distingue cual usar basándose en la cantidad y tipo de los argumentos pasados.

```csharp
public Classroom() { ... }                   // Constructor vacío
public Classroom(List<Student> lista) { ... } // Constructor con argumentos
```

## 3. Static Dispatch (C#) vs Dynamic Dispatch (Julia)

Aunque el Overloading se parece visualmente al **Multiple Dispatch** de Julia, el mecanismo interno es opuesto.

### C# Overloading = Static Dispatch (Tiempo de Compilación)
El compilador decide qué método invocar **antes de ejecutar el programa**, basándose exclusivamente en el **Tipo Declarado** de la variable contenedora.

### Julia Multiple Dispatch = Dynamic Dispatch (Tiempo de Ejecución)
El entorno decide qué función invocar **durante la ejecución**, inspeccionando el **Tipo Real** del valor en memoria.

### El "Caso Trampa"
Supongamos dos métodos: `Procesar(object x)` y `Procesar(string x)`.

```csharp
object miDato = "Hola"; // Declarado como 'object', contiene un 'string'
Procesar(miDato);
```

*   **En C#:** Se ejecuta `Procesar(object x)`.
    *   *Razón:* El compilador ve la variable `miDato` marcada como `object`. Ignora que dentro hay un string. Vincula la llamada estáticamente.
*   **En Julia:** Se ejecutaría `Procesar(string x)`.
    *   *Razón:* En tiempo de ejecución, el sistema ve que el valor es "Hola" (String) y busca la definición más específica.
