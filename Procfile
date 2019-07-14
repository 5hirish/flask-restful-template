web: gunicorn run_server:foobar_app --timeout 60 --keep-alive 5 --log-level debug
worker: celery worker -A foobar.worker.core.celery_task --loglevel=DEBUG