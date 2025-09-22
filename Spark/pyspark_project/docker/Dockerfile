# 1. Use Spark image as base
FROM bitnami/spark:3.5.0

# 2. Copy requirements.txt and install extra Python libs
COPY app/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 3. Copy application code and folders
COPY app /app
COPY data /app/data
COPY output /app/output

# 4. Set working directory inside the container
WORKDIR /app

# 5. Default command: run Spark job
CMD ["spark-submit", "spark_job.py"]