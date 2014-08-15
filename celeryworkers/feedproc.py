from __future__ import absolute_import
from celery import Celery


app = Celery('feedproc',
             include=['feedtasks'])


# Celery Config parameters
class Config:
    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE = "America/Los_Angeles"
    # Only run 4 threads total
    CELERYD_CONCURRENCY = 4
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    BROKER_URL = 'redis://localhost:6379/0'

app.config_from_object(Config)

if __name__ == '__main__':
    app.start()
