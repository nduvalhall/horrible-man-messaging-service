install:
	poetry install --no-root

dev:
	poetry run python src/run.py

docker.build:
	docker build --tag horrible-man-messaging-service-api:latest .

docker.run:
	docker run --rm -it -d --name api --network host horrible-man-messaging-service-api:latest