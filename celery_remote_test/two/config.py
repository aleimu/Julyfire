# -*- coding:utf-8 -*-

CELERY_ROUTES = {'two.add_remote': {'queue': 'q_remote_add'}}
BROKER_URL = 'redis://localhost:6379/0'     # 数据来源
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # 配置上这个才能返回计算结果