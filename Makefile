.PHONY: build run stop test

# Build Docker container
build:
	docker build -t apertus-socratic-coach .

# Run Docker container as required by Hack Apertus judging harness
run: build
	docker run -p 8501:8501 --env-file track_2b/.env apertus-socratic-coach

# Run offline evaluation suite inside container
test: build
	docker run --env-file track_2b/.env apertus-socratic-coach python evaluate.py