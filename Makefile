PYTHON_MODULES := dbpool.py test_pool.py

DEFAULT_ENV := py34

default: test
shell:
	.tox/$(DEFAULT_ENV)/bin/python -i
check: test
check-style:
	pep8 --repeat --ignore=E202,E501,E402 --exclude="*_pb2.py" $(PYTHON_MODULES)
	pylint -E --ignore-patterns=".*_pb2.py" $(PYTHON_MODULES)
test: check-style

.PHONY: default shell tox check check-style test
