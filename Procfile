release: python manage.py migrate
web: gunicorn django_satmap.wsgi --max-requests 500 --max-requests-jitter 50