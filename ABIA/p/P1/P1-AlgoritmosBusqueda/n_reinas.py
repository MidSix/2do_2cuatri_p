# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# El codigo original usaba de forma conceptual una clase abstracte
# pero no la implementaba como tal, es decir, no usaba la clase ABC de la libreria abc ni los decoradores @abstractmethod
# lo cual es un error conceptual, ya que sin eso la clase no es realmente abstracta
from abc import ABC, abstractmethod

# Aqui importamos la estructura de monticulos de la libreria heapq, que es una implementacion de monticulos binarios, 
# que son una estructura de datos que permite mantener una lista de elementos ordenados por prioridad, 
# donde el elemento con la menor prioridad es el primero en ser extraido "Si hay un empate en la prioridad, 
# se extrae el elemento que fue añadido primero",
# esto es util para implementar colas de prioridad, 
# como la que se usa en el algoritmo A*.
import heapq
# Simplemente para hacer mediciones de tiempo, y determinar refactorizaciones de tipo perf(performance)
import time

# Es un marcador que se usa para borrar un estado de forma logica
# (se dice de forma logica ya que no se borra realmente de la cola de prioridad,
# simplemente se marca con una etiqueta que se interpreta como "borrado" y 
# se ignora cuando se extrae de la cola de prioridad)
# esto se hace cuando se encuentran mejores soluciones y hace falta ignorar las
# peores soluciones que ya estan en la cola de prioridad.
# Esto se hace asi porque eliminar un elemento de la cola de prioridad es una operacion costosa,
# aproximadamente puede modelarse con O(n) en el peor caso, mientras 
# que marcar un elemento como borrado es una operacion O(1).
# luego al sacarlas solo hace falta un pequeño condicional que tambien es O(1) 
# para ignorar los elementos marcados como borrados. Se comprueba que es mejor
# esta implementacion ya que la suma de complejidades se define:
# O(1) + O(1) = O(max(O(1), O(1))) = O(1) que es mucho mejor que O(n).

# REMOVED: str = '<removed-task>'  # placeholder for a removed task.


class Solucion:  # clase solucion que hace override de metodos magicos, no se como se hace en C#
    """
    Esta clase representa una solucion, es decir, una configuracion de reinas en el tablero.
    Es decir, cada instancia de esta clase representa un estado del problema,
    donde "coords" es una lista de tuplas y cada tupla representa las coordenadas de una reina en el tablero, y "coste" 
    es el coste acumulado para llegar a esa configuracion. Cada objeto solucion es un nodo en el espacio de busqueda
    pues cada solucion es un estado del problema, es decir, una configuracion de reinas en el tablero, y cada nodo 
    tiene un coste asociado que representa el coste acumulado para llegar a esa configuracion.
    """

    def __init__(self, coords: list[tuple[int, int]], coste: int = 0):
        self.coords = coords
        self.coste: int = coste
        self.eliminado: bool = False

    # No hay literalmente ninguna rezon para pasar las coordenadas a string para compararlas
    # lo unico que se logra haciendo eso es perder eficiencia. Python ya permite la comparacion
    # nativa de listas, NO hace falta convertirlas a string para compararlas.
    # este es un punto a tener en cuenta para refactorizar.
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Solucion):
            return False
        # Comparacion nativa de listas de tuplas: Eficiente O(n)
        return self.coords == other.coords

    # Y esto directamente YA es un error conceptual grave, no solo lo hace mas ineficiente
    # sino ineficaz, es decir, cabe la posibilidad de que llegue a una solucion errada.
    # al comparar dos costes en string por ejemplo 10000 y 2 se comparan como "10000" < "2" 
    # lo cual es falso porque los strings se comparan caracter a caracter
    # si vemos SOLO el primer caracter 1 < 2 por lo que devuelve que "10000" < "2" es falso,
    # pero en realidad 10000 > 2, lo cual es un error grave. 

    # Este metodo se usa cuando hay un empate en la prioridad al insertar un nuevo 
    # elemento en la cola de prioridad. Si nunca se empata.
    # then never used this function.
    def __lt__(self, other: 'Solucion') -> bool:
        # Comparacion numerica real: Evita el error logico de comparar strings
        return self.coste < other.coste

    def __str__(self) -> str:
        return '-'.join(str(x) for x in self.coords)


class ListaCandidatos(ABC):  # Una clase abstracta
    # Se espera usar esta clase como una clase abstracta
    # sin embargo estrictamente hablando no lo es 
    # para que lo fuese tendria que heredar de la clase abstracta "ABC" de la libreria "abc"
    # y declarar los metodos abstractos con los decoradores "@abstractmethod"
    # por que esto importa? Pues porque sin hacer eso esta
    # clase es instanciable y se puede comprobar, sin embargo
    # por definicion una clase abstracta no puede ser instancible
    # en caso de serlo -> No es abstracta. 
    @abstractmethod
    def anhadir(self, solucion: Solucion, prioridad: int = 0):
        pass
    @abstractmethod
    def borrar(self, solucion: Solucion):
        pass
    @abstractmethod
    def obtener_siguiente(self) -> Solucion:
        pass
    @abstractmethod
    def __len__(self) -> int:
        pass


