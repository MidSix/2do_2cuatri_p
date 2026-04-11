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
{
    public string Nombre { get; set; }
    public List<string> Argumentos { get; set; }

    public Facto(string nombre, params string[] argumentos)
    // Constructor de la clase, el compilador lo interpreta como tal
    // ya que tiene el mismo nombre que la clase. "params" es
    // simplemente una keyword que permite pasar un numero variable
    // de argumentos, el ejemplo mas cercano en python en "*"
    // simplemente que como en python no se especifican los tipos
    // basta simplemente con escribir *args y ya esta, aqui en C#
    // hay que especificar el tipo en en este caso string[] argumentos
    // entonces seria params = "*" y string[] argumentos = args.
    // keyword equivalence -> params = *
    // variable name equivalence -> argumentos = args
    {
        Nombre = nombre;
        Argumentos = argumentos.ToList();
    }

    public override bool Equals(object obj)// Esto es para comparar estados después
    {
        if (obj is Facto f)
            return Nombre == f.Nombre && Argumentos.SequenceEqual(f.Argumentos);
        return false;
    }

    public override int GetHashCode() => HashCode.Combine(Nombre, Argumentos.Count);

    public override string ToString() => $"{Nombre}({string.Join(", ", Argumentos)})";
}
}