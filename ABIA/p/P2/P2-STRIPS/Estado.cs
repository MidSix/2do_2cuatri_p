/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/

namespace STRIPS{

    public class Estado
    {
        public HashSet<Facto> Hechos { get; private set; }//Aqui el hashset mencionado en el comentario de Facto.cs
        // Este HashSet es una propiedad cuyo setter solo es usable 
        // dentro de esta propia clase 
        //-----------------------------------------------------------
        // Aqui tenemos una sobrecarga de constructores. Es decir,
        // Estado puede inicializarse o bien como un hashset vacio,
        // o bien como un hashset con ya hechos incluido
        public Estado()
        {
            Hechos = new HashSet<Facto>();
        }
        public Estado(IEnumerable<Facto> hechosIniciales)//Esto es para crear un estado a partir de una lista de hechos, por ejemplo el estado inicial del mundo
        {
            Hechos = new HashSet<Facto>(hechosIniciales);
        }
        //___________________________________________________________

        //-----------------------------------------------------------
        // Ambos son metodos que albergan funciones anonimas
        // que llaman a los metodos Add y Remove que YA estan
        // implementados para los HashSet, con lo que nosotros
        // simplemente estamos encapsulando esas llamadas para hacerlas
        // mas sencillas. Nada mas.
        public void Agregar(Facto f) => this.Hechos.Add(f);//Añadir un facto
        public void Eliminar(Facto f) => this.Hechos.Remove(f);//Eliminar un facto
        //___________________________________________________________

        public bool Satisface(Estado objetivo) // Compara dos estados, en la practica se usará para comparar el estado actual del mundo con el estado objetivo
        {
            return objetivo.Hechos.All(this.Hechos.Contains);//Sencillito, si los hechos son identicos, los estados tambien
            //Si. Basciamente .All() es un metodo que se aplica sobre un
            // iterable, en este caso nuestra hashnet y espera recibir
            // como argumento una funcion que reciba como argumentos los
            // tipos de los argumentos que hay en el iterable sobre el
            // que se llama hashnet, en este caso el hashnet solo tiene
            // elementos de tipo Facto entonces espera recibir una
            // funcion que pueda recibir elementos de tipo facto 
            // y devolver un bool. Asi qeu .All() recorre nuestra
            // hashnet, y cada elemento se los pasa a la funcion 
            // Hechos.Contains "hay que recordar que NO estamos llamando
            // a esa funcion cuando la pasamos como argumento sino que
            // estamos pasando la referencia a la funcion, pero no 
            // llamandola", entonces cada elemento del HashSet de
            // objetivo.Hechos se le pasa al Hechos de la instancia
            // actual, si el facto esta devuelve true. Si devuelve true
            // para todos los factos quiere decir que dos estados
            // son el mismo ya que contienen los mismos factos.
        }


        public Estado Clonar()//Esto lo usará el planer para simular acciones sin reventar los estados
        {
            // Hacemos un deepcopy, no guardamos una nueva referencia
            // al mismo objeto porque pierde el punto de hacer esto.
            // el .ToArray() es necesario porque Facto espera recibir
            // un string[] y nosotros al crear esta instancia
            // convertimos a lista para poder usar el metodo .combine()
            // en el override del GetHashCode, una solucion bastante
            // comoda es simplemente pasar la lista de nuevo a array
            // para instanciar el Facto y luego volver a pasarla a Lista
            // un poco xd pero bueno. It works. Technical debt for a 
            // project that we'll never touch again, not a big problem.

            // Vale, esta linea esta cargada. Primero this.Hechos
            // contiene todos los factos del estado actual, te devuelve
            // un iterable que en este caso es una hashset, gucci. 
            // Ahora al aplicar .Select() este metodo implementa un 
            // loop interno que coge cada facto y con ese facto
            // instanciamos un nuevo facto cuyo nombre y argumentos
            // seran los mismos que el facto de la iteracion actual.
            // al terminar de ejecutar el .Select este devuelve un
            // iterable con todos los Factos que se le es pasado
            // al constructor de Estado, en este caso el constructor de
            // Estado esta usando su segunda definicion(el constructor
            // Estado esta sobrecargado). Con eso se crea correctamente
            // un nuevo Estado copia del actual.
            return new Estado(this.Hechos.Select(f => new Facto(f.Nombre, f.Argumentos.ToArray())));
        }

        public void Mostrar()//Esto es para mostrar el estado por consola, para debuggear y asi -> okay.
        {
            foreach (var hecho in Hechos.OrderBy(h => h.Nombre))
            {
                Console.WriteLine($" - {hecho}");
            }
        }
    }
}
