# -*- coding:utf-8 -*-
from kombu import Exchange, Queue

# 配置市区
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_BROKER = 'amqp://localhost'
# 定义一个默认交换机
default_exchange = Exchange('dedfault', type='direct')

# 定义一个媒体交换机
media_exchange = Exchange('media', type='direct')

# 创建三个队列，一个是默认队列，一个是video、一个image
CELERY_QUEUES = (
    Queue('default', default_exchange, routing_key='default'),
    Queue('videos', media_exchange, routing_key='media.video'),
    Queue('images', media_exchange, routing_key='media.image')
)

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'
#
CELERY_ROUTES = ({'tasks.image_compress': {
                        'queue': 'images',
                        'routing_key': 'media.image'
                 }},{'tasks.video_upload': {
                        'queue': 'videos',
                        'routing_key': 'media.video'
                 }},{'tasks.video_compress': {
                        'queue': 'videos',
                        'routing_key': 'media.video'
                 }}, )

# 在出现worker接受到的message出现没有注册的错误时，使用下面一句能解决
CELERY_IMPORTS = ("tasks",)
