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