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

import multiprocessing
import time
import concurrent.futures

import pandas as pd

pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

BATCH_SIZE = 200

FIRST_100_PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
POOL_WORKERS = 4

EXECUTOR_POOL_CLASS = concurrent.futures.ProcessPoolExecutor

# TIME_IN = "s"
TIME_IN = "ms"


def to_time(start, end):
    if TIME_IN == "s":
        return int(end - start)
    elif TIME_IN == "ms":
        return int(1000 * (end - start))
    else:
        return int(end - start)


def multiply_items(item):
    return item * item


def filter_evens(item):
    if (item % 2) != 0:
        return item


def is_prime(num):
    flag = False
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                flag = True
                break
    if flag:
        return None
    else:
        return num


def checksum(num):
    acum = 1
    for i in range(2, num):
        acum *= i
        acum = acum % 100 + 1
    return acum


def filter_divisible_by(item):
    for prime in FIRST_100_PRIMES:
        if (item % prime) == 0:
            return None
    return item


def is_emirp(number):
    revs_number = 0
    num = number
    # reverse the integer number using the while loop
    while num > 0:
        # Logic
        remainder = num % 10
        revs_number = (revs_number * 10) + remainder
        num = num // 10
    if number == revs_number:
        return None
    elif is_prime(revs_number):
        return number
    else:
        return None


def queue_generator(queue_out, data, measurements):
    start = time.time()
    for item in data:
        queue_out.put(item)
    end = time.time()
    queue_out.put("END")
    measurements["producer"] = to_time(start, end)


def coalesce(func, items):
    results = list()
    for i in items:
        results.append(func(i))
    return results


def queue_stage_parallel(queue_in, queue_out, funct, measurements):
    global EXECUTOR_POOL_CLASS
    with EXECUTOR_POOL_CLASS(max_workers=POOL_WORKERS) as executor:
        start = time.time()
        finish = False
        while True:

            j = 0
            future_list = list()

            while j < POOL_WORKERS:
                i = 0
                item_list = list()
                while i < BATCH_SIZE:
                    item = queue_in.get()
                    if item == "END":
                        finish = True
                        break
                    else:
                        item_list.append(item)
                    i += 1

                future_list.append(executor.submit(coalesce, funct, item_list))
                j += 1
                if finish:
                    break

            for f in future_list:
                result = f.result()
                for r in result:
                    if r:
                        queue_out.put(r)

            if finish:
                queue_out.put("END")
                break
        end = time.time()
        measurements[funct.__name__] = to_time(start, end)


def queue_stage(queue_in, queue_out, funct, measurements):
    start = time.time()
    while True:
        item = queue_in.get()
        if item == "END":
            queue_out.put("END")
            break
        result = funct(item)
        if result:
            queue_out.put(result)
    end = time.time()
    measurements[funct.__name__] = to_time(start, end)


def queue_consumer(queue_in, measurements):
    i, j = 0, 0
    start = time.time()
    while True:
        item = queue_in.get()
        if item == "END":
            break
        i += item
        j += 1
    end = time.time()
    measurements["consumer"] = to_time(start, end)
    measurements["NUM_items"] = j
    measurements["SUM_items"] = i


def handle_processes(process_list):
    for p in process_list:
        p.start()
    for p in process_list:
        p.join()


def sequential_pipeline(all_measurements, functions_list):
    label = "SEQUENTIAL (loop)"
    start = time.time()
    i, j = 0, 0
    for item in data:
        for fun in functions_list:
            item = fun(item)
            if not item:
                break
        if not item:
            continue
        i += item
        j += 1
    end = time.time()
    all_measurements[label] = {"NUM_items": j, "SUM_items": i}
    all_measurements[label]["producer"] = 0
    for f in functions_list:
        all_measurements[label][f.__name__] = 0
    all_measurements[label]["consumer"] = 0
    all_measurements[label]["RUNTIME"] = to_time(start, end)


def construct_pipeline(queue_stage_type):
    manager = multiprocessing.Manager()
    measurements = manager.dict()

    process_list, queues_list = list(), list()
    q = multiprocessing.Queue(maxsize=QUEUE_SIZE)
    process_list.append(multiprocessing.Process(target=queue_generator, args=(q, data, measurements,)))
    queues_list.append(q)
    for fun in PIPELINE_FUNCS:
        q = multiprocessing.Queue(maxsize=QUEUE_SIZE)
        process_list.append(
            multiprocessing.Process(target=queue_stage_type, args=(queues_list[-1], q, fun, measurements,)))
        queues_list.append(q)
    process_list.append(multiprocessing.Process(target=queue_consumer, args=(queues_list[-1], measurements,)))
    return process_list, measurements


def parallel_pipeline(label, all_measurements, process_list, process_measurements):
    global EXECUTOR_POOL_CLASS
    start = time.time()
    handle_processes(process_list)
    end = time.time()
    process_measurements["RUNTIME"] = to_time(start, end)
    all_measurements[label] = process_measurements.copy()


def sequential(all_measurements):
    sequential_pipeline(all_measurements, PIPELINE_FUNCS)


