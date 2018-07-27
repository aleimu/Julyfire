# -*- coding:utf-8 -*-

CELERY_ROUTES = {'two.add_remote': {'queue': 'q_remote_add'},
                 'one.add': {'queue': 'q_add'},
                 'one.rem': {'queue': 'q_rem'}}
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # 配置上这个才能返回计算结果