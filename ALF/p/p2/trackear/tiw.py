
import argparse
import sys
import os

class NafdaTransitionWeights:
    """
    Esta clase es una variante de la de la parte 1 y de siw.py, pero
    pensada para meter los pesos directamente en las transiciones.
    La estructura cambia un poco porque ahora las transiciones
    ocupan el doble de espacio (8 bytes en total).
    """
    def __init__(self, bin_filename):
        self.raw_bin = self.read_bin(bin_filename)
        self.dict_automatron = self.format_table()
        self.num_cells = int.from_bytes(self.raw_bin[0:4], byteorder='little')

    @staticmethod
    def read_bin(filename) -> list:
        with open(filename, 'rb') as f:
            return list(f.read())

    def format_table(self) -> dict:
        """
        Aquí leemos el binario original (el que no tiene pesos).
        Es el mismo proceso que en nadfa.py: vamos saltando de celda
        en celda y guardando estados y transiciones en un diccionario
        para no volvernos locos con los índices de los bytes.
        """
        table = self.raw_bin
        bytes_per_cell = 4
        num_cells = int.from_bytes(table[0:bytes_per_cell], byteorder='little')
        automaton = {}
        index = 4
        limit = 4 + (num_cells * bytes_per_cell)
        
        while index < len(table) and index < limit:
            cell_id = index // bytes_per_cell
            num_transitions = table[index + 3]
            weight_placeholder = int.from_bytes(table[index:index+3], byteorder='little')
            automaton[cell_id] = (num_transitions, weight_placeholder)
            index += bytes_per_cell
            
            for _ in range(num_transitions):
                t_cell_id = index // bytes_per_cell
                dest_cell = int.from_bytes(table[index:index+3], byteorder='little') + 1
                char_ascii = table[index+3]
                
                # Usamos latin-1 para que no rompa con tildes o eñes
                if char_ascii == 0:
                    char = 'ε'
                else:
                    char = chr(char_ascii)
                
                automaton[t_cell_id] = (char, dest_cell, 0) # Dejamos el peso a 0 para calcularlo luego
                index += bytes_per_cell
        return automaton

    def obtain_transitions(self, id_celda: int) -> list:
        # Auxiliar típica para sacar lo que cuelga de un estado
        num_trans = self.dict_automatron[id_celda][0]
        inicio = id_celda + 1
        return [self.dict_automatron[i] for i in range(inicio, inicio + num_trans)]

    def calculate_weights(self):
        """
        Esta es la parte complicada. Para calcular el peso de una
        transición, primero necesito saber el tamaño del lenguaje
        derecho del estado al que apunta.
        Uso una función recursiva con memoización porque si no,
        en el autómata 'large' esto tardaría una eternidad.
        """
        memo_state_size = {}

        def get_state_size(state_id):
            if state_id == 1: # El estado final cuenta como 1 (palabra vacía)
                return 1
            if state_id in memo_state_size:
                return memo_state_size[state_id]
            
            size = 0
            for char, dest, _ in self.obtain_transitions(state_id):
                size += get_state_size(dest)
            
            memo_state_size[state_id] = size
            return size

        # Ahora que sabemos los tamaños, calculamos el acumulado para cada transición
        new_dict = {}
        for cell_id, val in self.dict_automatron.items():
            if isinstance(val[0], int): # Si es un estado
                num_trans = val[0]
                new_dict[cell_id] = val
                
                # El peso de una transición es la suma de los lenguajes de las anteriores
                running_weight = 0
                inicio = cell_id + 1
                for i in range(num_trans):
                    char, dest, _ = self.dict_automatron[inicio + i]
                    new_dict[inicio + i] = (char, dest, running_weight)
                    running_weight += get_state_size(dest)
            else:
                if cell_id not in new_dict:
                    new_dict[cell_id] = val
        
        self.dict_automatron = new_dict

    def save_bin(self, output_filename):
        """
        Guardamos el nuevo binario. Como ahora cada transición ocupa 8
        bytes (dos celdas), tenemos que remapear todos los IDs de los
        estados. Es un lío de offsets, pero básicamente estamos
        inflando el archivo original para meter la información extra.
        """
        states = []
        for cell_id in sorted(self.dict_automatron.keys()):
            if isinstance(self.dict_automatron[cell_id][0], int):
                states.append(cell_id)
        
        num_states = len(states)
        total_trans = sum(self.dict_automatron[sid][0] for sid in states)
        new_num_cells = num_states + total_trans * 2 # Cada trans ahora son 2 celdas
        
        output = bytearray(4 + new_num_cells * 4)
        output[0:4] = new_num_cells.to_bytes(4, byteorder='little')
        
        # Mapeamos IDs viejos a IDs nuevos en el archivo inflado
        old_to_new = {}
        current_new_cell = 1
        for old_sid in states:
            old_to_new[old_sid] = current_new_cell
            current_new_cell += 1 + self.dict_automatron[old_sid][0] * 2
            
        for old_sid in states:
            new_sid = old_to_new[old_sid]
            num_trans, _ = self.dict_automatron[old_sid]
            
            # Escribimos la cabecera del estado
            off = new_sid * 4
            output[off:off+3] = (0).to_bytes(3, byteorder='little')
            output[off+3] = num_trans
            
            # Escribimos las transiciones expandidas
            for i in range(num_trans):
                char, dest_old, weight = self.dict_automatron[old_sid + 1 + i]
                dest_new = old_to_new[dest_old]
                
                # Celda A: Destino y Carácter (formato original)
                off_a = (new_sid + 1 + i*2) * 4
                output[off_a:off_a+3] = (dest_new - 1).to_bytes(3, byteorder='little')
                
                char_byte = 0 if char == 'ε' else ord(char)
                output[off_a+3] = char_byte
                
                # Celda B: Peso de la transición (3 bytes)
                off_b = off_a + 4
                output[off_b:off_b+3] = weight.to_bytes(3, byteorder='little')
                output[off_b+3] = 0
                
        with open(output_filename, 'wb') as f:
            f.write(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_bin')
    parser.add_argument('output_bin')
    args = parser.parse_args()
    
    try:
        tiw = NafdaTransitionWeights(args.input_bin)
        tiw.calculate_weights()
        tiw.save_bin(args.output_bin)
        print(f"Pesos en transiciones guardados en '{args.output_bin}'.")
    except Exception as e:
        sys.stderr.write(f"Error procesando el autómata: {e}\n")
        sys.exit(1)
