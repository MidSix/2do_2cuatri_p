/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/

using n_reinas;

namespace Ejecuciones
{
    public class Ejecucion2
    {
        public int CalculoCoste(Solucion actual, Solucion vecino)
        /*
            Calcula el coste de pasar de un estado a otro. Que es un estado?
            Es una configuracion de reinas en el tablero, representada
            por una lista de tuplas (fila, columna). basta con mover una reina
            para pasar de un estado a otro, lo que implica moverla de una fila
            a otra en la misma columna y eso incrementa el coste en 1.
        */
        {
            return 1;
        }

        public List<Solucion> GenerarVecinos(Solucion actual)
        {
            /*
                var -> keyword para inferencia de tipos, el compilador deduce el tipo a partir del valor asignado.
                los "!" es una indicacion al compilador que se usa para decirle que un nullable no es null en ese
                punto especifico.
            */
            var vecinos = new List<Solucion>();
            // "??" operador de coalescencia nula, si actual.Coords es null, entonces n será 0.
            int n = actual.Coords?.Count ?? 0;

            for (int i = 0; i < n; i++)
            {
                // Si entró a este bucle es porque actual.Coords no es null, 
                // entonces el "!" de `actual.Coords![i]` permite usarlo 
                // sin preocuparse por nulls en este contexto.
                // se llama "null-forgiving operator"
                var nuevaPosicion = new List<Tuple<int, int>>(actual.Coords!);
                int filaActual = actual.Coords![i].Item1;
                int columnaFija = actual.Coords![i].Item2;

                int nuevaFila = (filaActual + 1) % n;
                nuevaPosicion[i] = new Tuple<int, int>(nuevaFila, columnaFija);

                var nuevaSolucion = new Solucion(0, nuevaPosicion);
                vecinos.Add(nuevaSolucion);
            }

            return vecinos;
        }

        public bool CriterioParada(Solucion solucion)
        {
            int n = solucion.Coords?.Count ?? 0;
            for (int i = 0; i < n; i++)
            {
                for (int j = i + 1; j < n; j++)
                {
                    if (solucion.Coords?[i].Item1 == solucion.Coords?[j].Item1 || // Misma Fila
                        solucion.Coords?[i].Item2 == solucion.Coords?[j].Item2 || // Misma Columna
                        Math.Abs((solucion.Coords?[i].Item1 ?? 0) - (solucion.Coords?[j].Item1 ?? 0)) ==
                        Math.Abs((solucion.Coords?[i].Item2 ?? 0) - (solucion.Coords?[j].Item2 ?? 0))) // Diagonal
                    {
                        return false;
                    }
                }
            }
            return true;
        }

    //----------------------------------------------------------------------------------------------------------------------------

        public static void Semana2()
        {
            int reinas = 3;
            int revisados = 0;
            var ejec = new Ejecucion2();

            Console.WriteLine("--- Ejecución Búsqueda en Anchura (BFS) ---");
            while (revisados < 15000)
            {
                reinas++;
                var bfs = new BusquedaEnAnchura();

                var inicial_coords = new List<Tuple<int, int>>();
                for (int i = 0; i < reinas; i++)
                {
                    inicial_coords.Add(new Tuple<int, int>(0, i));
                }
                var solucionInicial = new Solucion(0, inicial_coords);

                (_, revisados) = bfs.Busqueda(solucionInicial, ejec.CriterioParada, ejec.GenerarVecinos, ejec.CalculoCoste);

                Console.WriteLine($"(BFS) Reinas: {reinas} \t| Nodos evaluados: {revisados}");

                // Evitar bucle infinito si por alguna razón no crece (aunque debería)
                if (reinas > 20) break;
            }
            Console.WriteLine("Límite de 15000 alcanzado o superado para BFS.\n");

            reinas = 3;
            revisados = 0;
            Console.WriteLine("--- Ejecución Búsqueda en Profundidad (DFS) ---");
            while (revisados < 15000)
            {
                reinas++;
                var dfs = new BusquedaEnProfundidad();

                var inicial_coords = new List<Tuple<int, int>>();
                for (int i = 0; i < reinas; i++)
                {
                    inicial_coords.Add(new Tuple<int, int>(0, i));
                }
                var solucionInicial = new Solucion(0, inicial_coords);

                (_, revisados) = dfs.Busqueda(solucionInicial, ejec.CriterioParada, ejec.GenerarVecinos, ejec.CalculoCoste);

                Console.WriteLine($"(DFS) Reinas: {reinas} \t| Nodos evaluados: {revisados}");

                if (reinas > 20) break;
            }
            Console.WriteLine("Límite de 15000 alcanzado o superado para DFS.\n");
        }
    }
}
