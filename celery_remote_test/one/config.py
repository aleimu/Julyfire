# -*- coding:utf-8 -*-
from kombu import Queue,Exchange

CELERY_ROUTES = {'one.add': {'queue': 'q_add'},
                 'one.rem': {'queue': 'q_rem'}}
BROKER_URL = 'redis://localhost:6379/0'     # 数据来源
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # 配置上这个才能返回计算结果

# # 配置队列（settings.py）
# CELERY_QUEUES = (
#     Queue('default', Exchange('default'), routing_key='default'),
#     Queue('for_task_collect', Exchange('for_task_collect'), routing_key='for_task_collect'),
#     Queue('for_task_compute', Exchange('for_task_compute'), routing_key='for_task_compute'),
# )
#
# # 路由（哪个任务放入哪个队列）
# CELERY_ROUTES = {
#     'umonitor.tasks.multiple_thread_metric_collector': {'queue': 'for_task_collect', 'routing_key': 'for_task_collect'},
#     'compute.tasks.multiple_thread_metric_aggregate': {'queue': 'for_task_compute', 'routing_key': 'for_task_compute'},
#     'compute.tasks.test': {'queue': 'for_task_compute', 'routing_key': 'for_task_compute'},
# }


# # 指定worker_compute去处理队列for_task_compute的任务
# celery worker -E -l INFO -n worker_compute -Q for_task_compute
# # 指定worker_collect去处理队列for_task_collect的任务
# celery worker -E -l INFO -n worker_collect -Q for_task_collect