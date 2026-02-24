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

from queue import Full, Empty
from threading import Thread, Semaphore
import time
import random
from multiprocessing import Queue
import pandas

# Variables de control
QUEUE_SIZE = 10
ITEMS_TO_PROCESS = 5.5e3
MIN_SLEEP_CONSUMER, MAX_SLEEP_CONSUMER = 100, 300
MIN_SLEEP_PRODUCER, MAX_SLEEP_PRODUCER = 100, 300
NUM_CONSUMERS, NUM_PRODUCERS = 3, 3
QUEUE_BLOCK = False

# No tocar estas
queue = Queue(QUEUE_SIZE)
items_pending = ITEMS_TO_PROCESS


def to_time_miliseconds(start, end):
    return int(1000 * (end - start))


counter_lock = Semaphore(1)


def decrease_counter():
    global items_pending
    counter_lock.acquire()
    items_pending -= 1
    counter_lock.release()


class ProducerThread(Thread):
    def run(self):
        global queue, items_pending, OUTPUT
        while True:
            sleep_time = random.randint(MIN_SLEEP_PRODUCER, MAX_SLEEP_PRODUCER)
            num = random.randint(0, 100)
            try:
                queue.put(num, block=QUEUE_BLOCK)
                # Si la cola está llena, se lanza la excepción "Full"
                if OUTPUT:
                    print("[+] PRODUCER {0} item number {1:3d}, sleeping {2} "
                          "seconds QUEUE : [{3}/{4}]".format(self.native_id, num,
                                                             sleep_time, queue.qsize(), QUEUE_SIZE))
            except Full:
                pass
                # La cola estaba llena, no se hace nada -> pass

            time.sleep(sleep_time / 1000)

            if items_pending <= 0:
                if OUTPUT:
                    print("[*] PRODUCER {0} --> FINISHING".format(self.native_id))
                break


class ConsumerThread(Thread):
    def run(self):
        global queue, items_pending, OUTPUT
        while True:
            sleep_time = random.randint(MIN_SLEEP_CONSUMER, MAX_SLEEP_CONSUMER)
            try:
                num = queue.get(block=QUEUE_BLOCK)
                # Si la cola está vacía, se lanza la excepción "Empty"
                decrease_counter()
                if OUTPUT:
                    print("[-] CONSUMER {0} item number {1:3d}, "
                          "sleeping {2} miliseconds QUEUE : [{3}/{4}] ITEMS: "
                          "[{5} pending]".format(self.native_id, num,
                                                 sleep_time, queue.qsize(),
                                                 QUEUE_SIZE, int(items_pending)))
            except Empty:
                pass
                # La cola estaba vacía, no se hace nada -> pass

            time.sleep(sleep_time / 1000)

            if items_pending <= 0:
                if OUTPUT:
                    print("[*] CONSUMER {0} --> FINISHING".format(self.native_id))
                break


def spawn():
    consumers_list = list()
    for _ in range(0, NUM_CONSUMERS):
        c = ConsumerThread()
        consumers_list.append(c)

    producers_list = list()
    for _ in range(0, NUM_PRODUCERS):
        p = ProducerThread()
        producers_list.append(p)

    for p, c in zip(consumers_list, producers_list):
        p.start()
        c.start()

    start = time.time()
    for p, c in zip(consumers_list, producers_list):
        c.join()
        p.join()
    end = time.time()
    return to_time_miliseconds(start, end)


def empty_queue(q):
    while not q.empty():
        q.get()


def save_config():
    d = dict()
    d["ITEMS_TO_PROCESS"] = int(ITEMS_TO_PROCESS)
    d["QUEUE_SIZE"] = int(QUEUE_SIZE)
    d["MIN_SLEEP_CONSUMER"] = int(MIN_SLEEP_CONSUMER)
    d["MAX_SLEEP_CONSUMER"] = int(MAX_SLEEP_CONSUMER)
    d["NUM_CONSUMERS"] = int(NUM_CONSUMERS)
    d["MIN_SLEEP_PRODUCER"] = int(MIN_SLEEP_PRODUCER)
    d["MAX_SLEEP_PRODUCER"] = int(MAX_SLEEP_PRODUCER)
    d["NUM_PRODUCERS"] = int(NUM_PRODUCERS)
    return d


def run_experiment():
    global i, measurements, items_pending, queue
    queue = Queue(QUEUE_SIZE)
    items_pending = ITEMS_TO_PROCESS
    measurements[i] = save_config()
    measure = spawn()
    measurements[i]["time"] = measure
    print("Took {0} miliseconds to produce and consume {1} items".format(measure, int(ITEMS_TO_PROCESS)))
    i += 1


