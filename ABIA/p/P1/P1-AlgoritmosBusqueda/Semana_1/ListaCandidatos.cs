namespace n_reinas
{
public interface IListaCandidatos// Esto es como una clase abstracta en Python, pero en C# se llama interfaz
{
    void Anhadir(Solucion solucion, int prioridad = 0);
    void Borrar(Solucion solucion);
    Solucion ObtenerSiguiente();
    int Count { get; } // Reemplaza al __len__
}

public class ColaDePrioridad : IListaCandidatos
{
    private PriorityQueue<Solucion, int> _cp = new();
    private Dictionary<string, Solucion> _buscador = new();
    public int REMOVED_COST { get; set; } = -1;
    public int Count => _buscador.Count;
    public void Anhadir(Solucion solucion, int prioridad = 0)
    {
        string id = solucion.ToString();

        if (_buscador.ContainsKey(id))
        {
            var solucionExistente = _buscador[id];
            if (solucionExistente.Coste <= prioridad) return;
            
            Borrar(solucionExistente);
        }

        _buscador[id] = solucion;
        _cp.Enqueue(solucion, prioridad);
    }

    public void Borrar(Solucion solucion)
    {
        string id = solucion.ToString();
        if (_buscador.Remove(id, out var encontrada))
        {
            encontrada.Coste = REMOVED_COST;// Marcado lógico: le ponemos un coste imposible

        }
    }

    public Solucion ObtenerSiguiente()
    {
        while (_cp.Count > 0)
        {
            var solucion = _cp.Dequeue();

            if (solucion.Coste != REMOVED_COST)
            {
                _buscador.Remove(solucion.ToString());
                return solucion;
            }
        }
        throw new KeyNotFoundException("No hay más candidatos.");// Esto es como un StopIteration en Python
    }
}

}