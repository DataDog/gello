web: gunicorn manage.py runserver
worker: celery worker -A celery_worker.celery --loglevel=info
