import argparse
"""
      Primero hay que saber como devuelve la salida antes de
      empezar a programar algo.

      - Teoremas devueltos para input 20 al ejecutar el programa.

      Teoremas = [
      MI(listo), MIU(listo), MII(listo), MIUIU(listo),
      MIIU(listo), MIIII(listo), MIUIUIUIU(listo), MIIUIIU(listo),
      MIIIIU(listo), MIIIIIIII, MUI, MIU, MIUIUIUIUIUIUIUIU,
      MIIIIUIIIIU, MUIU, MIUU, MIIIIIIIIU, MIIIIIIIIIIIIIIII, MUIIIII
      ]

      * Se entiende que las reglas que no se mencionen explicitamente
          que acepta es porque no las acepta la cadena.

      (MI -> Acepta regla 1 y 2)
      - MI ---regla1---> MIU (La cadena MIU inferida del Axioma MI se
      agrega a la lista de teoremas)
      - MI ---regla2---> MII (La cadena MII inferida del Axioma MI se
      agrega a la lista de teoremas)

      --> Agregar las inferencias a la lista de teoremas es algo que
          haremos para cada inferencia. Asi sacamos los elementos listados
          en la lista de Teoremas

      (MIU -> Acepta regla 2)
      - MIU --regla2---> MIUIU

      (MII -> Acepta regla 1 y 2)
      - MII --regla1---> MIIU
      - MII --regla2---> MIIIII

      (MIUIU -> Acepta regla 2)
      - MIUIU ---regla2---> MIUIUIUIU

      (MIIU -> Acepta regla 2)
      - MIIU ---regla2---> MIIUIIU

      (MIIII -> Acepta regla 1,2,3)
      - MIIII ---regla1---> MIIIIU
      - MIIII ---regla2---> MIIIIIIII
      - MIIII ---regla3---> MUI
      - MIIII ---regla3---> MIU

      (MIUIUIUIU -> Acepta regla 2)
      - MIUIUIUIU --->regla2---> MIUIUIUIUIUIUIUIU

      (MIIUIIU   -> Acepta regla 2)
      MIIUIIU --->regla2--->MIIUIIUIIUIIU

      (MIIIIU -> Acepta regla 2,3)
      - MIIIIU --->regla2---> MIIIIUIIIIU
      - MIIIIU --->regla3---> MUIU
      - MIIIIU --->regla3---> MIUU

      (MIIIIIIII -> Acepta regla 1, 2, 3)
      - MIIIIIIII --->regla1--->MIIIIIIIIU
      - MIIIIIIII --->regla2--->MIIIIIIIIIIIIIIII
      - MIIIIIIII --->regla3--->MUIIIII
      - Ya se completaron los 20 teoremas que pide el ejemplo del output.

      En resumen. Se aplican TODAS las reglas de inferencias que sean
      posibles sobre cada verdad(axioma o teorema). Como se hace? Se
      aplican todas las reglas posibles sobre una verdad las veces
      que dicha regla pueda aplicarse sobre ella, usualmente solo
      1 vez, pero fijese en el caso de la cadena MIIII, en ese caso
      la regla de inferencia 3 puede aplicarse 2 veces ya que
      al tener 4 I's puede agrupar 3 de ellas de 2 formas distintas
      "combinaciones sin repeticion", y las reglas se aplican en orden.
      Si una cadena acepta la regla 2,4,3 entonces primero se aplicara la
      regla 2, luego la 3 y por ultimo la 4. Cada resultado de inferencia
      se convierte en un nuevo teorema que sera agregado a la lista de
      teoremas de los que es posible inferir nuevos teoremas. El orden
      de inferencia para cada teorema dentro de la lista de teoremas
      seguira un esquema FIFO. Es decir, se inferira a partir de los
      teoremas mas antiguos

      -> Las reglas de inferencia que pueden aplicarse mas de una vez
          sobre una misma cadena son la regla 3 y 4, en caso que se
          puedan aplicar mas de una vez las agrupaciones se haran
          de izq a der, ejemplo:
          En el caso de MIIII -> M(III)I y luego MI(III) vamos moviendo
          la agrupacion de I's de izq a der, es la convencion que se
          sigue para retornar el mismo resultado que el output.
  """
MODULE_NAME = "miu.py"

