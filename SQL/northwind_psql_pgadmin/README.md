# **Northwind Analytics with SQL**

## Project Overview
```
This project is using retail sales data from the commonly used Northwind data, added on PostgreSQL and mounted on pgAdmin.

                  List of relations
 Schema |          Name          | Type  |   Owner
--------+------------------------+-------+------------
 public | categories             | table | admin_aris
 public | customer_customer_demo | table | admin_aris
 public | customer_demographics  | table | admin_aris
 public | customers              | table | admin_aris
 public | employee_territories   | table | admin_aris
 public | employees              | table | admin_aris
 public | order_details          | table | admin_aris
 public | orders                 | table | admin_aris
 public | products               | table | admin_aris
 public | region                 | table | admin_aris
 public | shippers               | table | admin_aris
 public | suppliers              | table | admin_aris
 public | territories            | table | admin_aris
 public | us_states              | table | admin_aris
```

After running the docker images defined in `docker-compose.yml`, the user should login to pgAdmin through browser on defined local host, using the UI `right-click on Servers → Register → Server…` and then respectively updating the General and Connection tabs.

<img width="1916" height="844" alt="image" src="https://github.com/user-attachments/assets/1f9971a7-4749-47ac-b1d0-58892286d620" />

## Sample Queries:

### 1. Using a plethora of filters on certain column

```sql
SELECT employee_id, last_name, first_name, city
FROM employees
WHERE city IN ('Tacoma', 'Kirkland', 'Seattle');
```

<img width="1915" height="895" alt="image" src="https://github.com/user-attachments/assets/4e2d7c0d-4fc3-48d9-8488-3c03b28639d5" />

### 2. Using wildcard filtering
```sql
SELECT employee_id, last_name, first_name, city
FROM employees
WHERE first_name LIKE 'A%';
```
<img width="1912" height="914" alt="image" src="https://github.com/user-attachments/assets/7fbe8de9-5d5d-4bdb-af12-2fe41b01094a" />

### 3. Aggregations & Sorting
```sql
SELECT country, city, COUNT(*) Num_Customers_per_city
FROM customers
GROUP BY country, city
ORDER BY Num_Customers_per_city DESC;
```
<img width="1906" height="989" alt="image" src="https://github.com/user-attachments/assets/41064608-ae26-4215-b15f-cb72d1129734" />

### 4. Aggregated query & "HAVING" condition
```sql
SELECT ship_country, ship_city, COUNT(*) orders_count
FROM orders
GROUP BY ship_country, ship_city
HAVING COUNT(*) > 10
ORDER BY ship_country, orders_count DESC;
```
<img width="1915" height="911" alt="image" src="https://github.com/user-attachments/assets/50f5f058-769c-477b-8050-40d7c3ef8e4f" />

### 5. Column Calculations/Concatenations, Joins, multiple "WHERE" conditions
Concept: Evaluate delayed orders, find responsible employee, include customer data for possible compensation 
```sql
SELECT o.order_id, (o.required_date - o.order_date) AS dategap, (o.required_date - o.shipped_date) AS ship_gap, 
(o.shipped_date - o.order_date) AS thresh_gap, o.ship_country, o.order_date, o.required_date, o.shipped_date,
e.employee_id, e.first_name ||' '|| e.last_name AS employee_full_name, e.title, e.reports_to, 
c.customer_id, c.contact_name, c.contact_title
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN employees e ON o.employee_id = e.employee_id
WHERE (o.required_date - o.shipped_date) < 0
AND e.title IN ('Sales Representative', 'Sales Manager')
ORDER BY dategap DESC;
```
<img width="1912" height="891" alt="image" src="https://github.com/user-attachments/assets/dda2084e-0035-403d-94d8-9b2debe2a399" />
