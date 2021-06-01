release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn Consultant.wsgi:application --log-file -
web2: daphne Consultant.routing:application
worker: python manage.py runworker channel_layer

