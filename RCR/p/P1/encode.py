import sys


if len(sys.argv) < 3:
    print("Uso: python3 encode.py <archivo_entrada.txt> <archivo_salida.lp>")
    sys.exit()

input_file = sys.argv[1]
output_file = sys.argv[2]

try:#He pensado que seria buena práctica aadir comentarios al archivo de salida, de esta forma me facilita el debugging
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    N, M = map(int, lines[0].split())# La funcion map basicamente aplica la función int a cada elemento de la lista resultante de split, me ahorra escribir un bucle.
    
    with open(output_file, 'w') as out:
        out.write(f"% Representación de {input_file}\n")
        out.write(f"size({N}).\n")#Ponemos los factos de tamaño y cantidad de regiones.
        out.write(f"m({M}).\n\n")
        
        out.write("% Regiones (Type 0: x fila, y columna)\n")#Aqui leemos la matriz de regiones 
        for x in range(N):
            row = lines[x + 1]
            for y in range(N):
                out.write(f"region({x},{y},{row[y]}).\n")

        
        out.write("% Agujeros por columna\n")#Aui la fila de agujeros par las columnas
        col_numbers = lines[N + 1].split()
        for y in range(N):
            out.write(f"t_c({y},{col_numbers[y]}).\n")
        
        out.write("% Agujros por fila\n")#Aqui las de las filas
        row_numbers = lines[N + 2].split()
        for x in range(N):
            out.write(f"t_r({x},{row_numbers[x]}).\n")
            
    print(f"'{output_file}' generado correctamente")

except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo '{input_file}'.")
except Exception as e:
    print(f"Error inesperado al procesar el archivo: {e}")