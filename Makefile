bash:
	docker exec -it hubble bash

shell:
	docker exec -it hubble ./manage.py shell

makemigrations:
	docker exec -it hubble ./manage.py makemigrations

migrate:
	docker exec -it hubble ./manage.py migrate

initialfixture:
	docker exec -it hubble ./manage.py loaddata initial

demofixture:
	docker exec -it hubble ./manage.py loaddata demo

missingmigrations:
	docker exec -it hubble ./manage.py makemigrations payment app_plugins django_mailman tieredweight

test:
	docker exec -it hubble coverage run manage.py test --no-input

test-and-report: test cov-report

cov-report:
	docker exec -it hubble coverage report -m

cov-report-html:
	docker exec -it hubble coverage html

statics:
	docker exec -it hubble ./manage.py collectstatic --noinput

makemessages:
	docker exec -it hubble django-admin makemessages

compilemessages:
	docker exec -it hubble django-admin compilemessages
