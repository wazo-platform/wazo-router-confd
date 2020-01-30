.PHONY:
venv:
	virtualenv -p python3.7 venv --no-site-packages

.PHONY: setup
setup:
	pip install -r requirements.txt
	pip install --editable .

.PHONY: dist
dist:
	python3 setup.py sdist bdist_wheel

.PHONY: clean
clean:
	rm -fr build dist *.egg-info

.PHONY: black
black:
	black --skip-string-normalization wazo_router_confd *.py

.PHONY: black-check
black-check:
	black --check --skip-string-normalization wazo_router_confd *.py

.PHONY: flake8
flake8:
	flake8 --ignore=E501,E402,W503 wazo_router_confd

.PHONY: mypy
mypy:
	mypy wazo_router_confd

.PHONY: pylint
pylint:
	pylint wazo_router_confd

.PHONY: pycodestyle
pycodestyle:
	pycodestyle --ignore=E501,W503,E402,E701 wazo_router_confd

.PHONY: check
check: black-check flake8 mypy pylint pycodestyle

.PHONY: test
test:
	py.test -p no:warnings

.PHONY: coverage
coverage:
	coverage run -m py.test -p no:warnings
	coverage report
	coverage html
	coverage xml

.PHONY: dockerfile
dockerfile:
	docker build -t wazopbx/wazo-router-confd:latest .

.PHONY: start-auth
start-auth:
	docker-compose -f docker-compose.wazo-auth.yaml -f docker-compose.yaml up -d

.PHONY: stop-auth
stop-auth:
	docker-compose -f docker-compose.wazo-auth.yaml -f docker-compose.yaml down
