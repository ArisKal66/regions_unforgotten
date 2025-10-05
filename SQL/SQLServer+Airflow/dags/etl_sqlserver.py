from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import pyodbc
import os

SQLSERVER_CONN = {
    "server": "sqlserver",
    "database": os.getenv("MSSQL_DB", "Northwind"),
    "username": "sa",
    "password": os.getenv("MSSQL_SA_PASSWORD")
}

def extract_orders():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SQLSERVER_CONN['server']};"
        f"DATABASE={SQLSERVER_CONN['database']};"
        f"UID={SQLSERVER_CONN['username']};"
        f"PWD={SQLSERVER_CONN['password']}"
    )
    conn = pyodbc.connect(conn_str)
    query = """
        SELECT o.order_id, c.company_name, o.order_date, od.unit_price, od.quantity
        FROM orders o
        JOIN order_details od ON o.order_id = od.order_id
        JOIN customers c ON o.customer_id = c.customer_id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df.to_dict(orient="records")

def transform_sales(**context):
    records = context['ti'].xcom_pull(task_ids="extract_orders")
    df = pd.DataFrame(records)
    df["Total"] = df["unit_price"] * df["quantity"]
    summary = df.groupby("company_name")["Total"].sum().reset_index()
    return summary.to_dict(orient="records")

def load_sales(**context):
    records = context['ti'].xcom_pull(task_ids="transform_sales")
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SQLSERVER_CONN['server']};"
        f"DATABASE={SQLSERVER_CONN['database']};"
        f"UID={SQLSERVER_CONN['username']};"
        f"PWD={SQLSERVER_CONN['password']}"
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("""
    IF OBJECT_ID('salespercustomer', 'U') IS NULL
    CREATE TABLE salespercustomer (
        company_name NVARCHAR(100),
        total DECIMAL(18,2)
    )
    """)
    conn.commit()

    cursor.execute("DELETE FROM salespercustomer")  # overwrite
    for row in records:
        cursor.execute(
            "INSERT INTO salespercustomer (company_name, Total) VALUES (?, ?)",
            row['company_name'], row['Total']
        )
    conn.commit()
    conn.close()

with DAG(
    dag_id="northwind_etl",
    start_date=datetime(2025, 10, 3),
    schedule=None,
    catchup=False
) as dag:

    extract_orders_task = PythonOperator(
        task_id="extract_orders",
        python_callable=extract_orders
    )

    transform_sales_task = PythonOperator(
        task_id="transform_sales",
        python_callable=transform_sales,
        provide_context=True
    )

    load_sales_task = PythonOperator(
        task_id="load_sales",
        python_callable=load_sales,
        provide_context=True
    )

    extract_orders_task >> transform_sales_task >> load_sales_task