class Automaton:
    """
    Tratamos de crear una especie de lista posicionada que nos permita aplicar las transiciones,
    para ello haremos uso de esta clase con la subclase estado.
    Lo que sabemos por el enunciado es que la primera celda contiene el número de celdas total
    """
    def __init__(self, binary_file):
        self.bin = self.read_bin(binary_file)
        self.cells=int.from_bytes(self.bin[0:4], byteorder='little')#Total de celdad
        self.automaton = self.gen_table(self.bin)

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
    
    def gen_table(self):
        return None

    class state:
        """
        Un estado contendrá:
        • Primera celda, con la información del estado:
        ◦ 1 byte: Número de celdas consecutivas (transiciones) que definen ese estado.
        ◦ 3 bytes: Peso de la indexación.
        • Celdas con información de las transiciones:
        ◦ 3 byte: Carácter que representa la transición.
        ◦ 1 byte: Celda destino de la transición
        """
        def __init__(self, transitions):
            self.weight = 0 #Inicialmente valen 0, desde la clase matriz ya emplearemos un algotimo de asignacion
            self.transitions = transitions
            self.cells






            
def format_table(table)->tuple:
    """Formateamos la tabla del automata sabemos que su estructura es la siguiente:
    los primeros 4 bytes son el número de celdas(autoexcluyendose), los siguientes 4 bytes 
    son el estado final de ahi en adelante tenemos:
    • Primera celda, con la información del estado:
    ◦ 1 byte: Número de celdas consecutivas (transiciones) que definen ese estado.
    ◦ 3 bytes: Peso de la indexación.
    • Celdas con información de las transiciones:
    ◦ 3 byte: Carácter que representa la transición.
    ◦ 1 byte: Celda destino de la transición
    Sabiendo esto almacenaremos una matriz con cada estado, sus transiciones y sus pesos(inicialmente 0).
    de la siguiente manera: el automatron será una matriz de listas, cada sublista será un estado y cada celda dentro de ese
    sublista será una tupla con el peso y las transiciones, cada transición será una tupla con el caracter y la celda destino.
    este automatron se retornará. 
    """
    bytes_per_cell = 4
    num_cells = int.from_bytes(table[0:4], byteorder='little')
    final_state = int.from_bytes(table[4:8], byteorder='little')
    automaton = []
    index = 8
    for _ in range(num_cells):
        num_transitions = table[index]
        weight = int.from_bytes(table[index+1:index+4], byteorder='little')
        index += bytes_per_cell
        transitions = []
        for _ in range(num_transitions):
            char = table[index]
            dest_cell = int.from_bytes(table[index+1:index+4], byteorder='little')
            transitions.append((char, dest_cell))
            index += bytes_per_cell
        automaton.append((weight, transitions))
    return automaton, final_state

def show_table(table):
    for i in range(0, len(table), 16):
        print(' '.join(f'{byte:02x}' for byte in table[i:i+16]))

if __name__ == "__main__":
    relative_path = './Automatas_Diccionarios/'
    filename = f'{relative_path}tiny.bin'
    automatron_table= read_bin(filename)
    automaton, final_state = format_table(automatron_table)
    show_table(automatron_table)