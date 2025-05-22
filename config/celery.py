import os

from celery import Celery
from celery.utils.log import get_task_logger
from django.conf import settings

logger = get_task_logger(__name__)

__all__ = ['app', 'debug_task', 'revoke_task', 'clear_tasks']

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery(
    'main',
    backend=settings.REDIS_URI,
    broker=settings.REDIS_URI,
)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True

CELERY_TIMEZONE = settings.TIME_ZONE
CELERY_ENABLE_UTC = bool(os.environ.get('CELERY_ENABLE_UTC', default=False))


@app.task(bind=True)
def debug_task(self):
    logger.info('Request: {0!r}'.format(self.request))  # pragma: no cover


def revoke_task(task_id):
    app.control.revoke(task_id)


def clear_tasks():
    return app.control.purge()