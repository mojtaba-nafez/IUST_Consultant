release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn -b 0.0.0.0 -p 8000 Consultant.wsgi:application --log-file -
web: daphne -b 0.0.0.0 -p 8001 Consultant.asgi:application
worker: python manage.py runworker channel_layer -v2

