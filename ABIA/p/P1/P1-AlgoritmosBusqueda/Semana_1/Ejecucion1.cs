/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/
using n_reinas;
namespace Ejecuciones{
public class Ejecucion1
{
    public int CalculoCoste(Solucion actual, Solucion vecino)//Función que calcula el coste incremental entre dos estados consecutivos. En este caso, se asume un coste uniforme de 1 para cada movimiento.
    {
        return 1; 
    }
    public int CalculoHeuristica(Solucion actual)//Funcion que no se utiliza en este caso, pero es necesaria para la firma del método de búsqueda. En A* se usaría para estimar el coste restante hasta la meta.
    {
        return 0; 
    }
    public List<Solucion> GenerarVecinos(Solucion actual)
    {
        var vecinos = new List<Solucion>();
        int n = actual.Coords?.Count ?? 0; 
        
        for (int i = 0; i < n; i++)
        {
            var nuevaPosicion = new List<Tuple<int, int>>(actual.Coords!);
            
            //    Lógica Python: vecino[i] = ((vecino[i][0] + 1) % reinas, vecino[i][1])
            //    Esto significa: Mantén la columna (Item2) igual, 
            //    pero incrementa la Fila (Item1) en 1.
            
            int filaActual = actual.Coords![i].Item1;
            int columnaFija = actual.Coords![i].Item2;
            
            int nuevaFila = (filaActual + 1) % n;// El operador % n hace que si está en la última fila, vuelva a la 0

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
                // Agregamos el chequeo de Item1 (Fila)
                if (solucion.Coords?[i].Item1 == solucion.Coords?[j].Item1 || // Me Faltaba esto antes Misma FILA
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
    public static void Semana1()
    {
        int reinas = 4;
        var solucion_inicial_coords = new List<Tuple<int, int>>();
        for (int i = 0; i < reinas; i++)
        {
            solucion_inicial_coords.Add(new Tuple<int, int>(0, i));
        }

        var ejec = new Ejecucion1();
        var solucionInicial = new Solucion(0, solucion_inicial_coords);

        AEstrella astar = new AEstrella();
        var (solucion, revisados) = astar.Busqueda(solucionInicial, ejec.CriterioParada, ejec.GenerarVecinos, ejec.CalculoCoste, ejec.CalculoHeuristica);

        Console.WriteLine($"Solución encontrada: {solucion}");
        Console.WriteLine($"Número de nodos expandidos: {revisados}");
    }

}
}