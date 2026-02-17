namespace n_reinas
{
public class Solucion
{
    public int Coste { get; set; }
    public Tuple<int,int>? Coords { get; set; }

    public override string ToString()//__str__
    {
        if (this.Coords != null)
        {
            return $"{this.Coords.Item1}-{this.Coords.Item2}";
        }
        return "Coordenadas: No definidas";
    }

    public static bool operator ==(Solucion a, Solucion b) => a.Coords?.ToString() == b.Coords?.ToString();
    public static bool operator !=(Solucion a, Solucion b) => !(a == b);
    public override bool Equals(object? obj) 
    {
        
        if (obj is not Solucion other) return false;// Si el otro objeto es nulo o no es de tipo Solucion, no son iguales

        if (ReferenceEquals(this, other)) return true;  // Si son la misma referencia en memoria, son iguales (optimización)

        return this.Coords == other.Coords;// Comparamos el contenido real
    }

    public override int GetHashCode() 
    {
        return HashCode.Combine(Coords);//Esto es una parida rara de referenciacion, no lo acabo de entender bien aun
    }
    
    public static bool operator <(Solucion? a, Solucion? b)
    {
    if (a is null) return b is not null; // Si a es nulo, entonces a < b solo si b no es nulo (porque un objeto nulo se considera menor que cualquier objeto no nulo)
    
    if (b is null) return false;

    return a.Coste < b.Coste;
    }

    public static bool operator >(Solucion? a, Solucion? b)
    {
        // Reutilizamos la lógica: "a > b" es lo mismo que decir "b < a"
        return b < a;
    }

    public static bool operator <=(Solucion? a, Solucion? b)
    {
        // "Menor o igual" es: o es menor, o son iguales
        return a < b || a == b;
    }

    public static bool operator >=(Solucion? a, Solucion? b)
    {
        return a > b || a == b;
    }
    //6 lineas de metodos mágicos en python = 40 lineas en C#, me encanta esta vaina

}
public interface IListaCandidatos// Esto es como una clase abstracta en Python, pero en C# se llama interfaz
{
    void Anhadir(Solucion solucion, int prioridad = 0);
    void Borrar(Solucion solucion);
    Solucion ObtenerSiguiente();
    int Count { get; } // Reemplaza al __len__
}


}