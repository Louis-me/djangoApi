import time

from celery import task



@task
def add(a,b):
    print("这是任务开始")
    print(a+b)
    time.sleep(10)
    print("这是任务结束")


