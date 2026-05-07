import argparse
import sys
import os

class CYK:
    def __init__(self):
        self.grammar = {} #Lo mejor aqui es un diccionario la clave es el No Terminal izquierdo y el valor una lista de lo que tiene a la derecha.
        self.axiom = None 

    def load_grammar(self, filename):#COn esto leemos el fichero, mucho mejor que en binary de la anterior jaja, aqui es texto plano
        """Carga la gramática desde un archivo. El formato del archivo es el siguiente:
            - La primera letra es el axioma y su regla de producción.    
            - Las siguientes líneas contienen las demas reglas de producción, una por línea, en el formato:
            Aα, donde A es un No Terminal y α es una cadena de símbolos (terminales y/o No Terminales). 
            Por ejemplo: SAB
                         Aa...
        """
        try:
            with open(filename, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
                
                if not lines:
                    raise ValueError("El fichero esta vacío")
                for line in lines:#Con este aproach recorremos el txt 2 veces, la primera para comprobar el formato y la segunda para cargarlo, pero es mas limpio y claro que hacerlo todo en una pasada
                                    #Ademas no creo que el rendimiento sea un gran problema dado que las gramaticas no suelen ser tan grandes, y la claridad del código es importante
                    if not line[0].isupper() or not line.isalpha(): #Ya comprobamos aqui errores de formato: La izquierda debe ser Mayúscula y todo deben ser letras
                        sys.stderr.write(f"Error de formato en la línea: {line}\n")
                        sys.exit(1)
                    izq, der = line[0], line[1:]
                
                self.axiom = lines[0][0]# El primer carácter de la primera línea es el axioma

                for line in lines:#Y aqui leemos las reglas que estan a una por linea
                    izq = line[0] # El primer carácter es el No Terminal 
                    der = line[1:] # Todo lo demás es la parte derecha 
                    
                    if izq not in self.grammar:#Esto es para asegurarnos de que el No Terminal izquierdo tenga una lista asociada en el diccionario
                        self.grammar[izq] = []
                    self.grammar[izq].append(der)
                    
        except Exception as e:
            sys.stderr.write(f"Error leyendo la gramatica: {e}\n")
            sys.exit(1)

    def check_grammar(self) -> bool:
        """
        Verifica si la gramática cargada cumple con la Forma Normal de Chomsky (FNC).
        Las reglas permitidas segun FNC son:
        1. A -> BC (Dos No Terminales / Mayúsculas)
        2. A -> a  (Un Terminal / Minúscula)
        No se permiten producciones vacías (épsilon).
        Asi que hacemos un filtrado positivo de las reglas, si alguna no cumple con estas condiciones, 
        entonces la gramática no esta en FNC.
        """
        if not self.grammar:#Primer paso evidente
            return False

        for _, producciones in self.grammar.items():
            for p in producciones:
                longitud = len(p)
                # Caso 1: Producción Terminal (A -> a)
                if longitud == 1:
                    if not p[0].islower():# El símbolo debe ser una letra minúscula
                        return False
                
                # Caso 2: Producción Binaria (A -> BC)
                elif longitud == 2:
                    if not (p[0].isupper() and p[1].isupper()):# Ambos símbolos deben ser letras mayúsculas
                        return False
                
                # Caso 3: Regla inválida (longitud 0/épsilon o > 2)
                else:
                    # FNC no permite producciones vacías ni reglas de más de 2 símbolos 
                    return False
                    
        return True#Más tarde para -g hare la logica de decir YES o NO
    
    def parse(self, word: str) -> bool:#Implementamos CYK, no voy a mentir, me base en un pseudocodigo que encontre en internet,
                                        # pero lo adapte a mi codigo y le di un toque mio 
        """
        Aqui aplicamos el algoritmo CYK para determinar si la palabra dada pertenece al lenguaje generado por la gramática en FNC.
        El algoritmo se basa en construir una tabla de análisis que indica qué No Terminales pueden generar
        cada subcadena de la palabra. La tabla se llena de abajo hacia arriba, comenzando con las subcadenas de longitud 1
        (los caracteres individuales) y luego combinando resultados para subcadenas más largas.
        """
        if not self.check_grammar():#Primero verificamos que la gramática esta en FNC, si no lo esta, no tiene sentido seguir con el algoritmo
            return False
        n = len(word)
        if n == 0:#Si la palabra es vacía, no es parte del lenguaje ya que no esta en FNC para empezar
            return False
        table = {}#Esta tabla es un diccionario donde la clave es una tupla (i, j) 
            #y el valor es un conjunto(set) de No Terminales que pueden generar la 
            # subcadena de longitud j qe comienza en la posición i de la palabra.
            #es relevante usar un set porque puede haber varias regla que generen la misma subcadena y no queremos duplicados.
        
        for i in range(1, n + 1):#Aqui simplemente recorremos cada caracter de la 
                                #palabra y buscamos que No Terminales pueden generar ese caracter, 
                                #osea reglas de tipo A -> a
            char = word[i-1]
            table[(i, 1)] = set()
            for nt, producciones in self.grammar.items():# Buscamos reglas de tipo A -> w_i, donde w_i es el caracter actual 
                if char in producciones:
                    table[(i, 1)].add(nt)
        # Aqui viene el famoso bucle triple que es característico del algoritmo CYK, donde llenamos la tabla para subcadenas de longitud mayor a 1
        #llevaba sin implementar una anidación triple desde el final de IS, aunque aqui tenia pseudocodigo para guiarme, asi que no me costo tanto, 
        # aunque si me costo un poco entender la logica de los indices y como se relacionan entre si
        
        for j in range(2, n + 1): # Longitud de la subcadena
            for i in range(1, n - j + 2): # Posicion de inicio 
                table[(i, j)] = set()#Asinamos un set vacio a cada celda antes de llenarla, esto es necesari para evitar errores de clave no encontrada
                
                for k in range(1, j): # Punto de división k 
                                    # Aplicamos la lógica A->BC 
                                    # B debe estar en la celda del primer trozo: (i, k) y
                                    # C debe estar en la celda del segundo trozo: (i + k, j - k)
                    for nt, producciones in self.grammar.items():
                        for prod in producciones:
                            if len(prod) == 2: # Solo reglas binarias A-> BC
                                B, C = prod[0], prod[1]
                                if B in table[(i, k)] and C in table[(i+k, j-k)]:
                                    table[(i, j)].add(nt)

        return self.axiom in table.get((1, n), set())  # Verificamos el axioma(La cadena pertenece al lenguaje si el axioma está en N_{1,n})
                                                        #es decir, si el axioma puede generar la subcadena que es toda la palabra (longitud n que empieza en 1)

if __name__ == "__main__":#Ahora solo queda la interfaz, voy a usar lo de la anterior practica y pista
    parser = argparse.ArgumentParser(description="cyk.py - Algoritmo CYK para Gramáticas en FNC")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g', action='store_true', help="Comprobar si la gramática está en FNC")
    group.add_argument('-p', action='store_true', help="Parsear cadenas desde stdin")
    
    parser.add_argument('grammar_file', help="Fichero de texto con la descripción de la gramática")#El enunciado dice que el 
    #programa debe recibir un argumento con el nombre del fichero de la gramática, 
    # asi que lo hacemos obligatorio y posicional, no es necesario usar un flag para esto, 
    # ya que el hecho de que sea posicional ya implica que es obligatorio y el nombre del 
    # argumento ya dice claramente que se trata del fichero de la gramática
    
    args = parser.parse_args()
    
    if not os.path.exists(args.grammar_file):
        sys.stderr.write(f"Error: El fichero '{args.grammar_file}' no existe.")
        sys.exit(1)
        
    cyk = CYK()
    cyk.load_grammar(args.grammar_file)
    
    if args.g:
        if cyk.check_grammar():
            print("YES")
        else:
            print("NO")
            
    elif args.p:  
        if not cyk.check_grammar():# El enunciado dice que hay que salir si no es FNC
            sys.stderr.write("Error: La gramática no está en Forma Normal de Chomsky(FNC).")
            sys.exit(1)
            
        input_text = sys.stdin.read()
        for word in input_text.splitlines():
            word = word.strip()
            if word:
                if cyk.parse(word):
                    print("YES")
                else:
                    print("NO")