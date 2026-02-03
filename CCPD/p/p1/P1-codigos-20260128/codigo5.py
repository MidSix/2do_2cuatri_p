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

COUNT_INI = int(1e2) # Esto es 100
COUNT_MAX = int(1e6) # Esto es 1.000.000
COUNT_STEP = int(1e1) # Esto es 10

count = COUNT_INI
while count <= COUNT_MAX:
    count = count * COUNT_STEP
    print(count)
