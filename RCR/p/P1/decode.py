"""
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - Lunes.
Encoding type -> 0
"""
import clingo
import sys


if len(sys.argv) < 4:
    print("Uso: python3 decode.py <archivo_logica.lp> <archivo_datos.lp> <salida.txt>")
    # <archivo.datos.lp> se consigue luego de codificar el problema
    # con encode.py y <archivo_logica.lp> es la logica en si del
    # problema, las reglas que han de cumplirse.  
    sys.exit()

#--------------------------------------------
output_file = sys.argv[-1] # esto toma el último argumento pasado
# por la linea de comandos.

# Esto es "negative" indexing, una característica de Python 
# que permite acceder a los elementos de una lista desde el final.
# En python hay tanto positive indexing (el de toda la vida, se empieza
# a contar desde 0) y negative indexing que empieza a contar desde el
# ultimo elemento de la secuencia (sys.argv devuelve una secuencia 
# donde cada elemento es un argumento pasado por la línea de comandos). 
#______________________________________________

#--------------------------------------------
input_files = sys.argv[1:-1] # Esto toma todos los argumentos pasados
# por la linea de comandos salvo el primero y el ultimo

# Esto es simplemente un array slicing, otra caracteristica de Python
# que permite indexar una secuencia de un iterable. La sintaxis es:
# iterable[start:stop:step], "stop es excluyente"
# start es el indice del primer elemento que se quiere incluir, como 
# el positive indexing empieza desde 0 pues start=1 se refiere al 
# segundo elemento de la secuencia, y stop=-1 se refiere al 
# ultimo elemento de la secuencia, pero como stop es excluyente pues
# tenemos al penultimo.
#______________________________________________

#--------------------------------------------
ctl = clingo.Control() # Simplemente creamos un objeto de control de
# clingo, por convencion se suele llamar ctl como abreviatura de "control"

# Se llama objeto de control porque es el encargado de controlar
# la comunicacion con el solver de clingo, o sea la comunicacion
# con clingo basicamente. Esto implica cargar los archivos de lógica, 
# resolver el programa, y recuperar los modelos que el solver encuentra.
# etc.
#______________________________________________

#--------------------------------------------
for arg in input_files:
    ctl.load(arg)
    # Ya sabemos lo que tiene input_files, simplemente los dos archivos
    # *.lp, el de logica y el de datos, ahora lo que hacemos es cargar
    # ambos archivos en el objeto de control. Donde se almacena ese 
    # 'objeto de control'? En la memoria RAM, bien. 
#______________________________________________

#--------------------------------------------
ctl.ground([("base", [])])
# 'ground' es la fase de instanciacion. Clingo 
# (En especifico gringo, el grounder de clingo)
# coge las reglas genericas con variables y las combina con los hechos 
# (datos concretos) para generar todas las reglas proposicionales 
# especificas posibles sin variables. Es un paso estrictamente 
# necesario antes de llamar a al solver.
#______________________________________________

#--------------------------------------------
ctl.configuration.solve.models="2" 
# Por defecto Clingo busca 1 solo modelo. 
# Le pedimos 2 para comprobar si el puzzle tiene una solucion unica. 
# De no tenerla puede ser esto sintama de un problema mal modelado 
#______________________________________________

num_models=0 # variable de control 
# para contar el numero de modelos encontrados, se inicializa a 0

size = 0 # Almacenará el tamaño del tablero extraído del solver 
# para poder crear la matriz bidimensional (el lienzo) 
# donde dibujaremos la solución al final.
stitches = []

#--------------------------------------------
with ctl.solve(yield_=True) as handle:
# 'yield_=True' le dice al solver de Clingo que no nos devuelva solo 
# un resumen final (SAT/UNSAT), sino que nos devuelva un "iterador" 
# (Lazy Evaluation), esto es importante recalcarlo porque de no ser
# asi clingo bloquearia el interprete de python hasta que encuentre
# todos los modelos posibles y una vez habiendolo hecho simplemente
# 'handle' seria un resumen que te dice si el problema 
# es SAT o UNSAT y el numero de modelos encontrados pero no te 
# daria acceso a los modelos en si que es lo que necesitamos
# Nota: Lleva un guion bajo porque 'yield' es una palabra reservada 
# en Python relacionada con la lazy evaluation.
#______________________________________________
    #--------------------------------------------
    for model in handle:
        # num_models se inicializa a 0 y se incrementa 
        # a 1 cuando se procesa el primer modelo encontrado.
        # por lo tanto si num_models ya no es 0, 
        # significa que hallamos una segunda solucion, por lo que
        # Hacemos break para no sobreescribir los datos del primer modelo.
    #______________________________________________
        if num_models > 0: 
            print("Encontrados más de 1 modelo, solo se procesará el primero.")
            break
            
        for atom in model.symbols(atoms=True): #Muy comodo poder recorrer los átomos de la solución directamente.
            
            if atom.name == "size" and len(atom.arguments) == 1:
                size = atom.arguments[0].number
            #--------------------------------------------    
            elif atom.name == "stitch" and len(atom.arguments) == 4:
                x = atom.arguments[0].number
                y = atom.arguments[1].number
                x1 = atom.arguments[2].number
                y1 = atom.arguments[3].number
                stitches.append((x, y, x1, y1))
            # Hay que tener en cuenta que un stitch conecta dos 
            # agujeros, o sea, dos celdas. Cada celda requiere un par 
            # de coordenadas para representarse, por tanto stitch
            # requiere 4 argumentos donde los 2 primeros representan el
            # primer punto de union(primera celda) y los 
            # dos ultimos el otro punto de union(segunda celda).
            # luego cada stitch representado por una tupla de 4 numeros
            # se agrega a la lista de stitches.
            #______________________________________________
            print
        # Marcamos que ya hemos procesado el primer modelo correctamente.
        num_models = 1 

if num_models == 0: 
    print("UNSATISFIABLE (No se encontró solución)")
else:
    print(f"Solución encontrada. Generado {output_file}")
    
    #Lo siguiente s oara hacer el dibujo
    grid = [["." for _ in range(size)] for _ in range(size)]# Creamos una matriz vacía llena de puntos

    for (x, y, x1, y1) in stitches: # Y simplemente recorremos las puntadas y dibujamos según corresponda
        if y == y1:# Si Y es igual, están en la misma columna -> Puntada Vertical
            top_x = min(x, x1)
            bottom_x = max(x, x1)
            grid[top_x][y] = "v"
            grid[bottom_x][y] = "^"
        
        elif x == x1: # Si X es igual, están en la misma fila -> Puntada Horizontal
            left_y = min(y, y1)
            right_y = max(y, y1)
            grid[x][left_y] = ">"
            grid[x][right_y] = "<"

    with open(output_file, 'w') as f:
        for fila in grid:
            f.write("".join(fila) + "\n")
            
