run:
	python -m robyn dev.py --dev

black:
	black app

lint:
	ruff check app

test:
	pytest app/tests