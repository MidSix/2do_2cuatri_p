/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/
namespace STRIPS{
public class Facto//Elemento esencial de los estados, representa una afirmación sobre el mundo, como "En(A, B)" o "Libre(C)"
//en la practica lo usaremos para decir cosas como "Sobremesa" y en argumentos tendremos [A] por ejemplo
//de manera que podamos hacer querys como Sobremesa(A)? y obtener True. La lista de argumentos definen la aridad
//Por ejemplo para el facto EncimaDe, los argumentos seria [A,B], y luego mediante un hashset de Factos
//podemos representar el estado del mundo, por ejemplo con los siguientes Factos: EncimaDe(A,B), 
//EncimaDe(B,C), Libre(C) podríamos representar un mundo donde A está encima de B,
// B está encima de C, y C está libre. 

// EncimaDe(A,B) -> Encima de A esta B.
// EncimaDe(B,C) -> Encima de B esta C.
// Libre(C) -> C está libre.

// El equivalente en python a un 'hashset' de C# son simplemente los
// 'set' de python, o sea, los conjuntos, son el equivalente directo.
// NO permite duplicados y NO hay ordern. Esto se debe precisamente
// a su implementacion con funcion hash, es decir, 
// a cada elemento le asignan un valor numerico unico, por eso no pueden
// haber dos objetos que sean el mismo. Tanto insercion, como la 
// iteracion asi como la eliminacion son O(1)
{
    // En C# en lugar de "atributos" como le llamamos en python
    // y definidos en el constructor, aqui los llamamos "campos" y se
    // definen antes del constructor, los campos son variables de
    // instancia privadas que para poder comunicarnos con ellas hemos de
    // usar las properties de los 
    // getter y setter. En este caso se simplifica la sintaxis
    // y se comprime la declaracion tanto de la variable de instancia
    // privada como del getter y setter en una unica linea, es la
    // version idiomatica que se usa en C# llamada auto-implemented 
    // properties
    public string Nombre { get; set; } // Aqui se define tanto el campo
    // que seria la variable de instancia privada __Nombre como tambien
    // sus getter y setter.
    public List<string> Argumentos { get; set; } // Lo mismo que ocurre
    // arriba

    public Facto(string nombre, params string[] argumentos)
    // Constructor de la clase, el compilador lo interpreta como tal
    // ya que tiene el mismo nombre que la clase. "params" es
    // simplemente una keyword que permite pasar un numero variable
    // de argumentos, el ejemplo mas cercano en python es "*"
    // simplemente que como en python no se especifican los tipos
    // basta simplemente con escribir *args y ya esta, aqui en C#
    // hay que especificar el tipo en en este caso string[] argumentos
    // entonces seria params = "*" y string[] argumentos = args.
    // keyword equivalence -> params = *
    // variable name equivalence -> argumentos = args

    // params se usa para no tener que instancia un array de argumentos
    // cada vez que queramos instanciar un Facto, en su lugar
    // simplemente separamos los argumentos por comas ',' y el
    // compilador ya se encarga de encapsularlos en un array de strings
    // para nosotros.
    {
        // Self-explanatory
        Nombre = nombre;
        Argumentos = argumentos.ToList();
    }
    // 'object obj', object es un alias de System.Object que es la 
    // clase base de TODA clase en C#, entonces le estamos diciendo
    // al compilador que obj puede pertenecer a cualquier clase

    // Antes saltaba un Warning en Equals porque no se declaraba la
    // posibilidad en 'object obj' de que object fuera NULL. Y en la 
    // firma original que estamos sobreescribiendo el tipo object
    // se declara como Nullable, o sea con "?".
    public override bool Equals(object? obj)// Esto es para comparar estados después
    // Hay dos formas para comparar elementos en C#(no digo que SOLO
    // haya estas dos, digo que hay dos, no se si hayan mas 
    // ademas de estas, tampoco quiero saber porque no hay tiempo
    // para todo xd). Tenemos el
    // '==' operator y el 'Equals()' method, ambos en funcion del tipo
    // comparan por referencia o por valor, entonces por que se decide
    // hacer un override de Equals() en lugar de una sobrecarga al
    // operador '==' cuando tecnicamente se pueden llegar al mismo
    // resultado? Es la eleccion de uno por sobre el otro arbitraria?
    // No. Se decide hacer un override(cambiar el comportamiento de 
    // un metodo) en lugar de una sobrecarga(cambiar el comportamiento
    // de un operador) a '==' porque los HashSet internamente usan
    // el metodo Equals() para hacer comparaciones. Para que quieren 
    // hacer comparaciones? Para determinar si un estado es el mismo
    // que otro y evitar agregar estados YA existente a un HashSet.
    // Por que hay que hacer esto? Pues hay que saber que por defecto
    // tanto 'Equals()' como '==' determinan igualdad por valor cuando
    // estamos frente a tipos como int, float, ... y determinan igualdad
    // por referencia(direccion de memoria a la que apuntan)
    // para objetos, ese es el comportamiento por defecto, entonces
    // si creas new Facto("A") y mas adelante vuelves a hacer un 
    // new Facto("A") son dos direcciones de memoria distinta, y se 
    // concluye que son objetos distintos *aunque* tengan el mismo 
    // contenido, por eso se quiere hacer un override de Equals() para
    // que el HashSet determine si YA existe un estado NO por la
    // direccion de memoria a la que apunta el objeto sino por el
    // contenido que tiene
    {
        // Rescatando el comentario de arriba, como obj 
        // puede ser un objeto de cualquier clase, aqui filtramos
        // evaluando solo si es de tipo Facto, si no es de tipo Facto
        // ya simplemente devolvemos un false
        if (obj is Facto f)
        // La implementacion interna de HashSet llama al metodo
        // Equals() del objeto que viva en un lugar del set(que
        // en este caso dicho objeto resulta ser un Facto)
        // cuando se intenta introducir otro objeto que tiene el mismo
        // hash que uno ya almacenado se llama a este metodo por lo que
        // aqui se retorna un bool resultante de hacer la comparacion
        // de abajo que mira si el nombre y argumentos del objeto
        // almacenado es el mismo que el nombre y argumentos del objeto
        // que pretende entrar al set. Si son iguales entonces el que 
        // pretende entrar es descartado pero si no son iguales devuelve
        // false y dejarias entrar al HashSet objetos duplicados.
        // Esto es importante porque al hacer Override le estamos
        // quitando el control a C# sobre el manejo de duplicados
        // en el set por lo que podriamos acabar haciendo que un 
        // set que de vanilla NO soporta duplicados los acabe soportando
        // xd, hay que tener cuidado con esto.
            return Nombre == f.Nombre && Argumentos.SequenceEqual(f.Argumentos);
        return false;
    }

    public override int GetHashCode() => HashCode.Combine(Nombre, Argumentos.Count);
    // Mas de lo mismo, sobreescribimos el metodo GetHashCode() que de 
    // vanilla retorna Hashes por referencia y eso no lo queremos.
    // entonces definimos los hashes "en funcion" del contenido
    // del obejto y NO de la direccion de memoria del objeto.
    // Ahi estamos generado un Hash a partir del Nombre del Facto
    // que es el tipo de Facto como Libre, EncimaDe, etc. y Luego 
    // un .Count() de los argumentos, a partir de esos dos inputs
    // genera un hash usando una funcion matematica determinista.
    // Entonces EncimaDe(A,B) y EncimaDe(C,D) devuelven el mismo hash
    // por lo que desempatan con el metodo Equals() para determinar
    // que ambos son distintos, aqui hay una disminucion del rendimiento
    // y esto se podria hacer mejor para no estar llamando a 
    // Equals() tantas veces pero nos podemos preocupar del
    // perf una vez todo este implementado porque de momento no lo esta
    // xd.

    public override string ToString() => $"{Nombre}({string.Join(", ", Argumentos)})";
}
}