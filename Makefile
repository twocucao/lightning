.PHONY:  help test
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-30s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

pytest := PYTHONPATH=. poetry run pytest

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


start: ## test
	poetry run gunicorn -b 0.0.0.0:8080 --worker-class=gevent --reload lightning_plus.wsgi:application


test: ## run tests quickly with the default Python
	$(pytest)
