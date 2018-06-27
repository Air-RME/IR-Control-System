import time
import redis
# import ir.transmitter as ir
# import signal
# import sys
# import os
import ir.led as led


class Receiver:
    # OPTION
    SURVEILLANCE_INTERVAL = 1
    REDIS_LISTNAME = 'order'
    runCodeQueue = redis.Redis(host='localhost', port=6379)

    @classmethod
    def start(self):
        try:
            while True:
                time.sleep(self.SURVEILLANCE_INTERVAL)
                if self.runCodeQueue.llen(self.REDIS_LISTNAME) != 0:
                    runKey = self.runCodeQueue.lpop(self.REDIS_LISTNAME).decode('utf-8')
                    # 本番用
                    # ir.transmission(runKey)
                    # デモ用
                    led.toggle_led(runKey)
                print('待機中')
        except KeyboardInterrupt:
            pass

# 別の方法
# SURVEILLANCE_INTERVAL = 0.5
#
# Q=[0,1,2,3,4]
#
# def task(arg1, arg2):
#     print(time.time())
#     if(len(Q)!=0):
#         Q.pop(0)
#         print(Q)
#     else:
#         print(os.getpid())
#         os.kill(os.getpid(), signal.SIGTERM)
#
# def handler(signa, frame):
#     print('終了')
#     sys.exit(0)
#
# signal.signal(signal.SIGTERM, handler)
# signal.signal(signal.SIGALRM, task)
# signal.setitimer(signal.ITIMER_REAL, 0.1, SURVEILLANCE_INTERVAL)
#
# while True:
#     pass
