#NAME ?= etchi17

all: build run push

images:
	docker images | grep etchi17

ps:
	docker ps -a | grep etchi17

build:
	docker build -t etchi17/iss-sighting-location:midterm .

run:
	docker run --name "iss-sighting-location" -d -p 5007:5000 etchi17/iss-sighting-location:midterm

push:
	docker push etchi17/iss-sighting-location:midterm
