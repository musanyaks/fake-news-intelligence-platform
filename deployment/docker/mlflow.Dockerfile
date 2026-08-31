FROM python:3.11-slim

WORKDIR /app

RUN pip install mlflow==2.8.0 psycopg2-binary==2.9.9 boto3==1.34.0

EXPOSE 5000

CMD mlflow server \
    --backend-store-uri $MLFLOW_BACKEND_STORE_URI \
    --default-artifact-root $MLFLOW_DEFAULT_ARTIFACT_ROOT \
    --host 0.0.0.0 \
    --port 5000
