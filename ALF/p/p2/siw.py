class Nafda():
    def __init__(self, bin_filename):
        self.raw_bin = self.read_bin(bin_filename)
        self.dict_automatron = self.format_table()

    def read_bin(filename)->list:
        automatron_bin = []
        with open(filename, 'rb') as f:
            while True:
                byte = f.read(1)
                if not byte:
                    break
                automatron_bin.append(byte[0])
        return automatron_bin

    def format_table(self) -> dict:
        """
        Formateamos la tabla del autómata. Sabemos que su estructura es la siguiente:
        Los primeros 4 bytes son el número total de celdas (autoexcluyéndose).
        A partir de ahí tenemos:
        
        • Primera celda, con la información del estado:
        ◦ 3 bytes: Peso de la indexación.
        ◦ 1 byte: Número de celdas consecutivas (transiciones) que definen ese estado.
        • Celdas con información de las transiciones:
        ◦ 3 bytes: Celda destino de la transición.
        ◦ 1 byte: Carácter que representa la transición.
        
        Almacenaremos un diccionario para fácil acceso donde cada elemento será una tupla (celda).
        """
        table=self.raw_bin
        bytes_per_cell = 4#int de referencia para no andar escribiendo 4 en todos lados
        num_cells = int.from_bytes(table[0:bytes_per_cell], byteorder='little')
        automaton = {}
        index = 4  # Empezamos directamente en la celda 1 (byte 4)
        limit = 4 + (num_cells * bytes_per_cell)# El tamaño total esperado será 4 (cabecera) + (num_cells * 4)
        
        while index < len(table) and index < limit:#El limite es por si por algún casual hay basura en el bin o vete a saber
            cell_id = index // bytes_per_cell # Calculamos el índice único de la celda
            
            below = int.from_bytes(table[index:index+3], byteorder='little')# Los primeros 3 bytes son el número de abajo (peso)
            above = table[index+3]# El cuarto byte es el caracter de arriba (num_transitions)
            num_transitions = above # Lo guardamos para saber cuántas vueltas dar en el for
            
            automaton[cell_id] = (above, below)# Guardamos la celda de estado en el diccionario
            index += bytes_per_cell
            
            for _ in range(num_transitions):
                trans_cell_id = index // bytes_per_cell # Calculamos el índice de la celda de transición
                
                dest_cell = int.from_bytes(table[index:index+3], byteorder='little')# Los primeros 3 bytes son la CELDA DESTINO (número de abajo)
                char_ascii = table[index+3]# El cuarto byte es el CARÁCTER (número de arriba)
                
                if 32 <= char_ascii <= 126:
                    char = chr(char_ascii)# Letras y símbolos normales
                elif char_ascii == 0:
                    char = 'ε'# Épsilon (fin de palabra o vacía), queda bonito
                else:
                    char = f"<{char_ascii}>"# Símbolos de control internos, aunque no debiera haber
                
                automaton[trans_cell_id] = (char, dest_cell)# Guardamos la celda de transición
                index += bytes_per_cell
                
        return automaton


def index_weights(automatron:list)->list:
    """
    Función que indexa los pesos del automata.
    se dedicará a recorrer el automata al revés empezando
    por el estado final para indexar los pesos siguiendo el algoritmo
    explicado en clase de prácticas
    """

    return automatron
if __name__ == "__main__":
    filename = 'tiny.bin'
    automatron = Nafda(filename)
    print(f"Autómata parseado: {automatron}")
