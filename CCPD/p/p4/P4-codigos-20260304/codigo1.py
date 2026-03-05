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

import numpy as np
import time
import sys
from multiprocessing import Pool
import os, psutil
import gc
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt

N_ITERS = 15

RESULTS_FOLDER = "results_codigo1"


def sci_not_str(num):
    if type(num) != int:
        return "{:1.2e}".format(num)
    else:
        return "{:1.0e}".format(num).replace("+0", "")


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


def process_chunk_list(chunk, a, b):
    ini, end = chunk
    result_final = list()

    result1 = [x * y for x, y in zip(a[ini:end], b[ini:end])]  # OP 1
    number_mask = [7] * len(result1)  # OP 2

    for i in range(0, N_ITERS):
        result1 = [x * y for x, y in zip(a[ini:end], b[ini:end])]  # OP 3
        result2 = [x + y for x, y in zip(a[ini:end], b[ini:end])]  # OP 4
        result3 = [x / y for x, y in zip(a[ini:end], b[ini:end])]  # OP 5
        result4 = [x // y for x, y in zip(a[ini:end], b[ini:end])]  # OP 6
        result_final = result1 + result2  # OP 7
        result_final = result_final + result3  # OP 8
        result_final = result_final + result4  # OP 9
        mask = [multiplication_is_even(x, y) for x, y in zip(result_final, number_mask)]  # OP 10
        result_final = [make_even_if_not(x, y) for x, y in zip(result_final, mask)]  # OP 11
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


def process_parallel(n, x1, x2, n_proc=2, funct=process_chunk_list):
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


def read_memory_usage():
    time.sleep(2)  # Allow time for any previous garballe collection or deletion to take place
    total_memory, used_memory, free_memory = map(
        int, os.popen('free -t -m').readlines()[-1].split()[1:])

    process = psutil.Process(os.getpid())
    print("RAM memory used: {0} MiB ({1}%)".format(
        to_mebibytes_int(process.memory_info().rss), round((used_memory / total_memory) * 100, 2)))


def validate(*args):
    length = len(args[0])
    for res in args[1:]:
        if len(res) != length:
            return False

    length = len(args[0])
    for i in range(0, length):
        value = args[0][i]
        for res in args[1:]:
            if value != res[i]:
                return False
                
    return True


def remove(*args):
    for var in args:
        del var
    gc.collect()
    read_memory_usage()


def plot(df, label, file_label):
    df.filter(like=label, axis=0).plot(kind='bar')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('{0}/{1}.png'.format(RESULTS_FOLDER, file_label))


def experiment(measurements):
    print("Max size of lists or arrays is {0}".format(N_MAX))
    print("Generating the lists data")
    start = time.time()
    A = [*range(1, N_MAX + 1)]  # [random.randint(1, 100) for _ in range(n_max)]
    B = [*range(1, N_MAX + 1)]  # [random.randint(1, 100) for _ in range(n_max)]
    end = time.time()
    print("Generation of the data took {0:,.4f} seconds".format(end - start))
    print("Size of a is: {0:3d} MiB".format(to_mebibytes_int(sys.getsizeof(A))))
    print("Size of b is: {0:3d} MiB".format(to_mebibytes_int(sys.getsizeof(B))))
    read_memory_usage()

    # Initialize measurements dictionary
    n = N_INI
    while n <= N_MAX:
        measurements[sci_not_str(n)] = dict()
        if n == N_MAX:
            break
        n = min(n * 10, N_MAX)
    num_loops = len(measurements.keys())

    print("Going to compute now for the lists")
    n = N_INI
    with tqdm(total=num_loops * (1 + len(N_PARALLELISM))) as pbar:
        while n <= N_MAX:
            sub_a = A[:n]
            sub_b = B[:n]
            print("Size of sub_a is: {0:3d} MiB".format(to_mebibytes_int(sys.getsizeof(sub_a))))
            print("Size of sub_b is: {0:3d} MiB".format(to_mebibytes_int(sys.getsizeof(sub_b))))

            start = time.time()
            resSEQ_LIST = process_chunk_list((0, n), sub_a, sub_b)
            end = time.time()
            measurements[sci_not_str(n)]["SEQ LIST"] = to_time_miliseconds(start, end)
            pbar.update(1)

            for n_processes in N_PARALLELISM:
                start = time.time()
                resPAR_LIST = process_parallel(n, sub_a, sub_b, n_processes, process_chunk_list)
                end = time.time()
                measurements[sci_not_str(n)]["{0}x LIST".format(n_processes)] = to_time_miliseconds(start, end)
                pbar.update(1)

            # Validation
            if not validate(resSEQ_LIST, resPAR_LIST):
                print("!!!! RESULTS NOT EQUAL !!!!")

            if n == N_MAX:
                break
            n = min(n * 10, N_MAX)
            print("N: {0}".format(sci_not_str(n)))
            read_memory_usage()
            remove(sub_a, sub_b)

    print("Removing result lists")
    remove(resSEQ_LIST, resPAR_LIST, sub_a, sub_b)

    print("Removing original lists")
    remove(A, B)

    print("Generating the array data")
    start = time.time()
    ax = np.arange(1, N_MAX + 1, 1)
    bx = np.arange(1, N_MAX + 1, 1)
    end = time.time()
    print("Generation of the data took {0:,.4f} seconds".format(end - start))
    print("Size of ax is: {0:3d} MiB".format(to_mebibytes_int(sys.getsizeof(ax))))
    print("Size of bx is: {0:3d} MiB".format(to_mebibytes_int(sys.getsizeof(bx))))
    read_memory_usage()

    print("Going to compute now for arrays")
    n = N_INI
    with tqdm(total=num_loops * (1 + len(N_PARALLELISM))) as pbar:
        while n <= N_MAX:
            sub_ax = ax[:n]
            sub_bx = bx[:n]

            start = time.time()
            resSEQ_VEC = process_chunk_array((0, n), sub_ax, sub_bx)
            end = time.time()
            measurements[sci_not_str(n)]["SEQ VEC"] = to_time_miliseconds(start, end)
            pbar.update(1)

            for n_processes in N_PARALLELISM:
                start = time.time()
                resPAR_VEC = process_parallel(n, sub_ax, sub_bx, n_processes, process_chunk_array)
                end = time.time()
                measurements[sci_not_str(n)]["{0}x VEC".format(n_processes)] = to_time_miliseconds(start, end)
                pbar.update(1)

            # Validation
            if not validate(resSEQ_VEC, resPAR_VEC):
                print("!!!! RESULTS NOT EQUAL !!!!")

            if n == N_MAX:
                break
            n = min(n * 10, N_MAX)
            print("N: {0}".format(sci_not_str(n)))


    print("Removing result arrays")
    remove(resSEQ_VEC, resPAR_VEC)

    print("Removing original arrays")
    remove(ax, bx)


if __name__ == "__main__":

    #####################
    ## ESTO EN LOCAL
    #####################
    measurements = dict()
    N_PARALLELISM = [2, 4, 8, 16]
    N_INI = int(1e3)
    N_MAX = int(1e4) # No excedas 5e6 si no tienes más de 8 GiB de RAM
    try:
        experiment(measurements)
    except KeyboardInterrupt:
        pass
    df = pd.DataFrame(measurements)
    print(df)

    #####################
    ## ESTO SOLO EN LA MR
    #####################
    # measurements = dict()
    # N_PARALLELISM = [2, 4, 8, 12, 16, 24, 32, 64, 128]
    # N_INI = int(1e4)
    # N_MAX = int(1e7)
    # experiment(measurements)
    # df = pd.DataFrame(measurements)
    # print(df)

    os.makedirs(RESULTS_FOLDER, exist_ok=True)
    plot(df, "SEQ", "SEQ")
    plot(df, "VEC", "ALL_VEC")
    plot(df, "LIST", "ALL_LIST")

