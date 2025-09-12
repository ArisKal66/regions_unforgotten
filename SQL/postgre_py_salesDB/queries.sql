-- 1st Qry, Total revenue per product category
SELECT
    p.category,
    SUM(fs.total_amount) AS total_rev_per_categ
FROM
    fact_sales fs
JOIN products p ON fs.product_id = p.product_id
GROUP BY p.category
ORDER BY total_rev_per_categ DESC;

-- 2nd Qry, Top 5 buyers
SELECT
    c.customer_id,
    SUM(fs.total_amount) AS total_rev_per_cust
FROM
    fact_sales fs
JOIN customers c ON fs.customer_id = c.customer_id
GROUP BY c.customer_id
ORDER BY total_rev_per_cust DESC
LIMIT 5;

-- 3rd Qry, Daily average revenue
WITH daily_revenues AS (
    SELECT
        d.date,
        SUM(fs.total_amount) daily_revenue
    FROM fact_sales fs
    JOIN dates d ON d.date_id = fs.date_id
    GROUP BY d.date
)
SELECT
    AVG(daily_revenue) AS avg_daily_rev
FROM daily_revenues;

-- 4th Qry, Store ranking by monthly sales
SELECT
    d.month,
    s.store_location,
    SUM(fs.total_amount) AS total_sales,
    RANK () OVER (PARTITION BY d.month ORDER BY SUM(fs.total_amount) DESC)
    AS sales_rank
FROM fact_sales fs
JOIN dates d ON fs.date_id = d.date_id
JOIN stores s ON fs.store_id = s.store_id
GROUP BY d.month, s.store_location
ORDER BY d.month, sales_rank;

-- 5th Qry, Customer filtering over threshold
SELECT
    c.customer_id,
    SUM(fs.total_amount) AS customer_totals
FROM fact_sales fs
JOIN customers c ON fs.customer_id = c.customer_id
GROUP BY c.customer_id
HAVING SUM(fs.total_amount) > 1000
ORDER BY customer_totals DESC
LIMIT 10;

-- 6th Qry, Last purchase per customer
SELECT
    c.customer_id,
    d.date,
    fs.total_amount,
    LAG(d.date) OVER (PARTITION BY c.customer_id ORDER BY d.date)
    AS last_purchase
FROM fact_sales fs
JOIN customers c ON fs.customer_id = c.customer_id
JOIN dates d ON fs.date_id = d.date_id
ORDER BY c.customer_id, d.date;