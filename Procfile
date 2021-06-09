release: python manage.py makemigrations User calendar_ channel chat_room message request
release: python manage.py migrate
web: daphne Consultant.asgi:application --port $PORT --bind 0.0.0.0 -v3
chatworker: python manage.py runworker --settings=Consultant.settings -v3

