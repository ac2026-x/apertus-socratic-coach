FROM python:3.11-slim

WORKDIR /app

# Copy dependency list and code
COPY track_2b/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "track_2b/app.py", "--server.port=8501", "--server.address=0.0.0.0"]