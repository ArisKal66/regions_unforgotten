import os
from dotenv import load_dotenv
import psycopg2
from faker import Faker
import random
from datetime import date, timedelta

customer_num = 20 #var1
store_num = 5 #var2

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

required = {"DB_HOST": DB_HOST, "DB_PORT": DB_PORT, "DB_NAME": DB_NAME, "DB_USER": DB_USER, "DB_PASS": DB_PASS}
missing = [k for k, v in required.items() if not v]
if missing:
    raise SystemExit(f"Missing required environment variable(s): {', '.join(missing)}")

def get_connection():
    return psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
    )

if __name__ == "__main__":
    fake = Faker()
    conn = get_connection()
    cur = conn.cursor()
    print("connected to DB: ", DB_NAME)

    for _ in range(customer_num):
        cur.execute("""
            INSERT INTO customers (full_name, gender, age, email)
            VALUES (%s, %s, %s, %s)
        """, (
            fake.name(),
            random.choice(["M", "F"]),
            random.randint(18,70),
            fake.email()
        ))

    products = ["Laptop", "TV", "Smartphone", "Headphones"] #var set1
    categories = ["Electronics", "Electronics", "Electronics", "Accessories"] #var set2

    for i in range(len(products)):
        cur.execute("""
            INSERT INTO products (product_name, category, price)
            VALUES (%s, %s, %s)
        """, (
            products[i],
            categories[i],
            round(random.uniform(50,2000), 2)
        ))

    for _ in range(store_num):
        cur.execute("""
            INSERT INTO stores (store_location, manager_name)
            VALUES (%s, %s)
        """, (
            fake.city(),
            fake.name()
        ))

    start_date = date(2025,1,1) #var3
    dates_num = 30 #var4

    for i in range(dates_num):
        date = start_date + timedelta(days=i)
        cur.execute("""
            INSERT INTO dates(date, d_o_week, month, year)
            VALUES (%s, %s, %s, %s)
            RETURNING date_id
        """, (date, date.strftime("%A"), date.strftime("%B"), date.year))
        date_id = cur.fetchone()[0]

    random_sales_min = 5 #var5
    random_sales_max = 100 #var6
    for _ in range(random.randint(random_sales_min,random_sales_max)):
        cur.execute("""
            INSERT INTO fact_sales(customer_id, product_id, store_id, date_id, quantity_sold, total_amount)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            random.randint(1, customer_num),
            random.randint(1,len(products)),
            random.randint(1,store_num),
            random.randint(1,dates_num),
            qty := random.randint(1,3),
            round(qty * random.uniform(50,2000), 2)
        ))

    conn.commit()
    cur.close()
    conn.close()
    print("Mock data created & inserted successfully")