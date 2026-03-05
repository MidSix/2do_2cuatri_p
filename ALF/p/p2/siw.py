 
def read_bin(filename)->list:
    """
    Leemos el archivo binario y lo almacenamos en una lista de enteros.
    """
    automatron_bin = []
    with open(filename, 'rb') as f:
        while True:
            byte = f.read(1)
            if not byte:
                break
            automatron_bin.append(byte[0])
    return automatron_bin

def format_table(table):
    """Formateamos la tabla del automata sabemos que su estructura es la siguiente:
    los primeros 4 bytes son el número de celdas(autoexcluyendose), los siguientes 4 bytes 
    son el estado final de ahi en adelante tenemos:
    • Primera celda, con la información del estado:
    ◦ 1 byte: Número de celdas consecutivas (transiciones) que definen ese estado.
    ◦ 3 bytes: Peso de la indexación.
    • Celdas con información de las transiciones:
    ◦ 1 byte: Carácter que representa la transición.
    ◦ 3 bytes: Celda destino de la transición
    Sabiendo esto almacenaremos una matriz con cada estado, sus transiciones y sus pesos(inicialmente 0).
    de la siguiente manera
    """
def show_table(table):
    for i in range(0, len(table), 16):
        print(' '.join(f'{byte:02x}' for byte in table[i:i+16]))

if __name__ == "__main__":
    relative_path = './Automatas_Diccionarios/'
    filename = f'{relative_path}tiny.bin'
    automatron_table = read_bin(filename)
    show_table(automatron_table)