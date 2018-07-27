# -*- coding:utf-8 -*-
import time
from datetime import timedelta
from celery import Celery

# celery = Celery(backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')
celery = Celery()

"""
# 常用配置与参考
# http://docs.jinkan.org/docs/celery/index.html 文档
app = Celery(__name__)
app.conf.update(
    BROKER_URL='amqp://root:qwertyuiop@10.2.5.51:5672//',  # 使用RabbitMQ作为消息代理
    CELERY_RESULT_BACKEND='redis://10.2.5.51:5123/0',  # 使用Redis作为结果存储
    CELERY_TASK_SERIALIZER='msgpack',  # 使用Msgpack作为有效载荷序列化方案
    CELERY_RESULT_SERIALIZER='json',  # 使用可读性好的Json作为结果最终存储
    CELERY_TASK_RESULT_EXPIRES=60 * 60 * 24,  # 设置任务过期时间为1天
    CELERY_ACCEPT_COUNT=['json', 'msgpack'],  # 指定接受的内容类型
    CELERYD_CONCURRENCY=20,  # 并发worker数
    CELERYD_MAX_TASKS_PER_CHILD=100,  # 每个worker最多执行万100个任务就会被销毁，可防止内存泄露
    CELERYD_TASK_TIME_LIMIT=60,  # 单个任务的运行时间不超过此值，否则会被SIGKILL 信号杀死
    BROKER_TRANSPORT_OPTIONS={'visibility_timeout': 90},
    CELERY_DISABLE_RATE_LIMITS=True,  # 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERYD_FORCE_EXECV=True,  # 非常重要,有些情况下可以防止死锁
    CELERYD_PREFETCH_MULTIPLIER=1,  # 一次预取多少条消息乘以并发进程数。 默认值为4（每个进程有四条消息）。
    CELERY_CREATE_MISSING_QUEUES=True,  # 某个程序中出现的队列，在broker中不存在，则立刻创建它
    CELERY_IMPORTS=("async_task.tasks", "async_task.notify"),  # 启动时要导入的一系列模块。
    # 定时任务
    CELERYBEAT_SCHEDULE = {
        'msg_notify': {
            'task': 'async_task.notify.msg_notify',
            'schedule': timedelta(seconds=10),
            # 'args': (redis_db),
            'options': {'queue': 'my_period_task'}
        },
        'report_result': {
            'task': 'async_task.tasks.report_result',
            'schedule': timedelta(seconds=10),
            # 'args': (redis_db),
            'options': {'queue': 'my_period_task'}
        },
        # 'report_retry': {
        #    'task': 'async_task.tasks.report_retry',
        #    'schedule': timedelta(seconds=60),
        #    'options' : {'queue':'my_period_task'}
        # },
    }
)


################################################
# 启动worker的命令
# *** 定时器 ***
# nohup celery beat -s /var/log/boas/celerybeat-schedule  --logfile=/var/log/boas/celerybeat.log  -l info &
# *** worker ***
# nohup celery worker -f /var/log/boas/boas_celery.log -l INFO &

# celery4.0 版本中才支持
# class config:
#     CELERY_ROUTES = {'two.add_remote': {'queue': 'remote_add'},
#                      'one.add': {'queue': 'add'},
#                      'one.rem': {'queue': 'rem'}}
#     BROKER_URL = 'redis://localhost:6379/0'
# celery.config_from_object(config)
"""

celery.config_from_object('config')
t1 = celery.send_task('two.add_remote', (1, 2))
t2 = celery.send_task('one.add', (3, 4))
t3 = celery.send_task('one.rem', (5, 6))

# print t1.get()
# print t2.get()
# print t3.get()

tt1=time.time()
while not (t1.ready() and t2.ready() and t3.ready()):
    time.sleep(0.1)
tt2=time.time()
print 'task done: {0}'.format(t1.get())
print 'task done: {0}'.format(t2.get())
print 'task done: {0}'.format(t3.get())

print("case time: ", tt2-tt1)