run:
	docker build -t scaffold-ai .
	docker run -p 8501:8501 --env-file track_2b/.env scaffold-ai

test:
	python track_2b/evaluate.py