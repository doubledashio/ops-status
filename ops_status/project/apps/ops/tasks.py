import logging

from celery import Task

from config.celery import app

logger = logging.getLogger(__name__)


class ExampleTaskClass(Task):
    """Example Celery task.

    Extends:
        Task
    """
    def run(self, *args, **kwargs):
        logger.info('Running ExampleTaskClass')


ExampleTask = app.register_task(ExampleTaskClass())  # noqa
