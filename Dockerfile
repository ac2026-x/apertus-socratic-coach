FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy track_2b codebase
COPY track_2b/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY track_2b/ /app/

# Expose Streamlit default port
EXPOSE 8501

ENV PYTHONUNBUFFERED=1

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]