# Spark ETL with PostgreSQL and pgAdmin (Dockerized)

## Project Overview
This project demonstrates an **ETL pipeline** using **Apache Spark** to process sample data and load it into a **PostgreSQL database** running inside Docker.  
Additionally, **pgAdmin** is provided as a web interface to inspect the database.  

The stack:
- **Apache Spark** (PySpark, running inside Docker)
- **PostgreSQL 15**
- **pgAdmin 4**
- **Docker (Desktop) + docker-compose**
- **Python 3.9**


## Features
- Read and transform mock transaction data with Spark
- Write results into a PostgreSQL table using JDBC
- Manage PostgreSQL with pgAdmin in a browser
- Environment variables are used to securely pass credentials


## Project Structure
```
├── app/
│ ├── spark_job.py # Main Spark ETL job
│ └── requirements.txt # Python dependencies
├── docker/
│ ├── Dockerfile # Spark container definition
│ └── docker-compose.yml # Multi-container setup
│ └── .env # Environment variables (not committed to Git)
├── .gitignore # Ignore credentials & local files
└── README.md # Project documentation
```

## Set up environment variables
- Create a `.env` file in the /docker directory

## Start containers
```bash
docker-compose -f docker/docker-compose.yml up --build
```

## Run the Spark ETL job
The Spark container will automatically run `spark_job.py`:

- Generate mock transactions
- Write them into PostgreSQL table transactions

## Access the Services
- **PostgreSQL** → `localhost:5432`
- **pgAdmin** → `http://localhost:5050`
- Login with `PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD` from `.env`
