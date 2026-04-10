/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/
using STRIPS;

namespace MundoBloques
{
    public static class MundoBloques
    {
        public static void ResolverEscenarioA()//Primer escenario
        {
            var bloques = new List<string> { "A", "B", "C" };
            var operadores = GenerarOperadores(bloques);

        // Estado Inicial todos en la mesa
            var inicial = new Estado(new List<Facto> {
                new Facto("SobreMesa", "A"),
                new Facto("SobreMesa", "B"),
                new Facto("SobreMesa", "C"),
                new Facto("Despejado", "A"),
                new Facto("Despejado", "B"),
                new Facto("Despejado", "C")
            });

            // Objetivo 1a: Pila A-B-C (A arriba, C abajo)
            var objetivo = new Estado(new List<Facto> {
                new Facto("SobreMesa", "C"),
                new Facto("EncimaDe", "B", "C"),
                new Facto("EncimaDe", "A", "B"),
                new Facto("Despejado", "A")
            });

            EjecutarAgente(inicial, objetivo, operadores);
        }


        public static void ResolverEscenarioB()//SEgundo escenario
        {
            var bloques = new List<string> { "A", "B", "C", "D", "E", "F" };
            var operadores = GenerarOperadores(bloques);

            // Estado Inicial 1b: 3 pilas: Pila(en orden arriba-abajo) C-B-A, Pila F-E, Bloque D solo
            var inicial = new Estado(new List<Facto> {
                new Facto("EncimaDe", "C", "B"), new Facto("EncimaDe", "B", "A"), new Facto("SobreMesa", "A"),
                new Facto("EncimaDe", "F", "E"), new Facto("SobreMesa", "E"),
                new Facto("SobreMesa", "D"),
                new Facto("Despejado", "C"), new Facto("Despejado", "F"), new Facto("Despejado", "D")
            });

            // Objetivo 1b: 3 pilas de dos bloques(en orden arriba-abajo) E-C, F-B, D-A
            var objetivo = new Estado(new List<Facto> {
                new Facto("EncimaDe", "E", "C"), new Facto("SobreMesa", "C"),
                new Facto("EncimaDe", "F", "B"), new Facto("SobreMesa", "B"),
                new Facto("EncimaDe", "D", "A"), new Facto("SobreMesa", "A"),
                new Facto("Despejado", "E"), new Facto("Despejado", "F"), new Facto("Despejado", "D")
            });

            EjecutarAgente(inicial, objetivo, operadores);
        }

        private static void EjecutarAgente(Estado inicial, Estado objetivo, List<Accion> ops)
        {//Aqui simplemente inicializamos el planificador con los operadores que hemos generado y se lo damos al agente
            Planificador planificador = new Planificador(ops);
            Agente agente = new Agente(planificador);
            agente.EjecutarTarea(inicial, objetivo);
        }


        private static List<Accion> GenerarOperadores(List<string> bloques)//esta es la funcion más importante de aqui
        {/*
            Esta función es el motor que automatiza la creación de todas las acciones 
            "legales" por asi decirlo del mundo:

            -Crea los tres tipos de movimientos permitidos generando las acciones para mover un 
              bloque de un sitio a otro (Bloque a Mesa, Mesa a Bloque y Bloque a Bloque).
            -Se asegura de q se respeta la física al definir las precondiciones necesarias para que el agente 
              respete las reglas, como que el bloque a mover no tenga nada encima y que el destino esté libre.
            -Actualiza la lógica del mundo al establecer las Listas de Adición y Borrado de STRIPS,
              indicando qué hechos dejan de ser ciertos y cuáles pasan a ser verdad tras cada movimiento.
            -HAce un shuffle de todas las posibilidades mediante bucles anidados, 
              crea todas las combinaciones posibles de origen y destino para que el planificador 
              tenga como un"catalogo" completo de dónde elegir para llegar al objetivo.
        */
            var lista = new List<Accion>();

            foreach (var b in bloques)
            {
                foreach (var s in bloques)
                {
                    if (b == s) continue;

                    var m2m = new Accion($"Mover {b} de {s} a Mesa");//Operador mover de bloque a mesa
                    m2m.Precondiciones.Add(new Facto("Despejado", b)); // No puede moverse si tiene otro encima 
                    m2m.Precondiciones.Add(new Facto("EncimaDe", b, s));
                    m2m.ListaBorrado.Add(new Facto("EncimaDe", b, s));
                    m2m.ListaAdicion.Add(new Facto("SobreMesa", b));
                    m2m.ListaAdicion.Add(new Facto("Despejado", s));
                    lista.Add(m2m);

                    var m2b = new Accion($"Mover {b} de Mesa a {s}");//operador mover de mesa a bloque
                    m2b.Precondiciones.Add(new Facto("Despejado", b));
                    m2b.Precondiciones.Add(new Facto("SobreMesa", b));
                    m2b.Precondiciones.Add(new Facto("Despejado", s)); // No puede moverse sobre uno ocupado 
                    m2b.ListaBorrado.Add(new Facto("SobreMesa", b));
                    m2b.ListaBorrado.Add(new Facto("Despejado", s));
                    m2b.ListaAdicion.Add(new Facto("EncimaDe", b, s));
                    lista.Add(m2b);

                    foreach (var d in bloques)
                    {
                        if (d == b || d == s) continue;

                        var b2b = new Accion($"Mover {b} de {s} a {d}");//operador mover de bloque a bloque
                        b2b.Precondiciones.Add(new Facto("Despejado", b));
                        b2b.Precondiciones.Add(new Facto("EncimaDe", b, s));
                        b2b.Precondiciones.Add(new Facto("Despejado", d));
                        b2b.ListaBorrado.Add(new Facto("EncimaDe", b, s));
                        b2b.ListaBorrado.Add(new Facto("Despejado", d));
                        b2b.ListaAdicion.Add(new Facto("EncimaDe", b, d));
                        b2b.ListaAdicion.Add(new Facto("Despejado", s));
                        lista.Add(b2b);
                    }
                }
            }
            return lista;
        }
    }
}