class ColaDePrioridad(ListaCandidatos):  # Cola de prioridad, usando la interfaz de ListaCandidatos

    def __init__(self):
        # cp : Cola de prioridad.
        # a heapq debemos pasarle una lista y sabemos que comprobar
        # si un elemento esta en una tiene coste O(n) por lo que se hace necesario
        # un diccionario que permita comprobar si un elemento esta en la cola de prioridad en O(1)
        # El monticulo guarda tuplas de (prioridad, objeto)
        self.cp: list[tuple[int, Solucion]] = []  # crea una lista y un diccionario
        
        # El diccionario es necesario para poder comprobar si un elemento esta en la 
        # cola de prioridad en O(1) y no O(n). Pero la forma en la que se implemento
        # transformando una tupla de coordenadas a string es ineficiente, ya que la 
        # conversion a string tiene un coste O(n)
        # y esto es completamente innecesario, ya que una tupla sabemos que es 
        # inmutable, es decir, es hashable, puede ser una key de un diccionario,
        # no hace falta convertir un hashable a otro hashable para que sea hashable xdd
        # y por tanto se puede usar directamente como key sin necesidad de convertirla a string.
        
        # El diccionario tiene como llave una configuracion de reinas en el tablero,\
        # representada por una tupla de tuplas de coordenadas,
        # y como valor una tupla de (prioridad, objeto), donde el objeto es la instancia 
        # de la clase Solucion que representa esa configuracion de reinas, y la prioridad es
        # el valor de prioridad asociado a esa solucion en la cola de prioridad.

        # Algo interesante de los type hints con listas es que estos solo te permiten
        # especificar un tipo de elemento de forma determinista, puedes comentar
        # de la existencia de varios tipos en la lista pero NO puedes especificar
        # su posicion, esto tiene todo el sentido del mundo porque hay que reccordar
        # que las listas son mutables, si list[int, Solucion] fuera valido entonces
        # diriamos que tenemos una lista donde la posicion 0 es int y la 1 es Solucion
        # bien pues. Si haces un pop(0) de esa lista, entonces la posicion 0 ahora es solucion
        # y la posicion 1 desaparece. Ya valio madres el type hint xd. de la lista xd.
        # si haces listp[int | Solucion] entonces el type hint es valido pero no es determinista
        # no sabes el numero de elementos dentro de la lista ni su posicion. 
        self.buscador: dict[tuple[tuple[int, int], ...], tuple[int, Solucion]] = {}

    def anhadir(self, solucion: Solucion, prioridad: int = 0):
        # Antes se usaba un str. Al pedirse mejorar la implementacion eso
        # ha sido cambiado. solucion.coords devuelve una lista, sabemos que
        # esto no es un objeto hashable, por eso NO lo podemos usar como una
        # key de un diccionario, para solucionar este problema el empleado
        # convertia la lista en un string, con esto logramos que sea un objeto
        # hashable, sin embargo es ineficiente, aunque ambos metodos son
        # O(n) lista -> tupla es Muchisimo mas rapido que Lista -> string
        # esto sucede porque de lista -> tupla simplemente se copian los punteros
        # a los objetos reales, mientras que de lista -> string 
        # se hace una conversion completa de cada elemento

        clave = tuple(solucion.coords)
        if clave in self.buscador:
            prioridad_vieja, solucion_vieja = self.buscador[clave]
            if prioridad_vieja <= prioridad:
                return
            self.borrar(solucion_vieja)  # Borrado logico de la solucion con peor prioridad
        
        # Al usar una tupla (), el tipado reconoce que la pos 0 es int y la pos 1 es Solucion
        # y por eso deja de dar warnings de tipo.
        entrada = (prioridad, solucion)
        self.buscador[clave] = entrada # -> llegados a este punto la entrada 
        heapq.heappush(self.cp, entrada)

    def borrar(self, solucion: Solucion):
        clave = tuple(solucion.coords)
        if clave in self.buscador:
            entrada = self.buscador.pop(clave)
            # Marcamos el objeto para que sea ignorado al salir del monticulo
            entrada[-1].eliminado = True

    def obtener_siguiente(self) -> Solucion:
        while self.cp:
            # Con heappop extraemos el elemento con menor prioridad, 
            # pero este elemento puede estar marcado como eliminado
            # de alli que hagamos un bucle que siga extrayendo elementos 
            # hasta encontrar uno que no este marcado como eliminado
            _, solucion = heapq.heappop(self.cp)
            if not solucion.eliminado:
                # Al extraerlo definitivamente, lo quitamos del buscador
                clave = tuple(solucion.coords)
                if clave in self.buscador:
                    del self.buscador[clave]
                return solucion
        raise KeyError('no hay siguiente en una cola de prioridad vacia')

    def __len__(self) -> int:
        return len(self.buscador)


