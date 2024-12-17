push:
	git add . && codegpt commit . && git push

setup:
	virtualenv .venv -p python3.10
	./.venv/bin/pip install pip-tools

install:
	./.venv/bin/pip-compile ./requirements/requirements.txt \
							./requirements/requirements-dev.txt \
							./requirements/requirements-ops.txt \
							./requirements/requirements-extra.txt \
							-v --output-file ./requirements.txt
	./.venv/bin/pip-sync -v

i18n:
	python manage.py makemessages -l zh_Hans
	python manage.py makemessages -l en
	python manage.py compilemessages

migrate:
	python manage.py makemigrations
	python manage.py migrate

collect-static:
	python manage.py collectstatic --noinput

setup-dev-user:
	DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=admin@example.com DJANGO_SUPERUSER_PASSWORD=password python manage.py createsuperuser --noinput


dev:
	daphne -b 0.0.0.0 -p 8001 core.asgi:application

run:
	gunicorn -w 4 -b 0.0.0.0:8001 asgi:application -k uvicorn.workers.UvicornWorker

clean-migrate:
	cd apps &&\
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete &&\
	find . -path "*/migrations/*.pyc"  -delete

init-buckets:
	python manage.py initialize_buckets

celery:
	celery -A common.celery worker -B --loglevel=info --pool threads

celery-inspect:
	celery -A common.celery inspect scheduled

celery-flower:
	celery -A common.celery flower
