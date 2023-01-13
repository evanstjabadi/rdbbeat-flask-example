from celery import Celery

from server.app import app as flask_app
from server.session_management import session_scope

REDIS_URL = "redis://localhost:6379/0"


def create_celery(flask_app=flask_app):
    celery_app = Celery("flask", broker=REDIS_URL)

    celery_app.conf.task_default_queue = "default"

    celery_app.conf.broker_transport_options = {
        "max_retries": 3,
        "interval_start": 0,
        "interval_step": 0.2,
        "interval_max": 0.2,
    }

    # Provide session scope to `rdbbeat`
    celery_app.conf.session_scope = session_scope
    celery_app.conf.update(flask_app.config)

    TaskBase = celery_app.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery_app.Task = ContextTask

    return celery_app


app = create_celery(flask_app=flask_app)
