.PHONY: build run run-env shell dev stop clean logs python

# Variables
IMAGE_NAME = raspberry-experiments
CONTAINER_NAME = rpi-experiments

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the container
run:
	docker run --rm --name $(CONTAINER_NAME) $(IMAGE_NAME)

# Run the container with environment variables
run-env:
	docker run --rm --name $(CONTAINER_NAME) --env-file .env $(IMAGE_NAME)

run-local:
	python3 main.py

# Run the container interactively
shell:
	docker run --rm -it --name $(CONTAINER_NAME) $(IMAGE_NAME) /bin/bash

# Run the container with volume mount for development
dev:
	docker run --rm -it --name $(CONTAINER_NAME) \
		-v $(PWD):/app \
		--env-file .env \
		$(IMAGE_NAME) /bin/bash

# Stop the container
stop:
	docker stop $(CONTAINER_NAME) || true

# Remove the container
clean:
	docker rm $(CONTAINER_NAME) || true
	docker rmi $(IMAGE_NAME) || true

# Show logs
logs:
	docker logs $(CONTAINER_NAME)

# Run Python shell in container
python:
	docker run --rm -it --name $(CONTAINER_NAME) $(IMAGE_NAME) python3

