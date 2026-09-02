"""Airflow DAG for data ingestion."""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "data-team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


def scrape_news(**context):
    print("Scraping news from configured sources...")


with DAG(
    "news_ingestion",
    default_args=default_args,
    description="Ingest news articles",
    schedule_interval="*/30 * * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ingestion"],
) as dag:

    scrape_task = PythonOperator(
        task_id="scrape_news",
        python_callable=scrape_news,
    )
