# SQL Server & Apache Airflow
## Components
Based on the respective `.yml` file the images used are the following:
    - mssql/server:2022-latest
    - apache/airflow:2.8.1

Aim of this project is to experiment with Microsoft's native SQL Server, create DAG oriented task flows with Airflow, while using existing Northwind commercial data.

## First Steps + Troubleshooting

As usual, creating `docker-compose.yml`, and building up virtual containers:
```bash
docker-compose -f docker-compose.yml up --build
```

Had some issues with the limitations of `MSSQL_SA_PASSWORD` residing in `.env` file, but everything worked out after examining generated logs:
```bash
docker ps -a
docker logs sqlserver
```

Decided to use SQL Server's cmd manually, e.g. creating the database loading records, in order to focus on debugging.

Using PowerShell in the respective folder:
```bash
docker exec -it sqlserver /opt/mssql-tools/bin/sqlcmd `
   -S localhost -U sa -P ${MSSQL_SA_PASSWORD} `
   -Q "CREATE DATABASE Northwind;"
```

Got the following error message:
```bash
OCI runtime exec failed: exec failed: unable to start container process: exec: "/opt/mssql-tools/bin/sqlcmd": stat /opt/mssql-tools/bin/sqlcmd: no such file or directory: unknown
```

Needed to take a deep dive and use bash inside the container:
```bash
docker exec -it sqlserver /bin/bash
ls /opt
```

Figured out that instead of `/mssql-tools/` I should have used `/mssql-tools18/`.
The next issue occured by the required encryption verification, but since this container is running locally, the recommended solution was to disable it:
```bash
docker exec -it sqlserver /opt/mssql-tools/bin/sqlcmd `
   -S localhost -U sa -P ${MSSQL_SA_PASSWORD} `
   -C
```
In a production scenario, I should use a valid SSL certificate.

After finally using MS SQL Server's cmd, proceeded with the creation of the database:
```sql
CREATE DATABASE Northwind;
GO
```

Confirming it was created:
```sql
SELECT name FROM sys.databases;
GO
```
console output:
```bash
name
-----------------------
master
tempdb
model
msdb
Northwind
```

The next step is about loading the `northwind.sql` data on SQL Server, from the project's root directory:
```bash
docker cp ./data/northwind.sql SQLserver:/tmp/northwind.sql
docker exec -it sqlserver /opt/mssql-tools/bin/sqlcmd `
   -S localhost -U sa -P ${MSSQL_SA_PASSWORD} `
   -C `
   -i /tmp/northwind.sql
```

During loading of the data, I got a bunch of `Incorrect syntax near...` messages that needed further investigation, as no Tables/Objects where generated within the database.
The issue in this case was in the nature of an non-MSSQL-Server-ready database, so I found one over @ [Microsoft's GitHub](https://github.com/microsoft/sql-server-samples/blob/master/samples/databases/northwind-pubs/instnwnd.sql).

In order to re-initiate the process, and confirm that the most recent `.sql` file is ready for the project:
```bash
docker-compose down -v

docker-compose up -d

docker exec -it sqlserver /opt/mssql-tools/bin/sqlcmd `
   -S localhost -U sa -P ${MSSQL_SA_PASSWORD} `
   -C `
   -Q "USE Northwind; :r /docker-entrypoint-initdb.d/instnwnd.sql"
```

```sql
USE Northwind;
GO
SELECT TABLE_SCHEMA, TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE';
GO
```