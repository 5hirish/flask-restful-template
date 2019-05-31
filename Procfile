web: gunicorn run_server:erpro_app --timeout 60 --keep-alive 5 --log-level debug
worker: celery worker -A erpro.worker.core.celery_task --loglevel=DEBUG