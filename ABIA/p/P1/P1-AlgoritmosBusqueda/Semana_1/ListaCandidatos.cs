namespace n_reinas
{
public interface ListaCandidatos// Esto es como una clase abstracta en Python, pero en C# se llama interfaz
{
    void Anhadir(Solucion solucion, int prioridad = 0);
    void Borrar(Solucion solucion);
    Solucion ObtenerSiguiente();
    int Count { get; } // Reemplaza al __len__
}
public class ColaDePrioridad : ListaCandidatos
{
    private ListaCandidatos lista;

    public ColaDePrioridad(ListaCandidatos lista)
    {
        this.lista = lista;
    }

    public void Anhadir(Solucion solucion, int prioridad = 0)
    {
        this.lista.Anhadir(solucion, prioridad);
    }

    public void Borrar(Solucion solucion)
    {
        this.lista.Borrar(solucion);
    }

    public Solucion ObtenerSiguiente()
    {
        return this.lista.ObtenerSiguiente();
    }

    public int Count => this.lista.Count;
}


}