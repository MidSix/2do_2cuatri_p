import clingo
import sys


if len(sys.argv) < 4:
    print("Uso: python3 decode.py <archivo_logica.lp> <archivo_datos.lp> <salida.txt>")
    sys.exit()

output_file = sys.argv[-1]
input_files = sys.argv[1:-1]

ctl = clingo.Control()
ctl.add("base", [], "")
for arg in input_files:
    ctl.load(arg)
ctl.ground([("base", [])])
ctl.configuration.solve.models="2" # This retrieves 2 models at most
num_models=0

size = 0
stitches = []

with ctl.solve(yield_=True) as handle:
    for model in handle:
        if num_models > 0: 
            print("Warning: more than 1 model (Tu puzzle tiene múltiples soluciones)")
            break
            
        for atom in model.symbols(atoms=True):#Muy comodo poder recorrer los átomos de la solución directamente.
            
            if atom.name == "size" and len(atom.arguments) == 1:
                size = atom.arguments[0].number
                
            elif atom.name == "stitch" and len(atom.arguments) == 4:
                x = atom.arguments[0].number
                y = atom.arguments[1].number
                x1 = atom.arguments[2].number
                y1 = atom.arguments[3].number
                stitches.append((x, y, x1, y1))
                
        num_models = 1 

if num_models == 0: 
    print("UNSATISFIABLE (No se encontró solución)")
else:
    print(f"Solución encontrada. Generando {output_file}...")
    
    #Lo siguiente s oara hacer el dibujo
    grid = [[" " for _ in range(size)] for _ in range(size)]# Creamos una matriz vacía llena de espacios

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
            
