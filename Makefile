prod-up:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-up-build:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

dev-up-build:
	docker compose -f docker-compose.yml -f docker-compose.devserver.yml up -d --build

# Press Ctrl + Z to make it a background process, but "exit" finishes the process instead of logout
prod-up-attached:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up

prod-up-build-attached:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build

prod-stop:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml stop

dev-stop:
	docker compose -f docker-compose.yml -f docker-compose.devserver.yml stop

reload-nginx:
	docker exec -it webb-nginx service nginx reload

bash:
	docker exec -it webb bash

shell:
	docker exec -it webb ./manage.py shell

makemigrations:
	docker exec -it webb ./manage.py makemigrations

migrate:
	docker exec -it webb ./manage.py migrate

initialfixture:
	docker exec -it webb ./manage.py loaddata initial

demofixture:
	docker exec -it webb ./manage.py loaddata demo

missingmigrations:
	docker exec -it webb ./manage.py makemigrations payment app_plugins django_mailman tieredweight

fasttest:
	docker exec -it webb coverage run --rcfile=.coveragerc-parallel manage.py test --no-input --keepdb --parallel --failfast

testtag:
	docker exec -it webb ./manage.py test --noinput --tag=$(tag)

testapp:
	docker exec -it webb ./manage.py test $(app) --noinput -v 3

test:
	docker exec -it webb coverage run manage.py test --no-input

test-and-report: test cov-report

fast-and-report: fasttest cov-combine-report

cov-report:
	docker exec -it webb coverage report

cov-report-html:
	docker exec -it webb coverage html

cov-combine-report:
	docker exec -it webb coverage combine
	docker exec -it webb coverage report

statics:
	docker exec -it webb ./manage.py collectstatic --noinput

makemessages:
	docker exec -it webb django-admin makemessages

compilemessages:
	docker exec -it webb django-admin compilemessages

sass:
	node-sass ./components/scss/webb.scss ./webb/static/css/webb.css

youtube-token:
	docker exec -it webb python ./scripts/youtube-token.py

init:
	test -n "$(name)"
	rm -rf ./.git
	find ./ -type f -exec perl -pi -e 's/webb/$(name)/g' *.* {} \;
	mv ./webb ./$(name)
