# Data Engineering Pipeline
## Requirements (invoked in docker yaml file)
    - Docker Desktop
    - Apache Airflow 3.1.0
    - PostgreSQL 16
    - PGadmin 4

## Preparation

To deploy Airflow on Docker Compose, you should fetch [docker-compose.yaml](https://airflow.apache.org/docs/apache-airflow/3.1.0/docker-compose.yaml).
This file contains several service definitions:

    -airflow-scheduler - The scheduler monitors all tasks and Dags, then triggers the task instances once their dependencies are complete.

    -airflow-dag-processor - The Dag processor parses Dag files.

    -airflow-api-server - The api server is available at http://localhost:8080.

    -airflow-worker - The worker that executes the tasks given by the scheduler.

    -airflow-triggerer - The triggerer runs an event loop for deferrable tasks.

    -airflow-init - The initialization service.

    -postgres - The database.

    -redis - The redis - broker that forwards messages from scheduler to worker.

### Directory components
The installation, configuration and deployment of containers should take place on a virtual environment:
Most of the times on Windows machines, the user should update policies to create and activate virtual environment. The virtual environmeent in this case may not make too much sense, but it's a good practice after all.
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
python -m venv venv
.\venv\Scripts\activate
```

Create the following folders, while making sure your user(s) are able to read/write:

```bash
mkdir dags,logs,plugins,config
```

After everything is set-up, the `docker-compose.yaml` fetched earlier should be in the project's root folder, while variable `AIRFLOW_UID` of the `.env` file should be assigned.
Additionally ports of `postgres` & `pgadmin` should be assigned, with some attention to not create conflicts among other running/generated containers.
<img width="621" height="851" alt="image" src="https://github.com/user-attachments/assets/a292fba2-26f6-455a-ad9e-5bca6d487a0b" />


In hindsight, the project should be consisted by multiple instances of powershell terminals, and the first docker-oriented prompts in the project's root folder are the following:
```
docker compose up airflow-init
docker compose up -d
```

By the time that message `airflow-init-1 exited with code 0` pops-up and the first `dag_processor` generated logs start appearing, it seems that the process is initiated.
<img width="1915" height="1080" alt="image" src="https://github.com/user-attachments/assets/476ac6a5-e54b-4e2b-b9d8-5a2d78685f16" />

## Server/Network connections

### PGadmin connection:
After logging in successfully to `http://localhost:8080/` for Airflow and `http://localhost:5052/browser/` for pg admin, a new Server should be added using the respective IP of the postgres SQL server in `Host Name/Adress` box of Connection Tab:
    - Examining existing images with `docker container ls`
    - `docker inspect <postgres-container-id>`
    - Something similar should be printed on terminal:
<img width="803" height="418" alt="image" src="https://github.com/user-attachments/assets/5f318d7f-208f-45f0-92ff-8ee388354f2f" />

Using the postgres assigned credentials (in this case stored in `.env` file, the connection is established. The next step is to create a dedicated database for the ETL process.
<img width="1908" height="612" alt="image" src="https://github.com/user-attachments/assets/797bb5ed-bb42-41d0-84a2-063cd96798c5" />

### Airflow connection:

After logging in to Airflow through `http://localhost:8080/`, the connection is assigned by clicking on `Admin -> Add Connection ->...`, while filling the necessary info:
<img width="1906" height="1005" alt="image" src="https://github.com/user-attachments/assets/eeed60de-115e-4c52-b207-dd87e8843ebb" />

After completing this step, it's high time to start working on the DAG file using `Pytrhon`!
