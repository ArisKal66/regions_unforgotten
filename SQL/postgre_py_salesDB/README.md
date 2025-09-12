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
1. PostgreSQL 16 (older versions should be ok though)
2. Python 3.13
  Python Libraries:
    - psycopg2 (inserting data on SQL server)
    - faker (mock data generation)

**Proceeding with DB creation/ingestion:**
```sql
CREATE DATABASE sales_db;
```

**Tables creation from `schema.sql`:**
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

**Fake (mock) data generation:**
```bash
python fake_data_generation.py
```

**Example Queries:**
1. Total Revenue by Product Category
```sql
SELECT
    p.category,
    SUM(fs.total_amount) AS total_rev_per_categ
FROM
    fact_sales fs
JOIN products p ON fs.product_id = p.product_id
GROUP BY p.category
ORDER BY total_rev_per_categ DESC;
```
<img width="268" height="90" alt="image" src="https://github.com/user-attachments/assets/fed5358a-4b80-4c86-b7c3-d2671871d54a" />


2. Ranking Stores by Sales per Month
```sql
SELECT
    c.customer_id,
    SUM(fs.total_amount) AS total_rev_per_cust
FROM
    fact_sales fs
JOIN customers c ON fs.customer_id = c.customer_id
GROUP BY c.customer_id
ORDER BY total_rev_per_cust DESC
LIMIT 5;
```

