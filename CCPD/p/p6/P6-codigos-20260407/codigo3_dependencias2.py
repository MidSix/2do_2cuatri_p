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
from concurrent.futures.process import ProcessPoolExecutor
from auxiliar import get_chunks, to_time_miliseconds, sci_not_str, flatten_list_of_lists, validate
import pandas as pd

pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

N_PROC = 4
DEBUG = True


def parallel(data, seed_ini, seed_end):
    resultsPar = data
    print("Executing with {0} procs".format(NUM_PROCS))

    orig_seed_ini = seed_ini
    orig_seed_end = seed_end

    proc_chunks = get_chunks(len(resultsPar), NUM_PROCS)

    if DEBUG:
        print("\nxxxxxxxx DATOS [SPLITTED] in {0} xxxxxxxxx".format(NUM_PROCS))
        for (ini, end) in proc_chunks:
            print("{0}".format(["{0:2d}".format(n) for n in data[ini:end]]))
        print("-----------------------\n")

    with ProcessPoolExecutor(max_workers=NUM_PROCS) as executor:
        i = 0
        while i < N_REPEATS:
            futures = list()
            boundaries = list()
            # 1st iteration
            boundaries.append((orig_seed_ini, resultsPar[proc_chunks[0][1]]))

            # Medium iterations
            for ini, end in proc_chunks[1:-1]:
                boundaries.append((resultsPar[ini - 1], resultsPar[end]))

            # Last iteration
            boundaries.append((resultsPar[proc_chunks[-1][0] - 1], orig_seed_end))

            for (ini, end), (seed_ini, seed_end) in zip(proc_chunks, boundaries):
                futures.append(executor.submit(sequential, resultsPar[ini:end], seed_ini, seed_end))

            resultsPar = list()
            for f in futures:
                resultsPar.append(f.result())
            resultsPar = flatten_list_of_lists(resultsPar)

            if DEBUG:
                print("------ RESULTADOS ({1}) - SPLITTED in {0} ----------".format(NUM_PROCS, i))
                for (ini, end) in proc_chunks:
                    print("{0}".format(["{0:2d}".format(n) for n in resultsPar[ini:end]]))
                print("-----------------------\n")

            i += 1
    return resultsPar


def fun(prev_n, num, next_n):
    res = (prev_n + num + next_n) % 100
    return res


def sequential(data, seed_ini, seed_end):
    results = list()

    # 1st iteration
    previous_num = seed_ini
    n = data[0]
    next_num = data[1]
    results.append(fun(previous_num, n, next_num))

    # Medium iterations
    for i in range(1, len(data) - 1):
        previous_num = n
        n = data[i]
        next_num = data[i + 1]
        res = fun(previous_num, n, next_num)
        results.append(res)

    # Last iteration
    previous_num = n
    n = data[-1]
    next_num = seed_end
    results.append(fun(previous_num, n, next_num))

    return results


def experiment():
    data = [x for x in range(int(N_MIN), int(N_MAX))]
    print("-> N = {0} (from {1} to {2})\n".format(int(N_MAX - N_MIN), sci_not_str(int(N_MIN)), int(N_MAX)))
    start = time.time()
    resultsSeq = data

    print("Running sequentially")
    SEED_1, SEED_2 = 3, 7
    if DEBUG:
        print("\nxxxxxxxx DATOS xxxxxxxxx")
        print("{0}".format(["{0:2d}".format(n) for n in data]))
        print("")

    i = 0
    while i < N_REPEATS:
        resultsSeq = sequential(resultsSeq, SEED_1, SEED_2)
        if DEBUG:
            print("------ RESULTADO ({0}) ----------".format(i))
            print("{0}".format(["{0:2d}".format(n) for n in resultsSeq]))
            print("-----------------------\n")
        i += 1
    end = time.time()
    time_seq = to_time_miliseconds(start, end)
    print("Sequential execution took {0} ms, sum of results is {1}\n".format(time_seq, sum(resultsSeq)))

    print("Running in parallel with {0} processes".format(NUM_PROCS))
    start = time.time()
    resultsPar = parallel(data, SEED_1, SEED_2)
    end = time.time()
    time_par = to_time_miliseconds(start, end)
    print("Parallel execution took {0} ms, sum of results is {1}\n".format(time_par, sum(resultsPar)))

    print("Speedup is {0:2f}".format(time_seq/time_par))

    valid, message = validate(resultsSeq, resultsPar)
    if not valid:
        print("Results ARE NOT equal")
        print(message)
    else:
        print("Results ARE equal\n\n")


if __name__ == '__main__':
    N_MIN, N_MAX = 1e1, 5e1
    N_REPEATS = 2
    NUM_PROCS = 4
    DEBUG = True
    print("####### VALIDATION EXPERIMENT")
    experiment()

    N_MIN, N_MAX = 1e1, 5e6
    N_REPEATS = 400
    NUM_PROCS = 8
    DEBUG = False
    print("####### PERFORMANCE EXPERIMENT")
    experiment()
