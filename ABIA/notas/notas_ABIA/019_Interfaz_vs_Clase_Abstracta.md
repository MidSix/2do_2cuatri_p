# Interfaz vs Clase Abstracta en C#

Al migrar código de Python a C#, es común encontrarse con la decisión de si usar una **Clase Abstracta** (`abstract class`) o una **Interfaz** (`interface`).

## 1. ¿Qué es una Interfaz?
En C#, una interfaz (por convención, su nombre empieza con `I`, como `IListaCandidatos`) es un **contrato puro**. Define **QUÉ** debe hacer una clase. 

Una interfaz sólo contiene las firmas de los métodos, propiedades o eventos. No puede tener variables de instancia (campos) ni, tradicionalmente, implementaciones de métodos.

```csharp
public interface IListaCandidatos
{
    // Solo decimos QUÉ métodos debe tener quien firme el contrato.
    void Anhadir(Solucion solucion, int prioridad = 0);
    Solucion ObtenerSiguiente();
    int Count { get; }
}
```

## 2. Diferencias Clave: Abstract Class vs Interface

| Característica                 | Clase Abstracta (`abstract class`)                                      | Interfaz (`interface`)                                                        |
| :----------------------------- | :---------------------------------------------------------------------- | :---------------------------------------------------------------------------- |
| **Concepto Relacional**        | "Es un..." (*IS-A*)                                                     | "Se comporta como / Es capaz de..." (*CAN-DO*)                                |
| **Implementación por defecto** | Puede contener métodos con código real y variables (estado).            | Es 100% abstracta (solo firmas)*. No tiene campos/variables propias.          |
| **Herencia Múltiple**          | **NO**. Una clase solo puede heredar de **UNA** sola clase base. `(C#)` | **SÍ**. Una clase puede implementar **MÚLTIPLES** interfaces simultáneamente. |
| **Constructores**              | Sí puede tener constructores.                                           | No puede tener constructores (no se puede instanciar).                        |

*(Nota: Desde C# 8.0, las interfaces pueden tener implementaciones por defecto, pero su uso principal sigue siendo como contrato puro).*

## 3. ¿Por qué usar `interface` en el problema de las N-Reinas?

Tu compañero Xoel decidió usar `IListaCandidatos` en lugar de `public abstract class ListaCandidatos` por una razón de diseño muy sólida:

1. **No había atributos:** En tu versión original de Python, tu clase `ListaCandidatos` solo tenía métodos vacíos (`pass`). Al no haber ninguna lógica repetida, variables compartidas ni comportamiento base que heredar, una clase abstracta era "demasiado peso" para lo que se necesitaba.
2. **Es un contrato puro:** Solo necesitábamos garantizar que cualquier estructura de datos que se pasara al algoritmo tuviera los métodos `Anhadir`, `Borrar`, `ObtenerSiguiente` y `Count`. Las interfaces son la herramienta exacta para esto.
3. **Flexibilidad Futura:** Si en C# deciden que `ColaDePrioridad` deba heredar de otra clase base distinta en el futuro (por ejemplo, de alguna clase interna de un motor gráfico), podrán hacerlo sin problema porque ya están implementando una interfaz. Si hubieran heredado de una clase abstracta, ya habrían "gastado" su única oportunidad de herencia.

```C#
    /*
        Y es muy curioso esto de las interfaces, aunque en python
        existen como concepto, no existen como sintaxis. NO hay un
        equivalente sintacticamente hablando en python de las interfaces,
        porque en python existe la herencia multiple. Por tanto puedes
        hacer que una clase herede de varias clases abstractas y
        ya esta. Sin embargo en C# no puedes hacer eso, solo
        puedes heredar de una clase, por lo que se crea una
        distincion entre lo que engloba lo que ES un objeto
        (Clase abstracta ya que esta puede implementar atributos)
        y SU comportamiento(interface dado que este SOLO puede implementar
        metodos y no atributos). En python la interfaz existe solo como concepto
        pues simplemente seria una clase abstracta sin atributos,
        solo con metodos, y al permitirse la herencia multiple gucci.
        Una clase abstracta con atributos y el resto de clases abstractas
        con comportamiento(conceptualmente una interface). En C#
        tendria que ser una clase abstracta con atributos
        e interfaces con comportamiento. Hay que fijarse que una
        interfaz no es una clase, por eso puede ser heredada por varias
        clases.

    */
```
### Ejemplo de cómo se lee conceptualmente:
* `Coche abstract class Auto` (Un Coche **ES UN** Auto). 
* `Coche implements IVehiculoMotor` (Un Coche **FIRMA EL CONTRATO** de tener un motor y poder acelerar).

En el caso de N-Reinas:
`ColaDePrioridad` **FIRMA EL CONTRATO** de comportarse como una `IListaCandidatos`.
