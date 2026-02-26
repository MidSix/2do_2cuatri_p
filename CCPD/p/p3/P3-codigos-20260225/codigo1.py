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

import os
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import Process, Manager, cpu_count, Queue

from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

global COUNT_STEP
global NUM_TASKS
global OUTPUT
global N_WORKERS_LIST
global COUNT_MAX
global COUNT_INI
global USE_PROCESSES
global USE_THREADS


def to_time_miliseconds(start, end):
    return int(1000 * (end - start))


def output_print(string):
    if OUTPUT:
        print(string)


def sci_not_str(num):
    if type(num) != int:
        return "{:1.2e}".format(num)
    else:
        return "{:1.0e}".format(num).replace("+0", "")


def evaluate_item(number, count):
    y = 0
    for i in range(0, count):
        y = y + int((y * 5.5) / 1e8) + i % (number + 10)  # Operación que usa suma, mult, div y módulo
    return y


def print_as_pandas_df(measurements):
    print("TIMES (ms):")
    print(pd.DataFrame(measurements))
    print("\n")


def plot(measurements, experiment_label):
    if not os.path.exists(experiment_label):
        os.mkdir(experiment_label)

    df = pd.DataFrame(measurements)
    df.plot(kind='bar', title="Time in miliseconds")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('{0}/{1}.png'.format(experiment_label, "ALL"))
    plt.close()

    # for config in measurements:
    #     df[config].plot(kind='bar', title="Time in milliseconds for {0}".format(config))
    #     plt.xticks(rotation=45)
    #     plt.tight_layout()
    #     plt.savefig('{0}/{1}.png'.format(experiment_label, config))
    #     plt.close()

    count = COUNT_INI
    while count <= COUNT_MAX:
        N = sci_not_str(count)
        df.loc[N, :].plot(kind='bar', title="Time in milliseconds for N={0}".format(N))
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('{0}/{1}.png'.format(experiment_label, sci_not_str(count)))
        plt.close()
        count = count * COUNT_STEP


def print_config():
    for param_name, param in [("OUTPUT", OUTPUT), ("NUM_LIST_LEN", NUM_TASKS), ("N_WORKERS_LIST", N_WORKERS_LIST),
                             ("COUNT_INI", sci_not_str(COUNT_INI)),  ("COUNT_MAX", sci_not_str(COUNT_MAX))]:
        print("{0: <15} -> {1}".format(param_name, str(param)))
    print("")


def run_experiment(measurements):
    tasks_list = [x for x in range(1, NUM_TASKS + 1)]
    count = COUNT_INI
    results = {}

    pools = []
    if USE_PROCESSES:
        pools.append((ProcessPoolExecutor, "PRO"))
    if USE_THREADS:
        pools.append((ThreadPoolExecutor, "THR"))

    while count <= COUNT_MAX:
        print("Going to benchmark {0}".format(count))
        with tqdm(total=len(pools) * len(N_WORKERS_LIST) + 1) as pbar:
            output_print("Benchmarking SEQ")
            start = time.time()
            result_items = list()
            for item in tasks_list:
                result_items.append(evaluate_item(item, count))
            end = time.time()
            results["SEQ"] = result_items

            if "SEQ" not in measurements:
                measurements["SEQ"] = dict()
            measurements["SEQ"][sci_not_str(count)] = to_time_miliseconds(start, end)
            pbar.update(1)

            for PoolType, PoolLabel in pools:
                for workers_num in N_WORKERS_LIST:
                    label = "{0}_{1}".format(PoolLabel, workers_num)
                    output_print("Benchmarking {0}".format(label))
                    if label not in measurements:
                        measurements[label] = dict()

                    start = time.time()
                    with PoolType(max_workers=workers_num) as executor:
                        futures = list()
                        for item in tasks_list:
                            futures.append(executor.submit(evaluate_item, item, count))
                        result_items = list()
                        for f in futures:
                            result_items.append(f.result())
                    end = time.time()
                    measurements[label][sci_not_str(count)] = to_time_miliseconds(start, end)
                    results[label] = result_items

                    pbar.update(1)

            count = count * COUNT_STEP
    print("")

    output_print("RESULTS:")
    for key in results:
        output_print("Resulting items of {0} are -> {1}".format(key, results[key]))
    output_print("")


