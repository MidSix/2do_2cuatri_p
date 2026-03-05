#! /usr/bin/python
#
# Copyright © 2024 by Jonatan Enes (jonatan.enes@udc.es)
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

import math

import numpy as np
import time
import sys
from multiprocessing import Pool
import gc

N_MAX_LIMIT = 1e9 # No tocar
N_ITERS = 15
SOURCE_DATA = "file"
PENALIZE_INPUT_TIME = 0.05
MODULE = int(1e3)

GENERATION = 0
COMPUTATION = 0
TOTAL = 0


def to_mebibytes_int(n):
    return int(n / (1024 * 1024))


def to_time_miliseconds(start, end):
    return int(1000 * (end - start))


def get_chunks(n, n_proc):
    chunksize = n // n_proc
    proc_chunks = []
    for i_proc in range(n_proc):
        chunkstart = i_proc * chunksize
        if i_proc < n_proc - 1:
            chunkend = (i_proc + 1) * chunksize
        else:
            chunkend = n
        proc_chunks.append((chunkstart, chunkend))
    return proc_chunks


def multiplication_is_even(a, b):
    if (a * b % 2) == 0:
        return True
    else:
        return False


def make_even_if_not(a, mask):
    if mask:
        return a + 1
    else:
        return a


def add_one(a):
    return a + 1


def sci_not_str(num):
    if type(num) != int:
        return "{:1.2e}".format(num)
    else:
        return "{:1.0e}".format(num).replace("+0", "")


