push:
	git add . && codegpt commit . && git push

setup:
	virtualenv .venv -p python3.10
	./.venv/bin/pip install pip-tools

install:
	./.venv/bin/pip-compile ./requirements/requirements-core.txt \
							./requirements/requirements-dev.txt \
							./requirements/requirements-ops.txt \
							./requirements/requirements-extra.txt \
							-v --output-file ./requirements.txt
	./.venv/bin/pip-sync -v

win-install:
	.\.venv\Scripts\pip-compile.exe ./requirements/requirements-core.txt ./requirements/requirements-dev.txt ./requirements/requirements-ops.txt  ./requirements/requirements-extra.txt -v --output-file ./requirements.txt
	.\.venv\Scripts\pip-sync.exe -v	

migrate:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py createcachetable django_cache

setup-dev-user:
	DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=admin@example.com DJANGO_SUPERUSER_PASSWORD=password python manage.py createsuperuser --noinput

i18n:
	python manage.py makemessages -l zh_Hans
	python manage.py makemessages -l en
	python manage.py compilemessages

collect-static:
	python manage.py collectstatic --noinput

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
	celery -A apps.core.celery worker -B --loglevel=info --pool threads

celery-inspect:
	celery -A apps.core.celery inspect scheduled

celery-flower:
	celery -A apps.core.celery flower

start-nats:
	python manage.py nats_listener

release:
	rm -Rf ./dist
	pyarmor cfg data_files="*"
	pyarmor cfg package_name_format megalab
	pyarmor cfg optimize 2
	pyarmor gen \
		--platform linux.x86_64 \
		--platform darwin.x86_64 \
		--platform darwin.aarch64 \
		--platform windows.x86_64 \
		--enable-jit \
		--mix-str -O ./dist -r --exclude "*.venv"  .
		
	# pyarmor gen --outer \
	# 	--platform windows.x86_64 \
	# 	--platform linux.x86_64 \
	# 	--platform darwin.x86_64 \
	# 	--mix-str -O ./dist -r --exclude "*.venv"  . 

hdinfo:
	python -m pyarmor.cli.hdinfo 

gen-license:
	pyarmor gen key -e 1