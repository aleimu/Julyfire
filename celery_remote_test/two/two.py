# -*- coding:utf-8 -*-
import time
from celery import Celery

app = Celery('two')
app.config_from_object('config')

@app.task
def add_remote(x, y):
    print ('add_remote:%s + %s' % (x, y))
    time.sleep(5)
    return x + y