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
import sys
import math
from shutil import copyfile

if __name__ == "__main__":
    N_MAX_LIMIT = 9

    if len(sys.argv) < 2:
        print("Parameters are lacking, 1 parameters are needed in the next order")
        print("+ Lenght of data (a number to be used as a power of 10, e.g. 3 -> 1e3)")
        exit(1)

    N_MAX = int(float(sys.argv[1]))  # num
    #N_MAX = int(math.pow(10, int(N_MAX)))

    print("Generating numbers")
    numbers = [*range(1, N_MAX + 1)]
    with open('a.txt', 'w') as filehandle:
        filehandle.writelines("%d\n" % n for n in numbers)

    copyfile('a.txt', 'ax.txt')
    copyfile('a.txt', 'b.txt')
    copyfile('a.txt', 'bx.txt')
