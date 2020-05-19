# Asynchronous Scraping Tasks with Redis, Celery.

Run task monitor:

```sh
$ python manage.py migrate
$ python manage.py runserver
```

Run celery to handle tasks:

```sh
$ celery worker --app=core --loglevel=info --logfile=logs/celery.log
```

Open your browser to http://localhost:8000 to monitor scraping tasks and create new one.
