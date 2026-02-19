namespace n_reinas
{   
public class AlgoritmoDeBusqueda
{
    public IListaCandidatos? Lista { get; set; }
    public int CalculoDePrioridad(object nodo_info, object? calculo_heuristica = null)
    {
        return 0;  
    }
   // Usamos PascalCase para el nombre del método: Busqueda
public (Solucion?, int) Busqueda(
    Solucion solucionInicial, 
    Func<Solucion, bool> criterioParada,       // Recibe Solucion, devuelve bool
    Func<Solucion, List<Solucion>> obtenerVecinos, // Recibe Solucion, devuelve Lista
    Func<Solucion,Solucion ,int> calculoCoste,   // Recibe 2 Solucion, devuelve int
    Func<Solucion, int>? calculoHeuristica = null)
{

    IListaCandidatos candidatos = Lista ?? throw new InvalidOperationException("La lista no está inicializada.");
    
    candidatos.Anhadir(solucionInicial, 0); 
    var vistos = new Dictionary<string, int>(); // Para evitar ciclos: mapeamos la representación de la solución a su coste más bajo encontrado
    bool finalizado = false;
    int revisados = 0;

    while (!finalizado && candidatos.Count > 0)
    {
        var solucion = candidatos.ObtenerSiguiente();
        vistos[solucion.ToString()] = solucion.Coste; // Guardamos el coste de la solución actual
        revisados+=1;

        if (criterioParada(solucion))
        {
            finalizado = true;
            break; // Salimos del bucle si se cumple el criterio de parada
        }
        else
        {
            var vecinos = obtenerVecinos(solucion);
            foreach (var vecino in vecinos)
            {
                var nueva_solucion= new Solucion(); // Creamos una nueva instancia para evitar mutar la original
                nueva_solucion.Coords=vecino.Coords; // Copiamos las coordenadas del vecino
                
                if (vistos.ContainsKey(nueva_solucion.ToString()))
                {
                    nueva_solucion.Coste=solucion.Coste+calculoCoste(solucion,nueva_solucion); // Calculamos el coste acumulado para esta nueva solución
                    candidatos.Anhadir(nueva_solucion,CalculoDePrioridad(nueva_solucion,calculoHeuristica));   
                }
            }
        if (!finalizado)
        {
            return (null, revisados); // Si no se ha encontrado una solución, devolvemos null y el número de nodos revisados   
        };
        }
    }
    return (solucion, revisados); 
    }
}
}