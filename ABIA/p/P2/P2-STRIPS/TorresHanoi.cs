/*
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - jueves.
*/
using STRIPS;

namespace TorresHanoi
{
    public static class TorresHanoi
    {
        public static void Resolver(int n)
        {
            List<string> postes = new List<string> { "PosteA", "PosteB", "PosteC" };
            List<string> discos = new List<string>();
            for (int i = 1; i <= n; i++) discos.Add($"D{i}"); // D1 es el menor, Dn es el mayor

            List<Facto> hechosIniciales = new List<Facto>(); // Genera el estado incial
            
            // Apilar todos los discos en el PosteA (Izquierdo)
            hechosIniciales.Add(new Facto("Sobre", $"D{n}", "PosteA"));
            for (int i = n - 1; i >= 1; i--)
            {
                hechosIniciales.Add(new Facto("Sobre", $"D{i}", $"D{i+1}"));
            }

            // Cúspides despejadas (el disco más pequeño y los otros dos postes)
            hechosIniciales.Add(new Facto("Despejado", "D1"));
            hechosIniciales.Add(new Facto("Despejado", "PosteB"));
            hechosIniciales.Add(new Facto("Despejado", "PosteC"));

            // Leyes físicas estáticas: MenorQue
            foreach (var d in discos)
            {
                foreach (var p in postes)
                    hechosIniciales.Add(new Facto("MenorQue", d, p)); // Todo disco cabe en un poste
            }
            for (int i = 1; i <= n; i++)
            {
                for (int j = i + 1; j <= n; j++)
                    hechosIniciales.Add(new Facto("MenorQue", $"D{i}", $"D{j}")); // Di es menor que Dj
            }

            Estado inicial = new Estado(hechosIniciales);

            // Generando estado objeto
            List<Facto> hechosObjetivo = new List<Facto>();
            
            // Apilar todos los discos en el PosteC (Derecho)
            hechosObjetivo.Add(new Facto("Sobre", $"D{n}", "PosteC"));
            for (int i = n - 1; i >= 1; i--)
            {
                hechosObjetivo.Add(new Facto("Sobre", $"D{i}", $"D{i+1}"));
            }
            Estado objetivo = new Estado(hechosObjetivo);

            // Generar acciones posibles
            List<string> entidades = new List<string>(postes);
            entidades.AddRange(discos);
            List<Accion> acciones = new List<Accion>();

            foreach (var disco in discos)
            {
                foreach (var origen in entidades)
                {
                    if (disco == origen) continue;
                    foreach (var destino in entidades)
                    {
                        if (disco == destino || origen == destino) continue;

                        var accion = new Accion($"Mover {disco} de {origen} a {destino}");
                        accion.Precondiciones.Add(new Facto("Despejado", disco));
                        accion.Precondiciones.Add(new Facto("Sobre", disco, origen));
                        accion.Precondiciones.Add(new Facto("Despejado", destino));
                        accion.Precondiciones.Add(new Facto("MenorQue", disco, destino)); // La clave de Hanoi

                        accion.ListaBorrado.Add(new Facto("Sobre", disco, origen));
                        accion.ListaBorrado.Add(new Facto("Despejado", destino));

                        accion.ListaAdicion.Add(new Facto("Sobre", disco, destino));
                        accion.ListaAdicion.Add(new Facto("Despejado", origen));

                        acciones.Add(accion);
                    }
                }
            }

            // Ejecucion del Agente
            Planificador planificador = new Planificador(acciones, new BusquedaAnchura());
            Agente agente = new Agente(planificador);
            agente.EjecutarTarea(inicial, objetivo);
        }
    }
}