/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/
using n_reinas;
namespace Ejecuciones{
//Igual reutilizo algo de código aqui, pero me parece mejor tenerlo algunas cosas a la vista
//en el mismo archivo, para no tener que ir a buscarlo a otro lado.
public class Ejecucion3
{
    public int CalculoCoste(Solucion actual, Solucion vecino)
    {
        return 1; 
    }
    public int CalculoHeuristica(Solucion solucion)
    {
    int conflictos = 0;
    int n = solucion.Coords?.Count ?? 0;

    for (int i = 0; i < n; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            var r1 = solucion.Coords![i];
            var r2 = solucion.Coords![j];

            if (r1.Item1 == r2.Item1 || // Comprobamos si se atacan (Misma Fila, Columna o Diagonal)
                r1.Item2 == r2.Item2 || 
                Math.Abs(r1.Item1 - r2.Item1) == Math.Abs(r1.Item2 - r2.Item2))
            {
                conflictos++;
            }
        }
    }
        return conflictos;
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
    
    //----------------------------------------------------------------------------------------------------------------------------
    public static void Semana3()
    {
        int reinas = 3; // Empezamos en 3 para que la primera iteración pruebe con 4
        var ejec = new Ejecucion3();
        int revisados = 0; 
        Console.WriteLine("Ejecución Búsqueda A*:");
        while (revisados < 15000)
        {
            AEstrella astar = new AEstrella();
            reinas++; 


            var solucion_inicial_coords = new List<Tuple<int, int>>();
            for (int i = 0; i < reinas; i++)
            {
                solucion_inicial_coords.Add(new Tuple<int, int>(0, i));
            }
            var solucionInicial = new Solucion(0, solucion_inicial_coords);


            (_, revisados) = astar.Busqueda(solucionInicial, ejec.CriterioParada, ejec.GenerarVecinos, ejec.CalculoCoste, ejec.CalculoHeuristica);

            Console.WriteLine($"(BúsquedaAStar)Reinas: {reinas} \t| Nodos expandidos: {revisados}");
        }
        
        Console.WriteLine("Límite de 15000 alcanzado");
        reinas=3;
        revisados=0;
        var ejec2 = new Ejecucion3();
        Console.WriteLine("Ejecución Búsqueda Avara:");
        while (revisados < 15000)
        {
            BusquedaAvara avara = new BusquedaAvara();
            reinas++;
            
            var solucion_inicial_coords = new List<Tuple<int, int>>();
            for (int i = 0; i < reinas; i++)
            {
                solucion_inicial_coords.Add(new Tuple<int, int>(0, i));
            }
            var solucionInicial = new Solucion(0, solucion_inicial_coords);

            (_, revisados) = avara.Busqueda(solucionInicial, ejec2.CriterioParada, ejec2.GenerarVecinos, ejec2.CalculoCoste, ejec2.CalculoHeuristica);

            Console.WriteLine($"(BúsquedaAvara)Reinas: {reinas} \t| Nodos expandidos: {revisados}");
        }
        
        Console.WriteLine("Límite de 15000 alcanzado");
    }
    
}
}
