.PHONY: lint
lint:  # Lints our code.
	python -m pylint ./

.PHONY: black
black:  # Formats our code.
	python -m black ./

.PHONY: refactor
refactor:  # Refactor our code.
    black lint

.PHONY: test
test:  # Runs tests.
	python -m pytest tests

# Set the image name
IMAGE_NAME := object-detection-lambda
TAG := latest

# Targets
.PHONY: docker-build
docker-build:
	docker build -t $(IMAGE_NAME):$(TAG) .

.PHONY: docker-run
docker-run:
	docker run -it --rm $(IMAGE_NAME):$(TAG)
