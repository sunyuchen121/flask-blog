import os

# beat 定时任务，默认不存储结果
# fast 快(优先)任务，默认不存储结果
# worker 一般任务，默认存储结果

if not os.environ.get("celery_broker_url", None):
    BROKER_URL = 'amqp://guest:guest@localhost:15672//'
else:
    BROKER_URL = os.environ.get("celery_broker_url")

if not os.environ.get("celery_backend_url", None):
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
else:
    CELERY_RESULT_BACKEND = os.environ.get("celery_backend_url")



