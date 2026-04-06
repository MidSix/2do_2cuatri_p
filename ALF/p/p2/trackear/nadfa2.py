
import argparse
import sys
import os

class Nafda2():
    """
    Versión del autómata optimizada con pesos en las transiciones.
    Hereda casi toda la lógica de nadfa.py pero cambia la forma
    de leer el binario y de calcular el índice, ya que ahora
    no hay que saltar a otros estados para sumar pesos.
    """
    def __init__(self, bin_filename):
        self.raw_bin = self.read_bin(bin_filename)
        self.dict_automatron = self.format_table()
    
    @staticmethod
    def read_bin(filename) -> list:
        with open(filename, 'rb') as f:
            return list(f.read())

    def format_table(self) -> dict:
        """
        Aquí leemos el binario 'inflado' que generó tiw.py.
        Cada transición ocupa dos celdas consecutivas:
        1. Destino (3B) + Carácter (1B)
        2. Peso (3B) + Relleno (1B)
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
            automaton[cell_id] = (num_transitions, 0)
            index += bytes_per_cell
            
            for _ in range(num_transitions):
                t_cell_id_a = index // bytes_per_cell
                dest_cell = int.from_bytes(table[index:index+3], byteorder='little') + 1
                char_ascii = table[index+3]
                
                if char_ascii == 0:
                    char = 'ε'
                else:
                    char = chr(char_ascii)
                index += bytes_per_cell
                
                # La siguiente celda tiene el peso ya calculado
                weight = int.from_bytes(table[index:index+3], byteorder='little')
                index += bytes_per_cell
                
                automaton[t_cell_id_a] = (char, dest_cell, weight)
        return automaton

    def obtain_transitions(self, id_celda: int) -> list:
        """
        Sacamos las transiciones saltando de 2 en 2 celdas
        porque cada una está expandida con su peso.
        """
        num_trans = self.dict_automatron[id_celda][0]
        res = []
        for i in range(num_trans):
            res.append(self.dict_automatron[id_celda + 1 + i*2])
        return res

    def list_words(self, id_celda: int = 2, prefijo: str = ""):
        # Funciona igual que en la versión estándar
        for char, dest_celda, weight in self.obtain_transitions(id_celda):
            if char == 'ε':
                print(prefijo)
            else:
                self.list_words(dest_celda, prefijo + char)

    def word_to_index(self, palabra: str) -> str:
        """
        Aquí es donde se nota la mejora de velocidad.
        No sumamos pesos de 'hermanos' haciendo saltos en memoria,
        sino que el peso que sumamos ya es el acumulado de todo
        lo que venía antes en ese estado.
        """
        indice = 1
        estado_actual = 2
        palabra_terminada = palabra + 'ε'
        
        for char in palabra_terminada:
            transiciones = self.obtain_transitions(estado_actual)
            found = False
            for t_char, dest, weight in transiciones:
                if t_char == char:
                    indice += weight # Peso directo, sin más bucles
                    estado_actual = dest
                    found = True
                    break
            if not found:
                return "unknown"
        
        if estado_actual == 1:
            return str(indice)
        return "unknown"

    def index_to_word(self, indice: int) -> str:
        """
        Para convertir de índice a palabra seguimos necesitando
        saber los tamaños de los lenguajes derechos de los destinos.
        Uso memoización para que el rendimiento sea aceptable.
        """
        memo_size = {}
        def get_size(sid):
            if sid == 1: return 1
            if sid in memo_size: return memo_size[sid]
            s = 0
            for c, d, w in self.obtain_transitions(sid):
                s += get_size(d)
            memo_size[sid] = s
            return s
        
        total_size = get_size(2)
        if indice < 1 or indice > total_size:
            return "index out of bounds"
            
        num = indice
        state = 2
        palabra = ""
        
        while num > 0:
            trans = self.obtain_transitions(state)
            found = False
            for c, d, w in trans:
                d_size = get_size(d)
                if num > d_size:
                    num -= d_size
                else:
                    if c != 'ε':
                        palabra += c
                    state = d
                    if state == 1:
                        num -= 1
                    found = True
                    break
            if not found: break
        return palabra

if __name__ == "__main__":
    # Forzamos latin-1 para las tildes y la eñe
    import io
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='latin-1')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='latin-1')

    parser = argparse.ArgumentParser()
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument('-d', action='store_true')
    grupo.add_argument('-i', action='store_true')
    grupo.add_argument('-w', action='store_true')
    parser.add_argument('input_bin')
    args = parser.parse_args()
    
    try:
        n2 = Nafda2(args.input_bin)
        if args.d:
            n2.list_words()
        elif args.i:
            input_text = sys.stdin.read()
            for word in input_text.splitlines():
                word = word.strip()
                if word: print(n2.word_to_index(word))
        elif args.w:
            input_text = sys.stdin.read()
            for line in input_text.splitlines():
                idx = line.strip()
                if idx:
                    try: print(n2.index_to_word(int(idx)))
                    except ValueError: print("index out of bounds")
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)
