release: python manage.py makemigrations
release: python manage.py migrate
web: daphne -b 0.0.0.0 -p 8000 Consultant.asgi:application
worker: python manage.py runworker channel_layer -v2

