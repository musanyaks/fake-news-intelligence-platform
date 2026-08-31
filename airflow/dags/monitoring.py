"""Airflow DAG for model monitoring and drift detection."""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator

default_args = {
    "owner": "ml-team",
    "depends_on_past": False,
    "email": ["ml-ops@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def run_drift_detection(**context):
    """Run Evidently drift detection."""
    import subprocess
    result = subprocess.run(
        ["python", "-m", "evidently", "run", "--config", "monitoring/evidently/drift_config.yaml"],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        raise RuntimeError(f"Drift detection failed: {result.stderr}")


def check_model_performance(**context):
    """Check if model performance is within thresholds."""
    import requests
    response = requests.get("http://api:8000/api/v1/model/metrics")
    metrics = response.json()
    
    if metrics.get("accuracy", 0) < 0.85:
        raise RuntimeError(f"Model accuracy {metrics['accuracy']} below threshold 0.85")
    
    print(f"Model performance OK: accuracy={metrics['accuracy']}")


with DAG(
    "model_monitoring",
    default_args=default_args,
    description="Monitor model performance and data drift",
    schedule_interval="0 6 * * *",  # Daily at 6 AM
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["monitoring", "ml"],
) as dag:

    check_performance = PythonOperator(
        task_id="check_model_performance",
        python_callable=check_model_performance,
    )

    drift_detection = PythonOperator(
        task_id="run_drift_detection",
        python_callable=run_drift_detection,
    )

    alert_slack = SimpleHttpOperator(
        task_id="alert_slack",
        http_conn_id="slack_webhook",
        endpoint="",
        method="POST",
        headers={"Content-Type": "application/json"},
        data='{"text": "Model monitoring check completed"}',
    )

    check_performance >> drift_detection >> alert_slack
