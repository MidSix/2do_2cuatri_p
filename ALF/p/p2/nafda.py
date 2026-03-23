import argparse
import sys
import os

class Nafda():
    """
    Clase que implementa un automáta sobre una implementación de lista dirigida sobre un diccionario
    Algo raro, pero es lo que se me ocurrió para manejar fácil el formato del binario.
    Modificada de la parte 1, le quite save y index_weights pq no hacian falta aqui
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
    
    def words_accepted(self, id_celda: int = 2, prefijo: str = ""):# Con toda la estructura ya hecha en la parte 1, esta función sale sola
        """
        Imprime recursivamente todas las palabras del autómata.
        """
        transitions = self.obtain_transitions(id_celda)# Obtenemos las transiciones de la celda actual
        
        for char, dest_celda in transitions:
            if char == 'ε' :  # O el carácter que denote fin de palabra 
                print(prefijo)#Imprimimos lo acumulado
            else:
                self.words_accepted(dest_celda, prefijo + char)
    
    def word_to_index(self, palabra: str) -> str:#Esta función ya estaba hecha en pseudocodigo, la adapte para nuestra clase
        """
        Calcula el índice de una palabra sumando los pesos de las transiciones
        lexicográficamente precedentes (Opción 'i' del programa).
        Basado fielmente en el pseudocódigo de la Figura 2.
        """
        indice = 1  
        estado_actual = 2  
        
        palabra_terminada = palabra + 'ε' # Simulamos el \0 de C añadiendo 'ε' al final de la palabra 
        
        for char in palabra_terminada: 
            transiciones = self.obtain_transitions(estado_actual)
            destino_correcto = None
            val_buscado = 0 if char == 'ε' else ord(char)# ('ε' debe valer 0 para ser el menor de todos)
            
            for trans_char, dest_cell in transiciones:
                
                val_trans = 0 if trans_char == 'ε' else ord(trans_char)
                
                if val_trans < val_buscado:# Regla del enunciado, sumamos el peso si es lexicográficamente precedente
                    peso_destino = self.dict_automatron[dest_cell][1]
                    indice += peso_destino 
                    
                elif val_trans == val_buscado:
                    destino_correcto = dest_cell
            
            if destino_correcto is not None:
                estado_actual = destino_correcto 
            else:
                return "unknown" 
                

        if estado_actual == 1:
            return str(indice)
        else:
            return "unknown" 


    def indice_a_palabra(self, indice: int) -> str:#Lo mismo que la anterior
        """
        Implementación fiel del pseudocódigo Indice_a_Palabra (Figura 3).
        """
        peso_total = self.dict_automatron[2][1]#Primero chequeamos el indice, si esta dentro del dic
        if indice < 1 or indice > peso_total:
            return "index out of bounds"
            
        estado_actual = 2#Inicializamos
        numero = indice
        palabra = ""
        
        while numero > 0: #Vamos restando basicamente
            transiciones = self.obtain_transitions(estado_actual)
            transicion_encontrada = False
            
            for c, dest_cell in transiciones:
                estado_aux = dest_cell
                peso_aux = self.dict_automatron[estado_aux][1]
                
                if numero > peso_aux:
                    numero -= peso_aux
                    
                else:
                    if c != 'ε': # Evitamos imprimir el carácter de control invisible
                        palabra += c
                        
                    estado_actual = estado_aux
                    
                    if estado_actual == 1:
                        numero -= 1
                    
                    transicion_encontrada = True
                    break 
                    
            if not transicion_encontrada:
                return "index out of bounds"
                
        return palabra

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="nadfa.py - Diccionario e indexación (Parte 2)")
    
    parser.add_argument('opcion', choices=['-d', '-i', '-w'],     # El PDF especifica tres opciones exactas: '-d', 'i', 'w' 
                        help="Opción a ejecutar: -d (diccionario), -i (palabra a índice), -w (índice a palabra)")
    
    parser.add_argument('input_bin', help="Fichero con la versión compilada y numerada del autómata.")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_bin):
        print(f"Error: El fichero de entrada '{args.input_bin}' no existe.", file=sys.stderr)
        sys.exit(1)
        
    try:
        automata = Nafda(args.input_bin)
        
        if args.opcion == '-d':# 1. Opción -d: Listar todo el diccionario
            automata.listar_palabras(id_celda=2, prefijo="")
            
        elif args.opcion == '-i':# 2. Opción i: Palabra a Índice (Leyendo de stdin)
            for linea in sys.stdin:# sys.stdin nos permite procesar las líneas enviadas por "cat" o introducidas a mano
                palabra = linea.strip() # Quitamos los saltos de línea y espacios fantasma porsiaca.
                if palabra:
                    resultado = automata.palabra_a_indice(palabra)
                    print(resultado)
                    
        elif args.opcion == '-w': # 3. Opción w: Índice a Palabra (Leyendo de stdin) 
            for linea in sys.stdin:
                str_indice = linea.strip()
                if str_indice:
                    try:
                        indice = int(str_indice)
                        resultado = automata.indice_a_palabra(indice)
                        print(resultado)
                    except ValueError:
                        print("index out of bounds")# Si nos meten texto en lugar de un número, lo considerao out
                        
    except Exception as e:#Error genérico
        print(f"Error interno procesando el autómata: {e}", file=sys.stderr)
        sys.exit(1)
