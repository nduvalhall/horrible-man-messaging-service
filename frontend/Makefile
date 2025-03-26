install:
	npm install
	
dev:
	npx vite dev

docker.build:
	docker build --tag horrible-man-messaging-service-frontend:latest .

docker.run:
	docker run --rm -it -d --name frontend --network host horrible-man-messaging-service-frontend:latest