#
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

import multiprocessing, time, random, os, threading
from multiprocessing import Process, Manager
from threading import Thread

NUM_WORKERS = 2  # Number of processes or threads to spawn
# (dependent of the scenario).

VARIABLE = 0
CYCLE_N_TIMES = 2

# Lee el valor de la variable
def get_VARIABLE_value():
    global VARIABLE
    if type(VARIABLE) is int:
        return VARIABLE
    elif type(VARIABLE) is multiprocessing.managers.ValueProxy:
        return VARIABLE.value
    else:
        print(type(VARIABLE))
        return VARIABLE

# Escribe un nuevo valor en la variable
def set_VARIABLE_value(v: int):
    global VARIABLE
    if type(VARIABLE) is int:
        VARIABLE = v
    elif type(VARIABLE) is multiprocessing.managers.ValueProxy:
        VARIABLE.value = v
    else:
        print(type(VARIABLE))
        VARIABLE = v

# Entra en un bucle de n iteraciones e imprime de cada vez el valor actual, y el que se escribe
# Si soy el último, escribe una separación
# Duerme durante NUM_WORKERS segundos para que haya siempre un desfase de 1 segundo entre proceso y proceso
def poll(delay_sleep, am_i_last, repeat_n_times):
    i = 1
    time.sleep(delay_sleep)
    while i <= repeat_n_times:
        prev_value = get_VARIABLE_value()
        set_VARIABLE_value(random.randint(1, 100))
        print("ENTITY {0}, number was {1}, "
              "now it is {2}".format(os.getpid(), prev_value, get_VARIABLE_value()))
        if am_i_last:
            print("------------")
        time.sleep(NUM_WORKERS)
        i += 1

# Lanza los workers, que pueden ser procesos o hilos
# El argumento "parallelism_option" es una librería, puede ser la que arranca hilos o procesos,
# ambas tienen la misma firma
def spawn(parallelism_option):
    worker_list = list()
    am_i_last = False
    for t in range(0, NUM_WORKERS):
        if t == NUM_WORKERS - 1:
            am_i_last = True
        c = parallelism_option(target=poll, args=(t, am_i_last, CYCLE_N_TIMES,))
        worker_list.append(c)

    for w in worker_list:
        w.start() # Arranca el hilo o proceso

    for w in worker_list:
        w.join() # Espera a que el hilo o proceso termine


if __name__ == "__main__":
    print("Started main process")
    print("Going to use parallelism with {0} entities".format(NUM_WORKERS))

    random_value = random.randint(1, 100)

    VARIABLE = random_value
    print("Setting variable value with random value = {0}\n".format(VARIABLE))

    print("Spawning processes (Escenario 1)")
    spawn(Process)

    print("Spawning threads (Escenario 2)")
    spawn(Thread)

    manager = Manager() # el Manager() se usa para crear shared objects
    # como? No lo se, no hay tiempo para eso xd.s
    VARIABLE = manager.Value('VARIABLE', random_value)

    print("Spawning processes with shared variable (Escenario 3)")
    spawn(Process)