def process_chunk_list(chunk, a, b):
    ini, end = chunk

    result1 = [x * y for x, y in zip(a[ini:end], b[ini:end])]
    number_mask = [7] * len(result1)

    for i in range(0, N_ITERS):
        result1 = [x * y for x, y in zip(a[ini:end], b[ini:end])]
        result2 = [x + y for x, y in zip(a[ini:end], b[ini:end])]
        result3 = [x / y for x, y in zip(a[ini:end], b[ini:end])]
        result4 = [x // y for x, y in zip(a[ini:end], b[ini:end])]
        result_final = result1 + result2
        result_final = result_final + result3
        result_final = result_final + result4
        mask = [multiplication_is_even(x, y) for x, y in zip(result_final, number_mask)]
        result_final = [make_even_if_not(x, y) for x, y in zip(result_final, mask)]
    return result_final


def process_chunk_array(chunk, ax, bx):
    ini, end = chunk
    vec_fun_mult = np.vectorize(multiplication_is_even)
    vec_fun_even = np.vectorize(make_even_if_not)

    result_final = ax[ini:end] * bx[ini:end]  # OP 1
    number_mask = np.ones(len(result_final)) * 7  # OP 2

    for i in range(0, N_ITERS):
        result1 = ax[ini:end] * bx[ini:end]  # OP 3
        result2 = ax[ini:end] + bx[ini:end]  # OP 4
        result3 = ax[ini:end] / bx[ini:end]  # OP 5
        result4 = ax[ini:end] // bx[ini:end]  # OP 6
        result_final = result1 + result2  # OP 7
        result_final = result_final + result3  # OP 8
        result_final = result_final + result4  # OP 9
        mask = vec_fun_mult(result_final, number_mask)  # OP 10
        result_final = vec_fun_even(result_final, mask)  # OP 11
    return result_final


def flatten_list_of_lists(l):
    # Read this like "for each sublist in l, give sublist, and for each item in sublist, give item"
    return [item for sublist in l for item in sublist]


def flatten_list_of_arrays(l):
    return np.concatenate(l)


def process_parallel_optimized(n, x1, x2, n_proc=2, funct=process_chunk_list):
    proc_chunks = get_chunks(n, n_proc)
    with Pool(processes=n_proc) as pool:
        data_chunks = list()
        for chunk in proc_chunks:
            ini, end = chunk
            data_chunks.append(((0, end - ini), x1[ini:end], x2[ini:end]))

        proc_results = [pool.apply_async(funct, args=chunk) for chunk in data_chunks]

        # blocks until all results are fetched
        result_chunks = [r.get() for r in proc_results]
        if funct == process_chunk_list:
            return flatten_list_of_lists(result_chunks)
        if funct == process_chunk_array:
            return flatten_list_of_arrays(result_chunks)


def process_parallel(n, x1, x2, n_proc=2, funct=process_chunk_list):
    proc_chunks = get_chunks(n, n_proc)
    with Pool(processes=n_proc) as pool:
        gc.collect()

        # starts the sub-processes without blocking
        # pass the chunk to each worker process
        proc_results = [pool.apply_async(funct, args=(chunk, x1, x2,)) for chunk in proc_chunks]

        # blocks until all results are fetched
        result_chunks = [r.get() for r in proc_results]

        if funct == process_chunk_list:
            return flatten_list_of_lists(result_chunks)
        if funct == process_chunk_array:
            return flatten_list_of_arrays(result_chunks)


def experiment_list():
    global GENERATION, COMPUTATION
    print("Max size of lists or arrays is {0}".format(sci_not_str(N_MAX)))
    start = time.time()
    if SOURCE_DATA == "gen":
        print("Generating the lists data")
        a = [*range(1, N_MAX + 1)]
        b = [*range(1, N_MAX + 1)]
    elif SOURCE_DATA == "file":
        print("Reading data from file")
        with open('a.txt', 'r') as filehandle:
            i, a = 0, list()
            for line in filehandle.readlines():
                a.append(int(line))
                i += 1
                if i >= N_MAX:
                    break
                if i % MODULE == 0:
                    time.sleep(PENALIZE_INPUT_TIME)
        with open('b.txt', 'r') as filehandle:
            i, b = 0, list()
            for line in filehandle.readlines():
                b.append(int(line))
                i += 1
                if i >= N_MAX:
                    break
                if i % MODULE == 0:
                    time.sleep(PENALIZE_INPUT_TIME)
    end = time.time()
    GENERATION = end - start
    print("Generation of the data took {0:,.4f} seconds".format(end - start))
    print("Size of a is: {0:3d} MiB".format(to_mebibytes_int(sys.getsizeof(a))))
    print("Size of b is: {0:3d} MiB".format(to_mebibytes_int(sys.getsizeof(b))))

    start = time.time()
    if PARALLELISM_OPT == "seq":
        process_chunk_list((0, N_MAX), a, b)
    else:
        process_parallel_optimized(N_MAX, a, b, PARALLELISM_DEGREE, process_chunk_list)
    end = time.time()
    COMPUTATION = end - start
    print("Computation took {0:,.4f} seconds".format(end - start))


def experiment_vect():
    global GENERATION, COMPUTATION
    print("Max size of lists or arrays is {0}".format(sci_not_str(N_MAX)))
    start = time.time()
    if SOURCE_DATA == "gen":
        print("Generating the array data")
        ax = np.arange(1, N_MAX + 1, 1)
        bx = np.arange(1, N_MAX + 1, 1)
    elif SOURCE_DATA == "file":
        print("Reading data from file")
        with open('a.txt', 'r') as filehandle:
            i, ax = 0, list()
            for line in filehandle.readlines():
                ax.append(int(line))
                i += 1
                if i >= N_MAX:
                    break
                if i % MODULE == 0:
                    time.sleep(PENALIZE_INPUT_TIME)
        with open('b.txt', 'r') as filehandle:
            i, bx = 0, list()
            for line in filehandle.readlines():
                bx.append(int(line))
                i += 1
                if i >= N_MAX:
                    break
                if i % MODULE == 0:
                    time.sleep(PENALIZE_INPUT_TIME)
        ax = np.array(ax)
        bx = np.array(bx)
    end = time.time()
    GENERATION = end - start
    print("Generation of the data took {0:,.4f} seconds".format(end - start))
    print("Size of ax is: {0:3d} MiB".format(to_mebibytes_int(sys.getsizeof(ax))))
    print("Size of bx is: {0:3d} MiB".format(to_mebibytes_int(sys.getsizeof(bx))))

    start = time.time()
    if PARALLELISM_OPT == "seq":
        process_chunk_array((0, N_MAX), ax, bx)
    else:
        process_parallel_optimized(N_MAX, ax, bx, PARALLELISM_DEGREE, process_chunk_array)
    end = time.time()
    COMPUTATION = end - start
    print("Computation took {0:,.4f} seconds".format(end - start))


if __name__ == "__main__":
    start = time.time()

    if len(sys.argv) < 6:
        print("Parameters are lacking, 4 parameters are needed in the next order")
        print("+ datatype [list/vec]")
        print("+ parallelism option [par/sec]")
        print("+ parallelism degree (a number, if seq then it will be ignored")
        print("+ Lenght of data in scientific notation (e.g. 3 -> 1e3)")
        print("+ Source of data generation [file/gen]")
        exit(1)

    DATATYPE = sys.argv[1]  # list/vec
    PARALLELISM_OPT = sys.argv[2]  # par/seq
    PARALLELISM_DEGREE = sys.argv[3]  # num
    N_MAX = int(float(sys.argv[4]))  # num
    SOURCE_DATA = sys.argv[5]

    PENALIZE_INPUT_TIME = 0.05

    measurements = dict()

    if N_MAX > N_MAX_LIMIT:
        print("N_MAX is higher than the limit {0}".format(N_MAX_LIMIT))
        exit(1)
    else:
        #MODULE = int(math.pow(10, int(N_MAX) - 1) / 8)
        MODULE = N_MAX / 80
        #N_MAX = int(math.pow(10, int(N_MAX)))
        print("N_MAX is {0}".format(sci_not_str(N_MAX)))
        print("MODULE is  {0}".format(MODULE))

    if PARALLELISM_OPT == "par":
        PARALLELISM_DEGREE = int(PARALLELISM_DEGREE)
        print("Running in parallel with a degree of {0}x".format(PARALLELISM_DEGREE))
    elif PARALLELISM_OPT == "seq":
        print("Running sequentially")
        PARALLELISM_DEGREE = None
    else:
        print("Type of parallelism '{0}' not recognized, use either 'par' or 'seq'".format(PARALLELISM_OPT))
        exit(1)

    if SOURCE_DATA == "gen":
        print("Data will come from internal generation")
    elif SOURCE_DATA == "file":
        print("Data will come from file")
    else:
        print("Data source not recognized, use either 'file' or 'gen'")
        exit(1)

    if DATATYPE == "list":
        print("Running lists")
        experiment_list()
    elif DATATYPE == "vec":
        print("Running vectors")
        experiment_vect()
    else:
        print("Data type not recognized, use either 'list' or 'vec'")
        exit(1)
    end = time.time()
    TOTAL = end - start
    print("Program execution took {0:,.4f} seconds".format(end - start))
    execution_label = "{0}_{1}_{2}_{3}".format(PARALLELISM_OPT, PARALLELISM_DEGREE, DATATYPE, SOURCE_DATA)
    print("DATA|{0};{1:,.2f};{2:,.2f};{3:,.2f}".format(execution_label, GENERATION, COMPUTATION, TOTAL))