def pretty_print_df(df, split_strings):
    df_string = df.to_string()
    num_dashes = 24 + 6 * len(df.columns)
    for split in split_strings:
        df_string = df_string.replace("\n{0}".format(split), '\n' + '-' * num_dashes + "\n{0}".format(split))
    return df_string


if __name__ == "__main__":
    OUTPUT = True
    SEPARATORS = ["ITEMS_TO_PROCESS", "MIN_SLEEP_CONSUMER", "MIN_SLEEP_PRODUCER", "QUEUE_SIZE", "time"]

    #####
    # Cambiar estos valores para hacer experimentos individuales
    print("## Experimento aislado ##")
    i = 0
    measurements = dict()
    ITEMS_TO_PROCESS = 1e2
    QUEUE_SIZE = 10
    MIN_SLEEP_CONSUMER, MAX_SLEEP_CONSUMER = 250, 500
    MIN_SLEEP_PRODUCER, MAX_SLEEP_PRODUCER = 250, 500
    NUM_CONSUMERS, NUM_PRODUCERS = 5, 5
    run_experiment()
    print("")
    print(pandas.DataFrame(measurements))
    print("######\n")

    OUTPUT = False  # Se desactiva porque a partir de ahora trabajaremos con muchos items

    ###
    # print("## EXP 1 --> Efecto del ratio de productores y consumidores ##")
    # i = 0
    # measurements = dict()
    # # Variables fijas
    # ITEMS_TO_PROCESS = 1e2
    # QUEUE_SIZE = 10
    # MIN_SLEEP_CONSUMER, MAX_SLEEP_CONSUMER = (250, 500)
    # MIN_SLEEP_PRODUCER, MAX_SLEEP_PRODUCER = (250, 500)
    # ##
    # # Variables a iterar usando los pares (tuples) de valores de la lista
    # for NUM_CONSUMERS, NUM_PRODUCERS in [(5, 5), (5, 10), (10, 5), (10, 10), (100, 100)]:
    #     run_experiment()
    # print("")
    # print(pretty_print_df(pandas.DataFrame(measurements), SEPARATORS))
    # print("######\n")
    ####

    ####
    # print("## EXP 2 --> Efecto de las esperas mínimas y máximas ##")
    # i = 0
    # measurements = dict()
    # # Variables fijas
    # ITEMS_TO_PROCESS = 2e2
    # QUEUE_SIZE = 10
    # NUM_CONSUMERS, NUM_PRODUCERS = 50, 50
    # ###
    # # Combinaciones de valores de 4 variables, 2 a 2 [4 combinaciones]
    # for MIN_SLEEP_CONSUMER, MAX_SLEEP_CONSUMER in [(250, 500), (500, 1000)]:
    #     for MIN_SLEEP_PRODUCER, MAX_SLEEP_PRODUCER in [(250, 500), (500, 1000)]:
    #         run_experiment()
    # print("")
    # print(pretty_print_df(pandas.DataFrame(measurements), SEPARATORS))
    # print("######\n")
    ####

    ###
    # print("## EXP 3 --> Efecto del tamaño de las colas ##")
    # i = 0
    # measurements = dict()
    # # Variables fijas
    # ITEMS_TO_PROCESS = 1e3
    # MIN_SLEEP_CONSUMER, MAX_SLEEP_CONSUMER = (250, 500)
    # MIN_SLEEP_PRODUCER, MAX_SLEEP_PRODUCER = (250, 500)
    # NUM_CONSUMERS, NUM_PRODUCERS = (50, 50)
    # ###
    # for QUEUE_SIZE in [1, 2, 10, 0]:
    #     run_experiment()
    # print("")
    # print(pretty_print_df(pandas.DataFrame(measurements), SEPARATORS))
    # print("######\n")
    ####

    ###
    # print("## EXP 4 --> Efecto del número de items a procesar ##")
    # i = 0
    # measurements = dict()
    # # Variables fijas
    # ITEMS_TO_PROCESS = 1e3
    # MIN_SLEEP_CONSUMER, MAX_SLEEP_CONSUMER = (250, 500)
    # MIN_SLEEP_PRODUCER, MAX_SLEEP_PRODUCER = (250, 500)
    # NUM_CONSUMERS, NUM_PRODUCERS = (50, 50)
    # QUEUE_SIZE = 10
    # ###
    # for ITEMS_TO_PROCESS in [1e2, 2e2, 4e2]:
    #     run_experiment()
    # print("")
    # print(pretty_print_df(pandas.DataFrame(measurements), SEPARATORS))
    # print("######\n")
    ####