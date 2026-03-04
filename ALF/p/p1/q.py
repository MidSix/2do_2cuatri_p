import argparse
import time # Para medir tiempos de ejecucion simplemente.
import math

MODULE_NAME = "q.py"

# En este primer ejercicio demostramos como la cardinalidad(elementos
# de un conjunto) tanto de los numeros Naturales "N" como de los numeros
# racionales "Q" es la misma. Esto lo hacemos pudiendo listar todos y
# cada uno de los numeros racionales, si los podemos listar significa
# que los podemos enumerar, si los podemos enumerar significa que existe
# una funcion biyectiva entre cada par (natural, racional). Es decir,
# a cada natural le corresponde uno y solo un racional y a cada racional
# le corresponde uno y solo un real.

# Entonces al enumerar los racionales demostramos que tanto N como Q
# tienen la misma cardinalidad. Comparar la cardinalidad entre conjuntos
# finitos es straight-forward. Simplemente se hace un len() de cada uno
# y se comprueba que ambos tengan el mismo numero de elementos, esto
# cambia cuando los conjuntos son infinitos, en este ultimo caso no
# podemos calcular el numero maximo de elementos de cada uno porque
# ninguno tiene una cota superior que limite su numero de elementos.
# por esta razon se hace uso de una funcion biyectiva para este fin.
# si entre cada par de elementos de dos conjunto cualesquiera(incluye
# tanto a finitos como a infinitos) podemos establecer una funcion
# biyectiva entre ellos, entonces ambos conjuntos tienen la misma
# cardinalidad.

# La "aplicacion biyectiva mas usual que se suele construir" es la de
# Georg Cantor.

def qa(n:int) -> bool:
    Result: list[str] = []
    i=1
    j=1
    k=2 # suma de i+j para la diagonal
    prints=0
    while prints<n:
        Result.append(f"{i}/{j}")
        prints+=1

        # Siguiente elemento en el zig-zag de Cantor
        if k % 2 == 1:
            if j == 1:
                k += 1
                i = k - 1
                j = 1
            else:
                i += 1
                j -= 1
        else:
            if i == 1:
                k += 1
                i = 1
                j = k - 1
            else:
                i -= 1
                j += 1
    print(" ".join(Result))
    return True

def qu(n:int) -> bool:#Apartado Opcional, podria implementarlo sobre qa, pero no se pide explicitamente
    Result: list[str] = []
    i=1
    j=1
    k=2
    prints=0
    while prints<n:
        # Solo imprimimos si son coprimos (MCD es 1) para fracciones irreducibles
        if math.gcd(i, j) == 1:
            Result.append(f"{i}/{j}")
            prints+=1

        if k % 2 == 1:
            if j == 1:
                k += 1
                i = k - 1
                j = 1
            else:
                i += 1
                j -= 1
        else:
            if i == 1:
                k += 1
                i = 1
                j = k - 1
            else:
                i -= 1
                j += 1
    print(" ".join(Result))
    return True

if __name__ == "__main__":
    #$ python q.py -a int or $ python q.py -u int
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('-a', type=int, help='Call function qa with an integer argument')
    parser.add_argument('-u', type=int, help='Call function qu with an integer argument')
    args = parser.parse_args()
    if args.a is not None:
        t_antes = time.perf_counter()
        qa(args.a)
        t_despues = time.perf_counter()
        t_ejecucion = t_despues - t_antes
        print(f"\n Ha demorado {t_ejecucion:.8f} s")
    elif args.u is not None:
        t_antes = time.perf_counter()
        qu(args.u)
        t_despues = time.perf_counter()
        t_ejecucion = t_despues - t_antes
        print(f"\n Ha demorado {t_ejecucion:.8f}s")
    else:
        print(f"\nUso:\npython {MODULE_NAME} -a <Call function qa with an integer argument>\n"
        f'or\npython {MODULE_NAME} -u <Call function qu with an integer argument>\n')