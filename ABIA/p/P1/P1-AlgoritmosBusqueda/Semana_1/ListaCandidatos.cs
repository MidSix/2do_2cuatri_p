/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/

namespace n_reinas
{
public interface IListaCandidatos// Esto es como una clase abstracta en Python, pero en C# se llama interfaz
{
    /*
        Y es muy curioso esto de las interfaces, aunque en python
        existen como concepto, no existen como sintaxis. NO hay un
        equivalente sintacticamente hablando en python de las interfaces,
        porque en python existe la herencia multiple. Por tanto puedes
        hacer que una clase herede de varias clases abstractas y
        ya esta. Sin embargo en C# no puedes hacer eso, solo 
        puedes heredar de una clase, por lo que se crea una
        distincion entre lo que engloba lo que ES un objeto
        (Clase abstracta ya que esta puede implementar atributos) 
        y SU comportamiento(interface dado que este SOLO puede implementar
        metodos y no atributos). En python la interfaz existe solo como concepto
        pues simplemente seria una clase abstracta sin atributos,
        solo con metodos, y al permitirse la herencia multiple gucci. 
        Una clase abstracta con atributos y el resto de clases abstractas
        con comportamiento(conceptualmente una interface). En C# 
        tendria que ser una clase abstracta con atributos
        e interfaces con comportamiento. Hay que fijarse que una
        interfaz no es una clase, por eso puede ser heredada por varias
        clases.
    */
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