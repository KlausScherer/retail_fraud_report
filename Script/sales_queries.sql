-- =========================================
-- PROYECTO SQL: ANALISIS DE VENTAS + FRAUDE
-- =========================================

-- Usar la base de datos
USE sales;

-- =========================================
-- 1. EXPLORACION GENERAL
-- =========================================

-- Total de ventas
SELECT SUM(quantity * price) AS total_sales
FROM sales;

-- Ventas por tienda
SELECT store_id, SUM(quantity * price) AS total_sales
FROM sales
GROUP BY store_id
ORDER BY total_sales DESC;

-- Top 10 productos más vendidos
SELECT product_id, SUM(quantity) AS total_units
FROM sales
GROUP BY product_id
ORDER BY total_units DESC
LIMIT 10;


-- =========================================
-- 2. ANALISIS DE CLIENTES
-- =========================================

-- Clientes con más compras
SELECT customer_id, COUNT(*) AS num_purchases
FROM sales
GROUP BY customer_id
ORDER BY num_purchases DESC
LIMIT 10;

-- Clientes que más gastan
SELECT customer_id, SUM(quantity * price) AS total_spent
FROM sales
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;


-- =========================================
-- 3. DETECCION DE FRAUDE
-- =========================================

-- Clientes con demasiadas compras en un día
SELECT customer_id, date, COUNT(*) AS purchases
FROM sales
GROUP BY customer_id, date
HAVING COUNT(*) > 20
ORDER BY purchases DESC;

-- Productos con picos sospechosos
SELECT product_id, date, SUM(quantity) AS total_sold
FROM sales
GROUP BY product_id, date
HAVING total_sold > 100
ORDER BY total_sold DESC;

-- Tiendas con ingresos anormales
SELECT store_id, date, SUM(quantity * price) AS revenue
FROM sales
GROUP BY store_id, date
ORDER BY revenue DESC
LIMIT 10;

-- Tipos de fraude (si tienes tabla fraud_flags)
SELECT fraud_type, COUNT(*) AS total_cases
FROM fraud_flags
GROUP BY fraud_type;


-- =========================================
-- 4. CONSULTAS AVANZADAS (PRO)
-- =========================================

-- Promedio de compras por cliente
SELECT AVG(purchases) AS avg_purchases_per_customer
FROM (
    SELECT customer_id, COUNT(*) AS purchases
    FROM sales
    GROUP BY customer_id
) sub;

-- Ticket promedio por compra
SELECT AVG(total_per_order) AS avg_ticket
FROM (
    SELECT (quantity * price) AS total_per_order
    FROM sales
) sub;

-- Ranking de clientes (top spenders)
SELECT customer_id,
       SUM(quantity * price) AS total_spent,
       RANK() OVER (ORDER BY SUM(quantity * price) DESC) AS ranking
FROM sales
GROUP BY customer_id;