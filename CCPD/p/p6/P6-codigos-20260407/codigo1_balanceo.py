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

import random
import time
from concurrent.futures.process import ProcessPoolExecutor
from auxiliar import get_chunks, to_time_miliseconds, sci_not_str, flatten_list_of_lists, validate

import pandas as pd
from tqdm import tqdm

pd.set_option('display.max_rows', 40)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

FUNCS = list()

N_REPEATS = 2e1


def is_prime(num):
    flag = False
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                flag = True
                break
    if flag:
        return False
    else:
        return True


def fun_cheap(items):
    start = time.time()
    results = list()
    for item in items:
        i = 0
        result = 0
        while i < N_REPEATS:
            revs_number = 0
            num = item
            while num > 0:
                remainder = num % 10
                revs_number = (revs_number * 10) + remainder
                num = num // 10
            i += 1
            result = (result + revs_number) % 7
        results.append(result)
    end = time.time()
    return results, to_time_miliseconds(start, end)


def fun_medium(items):
    start = time.time()
    results = list()
    for num in items:
        if is_prime(num):
            results.append(num)
    end = time.time()
    return results, to_time_miliseconds(start, end)


def fun_expensive(items):
    start = time.time()
    results = list()
    for item in items:
        if is_prime(item):
            revs_number = 0
            num = item
            while num > 0:
                remainder = num % 10
                revs_number = (revs_number * 10) + remainder
                num = num // 10
            if item == revs_number:
                results.append(item)
            if is_prime(revs_number):
                results.append(revs_number)
    end = time.time()
    return results, to_time_miliseconds(start, end)


def fun_par_unordered(data, proc_chunks, resultsPar):
    with ProcessPoolExecutor(max_workers=N_PROC) as executor:
        total_runtime = 0
        start = time.time()
        futures = list()
        for ini, end in proc_chunks:
            for fun in FUNCS:
                futures.append((fun.__name__, executor.submit(fun, data[ini:end])))

        for fun_name, f in futures:
            result, runtime = f.result()
            resultsPar[fun_name].append(result)
            total_runtime += runtime
        end = time.time()
        time_granted = N_PROC * to_time_miliseconds(start, end)
        time_efficiency = "{0} %".format(int(100 * (total_runtime / time_granted)))
    return resultsPar, time_efficiency


def chk_par_unordered(data, proc_chunks, resultsPar):
    with ProcessPoolExecutor(max_workers=N_PROC) as executor:
        total_runtime = 0
        start = time.time()
        futures = list()
        for fun in FUNCS:
            for ini, end in proc_chunks:
                futures.append((fun.__name__, executor.submit(fun, data[ini:end])))

        for fun_name, f in futures:
            result, runtime = f.result()
            resultsPar[fun_name].append(result)
            total_runtime += runtime
        end = time.time()
        time_granted = N_PROC * to_time_miliseconds(start, end)
        time_efficiency = "{0} %".format(int(100 * (total_runtime / time_granted)))
    return resultsPar, time_efficiency


def fun_par_ordered(data, proc_chunks, resultsPar):
    with ProcessPoolExecutor(max_workers=N_PROC) as executor:
        total_runtime = 0
        start = time.time()
        for ini, end in proc_chunks:
            futures = list()
            for fun in FUNCS:
                futures.append((fun.__name__, executor.submit(fun, data[ini:end])))

            for fun_name, f in futures:
                result, runtime = f.result()
                resultsPar[fun_name].append(result)
                total_runtime += runtime
        end = time.time()
        time_granted = N_PROC * to_time_miliseconds(start, end)
        time_efficiency = "{0} %".format(int(100 * (total_runtime / time_granted)))
    return resultsPar, time_efficiency


def chk_par_ordered(data, proc_chunks, resultsPar):
    with ProcessPoolExecutor(max_workers=N_PROC) as executor:
        total_runtime = 0
        start = time.time()
        for fun in FUNCS:
            futures = list()
            for ini, end in proc_chunks:
                futures.append((fun.__name__, executor.submit(fun, data[ini:end])))

            for fun_name, f in futures:
                result, runtime = f.result()
                resultsPar[fun_name].append(result)
                total_runtime += runtime
        end = time.time()
        time_granted = N_PROC * to_time_miliseconds(start, end)
        time_efficiency = "{0} %".format(int(100 * (total_runtime / time_granted)))
    return resultsPar, time_efficiency


def parallel_processing(data, parallel_funct):
    resultsPar = dict()
    for fun in FUNCS:
        resultsPar[fun.__name__] = list()

    proc_chunks = get_chunks(len(data), NUM_CHUNKS)

    resultsPar, time_efficiency = parallel_funct(data, proc_chunks, resultsPar)

    for k in resultsPar:
        resultsPar[k] = flatten_list_of_lists(resultsPar[k])
        resultsPar[k].sort()
    return resultsPar, time_efficiency


