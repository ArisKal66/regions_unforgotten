import psycopg2

try:
    conn = psycopg2.connect(
    host="localhost",
    database="sales_db",
    user="postgres",
    password="tragi60606"
    )
    print("Connected successfully")
    conn.close()
except Exception as e:
    print("Failed:", e)