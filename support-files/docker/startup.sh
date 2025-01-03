python manage.py migrate
python manage.py createcachetable django_cache
python manage.py plugin_init
supervisord -n