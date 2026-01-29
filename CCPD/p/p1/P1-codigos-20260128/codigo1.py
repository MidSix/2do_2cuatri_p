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

start = time.time()
for n in range(1, 10000):
    n*n
end = time.time()
print("Time in seconds is: " + str(end - start))
print("Time in milliseconds is: " + str(int(1000 * (end - start))))

start = time.time()
for n in range(1, 5000):
    for k in range(1, 5000):
        x = n*k
end = time.time()
print("Time in seconds is: " + str(end - start))
print("Time in milliseconds is: " + str(int(1000 * (end - start))))