def run_experiment_proc_per_process(measurements):
    def process_task(item, count, result_queue):
        result = evaluate_item(item, count)
        result_queue.put(result)

    tasks_list = [x for x in range(1, NUM_TASKS + 1)]
    count = COUNT_INI
    results = {}
    while count <= COUNT_MAX:
        print("Going to benchmark {0}".format(count))
        with tqdm(total=len(N_WORKERS_LIST)) as pbar:
            for workers_num in N_WORKERS_LIST:
                label = "PRO_per_task_{0}".format(workers_num)
                output_print("Benchmarking {0}".format(label))
                if label not in measurements:
                    measurements[label] = dict()

                start = time.time()
                result_items = []

                # Split the tasks list into batches based on the workers_num
                for i in range(0, len(tasks_list), workers_num):
                    batch = tasks_list[i:i + workers_num]
                    result_queue = Queue()

                    # Start processes for each item in the batch
                    processes = []
                    for item in batch:
                        p = Process(target=process_task, args=(item, count, result_queue))
                        processes.append(p)
                        p.start()

                    # Wait for all processes in the batch to finish
                    for p in processes:
                        p.join()

                    # Retrieve results from the queue
                    while not result_queue.empty():
                        result_items.append(result_queue.get())

                end = time.time()
                measurements[label][sci_not_str(count)] = to_time_miliseconds(start, end)
                results[label] = result_items

                pbar.update(1)

            count = count * COUNT_STEP
    print("")

    output_print("RESULTS:")
    for key in results:
        output_print("Resulting items of {0} are -> {1}".format(key, results[key]))
    output_print("")


if __name__ == "__main__":
    COUNT_STEP = 10

    USE_PROCESSES = True
    USE_THREADS = True
    OUTPUT = True

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    print("VALIDITY TEST")
    print("@@@@@@@@@@@@@@@@\n")
    N_WORKERS_LIST = [2, 4]
    NUM_TASKS = 5
    COUNT_INI, COUNT_MAX = int(1e3), int(1e4)
    print_config()
    measurements, experiment_label = dict(), "vailidity_test"
    try:
        run_experiment(measurements)
        run_experiment_proc_per_process(measurements)
    except KeyboardInterrupt:
        pass
    print_as_pandas_df(measurements)
    print("-" * 30 + "\n")
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # NUM_TASKS = 2000
    # USE_THREADS = False
    # OUTPUT = False
    # print("EFFECT OF PROCESS CREATION/DESTRUCTION WITH {0} TASKS".format(NUM_TASKS))
    # print("@@@@@@@@@@@@@@@@\n")
    # N_WORKERS_LIST = [2, 4, 8]
    # COUNT_INI, COUNT_MAX = int(1e1), int(1e3)
    # print_config()
    # measurements, experiment_label = dict(), "process_management"
    # try:
    #     run_experiment(measurements)
    #     run_experiment_proc_per_process(measurements)
    # except KeyboardInterrupt:
    #     pass
    # print_as_pandas_df(measurements)
    # plot(measurements, experiment_label)
    # print("-" * 30 + "\n")
    # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    #
    # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # print("EFFECT OF GIL")
    # print("@@@@@@@@@@@@@@@@\n")
    # N_WORKERS_LIST = [2, 4, 6, 8]
    # NUM_TASKS = 32
    # USE_THREADS = True
    # OUTPUT = False
    # COUNT_INI, COUNT_MAX = int(1e3), int(1e6)
    # print_config()
    # measurements, experiment_label = dict(), "gil_effect"
    # try:
    #     run_experiment(measurements)
    # except KeyboardInterrupt:
    #     pass
    # print_as_pandas_df(measurements)
    # plot(measurements, experiment_label)
    # print("-" * 30 + "\n")
    # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # NUM_TASKS = 4
    # N_WORKERS_LIST = [2, 3, 4, 5, 6]
    # print("NUM TASKS ({0}) SMALLER THAN POOL ({1})".format(NUM_TASKS, max(N_WORKERS_LIST)))
    # print("@@@@@@@@@@@@@@@@\n")
    # USE_THREADS = False
    # OUTPUT = False
    # COUNT_INI, COUNT_MAX = int(1e3), int(1e7)
    # print_config()
    # measurements, experiment_label = dict(), "data_smaller_pool"
    # try:
    #     run_experiment(measurements)
    # except KeyboardInterrupt:
    #     pass
    # print_as_pandas_df(measurements)
    # plot(measurements, experiment_label)
    # print("-" * 30 + "\n")
    # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # print("TRUE PARALLELISM")
    # print("@@@@@@@@@@@@@@@@\n")
    # USE_THREADS = False
    # OUTPUT = False
    # NUM_TASKS = 64  # For MR set 256
    # N_WORKERS_LIST = [2, 4, 8, 16, 24, 32, 64]  # For MR add 128, 256
    # COUNT_INI, COUNT_MAX = int(1e2), int(1e6)  # For MR increase to 1e7
    # print_config()
    # measurements, experiment_label = dict(), "true_parallelism"
    # try:
    #     run_experiment(measurements)
    # except KeyboardInterrupt:
    #     pass
    # print_as_pandas_df(measurements)
    # plot(measurements, experiment_label)
    # print("-" * 30 + "\n")
    # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
