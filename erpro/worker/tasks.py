import requests
import json

from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from celery import group, chain, states
from celery.utils.log import get_task_logger

from erpro.worker.core import celery_task, BaseTask

task_base_name = "erpro.worker."
logger = get_task_logger(__name__)


@celery_task.task(name=task_base_name + "import_products",
                  bind=False, max_retries=3, default_retry_delay=300, track_started=True,
                  base=BaseTask)
def import_products():
    return None
