import time
import redis
import json


class Receiver:
    # OPTION
    SURVEILLANCE_INTERVAL = 1
    REDIS_LISTNAME = 'order'
    runCodeQueue = redis.Redis(host='localhost', port=6379)
    mode = ["h", "c", "d"]
    strength = ["str1", "str3", "str4"]



    @classmethod
    def run(self):
        try:
            while True:
                time.sleep(self.SURVEILLANCE_INTERVAL)
                if self.runCodeQueue.llen(self.REDIS_LISTNAME) != 0:
                    order_json = self.runCodeQueue.lpop(self.REDIS_LISTNAME).decode('utf-8')
                    order_list = json.loads(order_json)
                    if order_list["on"] == "on":
                        order_list["mode"]
                        order_list["strength"]
                        order_list["temperature"]
                    elif order_list["off"] == "off":
                        pass
                    else:
                        print("error order code")

                    ir.transmission(runKey)

        except KeyboardInterrupt:
            print("error receiver")
            pass
