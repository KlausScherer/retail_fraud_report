import random
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
NUM_CUSTOMERS = random.randint(5000, 10000)
NUM_PRODUCTS = random.randint(40, 50)
NUM_STORES = random.randint(4, 7)

YEAR = 2025
MONTH = random.randint(1, 12)

if MONTH == 2:
    DAYS_IN_MONTH = 28
elif MONTH in [4, 6, 9, 11]:
    DAYS_IN_MONTH = 30
else:
    DAYS_IN_MONTH = 31

NUM_TRANSACTIONS = 50000

# -----------------------------
# PRECIOS PRODUCTOS
# -----------------------------
product_prices = {
    i: round(random.uniform(5, 500), 2)
    for i in range(1, NUM_PRODUCTS + 1)
}

# -----------------------------
# GENERAR SQL
# -----------------------------
sql = []

# DROP + CREATE DB
sql.append("DROP DATABASE IF EXISTS sales;")
sql.append("CREATE DATABASE sales;")
sql.append("USE sales;")

# TABLAS
sql.append("""
CREATE TABLE customers (
    customer_id INT PRIMARY KEY
);
""")

sql.append("""
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    base_price DECIMAL(10,2)
);
""")

sql.append("""
CREATE TABLE stores (
    store_id INT PRIMARY KEY
);
""")

sql.append("""
CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    store_id INT,
    date DATE,
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (store_id) REFERENCES stores(store_id)
);
""")

sql.append("""
CREATE TABLE fraud_flags (
    fraud_id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT,
    fraud_type VARCHAR(50),
    FOREIGN KEY (sale_id) REFERENCES sales(sale_id)
);
""")

# INSERTS DIMENSIONES
for c in range(1, NUM_CUSTOMERS + 1):
    sql.append(f"INSERT INTO customers VALUES ({c});")

for p, price in product_prices.items():
    sql.append(f"INSERT INTO products VALUES ({p}, {price});")

for s in range(1, NUM_STORES + 1):
    sql.append(f"INSERT INTO stores VALUES ({s});")

# -----------------------------
# GENERAR VENTAS
# -----------------------------
sale_id = 1

fraud_sales = set()

for _ in range(NUM_TRANSACTIONS):
    customer_id = random.randint(1, NUM_CUSTOMERS)
    product_id = random.randint(1, NUM_PRODUCTS)
    store_id = random.randint(1, NUM_STORES)

    day = random.randint(1, DAYS_IN_MONTH)
    date = datetime(YEAR, MONTH, day).strftime('%Y-%m-%d')

    quantity = random.randint(1, 5)
    price = product_prices[product_id]

    sql.append(
        f"INSERT INTO sales VALUES ({sale_id}, {customer_id}, {product_id}, {store_id}, '{date}', {quantity}, {price});"
    )

    sale_id += 1

# -----------------------------
# FRAUDE: cliente con muchas compras en un día
# -----------------------------
fraud_customer = random.randint(1, NUM_CUSTOMERS)
fraud_day = random.randint(1, DAYS_IN_MONTH)

for _ in range(200):
    product_id = random.randint(1, NUM_PRODUCTS)
    store_id = random.randint(1, NUM_STORES)
    date = datetime(YEAR, MONTH, fraud_day).strftime('%Y-%m-%d')

    sql.append(
        f"INSERT INTO sales VALUES ({sale_id}, {fraud_customer}, {product_id}, {store_id}, '{date}', 10, {product_prices[product_id]});"
    )

    sql.append(
        f"INSERT INTO fraud_flags (sale_id, fraud_type) VALUES ({sale_id}, 'high_frequency_customer');"
    )

    sale_id += 1

# -----------------------------
# GUARDAR ARCHIVO
# -----------------------------
output_path = r"C:\Users\klaus\Documents\Perfil Profesional\GitHub\Proyecto_2\Data\sales.sql"

with open(output_path, "w", encoding="utf-8") as f:
    for line in sql:
        f.write(line + "\n")

print(f"Archivo generado en: {output_path} 🚀")