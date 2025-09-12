# **Sales Data Analytics with SQL**
## Project Overview
```
This project simulates a retail sales data warehouse using a Star Schema in PostgreSQL.
It includes:

Database schema design (fact + dimension tables)

Mock data generation with Python + Faker library

Advanced SQL queries for analytics and reporting

The goal is to demonstrate SQL expertise in data modeling, ETL, and analytical querying
```

## Database Schema
The database follows a Star Schema design:
```
              +-----------------+
              |    customers    |
              +-----------------+
                      |
                      |
              +-----------------+
              |    fact_sales   |
              +-----------------+
              | customer_id     |
              | product_id      |
              | store_id        |
              | date_id         |
              | quantity_sold   |
              | total_amount    |
              +-----------------+
             /           |         \
            /            |          \
+---------------+ +---------------+ +---------------+
|   products    | |    stores     | |    dates      |
+---------------+ +---------------+ +---------------+
```
## Implementation/Execution
### Requirments:
1. PostgreSQL 16
2. Python 3.13
  Python Libraries:
    - psycopg2 (insert data on SQL server)
    - faker (to generate mock data)

Proceeding with DB creation:
```sql
CREATE DATABASE sales_db;
```

Tables creation from `schema.sql`:
```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    full_name TEXT,
    gender CHAR(1),
    age INT,
    email TEXT
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price DECIMAL(10,2)
);

CREATE TABLE stores (
    store_id SERIAL PRIMARY KEY,
    store_location TEXT,
    manager_name TEXT
);

CREATE TABLE dates (
  date_id SERIAL PRIMARY KEY,
  date DATE,
  d_o_week TEXT, --weekday
  month TEXT,
  year INT
);

-- fact table
CREATE TABLE fact_sales (
    sale_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    product_id INT REFERENCES products(product_id),
    store_id INT REFERENCES stores(store_id),
    date_id INT REFERENCES dates(date_id),
    quantity_sold INT,
    total_amount DECIMAL(10,2)
);
```
