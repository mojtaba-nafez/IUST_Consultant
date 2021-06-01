release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn Consultant.wsgi:application --log-file -
web2: daphne Consultant.asgi:application
worker: python manage.py runworker channel_layer

