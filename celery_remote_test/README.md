# 测试方法

## Start celeries

celery worker -A one --loglevel=info -Q q_add

celery worker -A one --loglevel=info -Q q_rem

celery worker -A two --loglevel=info -Q q_remote_add

## Run test script.

python test.py
