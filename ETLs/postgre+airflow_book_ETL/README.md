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

After everything is set-up, the `docker-compose.yaml` fetched earlier, should be in the project's root folder, while variable `AIRFLOW_UID` of the `.env` file should be assigned.

In hindsight the project should be consisted by multiple instances of powershell terminals, and the first docker-oriented prompts in the project's root folder are the following:
```
docker compose up airflow-init
docker compose up -d
```

By the time that message `airflow-init-1 exited with code 0` pops-up and the first `dag_processor` generated logs start appearing, it seems that the process is initiated.