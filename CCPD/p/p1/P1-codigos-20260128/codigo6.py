#! /usr/bin/python
#
# Copyright © 2025 by Jonatan Enes (jonatan.enes@udc.es)
# Computer Engineering department, Universidade da Coruña, Spain.
#
# This file is part of several courses on parallel processing from Universidade da Coruña,
# and it can only be used and/or modified by the author, the students or any 
# explicitly authorized person by the author, inside the context of the subject. 
# Redistribution to a third-party without previous authorization is strictly forbidden.
# No commercial use is allowed.
#
# This file has only academic purposes and should not be used for any real-world
# scenario, the author holds no accountability for its use or misuse.

import time
import random
import math


def suma_cuatro(x):
    return x + 4


def mult_dos(x):
    return x * 2


def suma_doce(x):
    return x + 12


def haz_raiz(x):
    return math.sqrt(x)


def aplica_operacion(op, x):
    return op(x)


def aplica_operacion_sobre_datos(op, *argv):
    print("------------------")
    print("Hi this is '{0}' function executing".format(aplica_operacion_sobre_datos.__name__))
    print("The function I was given to execute is -> {0}, also named as '{1}'".format(op, op.__name__))
    print("The DATA I have to process is -> {0}".format(argv))
    print("I have finished, giving back control")
    print("------------------")
    return [op(x) for x in argv]


def measure_times(target, args):
    print("xxxxxxxxxxxxxxxxxx")
    print("Hi this is '{0}' function executing".format(measure_times.__name__))
    print("Measuring times around the execution of the function '{0}'".format(target.__name__))
    start = time.time()
    result = target(*args)
    end = time.time()
    print("It took exactly {0:.2f} miliseconds".format(1000 * (end - start)))
    print("I have finished, giving back control")
    print("xxxxxxxxxxxxxxxxxx")
    return result


x = random.randint(1, 10)
print("##### IMPERATIVO CLÁSICO")
print("Voy a sumar 4 a el número aleatorio {0}, el resultado es {1}\n".format(x, suma_cuatro(x)))

print("##### FUNCIONAL SIMPLE")
print("Voy a sumar 4 a el número aleatorio {0}, el resultado es {1}".format(x, aplica_operacion(suma_cuatro, x)))
print("Voy a multiplicar por 2 el número aleatorio {0}, el resultado es {1}\n".format(x, aplica_operacion(mult_dos, x)))

print("##### FUNCIÓN MISTERIO")
print("Ahora tiraré un dado de 6 caras, si sale menor o igual 3, sumaré 4, sino multiplicaré por 2 al número aleatorio {0}".format(x))
print("En este punto aún no se qué función ejecutaré, pero más adelante en el código sé que ejecutaré una función llamada 'fun', ahora la escogeré")
choose = random.randint(1, 6)
if choose <= 3:
    fun = suma_cuatro
else:
    fun = mult_dos
print("El dado arrojó {0} así que la función a ejecutar será {1}, también llamada '{2}'".format(choose, fun, fun.__name__))
print("El resultado entonces es {0}\n".format(aplica_operacion(fun, x)))


print("##### LISTA DE FUNCIONES")
x = random.randint(1, 10)
print("Ahora voy a definir un array de funciones, y las voy a aplicar en orden al número aleatorio {0}".format(x))
funs = [suma_cuatro, mult_dos, suma_doce, haz_raiz]
for f in funs:
    x = f(x)
    print("Aplico la función '{0}', res -> {1}".format(f.__name__, x))
print("")


print("##### APLICAR FUNCIÓN CON ARGUMENTOS VARIABLES")
x = random.randint(1, 10)
y = random.randint(1, 10)
z = random.randint(1, 10)
data = (x, y, z)
print("Voy a generar 3 números aleatorios y a sumarles 4, números -> {0}".format(data))
print("La función será la de suma 4, pero realmente la aplicará otra función que recibe un número de argumentos variable")
print("El resultado es {0}\n".format(aplica_operacion_sobre_datos(suma_cuatro, *data)))


print("##### MEDICIÓN DE TIEMPOS Y PROGRAMACIÓN FUNCIONAL")
COUNT = int(5e2)
data = [x for x in range(1, COUNT)]
print("Voy a generar {0} números aleatorios y a sumarles 4".format(COUNT))
print("Pero esta vez envolveré la operación en otra función que mide tiempos y "
      "que a su vez llama a la función anterior de argumentos variables")
result = measure_times(target=aplica_operacion_sobre_datos, args=(suma_cuatro, *data))
print("La suma de todo es: {0} \n".format(sum(result)))
