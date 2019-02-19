from os import environ

from celery import Celery

environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarplateAPI.settings')

app = Celery('CarplateAPI')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
