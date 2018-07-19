import time
import redis
import importlib
# import ir.transmitter as ir
# import signal
# import sys
# import os
# import ir.ledTest as ledTest


class Receiver:
    # OPTION
    SURVEILLANCE_INTERVAL = 1
    REDIS_LISTNAME = 'order'
    runCodeQueue = redis.Redis(host='localhost', port=6379)
    counter = 0

    @classmethod
    def start(self):
        led = importlib.import_module('led')
        try:
            while True:
                time.sleep(self.SURVEILLANCE_INTERVAL)
                if self.runCodeQueue.llen(self.REDIS_LISTNAME) != 0:
                    runKey = self.runCodeQueue.lpop(self.REDIS_LISTNAME).decode('utf-8')
                    # ir.transmission(runKey)
                    led.toggle_led(runKey)
                    # ledTest.toggle_led(runKey)
                print('wait')
                if self.counter == 5:
                    self.runCodeQueue.rpush(self.REDIS_LISTNAME, 'right')
                elif self.counter == 10:
                    self.runCodeQueue.rpush(self.REDIS_LISTNAME, 'left')
                    self.runCodeQueue.rpush(self.REDIS_LISTNAME, 'right')
                    self.runCodeQueue.rpush(self.REDIS_LISTNAME, 'ana')
                elif self.counter == 15:
                    self.runCodeQueue.rpush(self.REDIS_LISTNAME, 'test')
                elif self.counter == 20:
                    self.runCodeQueue.rpush(self.REDIS_LISTNAME, 'left')
                elif self.counter == 25:
                    self.runCodeQueue.rpush(self.REDIS_LISTNAME, 'end')

                self.counter = self.counter+1

        except KeyboardInterrupt:
            pass