def parallel(all_measurements):
    process_list, process_measurements = construct_pipeline(queue_stage)
    label = "SIMPLE PARALLEL"
    parallel_pipeline(label, all_measurements, process_list, process_measurements)


def parallel_multi(all_measurements):
    process_list, process_measurements = construct_pipeline(queue_stage_parallel)
    label = "MULTI PARALLEL ({0})".format(EXECUTOR_POOL_CLASS.__name__.replace("PoolExecutor", ""))
    parallel_pipeline(label, all_measurements, process_list, process_measurements)


def parallel_multi_threads(all_measurements):
    global EXECUTOR_POOL_CLASS
    EXECUTOR_POOL_CLASS = concurrent.futures.ThreadPoolExecutor
    parallel_multi(all_measurements)


def parallel_multi_process(all_measurements):
    global EXECUTOR_POOL_CLASS
    EXECUTOR_POOL_CLASS = concurrent.futures.ProcessPoolExecutor
    parallel_multi(all_measurements)


def run_pipeline_experiment(pipeline_configs, experiment_label):
    print("~~~~ CONFIG ~~~~")
    print("BATCH_SIZE: {0} || QUEUE_SIZE: {1} || POOL_WORKERS: {2} || NUMS: {3}".format(BATCH_SIZE, QUEUE_SIZE, POOL_WORKERS, sci_not_str(len(data))))
    print("~~~~ EXPERIMENT {0} ~~~~".format(experiment_label))
    all_measurements = dict()
    for pipeline in pipeline_configs:
        #print("Running: {0}".format(pipeline.__name__))
        pipeline(all_measurements)
        time.sleep(2)
    print("~~~~ RESULTS ~~~~")
    print(pretty_print_df(pd.DataFrame(all_measurements), ["NUM_items", "producer", "RUNTIME"]))
    print("")


def sci_not_str(num):
    if type(num) != int:
        return "{:1.2e}".format(num)
    else:
        return "{:1.0e}".format(num).replace("+0", "")

SIMPLE_PIPELINE_FUNCS = [filter_evens, is_prime, multiply_items]
COMPLEX_PIPELINE_FUNCS = [filter_evens, filter_divisible_by, is_prime, is_emirp, checksum]

PIPELINE_FUNCS = COMPLEX_PIPELINE_FUNCS

def pretty_print_df(df, split_strings):
    df_string = df.to_string()
    num_dashes = 7 + 25 * len(df. columns)
    for split in split_strings:
        df_string = df_string.replace("\n{0}".format(split), '\n' + '-' * num_dashes + "\n{0}".format(split))
    return df_string

if __name__ == '__main__':
    def set_variables():
        global POOL_WORKERS, BATCH_SIZE, QUEUE_SIZE
        POOL_WORKERS = 8
        BATCH_SIZE = 50
        QUEUE_SIZE = 0  
        
    all_pipelines = [sequential, parallel, parallel_multi_threads, parallel_multi_process]

    ### RUN THIS LOCALLY ###
    
    data = range(int(0), int(1e3)) # Small data size for validation purposes
    
    ######### VALIDATION TEST #############
    set_variables()
    run_pipeline_experiment(all_pipelines, "VALIDATION TEST")

    data = range(int(0), int(1e2)) # Larger data size for experimentation, DO NOT GO HIGHER THAN 2.5e5

    ######## EFFECT OF SIMPLE AND MULTIPLE PARALLELISM #############
    # set_variables()
    # run_pipeline_experiment([sequential, parallel, parallel_multi_threads, parallel_multi_process],
    #                        "SIMPLE/MULTIPLE PARALLEL STAGE")
    
    ######## EFFECT OF POOL WORKERS #############
    # set_variables()
    # for POOL_WORKERS in [4, 8]:
    #   run_pipeline_experiment([parallel, parallel_multi_process],
    #                            "EFFECT OF POOL WORKERS {0}".format(POOL_WORKERS))
    
    ######## EFFECT OF QUEUE SIZE #############
    # set_variables()
    # for QUEUE_SIZE in [0, 5]:
    #    run_pipeline_experiment([parallel, parallel_multi_process],
    #                            "EFFECT OF QUEUE SIZE {0}".format(QUEUE_SIZE))
    
    ######## EFFECT OF BATCH SIZE #############
    # set_variables()
    # for BATCH_SIZE in [1, 100]:
    #    run_pipeline_experiment([parallel, parallel_multi_process],
    #                            "EFFECT OF BATCH SIZE {0}".format(BATCH_SIZE))


    # ## YOU MAY RUN THIS REMOTELY ###
    # ######### EFFECT OF POOL WORKERS #############
    # PIPELINE_FUNCS = COMPLEX_PIPELINE_FUNCS
    #
    # data = range(int(1e2), int(2.5e5))  # Larger data size for experimentation, DO NOT GO HIGHER THAN 2.5e5
    # BATCH_SIZE = 50
    # QUEUE_SIZE = 0
    # for P in [2, 4, 8, 12, 16, 24, 32]:
    #     POOL_WORKERS = P
    #     run_pipeline_experiment([parallel, parallel_multi_process],
    #                             "EFFECT OF POOL WORKERS")
