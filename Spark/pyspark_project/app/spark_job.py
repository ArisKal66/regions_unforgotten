from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum

spark = SparkSession.builder \
    .appName("PySparkETL") \
    .getOrCreate()

df = spark.read.options(header='True').options(inferSchema='True').csv("data/big_data.csv")

agg_df = df.groupBy("channel").agg(_sum("amount").alias("total_revenue"))
agg_df.write.mode("overwrite").parquet("output/revenue_by_channel.parquet")

agg_df.show()
spark.stop()