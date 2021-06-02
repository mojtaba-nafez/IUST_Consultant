release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn Consultant.wsgi:application --log-file -
web2: daphne Consultant.asgi:application --port $PORT --bind 0.0.0.0 -v3
worker: python3 manage.py runworker channel_layer

