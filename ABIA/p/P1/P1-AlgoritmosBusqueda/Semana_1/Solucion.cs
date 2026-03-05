/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/

namespace n_reinas
{
// Esta es la clase que usamos para definir los estados, cada estado, es decir
// cada configuracion de reinas en el tablero, se representa con una instancia de esta clase.

// En ningun caso logico coords deberia ser null porque el unico punto donde se instancia
// esta clase es al crear la solucion inicial y al agregar vecinos. 
// para la solucion inicial se le asigna una lista de coordenadas, 
// y para los vecinos se se agregan nuevas instancias a partir de la solucion actual,
// que como minimo sera la inicial que ya tiene coordenadas.
public class Solucion(int coste, List<Tuple<int,int>>? coords)
{
    public int Coste { get; set; } = coste;
    public List<Tuple<int,int>>? Coords { get; set; } = coords;


    public override string ToString() //__str__
    {
        if (this.Coords != null)
        {
            string result = "";
            foreach (var coord in this.Coords)
            {
                result += $"{coord.Item1}-{coord.Item2} ";
            }
            return result.TrimEnd();
        }
        return "Coordenadas: No definidas";
    }
    // Sobrecarga de operadores para comparar soluciones
    public static bool operator ==(Solucion a, Solucion b) => a.Coords?.ToString() == b.Coords?.ToString();
    public static bool operator !=(Solucion a, Solucion b) => !(a == b);
    
    public override bool Equals(object? obj) 
    {
        if (obj is not Solucion other) return false;
        if (ReferenceEquals(this, other)) return true;
        
        if (this.Coords == null && other.Coords == null) return true;
        if (this.Coords == null || other.Coords == null) return false;
        
        return this.Coords.SequenceEqual(other.Coords);
    }

    public override int GetHashCode() 
    {
        if (Coords == null) return 0;
        return HashCode.Combine(string.Join(",", Coords.Select(c => $"{c.Item1}-{c.Item2}")));
    }
    
    public static bool operator <(Solucion? a, Solucion? b)
    {
    if (a is null) return b is not null; // Si a es nulo, entonces a < b solo si b no es nulo (porque un objeto nulo se considera menor que cualquier objeto no nulo)
    
    if (b is null) return false;

    return a.Coste < b.Coste;
    }

    public static bool operator >(Solucion? a, Solucion? b)
    {
        return b < a;// Reutilizamos la lógica: "a > b" es lo mismo que decir "b < a"
    }

    public static bool operator <=(Solucion? a, Solucion? b)
    {
        return a < b || a?.Equals(b) == true;
    }

    public static bool operator >=(Solucion? a, Solucion? b)
    {
        return a > b || a?.Equals(b) == true;
    }
    //6 lineas de metodos mágicos en python = 40 lineas en C#, me encanta esta vaina
}
}