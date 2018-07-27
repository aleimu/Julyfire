# -*- coding:utf-8 -*-
from celery import Celery
import time


app = Celery()
app.config_from_object('celeryconfig')

# 视频压缩
@app.task
def video_compress(video_name):
    time.sleep(10)
    print 'Compressing the:', video_name
    return 'success'

@app.task
def video_upload(video_name):
    time.sleep(5)
    print u'正在上传视频'
    return 'success'

# 压缩照片
@app.task
def image_compress(image_name):
    time.sleep(10)
    print 'Compressing the:', image_name
    return 'success'

# 其他任务
@app.task
def other(str):
    time.sleep(10)
    print 'Do other things'
    return 'success'
