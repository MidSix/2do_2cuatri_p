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
import threading


def to_time_miliseconds(start, end):
    return int(1000 * (end - start))

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


def pipe_generator(pipe_out, data):
    output_pipe, _ = pipe_out
    start = time.time()
    for item in data:
        output_pipe.send(item)
    end = time.time()
    print("Stage 'generator' has finished after {0} ms".format(to_time_miliseconds(start, end)))
    output_pipe.close()


def pipe_stage(pipe_in, pipe_out, funct):
    _, input_pipe = pipe_in
    output_pipe, _ = pipe_out
    start = time.time()
    try:
        while True:
            item = input_pipe.recv()
            result = funct(item)
            if result:
                output_pipe.send(result)
    except EOFError:
        end = time.time()
        print("Stage '{0}' has finished after {1} ms".format(funct.__name__, to_time_miliseconds(start, end)))
        output_pipe.close()


def pipe_consumer(pipe_in):
    i = 0
    try:
        while True:
            i += pipe_in[1].recv()
    except EOFError:
        print("[PIPELINE] End result is {0}".format(i))


def run_sequential():
    start = time.time()
    i = 0
    for item in data:
        item = filter_evens(item)
        if not item:
            continue
        item = is_prime(item)
        if not item:
            continue
        item = multiply_items(item)
        if not item:
            continue
        i += item
    end = time.time()
    print("[SEQ] finished after {0} ms".format(to_time_miliseconds(start, end)))
    print("[SEQ] End result is {0}".format(i))


def run_pipeline(implementation="process"):
    pipe_list = list()
    process_list = list()

    if implementation == "process":
        entity_type = multiprocessing.Process
    elif implementation == "threads":
        entity_type = threading.Thread
    else:
        entity_type = multiprocessing.Process

    # Generator
    pipe1 = multiprocessing.Pipe(duplex=True)
    p1 = entity_type(target=pipe_generator, args=(pipe1, data,))
    pipe_list.append(pipe1)
    process_list.append(p1)

    # Stages
    pipe2 = multiprocessing.Pipe(duplex=True)
    p2 = entity_type(target=pipe_stage, args=(pipe1, pipe2, filter_evens,))
    pipe_list.append(pipe2)
    process_list.append(p2)

    pipe3 = multiprocessing.Pipe(duplex=True)
    p3 = entity_type(target=pipe_stage, args=(pipe2, pipe3, is_prime,))
    pipe_list.append(pipe3)
    process_list.append(p3)

    pipe4 = multiprocessing.Pipe(duplex=True)
    p4 = entity_type(target=pipe_stage, args=(pipe3, pipe4, multiply_items,))
    pipe_list.append(pipe4)
    process_list.append(p4)

    # Consumer
    p5 = entity_type(target=pipe_consumer, args=(pipe4,))

    start = time.time()

    if implementation == "process":
        for pipe, p in zip(pipe_list, process_list):
            p.start()
            pipe[0].close()
    else:
        for p in process_list:
            p.start()

    p5.start()
    p5.join()
    end = time.time()
    print("[PIPELINE ({0})] finished after {1} ms".format(implementation, to_time_miliseconds(start, end)))


if __name__ == '__main__':
    data = range(int(1e1), int(1e2))  # Max number is 2e5
    print("------------------------------")
    print("SEQUENTIALLY")
    run_sequential()
    print("")

    print("------------------------------")
    print("PARALLEL [THREADS]")
    run_pipeline(implementation="threads")
    print("")

    print("------------------------------")
    print("PARALLEL [PROCESS]")
    run_pipeline(implementation="process")
    print("")
