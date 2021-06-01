release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn Consultant.wsgi:application --log-file -
web2: daphne Consultant.asgi:application --port 8001 --bind 0.0.0.0 -v3

