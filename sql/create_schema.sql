-- 1. DIMENSION TABLES (Boyut Tabloları)

-- Müşteri Boyut Tablosu
DROP TABLE IF EXISTS dim_customers CASCADE;
CREATE TABLE dim_customers AS
SELECT DISTINCT 
    customer_id, 
    customer_unique_id, 
    customer_city, 
    customer_state
FROM raw_customers;

ALTER TABLE dim_customers ADD PRIMARY KEY (customer_id);

-- Ürün Boyut Tablosu
DROP TABLE IF EXISTS dim_products CASCADE;
CREATE TABLE dim_products AS
SELECT DISTINCT 
    product_id, 
    product_category_name_english AS category_name,
    product_weight_g
FROM raw_products;

ALTER TABLE dim_products ADD PRIMARY KEY (product_id);

-- Zaman Boyut Tablosu (Power BI'da Time Intelligence DAX'ları için kritik)
DROP TABLE IF EXISTS dim_time CASCADE;
CREATE TABLE dim_time AS
SELECT DISTINCT
    CAST(order_purchase_timestamp AS DATE) AS date_key,
    EXTRACT(YEAR FROM CAST(order_purchase_timestamp AS TIMESTAMP)) AS year,
    EXTRACT(MONTH FROM CAST(order_purchase_timestamp AS TIMESTAMP)) AS month,
    EXTRACT(DAY FROM CAST(order_purchase_timestamp AS TIMESTAMP)) AS day,
    EXTRACT(QUARTER FROM CAST(order_purchase_timestamp AS TIMESTAMP)) AS quarter
FROM raw_orders
WHERE order_purchase_timestamp IS NOT NULL;

ALTER TABLE dim_time ADD PRIMARY KEY (date_key);

-- 2. FACT TABLE (Gerçek Tablosu - İşlemlerin merkez noktası)
-- Siparişler ve sipariş kalemlerini birleştirerek tek bir satış fact tablosu yaratıyoruz.
DROP TABLE IF EXISTS fact_sales CASCADE;
CREATE TABLE fact_sales AS
SELECT 
    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    o.customer_id,
    CAST(o.order_purchase_timestamp AS DATE) AS order_date_key,
    o.order_status,
    oi.price,
    oi.freight_value,
    o.delivery_duration_days,
    o.is_delayed
FROM raw_order_items oi
JOIN raw_orders o ON oi.order_id = o.order_id;

-- Yabancı anahtar (Foreign Key) ilişkilerini kurma
ALTER TABLE fact_sales ADD CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES dim_products(product_id);
ALTER TABLE fact_sales ADD CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id);
ALTER TABLE fact_sales ADD CONSTRAINT fk_time FOREIGN KEY (order_date_key) REFERENCES dim_time(date_key);