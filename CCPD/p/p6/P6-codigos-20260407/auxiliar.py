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

def to_time_miliseconds(start, end):
    return int(1000 * (end - start))


def validate(*args):
    length = len(args[0])
    for res in args[1:]:
        if len(res) != length:
            return False, "size mismatch"
        length = len(res)

    length = len(args[0])
    for i in range(0, length):
        value = args[0][i]
        for res in args[1:]:
            if value != res[i]:
                return False, "value mismatch"
            value = res[i]
    return True, ""


def get_chunks(n, num_chunks):
    chunksize = n // num_chunks
    proc_chunks = []
    for i_proc in range(num_chunks):
        chunkstart = i_proc * chunksize
        if i_proc < num_chunks - 1:
            chunkend = (i_proc + 1) * chunksize
        else:
            chunkend = n
        proc_chunks.append((chunkstart, chunkend))
    return proc_chunks


def flatten_list_of_lists(l):
    # Read this like "for each sublist in l, give sublist, and for each item in sublist, give item"
    return [item for sublist in l for item in sublist]


def sci_not_str(num):
    if type(num) != int:
        return "{:1.2e}".format(num)
    else:
        return "{:1.0e}".format(num).replace("+0", "")
