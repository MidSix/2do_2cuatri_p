---
id: anatomia-metodo-csharp
aliases: [Modificadores C#, public static void main]
tags:
  - ABIA
  - C_sharp
  - programación_orientada_objetos
created: 2026-02-01
---

# 005 - Métodos en C#: Desglosando la "Burocracia"

C# nos obliga a ser muy específicos con cada pieza de código. Aquí tienes el desglose de lo que significan esas palabras que siempre ves al principio de un programa.

## 1. `public` / `private` / `internal` (El Permiso)
Define el **Modificador de Acceso**. Es decir, ¿quién tiene permiso para ver y usar este código?

*   **`public`**: Acceso total. Cualquier parte de tu programa puede llamar a este codigo.

* `internal`: Acceso parcial. Cualquier parte de tu programa puede llamar a este codigo(clase/funcion) SIEMPRE que formen parte del mismo proyecto, es decir, que su .csproj sea el mismo, o sea, que se encuentren en el mismo path (O que se estableza alguna excepcion a proyectos especificos como InternalsVisibleTo).

*   **`private`**: Acceso restringido. Solo se puede usar dentro de la misma clase donde fue creada. PERO, las clases no pueden ser private, solo los metodos (basicamente porque si haces que una )

### **Amplicacion:**
#### 1.1. La Regla de Contención (Restricción de Nivel)

El nivel de acceso de un miembro (método, propiedad, campo) no puede ser superior al nivel de acceso de la clase que lo contiene (No porque no lo puedes programar de  esa forma sino porque el compilador lo ignorara si lo haces, pero no te saltara ningun error de sintaxis ni nada por el estilo).

- Si una clase se define como `internal`, el compilador trata a todos sus miembros `public` como si fueran `internal` para cualquier entidad fuera del proyecto, es decir, que aunque sean publics un proyecto ajeno no podra acceder a ellos ya que su acceso esta condicionado primero a que la clase sea accesible y si esta no es accesible automaticamente sus metodos tampoco lo son.
- Declarar un método `public` dentro de una clase `internal` no otorga visibilidad externa; solo define el comportamiento del miembro si la clase llegara a cambiar a `public` en el futuro.

#### 1.2. Comportamiento de Modificadores en Clases

- **`public`**: La clase es accesible desde cualquier ensamblado (proyecto) que la referencie.
- **`internal`**: La clase es accesible únicamente dentro del mismo ensamblado (`.csproj`). Es el valor **por defecto** si se omite el modificador. VALOR POR DEFECTO
- **`private`**: Solo permitido en clases anidadas (dentro de otra clase). Una clase en el nivel superior de un archivo no puede ser `private`.

#### 1.3. Comportamiento de Modificadores en Métodos

- **`public`**: Accesible por cualquier código que tenga visibilidad sobre la clase contenedora.
- **`internal`**: Accesible solo por código dentro del mismo ensamblado.
- **`private`**: Accesible solo por miembros de la misma clase. **Es el valor por defecto para métodos**. VALOR POR DEFECTO

#### 1.4. El efecto de `InternalsVisibleTo`

Este atributo de ensamblado altera la frontera del modificador `internal`:

- Otorga a un segundo ensamblado específico (Proyecto B) el mismo nivel de acceso que tiene el ensamblado original (Proyecto A).
- Bajo esta configuración, los miembros `internal` de la clase `internal` en el Proyecto A se vuelven totalmente visibles y utilizables para el Proyecto B.
- En este escenario, no existe diferencia funcional entre un método `public` y uno `internal` dentro de una clase `internal`; ambos son accesibles para el ensamblado "amigo".

---
### Matriz de Accesibilidad Final

| **Modificador**       | **Clase internal**                                           | **Clase public**                           |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------ |
| **Método `public`**   | Visible solo en mismo `.csproj` (o amigos)                   | Visible en cualquier parte                 |
| **Método `internal`** | Visible solo en mismo `.csproj` (o amigos)                   | Visible solo en mismo `.csproj` (o amigos) |
| **Método `private`**  | Visible solo en la misma `class` (solo para clases anidadas) | Visible solo en la misma `class`           |
## 2. `static` (La Pertenencia)
Este es el concepto más importante para entender por qué C# se siente distinto a Python. Define **a quién le pertenece** el método.

*   **Con `static`**: Le pertenece a la **Clase** (es una herramienta general). No necesitas crear nada para usarla.
    *   *Ejemplo:* `Math.Sqrt(16)`. No creas una "instancia de matemáticas", solo usas la herramienta.
    *   *Uso:* Se invoca directamente como `Clase.Metodo()`.
*   **Sin `static`**: Le pertenece al **Objeto** (necesitas crear una instancia con `new`).
    *   *Ejemplo:* Si tienes una clase `Coche`, el método `Arrancar()` no es estático porque necesitas un coche específico (un objeto) para arrancarlo.

> **Regla de oro:** Como C# te obliga a meter todo en clases, usas `static` para crear funciones "sueltas" o de utilidad que no requieren un objeto real para funcionar.

## 3. `void` o Tipo (El Retorno)
Indica qué nos va a devolver la función cuando termine su trabajo.

*   **`void`**: No devuelve nada. La función hace un trabajo (como imprimir en pantalla o guardar un archivo) y termina.
*   **Tipo (int, string, bool...)**: La función calcula algo y nos entrega un resultado que podemos guardar en una variable.

## 4. `Main` (El Inicio)
Es el nombre reservado para el **punto de entrada**.

*   El ordenador es como un lector que entra en una biblioteca gigante (tu código). El `Main` es el cartel de **"EMPIECE AQUÍ"**. Sin un método llamado exactamente `Main`, el ordenador no sabría por dónde empezar a ejecutar el programa.

---

## Ejemplo Resumen:
```csharp
public static void Saludar() 
{
    Console.WriteLine("Hola");
}
```
*   **`public`**: Cualquiera puede usarlo.
*   **`static`**: Se usa llamando a la clase, no hace falta un objeto.
*   **`void`**: Solo imprime, no devuelve datos.
*   **`Saludar`**: Es el nombre que le hemos dado.

**Relacionado:**
*   [[004_Python_to_CSharp_Cheatsheet|Python to C# Cheatsheet]]