def save_config():
    d = dict()
    d["N_FUNCS"] = len(FUNCS)
    d["N_CHUNKS"] = NUM_CHUNKS
    d["N_PROC"] = N_PROC
    return d


def get_data_ranged(min, max):
    #Compresion de listas para generar una lista con los números entre min y max
    return [x for x in range(int(min), int(max))]


def pretty_print_df(df, split_strings):
    df_string = df.to_string()
    num_dashes = 102
    for split in split_strings:
        df_string = df_string.replace("\n{0}".format(split), '\n' + '-' * num_dashes + "\n{0}".format(split))
    return df_string


ALL_FUNCS = [fun_cheap, fun_medium, fun_expensive]
ALL_EXPENSIVE_FUNCS = [fun_expensive, fun_expensive, fun_expensive, fun_expensive]


def experiment():
    global NUM_CHUNKS, N_PROC, FUNCS
    print("RUNNING EXPERIMENTS WITH {0} FUNCTIONS: {1}".format(len(FUNCS), [f.__name__ for f in FUNCS]))

    data = get_data_ranged(int(N_BASE), int(N_BASE) + N_LEN)

    print("####### N = {0} (from {1} to {2}) #######\n".format(int(N_LEN), int(N_BASE), int(N_BASE + N_LEN)))

    print("Running sequentially")
    resultsSeq = dict()
    sstart = time.time()
    for fun in FUNCS:
        if fun.__name__ not in resultsSeq:
            resultsSeq[fun.__name__] = list()
        result, runtime = fun(data)
        resultsSeq[fun.__name__].append(result)
        print("Function {0} finished after {1} ms".format(fun.__name__, runtime))
    for k in resultsSeq:
        resultsSeq[k] = flatten_list_of_lists(resultsSeq[k])
        resultsSeq[k].sort()
    eend = time.time()
    print("SEQ execution took {0} ms".format(to_time_miliseconds(sstart, eend)))
    print("-" * 40)
    print("\n")

    print("Running parallel arrangements")
    all_measurements = list()
    all_efficiencies = list()
    with tqdm(total=len(NUM_CHUNKS_OPTS) * len(N_PROC_OPTS) * 4) as pbar:
        for NUM_CHUNKS in NUM_CHUNKS_OPTS:
            for N_PROC in N_PROC_OPTS:
                times = save_config()
                times_efficiency = save_config()
                for par_fun in [chk_par_ordered, fun_par_ordered, chk_par_unordered, fun_par_unordered]:
                    start = time.time()
                    resultsPar, t_efficiency = parallel_processing(data, par_fun)
                    for k in resultsSeq:
                        if not validate(resultsSeq[k], resultsPar[k]):
                            print("!!!! RESULTS NOT EQUAL for {0} !!!!".format(par_fun.__name__))
                            break
                    end = time.time()
                    times[par_fun.__name__] = to_time_miliseconds(start, end)
                    times_efficiency[par_fun.__name__] = t_efficiency
                    pbar.update(1)
                all_measurements.append(times)
                all_efficiencies.append(times_efficiency)
    print("\n")

    print("~" * 40)
    print("|" + " " * 7 + "Parallel times (ms)" + " " * 12 + "|")
    print("~" * 102)
    print(pretty_print_df(pd.DataFrame(all_measurements), [i * len(N_PROC_OPTS) for i in range(0, len(NUM_CHUNKS_OPTS))]))
    print("~" * 102)
    print("\n")

    print("~" * 45)
    print("|" + " " * 5 + "Parallel % of time in execution" + " " * 7 + "|")
    print("~" * 102)
    print(pretty_print_df(pd.DataFrame(all_efficiencies), [i * len(N_PROC_OPTS) for i in range(0, len(NUM_CHUNKS_OPTS))]))
    print("~" * 102)
    print("\n")


if __name__ == '__main__':
    global NUM_CHUNKS, N_PROC

    # N_BASE, N_LEN = (1e5, 3000)
    # NUM_CHUNKS_OPTS = [4, 10, 20, 80]
    # N_PROC_OPTS = [2, 3, 4, 8, 12, 16]

    N_BASE, N_LEN = (1e2, 3000)
    NUM_CHUNKS_OPTS = [4, 20]
    N_PROC_OPTS = [2, 3, 4]

    FUNCS = ALL_FUNCS
    experiment()

    FUNCS = ALL_EXPENSIVE_FUNCS
    experiment()
