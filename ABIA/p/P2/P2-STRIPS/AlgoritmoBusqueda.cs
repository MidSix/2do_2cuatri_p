

namespace STRIPS
{
    // Esto es lo de las interfaces que implementamos en la practica 1
    // Basicamente obliga que todas las clases que hereden de esta
    // interfaz implementen los metodos(firmas) que esta define.
    // La diferencia entre una Interfaz y una clase abstracta es que la
    // primera a diferencia de la segunda NO tiene atributos/campos 
    // es decir, no tiene un 'estado', una interfaz solo define metodos
    public interface IAlgoritmoBusqueda // Para recordar la 'I' que 
    // se antecede es simplemente una convencion de C# para llamar 
    // a las clases que son interfaces, igual que en python usamos
    // el prefijo '_' sobre el nombre de atributos 
    // para especificar que son protegidos aunque sintacticamente
    // no hagan absolutamente nada semanticamente tienen su utilidad.
    {
        List<Accion>? Buscar(Estado inicial, Estado objetivo, List<Accion> operadores);
    }

    // Aqui esta BFS que antes se implementaba en Planificador.cs
    // se decidio moverlo aqui para separar correctamente los roles.
    public class BusquedaAnchura : IAlgoritmoBusqueda
    {
        public List<Accion>? Buscar(Estado inicial, Estado objetivo, List<Accion> operadores)
        {
            Queue<(Estado estadoActual, List<Accion> camino)> cola = new Queue<(Estado, List<Accion>)>();
            HashSet<string> visitados = new HashSet<string>();
            cola.Enqueue((inicial, new List<Accion>()));

            int nodosExpandidos = 0;

            while (cola.Count > 0)
            {
                var (actual, planActual) = cola.Dequeue();
                nodosExpandidos++;

                if (actual.Satisface(objetivo))
                {
                    Console.WriteLine($"[BusquedaAnchura] Objetivo alcanzado tras evaluar {nodosExpandidos} estados.");
                    return planActual;
                }

                string hashEstado = ObtenerIdentificadorEstado(actual);
                if (visitados.Contains(hashEstado)) continue;
                
                visitados.Add(hashEstado);

                foreach (var operador in operadores)
                {
                    if (operador.EsAplicable(actual))
                    {
                        cola.Enqueue((operador.Aplicar(actual), new List<Accion>(planActual) { operador }));
                    }
                }
            }

            Console.WriteLine("[BusquedaAnchura] No se ha encontrado ninguna solución posible.");
            return null;
        }

        private string ObtenerIdentificadorEstado(Estado e)//Esto es para crear un identificador único 
        // para cada estado, para evitar ciclos,(Lo hubo que meter porque me crasheo el PC en el primer test xd)
        {
            return string.Join("|", e.Hechos
                .Select(f => f.ToString())
                .OrderBy(s => s));
        }
    }
}
