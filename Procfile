release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn permaculturelne.wsgi --log-file -
