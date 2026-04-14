# Práctica: Algoritmos de Búsqueda - STRIPS (C#)

**Asignatura:** ABIA (Algoritmos Básicos de la Inteligencia Artificial)
**Grupo:** G1.1 - Jueves
**Autores:**
* Xoel Sánchez Dacoba
* Sebastián David Moreno Expósito

### Breve introducción a los problemas que se resolvieron implementado el planificador STRIPS 

Primero se considera importante una breve contextualización de ambos problemas propuestos en la practica que han sido solucionados usando el planificador STRIPS. 

- **Mundo de Bloques**
- **Torres de Hanoi**

 Para el mundo de bloques se nos han presentado **dos** posibles escenarios con estados de inicio/fin distintos, y para las Torres de Hanoi la variabilidad se encuentra en permitir elegir al usuario un numero **n** natural de discos. A continuación un resumen tabulado: 
#### Estado Inicial y Objetivo
| Problema               | Estado Inicial                                    | Estado Objetivo                                               |
| ---------------------- | ------------------------------------------------- | ------------------------------------------------------------- |
| **Mundo de Bloques A** | 3 bloques (A,B,C) sobre mesa, todos despejados    | Pila A-B-C (A arriba)                                         |
| **Mundo de Bloques B** | 6 bloques en 3 pilas desordenadas                 | 3 pilas de 2 bloques cada una:      **E-C**, **F-B**, **D-A** |
| **Torres de Hanoi**    | n discos apilados en PosteA (Dn abajo, D1 arriba) | n discos apilados en PosteC                                   |

### Como se pensó para resolver el problema?

Para resolver ambos problemas nuestra vision fue adoptar un modelo mental top-down, es decir, empezamos abstrayendo la implementación especifica de partes concretas y asumir que dichas partes funcionan, a partir de allí pensamos conjuntamente como comunicar cada una de estas partes/entidades antes de adentrarnos en su implementación. Todo programa empieza por un input, con lo cual quien es ese input? De esta pregunta salió el programa principal que simplemente es un loop que espera recibir del usuario números específicos que mediante un **switch-case** le permiten al usuario elegir si quiere seleccionar el **Mundo de bloques** o **Torres de Hanoi**, tras esta elección si prefiere el escenario A o B en el caso del primero o el numero de discos en el caso del segundo. Con esto en función de la elección del usuario nos adentramos en un modulo especifico por problema, dentro de este modulo nos encargamos de llamar al agente que ya es el encargado de llamar al planificador y este ultimo el encargado de usar el algoritmo de búsqueda para conseguir el plan que se le retorna al Agente,  luego el agente con el plan en mano empieza a aplicar las acciones y tras cada una de ellas muestra el resultado por pantalla. Este fue el modelo mental que teníamos antes de dar comienzo a la implementación técnica de los componentes individuales 

### Implementación técnica 
#### Definición de Factos
Para definir un "mundo" se nos ocurrió hacerlo simplemente describiendo lo que hay dentro de el. Ahi entran en juego los 'Factos' Estas son las verdades que conforman un estado/mundo, es completamente reutilizable tanto para el **Mundo de bloques** como para el de **Torres de Hanoi**. 
Por tanto un **Estado** simplemente se define como un HashSet de Factos(HashSet para facilitar el handling de duplicados y ya que estamos mejorar la eficiencia del código ya que el acceso a este contenedor de Factor es O(1) al tener un Hash por cada objeto de tipo Facto dentro del set).

Al implementar los **Factos** nos encontramos con algunos problemas en cuanto al manejo de duplicados, un "HashSet no permite duplicados", pues... Los métodos internos que usa un HashSet para prevenir los duplicados usan la **igualdad por referencia** es decir, dos objetos almacenados en la misma dirección de memoria se considera que son el mismo ergo dos objetos con dirección de memoria distinto se consideran diferentes, o sea, si instanciamos dos factos en momentos distintos con el mismo contenido como por ejemplo 
`var A = new Facto("EncimaDe", "A", "B")` y luego mas adelante hacemos 
`var B = new Facto("EncimaDe", "A", "B")` resulta que A != B, porque son dos objetos distintos que aun teniendo el mismo contenido se consideran distintos al apuntar a direcciones de memoria distintas, esto permite duplicados en el HashSet así que tuvimos que sobrescribir tanto los métodos `Equals()` como `GetHashCode` ya que ambos se evaluaban por referencia y NO por valor.

>En cuanto a los Factos que tenemos definidos en la practica son los siguientes:

