/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/
namespace STRIPS
{
    public class Agente
    {
        private Planificador _planificador;//Estas de aqui son private porque no queremos que nadie más que el agente pueda acceder a ellas, el planificador es parte del agente y el estado actual también
        private Estado _estadoActual;//(No queremos que sea accesible porque el agente es el único que debe manejar su estado interno)

        public Agente(Planificador planificador)
        {
            _planificador = planificador;//Hacemos que se inicialice el planificador al crear el agente
        }

        public void EjecutarTarea(Estado inicial, Estado objetivo)
        {
            Console.WriteLine("Estado Inicial:");
            MostrarMundo(inicial);//Mostramos el estado inicial del mundo
            Console.WriteLine("========================================\n");
            Console.WriteLine("Objetivo:");
            MostrarMundo(objetivo);//Mostramos el estado objetivo del mundo
            Console.WriteLine("========================================\n");
            _estadoActual = inicial;

            List<Accion> plan = _planificador.GenerarPlan(inicial, objetivo);//Aqui obtenemos el plan

            if (plan == null)//Esto en principio no lo habia puesto, pero es importante comprobar 
            // si el planificador ha encontrado un plan válido o no, 
            // porque si no lo ha encontrado y el plan es null, 
            // entonces intentar ejecutar un plan null nos daría un error
            {
                Console.WriteLine("El agente no ha encontrado un plan válido.");
                return;
            }

            Console.WriteLine("Plan Generado por Agente:");//Mostramos el plan completo
            for (int i = 0; i < plan.Count; i++)
            {
                Console.WriteLine($"{i + 1}. {plan[i].Nombre}");
            }
            Console.WriteLine("========================================\n");//Un separarador Fancy

            // 3. Ejecutar cada acción del plan secuencialmente
            foreach (var accion in plan)
            {
                _estadoActual = accion.Aplicar(_estadoActual);//Aplicamos la acción en la cola

                // 4. Mostrar el entorno actualizado tras cada acción 
                Console.WriteLine($"\nEjecutando: {accion.Nombre}");
                MostrarMundo(_estadoActual);//LLamamos a mostrar mundo en cada accion, como requiere la practica

            }

            Console.WriteLine("Objetivo alcanzado");
        }
        private void MostrarMundo(Estado estado)
        {
            Console.WriteLine("Estado del Mundo actual:");
            DibujarMundoBloques(estado);//Aqui pondremos un if dependiendo de si es hanoi o bloques, de momento lo dejo fijo
        }
        private static void DibujarMundoBloques(Estado estado)//Esta representación es bastante básica,
            {//pero llevo un rato decidirme por como queria representar el mundo, y esta llevo bastante tiempo jajaja
                var bases = estado.Hechos//Primero queremos aquellos bloques que están sobre la mesa
                    .Where(f => f.Nombre == "SobreMesa")
                    .Select(f => f.Argumentos[0])
                    .ToList();

                // 2. Para cada base, construimos su torre hacia arriba
                List<List<string>> torres = new List<List<string>>();//Basicamente construimos "torres" de bloques
                foreach (var baseBloque in bases)//para cada bloque en la mesa, miramos si tiene uno encima, y loañadimos
                {//y luego miramos si el que tiene encima tiene otro encima, y asi sucesivamente hasta que no haya más bloques encima, 
                // entonces tendremos una torre completa de bloques sobre esa base y pasaremos a la siguiente base de torre
                    List<string> torreActual = new List<string> { baseBloque };
                    string actual = baseBloque;
                    bool tieneEncima = true;//Por defecto asumimos que tiene un bloque encima
                    while (tieneEncima)
                    {
                        var encima = estado.Hechos.FirstOrDefault(f => f.Nombre == "EncimaDe" && f.Argumentos[1] == actual);
                        if (encima != null)
                        {
                            actual = encima.Argumentos[0];
                            torreActual.Add(actual);
                        }
                        else
                        {
                            tieneEncima = false;
                        }
                    }
                    torres.Add(torreActual);//Añadimos la torre completa a la lista de torres
                }

                // 3. Imprimir de forma legible (de arriba hacia abajo)
                int alturaMaxima = torres.Max(t => t.Count);//Queremos saber cual es la torre más alta para imprimir desde esa altura hacia abaj
                for (int nivel = alturaMaxima - 1; nivel >= 0; nivel--)
                {
                    string print = "";
                    foreach (var torre in torres)
                    {
                        if (nivel < torre.Count)
                            print += $" [{torre[nivel]}] ";
                        else
                            print += "     "; // Espacio vacío si la torre es más baja(puede ser que una torre tenga 3 bloques y otra solo 1, entonces en el nivel 2 la torre de 1 bloque ya no tiene nada que mostrar)
                    }
                    Console.WriteLine(print);
                }

                Console.WriteLine(new string('-', bases.Count * 5 + 2));//Esto es para dibujar una "mesa"
                Console.WriteLine("  M E S A  \n");
                //De hecho este código de bloques es bastante flexible, podriamos añadir n posiciones en la mesa, y el código seguiría funcionando sin necesidad de cambiar nada
                //hasta hice que la longitud de la mesa se adapte al número de bloques que hay, aunque en esta práctica solo hay 3 bloques
            }
    }
}
