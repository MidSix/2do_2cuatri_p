/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/

namespace STRIPS{

    public class Planificador
    {
        private List<Accion> _operadores;

        public Planificador(List<Accion> operadores)
        {
            _operadores = operadores;//LLamo a las acciones operadores aqui por una movida de C#, que me decia que habia ambiguedad entre el constructor de Planificador y el metodo GenerarPlan, que tambien se llama Planificador, asi que le puse _operadores para diferenciarlo
        }
        public List<Accion> GenerarPlan(Estado inicial, Estado objetivo)//Aplicamos Busqueda en Anchura
        {//Recicle el código de BFS que hice para el ejercicio anterior, pero adaptandolo a STRIPS.
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
                    Console.WriteLine($"[Planificador] Objetivo alcanzado tras evaluar {nodosExpandidos} estados.");//Esto es para debugging, lo quitaré luego
                    return planActual;
                }

                string hashEstado = ObtenerIdentificadorEstado(actual);
                if (visitados.Contains(hashEstado))
                {
                    continue;
                }
                visitados.Add(hashEstado);

                foreach (var operador in _operadores)
                {
                    if (operador.EsAplicable(actual))//Es aplicable solo si se cumplen las precondiciones de la acción en el estado actual
                    {
                        Estado siguienteEstado = operador.Aplicar(actual);
                        List<Accion> siguientePlan = new List<Accion>(planActual) { operador };
                        cola.Enqueue((siguienteEstado, siguientePlan));
                    }
                }
            }

            Console.WriteLine("[Planificador] No se ha encontrado ninguna solución posible.");
            return null;
        }

        private string ObtenerIdentificadorEstado(Estado e)//Esto es para crear un identificador único para cada estado, para evitar ciclos en la búsqueda
        {
            return string.Join("|", e.Hechos
                .Select(f => f.ToString())
                .OrderBy(s => s));
        }
    }
}


