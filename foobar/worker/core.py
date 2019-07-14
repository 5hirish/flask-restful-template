import os
from celery import Celery

from foobar.service.core import create_app
from foobar.config import DevConfig, TestConfig, ProdConfig

# celery worker -A foobar.worker.core.celery_task --loglevel=DEBUG
# celery flower -A foobar.worker.core.celery_task


flask_env = str(os.environ.get('FLASK_ENV'))
if flask_env == 'dev':
    app_config = DevConfig
elif flask_env == 'test':
    app_config = TestConfig
else:
    app_config = ProdConfig


task_app = create_app(app_config, enable_blueprints=False)
task_app.app_context().push()

# logger = get_logger()
celery_task = Celery()
celery_task.config_from_object(task_app.config, namespace='CELERY')
celery_task.autodiscover_tasks(packages=['foobar.worker'])


class BaseTask(celery_task.Task):
    """Abstract base class for all tasks in the app."""

    abstract = True

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to something like sentry at retry."""
        super(BaseTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to something like sentry."""
        super(BaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)
