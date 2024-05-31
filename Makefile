.PHONY: run test

run:
	poetry run python neptunseye/main.py

test:
	pytest tests/
