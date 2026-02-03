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
import random

start = time.time()
count = random.randint(1000, 10000)
print("Going to iterate {0} times".format(count))
for n in range(1, count):
    for k in range(1, count):
        n*k
end = time.time()
print("It took {0} seconds, or {1} miliseconds".format(
    int(end - start), 
    int(1000 * (end - start))))
print("It took exactly {0:.2f} seconds".format(end - start))
