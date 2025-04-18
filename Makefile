SHELL := /bin/bash
PWD := $(shell pwd)

GIT_REMOTE = github.com/7574-sistemas-distribuidos/docker-compose-init

default: build

all:

deps:
	go mod tidy
	go mod vendor

build: deps
	GOOS=linux go build -o bin/client github.com/7574-sistemas-distribuidos/docker-compose-init/client
.PHONY: build

docker-image:
	docker build -f ./middleware/consumer/consumer.dockerfile --no-cache -t "consumer:latest" ./middleware/consumer
	docker build -f ./middleware/producer/producer.dockerfile --no-cache -t "producer:latest" ./middleware/producer

	docker build -f ./rabbitmq/rabbitmq.dockerfile --no-cache -t "rabbitmq:latest" ./rabbitmq

	docker build -f ./client/client.dockerfile --no-cache -t "client:latest" .

	docker build -f ./filters/twentieth_century/twentieth_century_filter.dockerfile --no-cache -t "twentieth_century_filter:latest" .
	docker build -f ./filters/arg_esp_production/arg_esp_production_filter.dockerfile --no-cache -t "arg_esp_production_filter:latest" .

	# Execute this command from time to time to clean up intermediate stages generated
	# during client build (your hard drive will like this :) ). Don't left uncommented if you
	# want to avoid rebuilding client image every time the docker-compose-up command
	# is executed, even when client code has not changed
	# docker rmi `docker images --filter label=intermediateStageToBeDeleted=true -q`
.PHONY: docker-image

docker-compose-up: docker-image
	docker compose -f docker-compose.yaml up -d --build --force-recreate
.PHONY: docker-compose-up

docker-compose-down:
	docker compose -f docker-compose.yaml stop -t 1
	docker compose -f docker-compose.yaml down
.PHONY: docker-compose-down

docker-compose-logs:
	docker compose -f docker-compose.yaml logs -f
.PHONY: docker-compose-logs
