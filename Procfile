release: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py compress
web: ./.docker/web.sh
worker: ./.docker/q.sh
