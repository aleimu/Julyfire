# -*- coding:utf-8 -*-

import time
from celery import Celery

app = Celery('one')
app.config_from_object('config')

@app.task
def add(x, y):
    print ('add:%s + %s' % (x, y))
    time.sleep(5)
    return x + y

@app.task
def rem(x, y):
    print ('rem:%s - %s' % (x, y))
    time.sleep(1)
    return x - y
