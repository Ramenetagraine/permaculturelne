release: python manage.py makemigrations && python manage.py migrate
web: gunicorn festival.wsgi --log-file
