web: gunicorn app:app
worker: celery worker -A celery_worker.celery --loglevel=info --without-gossip
release: python manage.py db upgrade && python manage.py deploy
