web: gunicorn stock.wsgi --log-file -
worker: celery -A stock worker --events --loglevel INFO 
beat: celery -A stock beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
