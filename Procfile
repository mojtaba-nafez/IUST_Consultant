release: python manage.py makemigrations
release: python manage.py migrate
web: daphne Consultant.asgi:application --port 8000 --bind 0.0.0.0 -v3 --log-file -


