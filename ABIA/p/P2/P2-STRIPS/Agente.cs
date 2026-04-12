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
        // 
        private Estado? _estadoActual;//(No queremos que sea accesible porque el agente es el único que debe manejar su estado interno)

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

            List<Accion>? plan = _planificador.GenerarPlan(inicial, objetivo);//Aqui obtenemos el plan

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

            // Ejecutar cada acción del plan secuencialmente
            foreach (var accion in plan)
            {
                _estadoActual = accion.Aplicar(_estadoActual);//Aplicamos la acción en la cola
                // Importante recalcar que aqui para nada
                // necesitamos comprobar si podemos o no aplicar
                // la accion porque ese trabajo de comprobacion
                // es trabajo del algoritmo de busqueda. En este punto
                // ya tenemos la seguridad de que las acciones del plan
                // no solo se pueden aplicar sino que son las correctas
                // por lo que simplemente las vamos aplicando de forma
                // secuencial para llegar al estado objetivo
                
                // .Aplicar() devuelve la clonacion del estado actual
                // eliminando y agregando los factos requeridos.

                // Mostrar el entorno actualizado tras cada acción 
                Console.WriteLine($"\nEjecutando: {accion.Nombre}");
                MostrarMundo(_estadoActual);//LLamamos a mostrar mundo en cada accion, como requiere la practica

            }

            Console.WriteLine("Objetivo alcanzado");
        }
        private void MostrarMundo(Estado estado) // Esta funcion hace
        // las de wrapper para llamar a la funcion de dibujo particular
        // que corresponde. Por tanto es esta la funcion la que llama
        // el agente.
        {
            Console.WriteLine("Estado del Mundo actual:");
            
            // Evaluamos dinámicamente en qué mundo estamos para evitar crasheos visuales
            if (estado.Hechos.Any(f => f.Nombre == "SobreMesa"))
            // Bastante self-explanined, si hay al menos un hecho 
            // del estado con el nombre 'SobreMesa' se trata 
            // del mundo de bloques
            {
                DibujarMundoBloques(estado);
            }
            else
            {
                DibujarTorresHanoi(estado);
            }
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

        private static void DibujarTorresHanoi(Estado estado)
        {
            string[] postes = { "PosteA", "PosteB", "PosteC" };
            List<List<string>> torres = new List<List<string>>();

            // Extraemos la configuración actual de cada torre
            foreach (var poste in postes)
            {
                List<string> torreActual = new List<string>();
                
                // Buscamos si hay algún disco directamente sobre la base de este poste
                var baseDisco = estado.Hechos.FirstOrDefault(f => f.Nombre == "Sobre" && f.Argumentos[1] == poste);
                
                if (baseDisco != null)
                {
                    string actual = baseDisco.Argumentos[0];
                    torreActual.Add(actual);
                    bool tieneEncima = true;
                    
                    // Escalamos la torre viendo qué disco está sobre el disco actual
                    while (tieneEncima)
                    {
                        var encima = estado.Hechos.FirstOrDefault(f => f.Nombre == "Sobre" && f.Argumentos[1] == actual);
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
                }
                torres.Add(torreActual);
            }

            // Dibujamos de arriba hacia abajo
            // Fijamos la altura máxima al total de discos para que el dibujo no salte
            int totalDiscos = torres.Sum(t => t.Count);
            int alturaMaxima = Math.Max(1, totalDiscos);

            Console.WriteLine(); // Espaciado extra
            for (int nivel = alturaMaxima - 1; nivel >= 0; nivel--)
            {
                string fila = "";
                foreach (var torre in torres)
                {
                    if (nivel < torre.Count)
                    {
                        string disco = $"[{torre[nivel]}]";
                        // Magia de C#: Centramos el string del disco en una columna de 10 caracteres
                        int paddingIzquierdo = (10 + disco.Length) / 2;
                        fila += disco.PadLeft(paddingIzquierdo).PadRight(10);
                    }
                    else
                    {
                        // Si no hay disco a esta altura, dibujamos el poste vertical
                        fila += "    |     ";
                    }
                }
                Console.WriteLine(fila);
            }

            // 3. Dibujamos las bases de los postes y la mesa
            Console.WriteLine("  |____|    |____|    |____|  ");
            Console.WriteLine("------------------------------");
            Console.WriteLine("  PosteA    PosteB    PosteC  \n");
        }
    }
}
