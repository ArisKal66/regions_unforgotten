from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pyodbc
import pandas as pd

def extract_transform_load():
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={MSSQL_HOST},{MSSQL_PORT};"
        f"DATABASE={MSSQL_DB};"
        f"UID={MSSQL_USER};PWD={MSSQL_PASSWORD};"
        f"Encrypt=no;"
    )

    with pyodbc.connect(conn_str) as conn:
        query = "SELECT TOP 10 * FROM Customers;"
        df = pd.read_sql(query, conn)
        df["CompanyName"] = df["CompanyName"].str.upper()
        df.to_csv("/opt/airflow/dags/output/customers.csv", index=False)
        print("ETL complete, data saved to output/customers.csv")

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="northwind_etl",
    start_date=datetime(2025, 10, 6),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["sqlserver", "northwind"],
) as dag:

    etl_task = PythonOperator(
        task_id="extract_transform_load",
        python_callable=extract_transform_load,
    )

    etl_task