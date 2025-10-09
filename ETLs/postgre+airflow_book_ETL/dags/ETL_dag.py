from datetime import datetime, timedelta
from airflow import DAG

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 10, 9),
    'retries': 1,
    'retry_delay': timedelta(minutes=10),
}

dag = DAG(
    'load_DE_books_from_Amazon',
    default_args=default_args,
    description='fetching and loading in postgres',
    schedule=timedelta(days=1),
    catchup=False
)