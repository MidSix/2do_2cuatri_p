"""
Miembros:
    - Xoel Sánchez Dacoba
    - Sebastián David Moreno Expósito
Grupo de prácticas:
    G1.1 - Lunes.
Encoding type -> 0
"""
import sys


if len(sys.argv) < 3:
    print("Uso: python3 encode.py <archivo_entrada.txt> <archivo_salida.lp>")
    sys.exit()

input_file = sys.argv[1]
output_file = sys.argv[2]

try:#He pensado que seria buena práctica aadir comentarios al archivo de salida, de esta forma me facilita el debugging
    #--------------------------------------------
    with open(input_file, 'r') as f:
        # 'r' -> significa que abrimos el archivo en modo lectura
        # 'with' es un context manager, eso en cristiano quiere decir
        # que 'gestiona' la 'conexion' de python con otros proceso.
        # Que implica 'gestionar'? Implica que tras salir de este 
        # bloque de codigo se cierra automaticamente la conexion
        # con el proceso en cuestion, ademas, tiene handlers de
        # excepciones donde si falla en algun caso en la conexion
        # simplemente la cierra igualmente.
        # El proceso que se abre aqui seria 'open' pero podria ser 
        # conectarse a una base de datos o a un solver como el de clingo
        # que lo hacemos despues, o a una maquina remota via protocolo
        # ssh, etc.
    #______________________________________________
        #--------------------------------------------
        lines = [line.strip() for line in f if line.strip()]
        # List comprehension que incluye un bucle for y un condicional in-line
        # Primero iteramos sobre el archivo que abrimos antes
        # (cada iteracion es una fila/linea del archivo)
        # luego aplicamos el condicional. Si tras hacer strip()
        # a la linea esta no es vacia(False) entonces es True, pasa el
        # condicional y se incluye dicha linea en la lista resultante
        # de esta manera tendremos una lista donde cada elemento 
        # es una linea del archivo de entrada.
        #______________________________________________
    #--------------------------------------------
    N, M = map(int, lines[0].split())
    # La funcion map basicamente aplica la funcion int a cada elemento
    # de la primera fila del archivo de entrada *.txt, es decir, 
    # se le aplica la funcion int al primer elemento de la lista 'lines'
    # para que? Pues para convertir el tamano del tablero (N) y 
    # la cantidad minima de stitches entre cada par de regiones 
    # adyacentes (M) a enteros porque por defecto al leer 
    # un archivo con open() todo lo que se lee es texto, o sea strings, 
    #______________________________________________
    #--------------------------------------------
    with open(output_file, 'w') as out:
        # 'w' -> significa que abrimos el archivo en modo escritura,
        #  si el archivo no existe se crea, y si existe se sobreescribe.
    #______________________________________________
        out.write(f"% Representación de {input_file}\n")
        out.write(f"size({N}).\n")#Ponemos los factos de tamaño y cantidad de regiones.
        out.write(f"m({M}).\n\n")
        
        out.write("% Regiones (Type 0: x fila, y columna)\n")#Aqui leemos la matriz de regiones 
        #--------------------------------------------
        for x in range(N): 
        # N = Dimension de la matriz(tablero) cuadrada
        # es decir, el numero de filas y columnas es el mismo,
        # por eso usamos N para ambos bucles.
        #______________________________________________
            #--------------------------------------------
            row = lines[x + 1]
            # Cada elemento de lines es una fila. Y hay que recordar 
            # que la primera fila (lines[0]) es la que contiene 
            # el tamano del tablero y la cantidad minima de stitches
            # por ello empezamos a contar las rows a partir de lines[1]
            # que es donde encontramos las regiones del tablero.
            #______________________________________________
            for y in range(N):
                #--------------------------------------------
                out.write(f"region({x},{y},{row[y]}).\n")
                # Simplemente se declaran por cada casilla del tablero
                # un hecho que es region(x,y,tipo) donde 'x' es la fila, 
                # 'y' es la columna y 'tipo' es el tipo de region a la
                # que pertenece dicha casilla.
                #______________________________________________
        #--------------------------------------------
        out.write("% Agujeros por columna\n")#Aui la fila de agujeros par las columnas
        col_numbers = lines[N + 1].split()
        for y in range(N):
            out.write(f"t_c({y},{col_numbers[y]}).\n")
        
        out.write("% Agujros por fila\n")#Aqui las de las filas
        row_numbers = lines[N + 2].split()
        for x in range(N):
            out.write(f"t_r({x},{row_numbers[x]}).\n")
        # Esta parte diria que entendiendo lo anterior se entiende
        # perfectamente sin caer en explicaciones redundantes.
        #______________________________________________
    print(f"'{output_file}' generado correctamente")

#--------------------------------------------
except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo '{input_file}'.")
except Exception as e:
    print(f"Error inesperado al procesar el archivo: {e}")
# Self-explanatory exceptions xd.
#______________________________________________