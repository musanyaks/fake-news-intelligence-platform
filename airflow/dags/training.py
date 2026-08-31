"""Airflow DAG for model training."""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "ml-team",
    "depends_on_past": False,
    "email_on_failure": True,
    "email": ["ml-ops@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "model_training",
    default_args=default_args,
    description="Retrain fake news detection model",
    schedule_interval="0 2 * * 0",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ml", "training"],
) as dag:

    preprocess = BashOperator(
        task_id="preprocess_data",
        bash_command="python -m src.pipelines.batch_pipeline",
    )

    train = BashOperator(
        task_id="train_model",
        bash_command="python training/train.py --data data/processed/train.csv",
    )

    evaluate = BashOperator(
        task_id="evaluate_model",
        bash_command="python -m src.evaluation.evaluator",
    )

    preprocess >> train >> evaluate
