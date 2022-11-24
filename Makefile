format:
	poetry run isort app
	poetry run black app

lint:
	poetry run pylint --django-settings-module=core.settings app
