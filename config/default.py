from celery.schedules import crontab
from dotenv import load_dotenv
from split_settings.tools import include, optional

load_dotenv()

include(
    "components/base.py",
    "components/locale.py",
    "components/app.py",
    "components/cache.py",
    "components/celery.py",
    "components/database.py",
    "components/drf.py",
    "components/keycloak.py",
    "components/log.py",
    "components/minio.py",
    "components/nats.py",
    "components/unfold.py",
    "components/extra.py",
)


CELERY_BEAT_SCHEDULE = {
    'sync_periodic_update_task_status': {
        'task': 'apps.cmdb.celery_tasks.sync_periodic_update_task_status',
        'schedule': crontab(minute='*/5'),
    },
}