#__file__ es un metodo magico que devuelve el path desde la raiz
#del sistema de archivos hasta nuestro modulo python.

#split devuelve una lista donde cada elemento es el resultado de
#separar el string original por el caracter especificado en parentesis
#accedemos al ultimo elemento que resulta ser el nombre de nuestro
#modulo

def regla1(curr: str, candidates: list[str] , limit: int):
    # --- Regla 1: xI -> xIU ---
    if len(candidates) < limit:
        if curr.endswith("I"):
            new_t = curr + "U"
            candidates.append(new_t)

def regla2(curr: str, candidates: list[str], limit: int):
    # --- Regla 2: Mx -> Mxx ---
    if len(candidates) < limit:
        if curr.startswith("M"):
        # SOLO hay y SOLO podra haber UNA sola M en todas
        # las cadenas de este lenguaje. Y estara justo al inicio
        # de toda cadena.
            x = curr[1:] # Todo lo que sigue a la M
            new_t = "M" + x + x
            candidates.append(new_t)

def regla3(curr: str, candidates: list[str], limit: int):
    # --- Regla 3: III -> U ---
    # "combinaciones sin repetición", "de izq a der" -> buscamos todas las ocurrencias
    if len(candidates) < limit:
        # Iteramos sobre el string para encontrar 'III'
        # Rango hasta len-2 para asegurar grupos de 3
        for i in range(len(curr) - 2):
            if curr[i:i+3] == "III":
                if len(candidates) < limit:
                    # Reemplazamos esa ocurrencia específica por U
                    new_t = curr[:i] + "U" + curr[i+3:]
                    candidates.append(new_t)
                else:
                    break

def regla4(curr: str,candidates: list[str], limit:int):
    # --- Regla 4: UU -> _ (eliminar) ---
    if len(candidates) < limit:
        # Iteramos sobre el string para encontrar 'UU'
        # Rango hasta len-1 para asegurar grupos de 2
        for i in range(len(curr) - 1):
            if curr[i:i+2] == "UU":
                if len(candidates) < limit:
                    # Eliminamos esa ocurrencia específica
                    new_t = curr[:i] + "" + curr[i+2:]
                    candidates.append(new_t)
                else:
                    break

def generate_MIU_theorems(limit: int) -> None:
    theorems = ["MI"]
    seen = {"MI"}
    current_idx = 0
    # Bucle principal de generación
    while len(theorems) < limit:
        if current_idx >= len(theorems):
            # Si ya hemos procesado todos los teoremas actuales
            # y no alcanzamos el límite, paramos. Aunque esta situacion
            # jamas deberia ocurrir, esta presente para mayor robustez.
            break

        # En cada iter tomamos un teorema y sumamos 1 al indice de
        # seleccion de los teoremas, por tanto en la siguiente
        # iter pues seleccionaremos el siguiente xd. Mientras los
        # teoremas como se ve mas abajo se van agregando al final.
        # Por lo que este proceso sigue el principio FIFO.
        curr = theorems[current_idx]
        # Si, los type hints tambien pueden colocarse
        # cuando defines variables, puede ser util para saber que
        # dentro de candidates meteras elementos str.
        candidates: list[str] = []
        current_idx += 1

        regla1(curr, candidates, limit)
        regla2(curr, candidates, limit)
        regla3(curr, candidates, limit)
        regla4(curr, candidates, limit)

