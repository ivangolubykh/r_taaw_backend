.PHONY: help test test-cov coverage translations migrate makemigrations createsuperuser

# Include optional local overrides
-include Makefile.local

help:
	@echo "Available commands:"
	@echo "  make test               - Run tests only (with colored output)"
	@echo "  make test-cov           - Run tests and show coverage report (terminal)"
	@echo "  make coverage           - Show coverage report from last run"
	@echo "  make translations       - Generate translations for all supported languages"
	@echo "  make migrate            - Apply migrations"
	@echo "  make makemigrations     - Create new migrations"
	@echo "  make createsuperuser    - Create a superuser"

test:
	bash scripts/test.sh

test-cov:
	bash scripts/test.sh
	bash scripts/coverage.sh

coverage:
	bash scripts/coverage.sh

translations:
	bash scripts/make_translations.sh

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

createsuperuser:
	python manage.py createsuperuser
