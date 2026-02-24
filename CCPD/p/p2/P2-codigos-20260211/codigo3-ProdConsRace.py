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
SLEEP_TIME = 0.1

PADDING = "\t\t\t\t\t\t"
won_lock_t1 = 0 # Variables usadas por los threads como contador
won_lock_t2 = 0
# Las variables won_lock son escritas por 1 solo thread cada una, y leídas por el proceso padre -> no hay peligro
FINISH = False


def my_print(s):
    now = datetime.datetime.now()
    print("[{0:2}:{1:2}] -> {2}".format(now.minute, now.second, s))

def producer_notify(s):
    my_print(PADDING + "Producer notify: " + s)

def consumer_notify(s):
    my_print("Consumer notify: " + s)

def consumer():
    global item, won_lock_t2, FINISH
    while not FINISH:
        consumer_notify("Waiting for new items")
        item_ready.acquire()
        won_lock_t2 += 1
        consumer_notify("Entering production bay")
        consumer_notify("Consuming item")
        time.sleep(SLEEP_TIME)
        consumer_notify("Consumed item number {0}".format(item))
        item_ready.release()

def producer():
    global item, won_lock_t1, FINISH
    while not FINISH:
        producer_notify("Waiting to access production bay")
        item_ready.acquire()
        won_lock_t1 += 1
        producer_notify("Entering production bay")
        producer_notify("Producing an item")
        item = random.randint(0, 1000)
        time.sleep(SLEEP_TIME)
        producer_notify("Produced item number {0}".format(item))
        item_ready.release()

if __name__ == '__main__':
    my_print("Launching threads")
    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start()
    t2.start()
    try:
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        # FINISH es una variable de tipo 'flag', se usa para señalar a todos los threads que deben acabar
        # Como es una variable que solo escribe el proceso y que los threads solo leen, no hay peligro
        FINISH = True
        print("Consumer won the lock {0} times".format(won_lock_t2))
        print("Producer won the lock {0} times".format(won_lock_t1))
        t1.join()
        t2.join()
