# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import heapq


REMOVED = '<removed-task>'  # placeholder for a removed task


class Solucion:#clase solucion que hace override de metodos magicos, no se como se hace en C#

    def __init__(self, coords, coste=0):
        self.coords = coords
        self.coste = coste

    def __eq__(self, other):
        return str(self.coords) == str(other.coords)

    def __lt__(self, other):
        return str(self.coste) < str(other.coste)

    def __str__(self):
        return '-'.join(str(x) for x in self.coords)


class ListaCandidatos:#Una clase abstracta

    def anhadir(self, solucion, prioridad=0):
        pass

    def borrar(self, solucion):
        pass

    def obtener_siguiente(self):
        pass

    def __len__(self):
        pass


class ColaDePrioridad(ListaCandidatos):#Cola de prioridad, usando la interfaz de ListaCandidatos

    def __init__(self):
        self.cp = []# crea una lista y un diccionario
        self.buscador = {}

    def anhadir(self, solucion, prioridad=0):
        str_solucion = str(solucion)
        if str_solucion in self.buscador:
            solucion_buscador = self.buscador[str_solucion]
            if solucion_buscador[0] <= prioridad:
                return
            self.borrar(solucion)
        entrada = [prioridad, solucion]
        self.buscador[str_solucion] = entrada
        heapq.heappush(self.cp, entrada)

    def borrar(self, solucion):
        entrada = self.buscador.pop(str(solucion))
        entrada[-1].coste = REMOVED

    def obtener_siguiente(self):
        while self.cp:
            prioridad, solucion = heapq.heappop(self.cp)
            if solucion.coste is not REMOVED:
                del self.buscador[str(solucion)]
                return solucion
        raise KeyError('no hay siguiente en una cola de prioridad vacia')

    def __len__(self):
        return len(self.buscador)


class AlgoritmoDeBusqueda:

    def __init__(self, lista=ListaCandidatos):
        self.lista = lista

    def calculo_de_prioridad(self, nodo_info, calculo_heuristica=None):
        return 0

    def busqueda(self, solucion_inicial, criterio_parada, obtener_vecinos, calculo_coste, calculo_heuristica=None):
        candidatos = self.lista()
        candidatos.anhadir(Solucion(solucion_inicial, 0))
        vistos = dict()
        finalizado = False
        revisados = 0
        while len(candidatos) > 0 and not finalizado:
            solucion = candidatos.obtener_siguiente()
            vistos[str(solucion)] = solucion.coste
            revisados += 1
            if criterio_parada(solucion):
                finalizado = True
                break
            vecinos = obtener_vecinos(solucion)
            for vecino in vecinos:
                nueva_solucion = Solucion(
                    coords = vecino
                )
                if str(nueva_solucion) not in vistos:
                    nueva_solucion.coste = solucion.coste+calculo_coste(solucion, nueva_solucion)
                    candidatos.anhadir(nueva_solucion, prioridad=self.calculo_de_prioridad(nueva_solucion, calculo_heuristica))
        if not finalizado:
            return None
        return solucion, revisados


class AEstrella(AlgoritmoDeBusqueda):

    def __init__(self):
        super(AEstrella, self).__init__(ColaDePrioridad)

    def calculo_de_prioridad(self, solucion, calculo_heuristica=None):
        return solucion.coste + calculo_heuristica(solucion)


if __name__ == '__main__':
    reinas = 4
    solucion_inicial = [(0,i) for i in range(reinas)]

    def calculo_coste(solucion, nueva_solucion):
        return 1

    def calculo_heuristica(solucion):
        return 0

    def obtener_vecinos(solucion):
        vecinos = []
        for i in range(len(solucion.coords)):
            vecino = [*solucion.coords]
            vecino[i] = ((vecino[i][0] + 1) % reinas, vecino[i][1])
            vecinos.append(vecino)
        return vecinos

    def criterio_parada(solucion):
        for i in range(len(solucion.coords)):
            nodo_i = solucion.coords[i]
            for j  in range(i+1, len(solucion.coords)):
                nodo_j = solucion.coords[j]
                if nodo_i[0] == nodo_j[0] or nodo_i[1] == nodo_j[1] or abs(nodo_i[0] - nodo_j[0]) == abs(nodo_i[1] - nodo_j[1]):
                    return False
        return True

    astar = AEstrella()
    solucion, revisados = astar.busqueda(solucion_inicial, criterio_parada, obtener_vecinos, calculo_coste, calculo_heuristica)
    print('Coordenadas:', solucion.coords)
    print('Nodos evaluados:', revisados)


