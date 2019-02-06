import time
import redis
import json

import IRControlSystem.lib.Ir_sender.transmitter as ir


class Receiver:
    # OPTION
    SURVEILLANCE_INTERVAL = 1
    REDIS_LISTNAME = 'order'
    runCodeQueue = redis.Redis(host='localhost', port=6379)
    mode = ["c_", "h_", "d_"]
    strength = ["dir3_str1.json", "dir3_str3.json", "dir3_str4.json"]
    DIR_NAME = "IRControlSystem/lib/Ir_code/"
    DRY_MAP = {}

    @classmethod
    def run(self):
        try:
            while True:
                time.sleep(self.SURVEILLANCE_INTERVAL)
                if self.runCodeQueue.llen(self.REDIS_LISTNAME) != 0:
                    order_json = self.runCodeQueue.lpop(self.REDIS_LISTNAME).decode('utf-8')
                    order_list = json.loads(order_json)

                    if order_list["on"] == "on":
                        if order_list["mode"] == 2:
                            runKey = str(order_list["temperature"])
                            fileName = self.DIR_NAME + "d_dir3.json"

                        else:
                            keyM = self.mode[order_list["mode"]]
                            keyS = self.strength[order_list["strength"]]
                            runKey = str(order_list["temperature"])
                            fileName = self.DIR_NAME + keyM + keyS

                        ir.boot("on", self.DIR_NAME)
                        time.sleep(self.SURVEILLANCE_INTERVAL * 3)
                        ir.transmission(runKey, fileName)
                        time.sleep(self.SURVEILLANCE_INTERVAL * 3)
                    elif order_list["on"] == "off":  # 電源オフ
                        ir.boot("off", self.DIR_NAME)
                        time.sleep(self.SURVEILLANCE_INTERVAL * 3)
                        # 二回停止しないと洗浄モードが切れないため
                        ir.boot("off", self.DIR_NAME)
                        time.sleep(self.SURVEILLANCE_INTERVAL * 3)
                    else:
                        print("error order code")

        except KeyboardInterrupt:
            print("error receiver")
            pass