class AlgoritmoDeBusqueda:

    def __init__(self, lista_tipo=ListaCandidatos):
        self.lista_tipo = lista_tipo

    def calculo_de_prioridad(self, solucion: Solucion, calculo_heuristica=None) -> int:
        return 0

    def busqueda(self, solucion_inicial: list[tuple[int, int]], criterio_parada, obtener_vecinos, calculo_coste, calculo_heuristica=None):
        candidatos = self.lista_tipo()
        candidatos.anhadir(Solucion(solucion_inicial, 0))
        
        # vistos: Diccionario de estados ya expandidos para evitar ciclos.
        # Usamos tuplas como claves para maxima eficiencia en lugar de strings.
        vistos: dict[tuple, int] = {}
        finalizado = False
        revisados = 0
        
        while len(candidatos) > 0 and not finalizado:
            solucion = candidatos.obtener_siguiente()
            
            clave_estado = tuple(solucion.coords)
            vistos[clave_estado] = solucion.coste
            revisados += 1
            
            if criterio_parada(solucion):
                finalizado = True
                break
                
            vecinos = obtener_vecinos(solucion)
            for vecino in vecinos:
                nueva_solucion = Solucion(coords=vecino)
                clave_vecino = tuple(nueva_solucion.coords)
                
                if clave_vecino not in vistos:
                    # g(n) = g(padre) + coste_movimiento
                    nueva_solucion.coste = solucion.coste + calculo_coste(solucion, nueva_solucion)
                    # f(n) = g(n) + h(n)
                    prioridad = self.calculo_de_prioridad(nueva_solucion, calculo_heuristica)
                    candidatos.anhadir(nueva_solucion, prioridad=prioridad)
                    
        return (solucion, revisados) if finalizado else (None, revisados)


class AEstrella(AlgoritmoDeBusqueda):

    def __init__(self):
        super(AEstrella, self).__init__(ColaDePrioridad)

    def calculo_de_prioridad(self, solucion: Solucion, calculo_heuristica=None) -> int:
        # A* utiliza f(n) = g(n) + h(n)
        h = calculo_heuristica(solucion) if calculo_heuristica else 0
        return solucion.coste + h


if __name__ == '__main__':
    reinas = 4
    # Tenemos un generador con potencial de crear tantos elementos como numero de reinas haya.
    # Se pasa como argumento a una funcion lista que crea las coordenadas de cada reina en la primera fila.
    # La solucion inicial es colocar todas las reinas en la fila 0 (punto de partida).
    
    # Puesto que siempre se empieza con la misma solucion inicial el algoritmo de busqueda siempre 
    # devolvera la misma configuracion de reinas ya que nuestro algoritmo de busqueda es determinista.
    solucion_inicial = [(0, i) for i in range(reinas)]

    # Esto no se puede modificar porque lo especifica el enunciado, pero por convencion 
    # se definen arriba del todo y se llaman aqui.
    def calculo_coste(solucion, nueva_solucion):
        return 1

    def calculo_heuristica(solucion):
        return 0  # h=0 (Se mejorara en la Semana 3)

    def obtener_vecinos(solucion):
        vecinos = []
        for i in range(len(solucion.coords)):
            vecino = list(solucion.coords)
            # Mover la reina de la columna i a la siguiente fila.
            vecino[i] = ((vecino[i][0] + 1) % reinas, vecino[i][1])
            vecinos.append(vecino)
        return vecinos

    def criterio_parada(solucion: Solucion):
        coords = solucion.coords
        for i in range(len(coords)):
            r1 = coords[i]
            for j in range(i + 1, len(coords)):
                r2 = coords[j]
                # Ataque en fila, columna o diagonal.
                if r1[0] == r2[0] or r1[1] == r2[1] or abs(r1[0] - r2[0]) == abs(r1[1] - r2[1]):
                    return False
        return True

    astar = AEstrella()
    
    time_inicio = time.time()
    solucion, revisados = astar.busqueda(solucion_inicial, criterio_parada, obtener_vecinos, calculo_coste, calculo_heuristica)
    time_fin = time.time()
    
    if solucion:
        print('Coordenadas:', solucion.coords)
        print('Nodos evaluados:', revisados)
        print(f'Tiempo de ejecucion: {time_fin - time_inicio:.6f} segundos')
    else:
        print('No se encontró solución.')
