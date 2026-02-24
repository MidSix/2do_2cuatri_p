#
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
import threading
import datetime

item_ready = threading.Semaphore(1)

item = 0
EAT_TIME = 0.1

PADDING = "\t\t\t\t\t\t\t"

def my_print(s):
    now = datetime.datetime.now()
    print("[{0:2}:{1:2}] -> {2}".format(now.minute, now.second, s))

def slow_notify(s):
    my_print(PADDING + "Slow consumer: " + s)

def fast_notify(s):
    my_print("Fast consumer: " + s)

def consumerFast():
    count = 0
    while True:
        fast_notify("Waiting to enter diner")
        item_ready.acquire()
        fast_notify("Entering diner and eating")
        time.sleep(EAT_TIME)
        count += 1
        fast_notify("Exiting diner, I have eaten {0} times".format(count))
        item_ready.release()
        fast_notify("Going to queue to eat again")

def consumerSlow():
    count = 0
    while True:
        slow_notify("Waiting to enter diner")
        success = item_ready.acquire(timeout=0.1) # Operación no-bloqueante al usar un timeout
        # Se guarda el resultado en success, si se adquirió el lock, sera True, sino será False
        if not success:
            slow_notify("Someone is inside, going to make time")
            time.sleep(1)
            continue
        slow_notify("Entering diner and eating something")
        time.sleep(EAT_TIME)
        count += 1
        slow_notify("Exiting diner, I have eaten {0} times".format(count))
        slow_notify("Going for a brief walk")
        item_ready.release()
        time.sleep(1)

if __name__ == '__main__':
    my_print("Launching threads")
    t1 = threading.Thread(target=consumerFast)
    t2 = threading.Thread(target=consumerSlow)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
