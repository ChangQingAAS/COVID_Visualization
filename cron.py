import threading
from datetime import datetime
from time import sleep
from os import popen
from config import *


def cron_task():
    print(f"定时任务开启，每{PAUSE}小时自动更新数据")
    while True:
        now = datetime.now()
        if(now.hour % PAUSE) == 0 and now.minute == 0 and now.second == 0:
            task = popen('python spider.py 0')
            sleep(10)
            result = task.read()
            print(result)
            task.close()
            task = popen('python spider.py 1')
            sleep(10)
            result = task.read()
            print(result)
            task.close()
            sleep(60*60*6 - 100)
        sleep(1)


if __name__ == "__main__":
    threading.Thread(target=cron_task).start()
