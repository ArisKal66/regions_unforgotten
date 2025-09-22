import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("PostgresETL").getOrCreate()

data = [
    ("2025-01-01 10:00:00", "sub_001", 19.99, "mobile"),
    ("2025-01-01 11:00:00", "sub_002", 39.50, "web"),
    ("2025-01-02 12:00:00", "sub_001", 12.00, "store"),
]

columns = ["timestamp", "sub_id", "amount", "channel"]
df = spark.createDataFrame(data, columns)

pg_user = os.environ["POSTGRES_USER"]
pg_pass = os.environ["POSTGRES_PASSWORD"]
pg_db   = os.environ["POSTGRES_DB"]
pg_host = os.environ.get("POSTGRES_HOST", "postgres")
pg_port = os.environ.get("POSTGRES_PORT", "5432")

jdbc_url = f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_db}"

connection_props = {
    "user": pg_user,
    "password": pg_pass,
    "driver": "org.postgresql.Driver"
}

df.write.jdbc(
    url=jdbc_url,
    table="transactions",
    mode="overwrite",
    properties=connection_props
)

print("Data written to PostgreSQL!")
spark.stop()