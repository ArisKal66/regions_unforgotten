FROM bitnami/spark:3.5.0

COPY ../jars/postgresql-42.7.8.jar /opt/spark/jars/

WORKDIR /app

COPY ../app /app



# COPY ../requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt