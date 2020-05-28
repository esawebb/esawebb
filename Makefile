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

test:
	docker exec -it hubble ./manage.py test

statics:
	docker exec -it hubble ./manage.py collectstatic --noinput

makemessages:
	docker exec -it hubble django-admin makemessages

compilemessages:
	docker exec -it hubble django-admin compilemessages
