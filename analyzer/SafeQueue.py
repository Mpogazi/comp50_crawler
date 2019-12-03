

import threading

class SafeQueue:
    def __init__(self):
        self.__list = []
        self.__lock = threading.Lock()
        self.__items = threading.Semaphore(0)

    def get(self):
        self.__items.acquire() #wait operation
        with self.__lock:
            return self.__list.pop(0)


    def put(self, item):
        
        with self.__lock:
            self.__list.append(item)
        self.__items.release() # signal operation                

                