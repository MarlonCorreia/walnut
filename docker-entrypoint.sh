#!/bin/bash
set -e

if [ "$1" = "manage" ]; then
    shift 1
    exec python manage.py "$@"

elif [ "$1" = "celery" ]; then
    # Start celery workers
    shift 1
    echo Starting celery workers
    exec celery -A settings worker -l INFO -Q "$@"

else
    python manage.py collectstatic --noinput  # Collect static files
    python manage.py migrate                  # Apply database migrations

    touch /usr/src/logs/gunicorn.log
    touch /usr/src/logs/access.log
    tail -n 0 -f /usr/src/logs/*.log &

    # Start Gunicorn processes
    echo Starting Gunicorn.
    exec gunicorn settings.wsgi \
        --name walnut \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --timeout 120 \
        --log-level=info \
        --log-file=/usr/src/logs/gunicorn.log \
        --access-logfile=/usr/src/logs/access.log \
        --access-logformat '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' \
        "$@"
fi