- `SobreMesa(X)` --> Bloque X está directamente sobre la mesa
- `EncimaDe(A,B)` --> Encima de A esta B
- `Despejado(X)` --> El sitio X (bloque o poste) no tiene nada encima
- `MenorQue(D{n},P)` --> Disco n es menor que el poste
- `MenorQue(D{n},D{n+1})` -->Disco n es menor que disco n+1
- `Sobre(D{n}, P)` --> Disco n esta sobre el poste(o sea, arriba de el)
- `Sobre(D{n}, D{n+1})` --> Disco n se encuentra encima del disco n+1


Aquí hay un  pequeño resumen sobre los componentes básicos de la practica 

| Clase              | Propósito                                  | Approach que se siguió                                                  |
| ------------------ | ------------------------------------------ | ----------------------------------------------------------------------- |
| **`Estado`**       | Representa configuración del mundo         | `HashSet<Facto>` → O(1) búsqueda, sin duplicados                        |
| **`Facto`**        | Atomo de conocimiento sobre el mundo       | Sobrescribe `Equals()` y `GetHashCode()` para comparación por contenido |
| **`Accion`**       | Operador STRIPS (precondiciones + efectos) | Encapsula lógica de transición de estado                                |
| **`Planificador`** | Orquesta la búsqueda                       | Delega matemáticamente al algoritmo                                     |
| **`Agente`**       | Ejecuta el plan generado                   | Maneja estado interno privado, encapsulamiento                          |

#### Algoritmo de Búsqueda Implementado
- **Tipo**: BusquedaAnchura (BFS)
- **Complejidad Espacial**: O(b^d) donde b = ramificación, d = profundidad
- **Garantía**: Solución óptima (camino más corto en grafos no ponderados)

---

### Justificación de algunas decisiones técnicas

#### ¿Por qué clonar estados al aplicar acciones?
```csharp
Estado nuevoEstado = estadoActual.Clonar(); // Deep copy, no referencia compartida
```
- **Razón**: Evita mutación lateral que corrompa el árbol de búsqueda
- **Alternativa rechazada**: Modificar in-place --> ciclos imposibles de detectar

#### ¿Por qué interfaz `IAlgoritmoBusqueda`?
```csharp
public interface IAlgoritmoBusqueda {
    List<Accion>? Buscar(Estado inicial, Estado objetivo, List<Accion> operadores);
}
```
- **Razón**: Programación orientada a interfaces permite cambiar algoritmos sin modificar `Planificador` ya que obligamos que clases(algoritmos de búsqueda) que hereden de la interfaz estén en la obligación de implementar los métodos/firmas que esta declare 
- **Patrón**: Dependency Inversion Principle (DIP)

#### ¿Por qué `readonly` en `_acciones`?
```csharp
private readonly List<Accion> _acciones;
```
- **Razón**: Inmutabilidad del catálogo de operadores, seguridad contra modificaciones accidentales

---

### Análisis Crítico y Comparativo

Tanto para **Mundo de bloques** como para **Torres de Hanoi** usamos BFS(Breadh-First-Search)
#### Elección del Algoritmo de Búsqueda
| Algoritmo | Óptimo         | Memoria       | Adecuado para Hanoi      |
| --------- | -------------- | ------------- | ------------------------ |
| **BFS**   | Sí             | Alta (O(b^d)) | Escala mal con n grande  |
| **DFS**   | No garantizado | Baja          | Puede entrar en ciclos   |
| **A***    | Sí             | Media         |  Con heurística adecuada |

#### Limitaciones Identificadas
1. **BFS no escala**: Para Torres de Hanoi con n > 6, el espacio de estados explota rápidamente
2. **Sin poda**: BFS explora todos los nodos válidos sin optimización adicional
3. **Heurística ausente**: No se implementó función heurística para A* en este caso
-> Aunque la implementación de un algoritmo mas optimo en ningún caso se considero como una **necesidad** para esta practica 
#### Mejoras Potenciales (para futuras iteraciones)
- Implementar **A*** con heurística h(n) = número de discos mal colocados
- Añadir **poda por profundidad máxima** para evitar explosión combinatoria
- Usar **representación compacta del estado** para reducir memoria

---

#### Metodología de Integración
- **Pair programming** para funciones críticas: `GenerarOperadores()`, `Aplicar()`
- **Revisión cruzada**: Cada miembro revisó el código del otro antes de integración final
- **Compromiso técnico**: Decisión conjunta sobre usar BFS vs A* (BFS por simplicidad y garantía de optimalidad)


