FROM apache/airflow:2.7.3-python3.11

USER root
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

USER airflow
COPY pyproject.toml /opt/airflow/
RUN pip install --no-cache-dir -e /opt/airflow/

ENV PYTHONPATH=/opt/airflow
