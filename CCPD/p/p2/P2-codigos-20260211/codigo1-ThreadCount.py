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

import time
import random
import threading
import pandas as pd

MAX_WAIT_TIME_MS = 200
DUMP_EVERY_N_COUNTS = 20
TO_BE_ADDED = 5e1
N_THREADS = 20


class CountContainer(object):
    def __init__(self, ini_value):
        self.__count__ = ini_value
        self.__count_access = threading.Semaphore(1)

    def get_count(self):
        return self.__count__

    def set_count(self, new_count):
        self.__count__ = new_count

    def lock_count(self):
        self.__count_access.acquire()

    def unlock_count(self):
        self.__count_access.release()

    def add_to_count(self, x, n):
        # dividido 1000 porque son milisegundos.
        # NO SIEMPRE espera 200 milisegundos entre cada
        # vez que se suma 1, sino que se toman valores random
        # entre el max y min, por media estadistica suele caer
        # muchas mas veces valores cercanos a la media. Por eso
        # veras como pareciera que el tiempo de espera tiende a ser
        # algo parecido a MAX_WAIT_TIME_MS / 2.
        time.sleep(random.randint(0,MAX_WAIT_TIME_MS) / 1000)
        x += n
        return x


def unsafe(count, n):
    while n > 0:
        c = count.get_count()
        c = count.add_to_count(c, 1)
        count.set_count(c)
        n -= 1


def safe(count, n):
    while n > 0:
        count.lock_count()  #LOCK ACQ. Si otro hilo lleva el LOCK a 0
        # entonces el hilo que hace LOCK ACQ espera en esta linea hasta
        # que el otro haga LOCK FREE.
        c = count.get_count()
        c = count.add_to_count(c, 1)
        count.set_count(c)
        count.unlock_count() #LOCK FREE
        n -= 1


def spawn(measurements, counts, method_string, method):
    global N_THREADS, TO_BE_ADDED

    count = CountContainer(0)
    threads = list()
    n = int(TO_BE_ADDED / N_THREADS)
    n_mod = TO_BE_ADDED % N_THREADS
    for thread_num in [*range(0, N_THREADS, 1)]:
        thread_slice = n
        if thread_num < n_mod:
            thread_slice += 1
        t = threading.Thread(target=method, args=(count, thread_slice,))
        threads.append(t)

    start = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end = time.time()

    measurements[method_string] = int(1000 * (end - start))
    counts[method_string] = count.get_count()


def save_config():
    d = dict()
    d["MAX_WAIT_TIME_MS"] = MAX_WAIT_TIME_MS
    d["TO_BE_ADDED"] = TO_BE_ADDED
    d["N_THREADS"] = N_THREADS
    return d


def run_experiment(functions):
    global all_measurements, counts
    measurements = save_config()
    counts = save_config()
    print("Running experiment with config: {0}".format(save_config()))
    for (f_name, funct) in functions:
        spawn(measurements, counts, f_name, funct)
    all_measurements.append(measurements)
    all_counts.append(counts)


def print_results(all_measurements, all_counts):
    print("-----------------")
    print("TIME MEASUREMENTS (in ms)")
    print(pd.DataFrame(all_measurements))
    print("-----------------")
    print("FINAL COUNT VALUE")
    print(pd.DataFrame(all_counts))
    print("-----------------")


if __name__ == '__main__':
    functs = [("UNS", unsafe), ("SAF", safe)]

    all_measurements = list()
    all_counts = list()
    TO_BE_ADDED = int(2e2)
    MAX_WAIT_TIME_MS = 200
    N_THREADS = 10
    try:
        run_experiment(functs)
    except KeyboardInterrupt:
        pass
    print_results(all_measurements, all_counts)

    # all_measurements = list()
    # all_counts = list()
    # TO_BE_ADDED = int(4e2)
    # DUMP_EVERY_N_COUNTS = 20
    # MAX_WAIT_TIME_MS = 200
    # try:
    #     for N_THREADS in [20, 40, 80]:
    #         run_experiment(functs)
    # except KeyboardInterrupt:
    #     pass
    # print_results(all_measurements, all_counts)
    #
    # all_measurements = list()
    # all_counts = list()
    # TO_BE_ADDED = int(4e2)
    # DUMP_EVERY_N_COUNTS = 20
    # N_THREADS = 20
    # MAX_WAIT_TIME_MS = 200
    # try:
    #     for MAX_WAIT_TIME_MS in [200, 400, 600]:
    #         run_experiment(functs)
    # except KeyboardInterrupt:
    #     pass
    # print_results(all_measurements, all_counts)