# Candidates es una lista que redefinimos en cada iter
# las funciones regla1,2,3,4 agregan los teoremas inferidos del teorema
# actual(curr) NO a la lista de teoremas
# sino a la lista candidatos, por que? Para permitir que este mismo
# codigo pueda ser reutilizado tanto por la flag -a como la -u.
# Si tenemos la flag -a los teoremas se iran agregando a la lista
# teoremas sin mayor comprobacion salvo la que impide agregar mas
# teoremas si supera el limit impuesto por el usuario via ejecucion
# CLI. Si tenemos la flag -u se iran agregando a la lista teoremas
# siempre que en nuestro conjunto auxiliar no esten, si no estan en el
# conjunto quiere decir que el teorema es nuevo, ya que el conjunto
# lo vamos actualizando a la par de nuestra lista de teoremas.

        if args.a is not None:
            # Si nos da igual la posibilidad de
            # teoremas repetidos simplemente agregamos uno a uno
            # los teoremas de candidates a theorems y deteniendo esta
            # operacion inmediatamente si llegamos al limite de
            # teoremas que el usuario esta pidiendo.
            for new_t in candidates:
                # Si ya tenemos suficientes, paramos inmediatamente
                if len(theorems) >= limit:
                    break
                theorems.append(new_t)
        else:
            # Si se ejecuta este bloque quiere decir que el usuario
            # ejecuto el programa con la flag -u, UNIQUE theorems.
            # por tanto lo unico que haremos sera tomar la lista
            # candidates que conforman todos los teoremas que se
            # infirieron en una sola iteracion(es decir, todos los
            # teoremas que se infieron partiendo de UN solo teorema)
            # y SOLAMENTE agregaremos a la lista de teoremas aquellos
            # teoremas de candidates que NO esten en la lista theorems
            # es decir, aquellos que NO esten repetidos, de esta manera
            # la lista theorem que nos quedara al final sera UNIQUE.
            for new_t in candidates:
                # Si ya tenemos suficientes, paramos inmediatamente
                if len(theorems) >= limit:
                    break
                # Los conjuntos en python funcionan por hash.
                # Es decir, no va comparando elemento a elemento
                # para ver si esta o no, simplemente ve si el hash
                # de un objeto inmutable existe en el conjunto,
                # si lo hace entonces existe en el conjunto, si no,
                # no existe. por tanto la complejidad de esta
                # comprobacion es O(1)
                if new_t not in seen:
                    theorems.append(new_t)
                    seen.add(new_t)

    # Imprimir resultados
    for t in theorems:
        print(t)

def is_a_MIU_thorem(theorem: str):
    """
    Procedimiento de decisión del sistema MIU.
    Cabe aclarar que un procedimiento de dicision es una serie de pasos
    que permitin "decidir" si un teorema dado pertenece o no a un
    sistema/lenguaje formal. Por lo tanto esta funcion se usa
    para determinar si una cadena es un teorema válido del sistema
    formal MIU o no.
    """
    # El axioma base empieza por M, y ninguna regla añade o quita M.
    # Por tanto, debe tener exactamente una 'M' y estar al principio.
    # ambos metodos str son self-explanatory.
    if not theorem.startswith('M') or theorem.count('M') != 1:
        return False

    # Los simbolos con los que cuente el teorema deben ser parte
    # del abecedario del lenguaje formal MIU, de no serlo, el teorema
    # dado no podra inferirse usando este lenguaje porque al menos uno
    # de los simbolos de los que se compone el teorema no existen en el
    # lenguaje.
    for char in theorem:
        if char not in ('M', 'I', 'U'):
            return False

    # Comprobación de la invariante. Si esto varia, entonces no puede
    # ser un teorema del lenguaje.
    # El número de 'I's no puede ser congruente(igual a cero en modulo 3)
    # con 0 (módulo 3).
    num_i = theorem.count('I')
    if num_i % 3 == 0:
        return False

    return True

if __name__ == "__main__":
    #$ python miu -a n:int or $ python miu -u n:int
    parser = argparse.ArgumentParser(
        description="Write an int n with one of the available flags"
        + " (-a or -u) to get n theorems given the initial axioms"
        + " and inferential rules"
        )
    parser.add_argument('-a', type=int,
                        help='With this flag calculate n theorems'
                        )
    parser.add_argument('-u', type=int,
                        help='With this flag calculate n UNIQUE theorems'
                        )
    parser.add_argument('-s', type=str,
                        help='With this flag evaluate wether a given' \
                        'theorem is part of the MIU formal language or not.'
    )
    args = parser.parse_args()

    if args.a is not None:
        generate_MIU_theorems(args.a)
    elif args.u is not None:
        generate_MIU_theorems(args.u)
    elif args.s is not None:
        res = is_a_MIU_thorem(args.s)
        print(f"El bool indica si forma parte o no del lenguaje.\n"
              f"Si es True -> forma parte, Si es False -> NO forma parte\n\n"
              f"respuesta = {res}")
    else:
        print(f"\nUso:\npython {MODULE_NAME} -a <num_theorems>\n"
        f"or\npython {MODULE_NAME} -u <num_theorems> -> for UNIQUE theorems\n")