release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn -b 0.0.0.0 -p 8000 Consultant.wsgi:application --log-file -


