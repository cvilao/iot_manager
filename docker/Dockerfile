# Dockerfile to serve MLflow model with FastAPI
FROM python:3.10-slim
WORKDIR /app
COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ../bin/publish.py ./bin/app.py
CMD ["uvicorn", "evaluation.app:app", "--host", "0.0.0.0", "--port", "8080"]
