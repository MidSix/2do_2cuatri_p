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

# El número es el valor inicial:
# 0 -> nadie puede acceder hasta que no se haga 1 release
# 1 -> puede acceder 1 hilo
item_ready = threading.Semaphore(0) # Esto por defecto está en 0
item_consumed = threading.Semaphore(1) # Esto por defecto está en 1

item = 0
SLEEP_TIME = 0.25 # Tiempo de espera para consumir un item, en segundos

PADDING = "\t\t\t\t\t\t\t\t"

ITEMS_TO_CONSUME = 50
ITEMS_CONSUMED = False

def producer_notify(s):
    now = datetime.datetime.now()
    print("Producer notify: " + "[{0:2}:{1:2}:{2:2}] -> {3}".format(now.hour, now.minute, now.second, s))

def consumer_notify(s):
    print(PADDING + "Consumer notify: " + s)

def consumer():
    # Una variable declarada como global hace referencia a una variable compartida entre todos los hilos
    global item, ITEMS_CONSUMED
    items_consumed = 0
    while True:
        consumer_notify("Waiting for new items")
        item_ready.acquire()
        consumer_notify("consuming item")
        time.sleep(SLEEP_TIME)
        items_consumed += 1
        consumer_notify("Consumed item number {0}".format(item))
        item_consumed.release()

        if items_consumed >= ITEMS_TO_CONSUME:
            ITEMS_CONSUMED = True
            break

def producer():
    global item, ITEMS_CONSUMED
    while True:
        producer_notify("Waiting to produce a new item")
        item_consumed.acquire()
        producer_notify("Producing an item")
        item = random.randint(0, 1000)
        producer_notify("Produced item number {0}".format(item))
        item_ready.release()

        if ITEMS_CONSUMED:
            break

if __name__ == '__main__':
    print("Launching threads")
    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
