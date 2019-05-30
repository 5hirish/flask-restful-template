import os
from erpro.worker.core import celery_task

if __name__ == '__main__':

    argv = [
        'worker',
        '--loglevel=DEBUG',
    ]
    celery_task.worker_main(argv)
