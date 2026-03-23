import argparse
import sys
import os

class Nafda():
    """
    Clase que implementa un automáta sobre una implementación de lista dirigida sobre un diccionario
    Algo raro, pero es lo que se me ocurrió para manejar fácil el formato del binario.
    Puede que me complicase un poco la vida.
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
                
                dest_cell = int.from_bytes(table[index:index+3], byteorder='little')+1# Los primeros 3 bytes son la CELDA DESTINO (número de abajo), 
                #Añadimos un offset de 1 a la celda de destino por como es el .bin, que se autoexcluye al calcular su destino
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
    
    def is_state(self,item:tuple)->bool:
        """
        Si una tupla es la cabecera de un estado,
        entonces el primer elemento es un entero (número de transiciones) y el segundo es el peso de indexación.
        """
        return isinstance(item[0], int)
 
    def obtain_transitions(self, id_celda: int) -> list:
        estado = self.dict_automatron[id_celda]
        num_transiciones = estado[0]
        inicio_transiciones = id_celda + 1 # Las transiciones arrancan en la celda inmediata al estado
        return [self.dict_automatron[i] for i in range(inicio_transiciones, inicio_transiciones + num_transiciones)]
    
    def __str__(self) -> str:
        return str(self.dict_automatron)
    
    def __len__(self):#Pensé que le iba a dar más uso, pero nay
        return self.dict_automatron.__len__()
    
    def index_weights(self,id_celda:int=2) -> int:#Pensar esta función llevo un rato muy largo de Dios
        """
        Función que indexa los pesos del automata.
        Aplica recorrido en profundidad recursivo.
        Por defecto arranca en el estado inicial (celda 1).
        """
        estado = self.dict_automatron[id_celda]
        num_transiciones = estado[0]
        peso_actual = estado[1]
        
        if peso_actual > 0:#Si ya se paso por aqui, mantenemos el peso
            return peso_actual
            
        if id_celda == 1: #Fondo de la "pila", el estado final 
            nuevo_peso = 1
            self.dict_automatron[id_celda] = (num_transiciones, nuevo_peso)
            return nuevo_peso
            
        suma_pesos = 0
        transiciones = self.obtain_transitions(id_celda)
        for _, dest_celda in transiciones:
            suma_pesos += self.index_weights(dest_celda)#La llamada recursiva
            
        self.dict_automatron[id_celda] = (num_transiciones, suma_pesos)
        return suma_pesos#Retornamos la suma para la call
    
    def save_bin(self, output_filename: str):
        """
        Crea una copia de los bytes originales y sobrescribe únicamente
        los 3 bytes de peso de cada celda de estado con los nuevos valores calculados.
        De esta forma, preservamos intacta la estructura y los caracteres originales.
        Ya fui previsor y por esto guardo el bin original
        """
        binario_ew = bytearray(self.raw_bin)
        bytes_per_cell = 4
        
        for cell_id, tupla in self.dict_automatron.items(): # Recorremos solo las celdas de estado

            if self.is_state(tupla):
                peso_calculado = tupla[1]
                byte_index = (cell_id) * bytes_per_cell#Como no cambiamos los ids, la direccion es la misma
                peso_bytes = peso_calculado.to_bytes(3, byteorder='little')
                binario_ew[byte_index : byte_index+3] = peso_bytes
                
        with open(output_filename, 'wb') as f:
            f.write(binario_ew)

if __name__ == "__main__":#Voy a usar argparse porque me es bastante cómodo
    parser = argparse.ArgumentParser(description="siw.py - State Indexing Weights")
    parser.add_argument('input_bin', help="Fichero con la versión compilada de un autómata finito acíclico.")
    parser.add_argument('output_bin', help="Fichero de salida en el que se guardará la nueva versión con los pesos.")
    
    args = parser.parse_args()
    
    # Manejo de errores de fichero no existente y demás
    if not os.path.exists(args.input_bin):
        print(f"Error: El fichero de entrada '{args.input_bin}' no existe.", file=sys.stderr)
        sys.exit(1)
        
    try:#Instanciamos, indexamos pesos y guardamos
        automata = Nafda(args.input_bin)
        automata.index_weights(id_celda=2)
        automata.save_bin(args.output_bin)
        
        print(f"Pesos calculados y guardados en '{args.output_bin}'.")
        
    except Exception as e:#Error genérico
        print(f"Error procesando el autómata: {e}", file=sys.stderr)
        sys.exit(1)

