import os
from celery import Celery
from celery.schedules import crontab



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('scholarmap')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send-gmail-eslatmalar":{
        'task': 'api.tasks.check_eslatmalar',
        'schedule': crontab(hour=1, minute=0),  # Har kuni soat 8:00 da ishga tushadi
    }

}