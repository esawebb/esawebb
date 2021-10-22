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

fasttest:
	docker exec -it hubble coverage run --rcfile=.coveragerc-parallel manage.py test --no-input --keepdb --parallel --failfast

test:
	docker exec -it hubble coverage run manage.py test --no-input

test-and-report: test cov-report

fast-and-report: fasttest cov-combine-report

cov-report:
	docker exec -it hubble coverage report

cov-report-html:
	docker exec -it hubble coverage html

cov-combine-report:
	docker exec -it hubble coverage combine
	docker exec -it hubble coverage report

statics:
	docker exec -it hubble ./manage.py collectstatic --noinput

makemessages:
	docker exec -it hubble django-admin makemessages

compilemessages:
	docker exec -it hubble django-admin compilemessages

sass:
	node-sass ./components/scss/hubble.scss ./spacetelescope/static/css/hubble.css

