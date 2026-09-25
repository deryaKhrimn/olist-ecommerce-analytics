-- View 1: Genel Satış Performansı ve Ciro Analizi
CREATE OR REPLACE VIEW vw_sales_performance AS
SELECT 
    fs.order_id,
    dt.year,
    dt.month,
    dp.category_name,
    dc.customer_city,
    dc.customer_state,
    fs.price,
    fs.freight_value,
    (fs.price + fs.freight_value) AS total_order_value
FROM fact_sales fs
JOIN dim_time dt ON fs.order_date_key = dt.date_key
JOIN dim_products dp ON fs.product_id = dp.product_id
JOIN dim_customers dc ON fs.customer_id = dc.customer_id
WHERE fs.order_status = 'delivered';


-- View 2: Lojistik ve Teslimat Performansı Analizi (Gecikmeleri incelemek için)
CREATE OR REPLACE VIEW vw_delivery_analysis AS
WITH DeliveryCTE AS (
    SELECT 
        dc.customer_state,
        fs.is_delayed,
        fs.delivery_duration_days,
        COUNT(fs.order_id) AS total_orders
    FROM fact_sales fs
    JOIN dim_customers dc ON fs.customer_id = dc.customer_id
    WHERE fs.order_status = 'delivered'
    GROUP BY dc.customer_state, fs.is_delayed, fs.delivery_duration_days
)
SELECT 
    customer_state,
    is_delayed,
    AVG(delivery_duration_days) AS avg_delivery_days,
    SUM(total_orders) AS order_count
FROM DeliveryCTE
GROUP BY customer_state, is_delayed;

-- View 3: Ödeme Yöntemi Davranışları (Payment Behavior)
-- Müşterilerin hangi ödeme yöntemlerini tercih ettiğini ve ortalama sepet tutarlarını gösterir.
CREATE OR REPLACE VIEW vw_payment_behavior AS
SELECT 
    rp.payment_type,
    COUNT(rp.order_id) AS total_transactions,
    SUM(rp.payment_value) AS total_revenue,
    AVG(rp.payment_value) AS avg_ticket_size
FROM raw_payments rp
GROUP BY rp.payment_type;

-- View 4: Kategori Bazlı Karlılık ve Satış Performansı
-- Hangi ürün kategorisinin daha çok sattığını ve ortalama kargo maliyetlerini inceler.
CREATE OR REPLACE VIEW vw_category_performance AS
SELECT 
    dp.category_name,
    COUNT(fs.order_item_id) AS total_items_sold,
    SUM(fs.price) AS total_sales_revenue,
    AVG(fs.freight_value) AS avg_freight_cost
FROM fact_sales fs
JOIN dim_products dp ON fs.product_id = dp.product_id
WHERE fs.order_status = 'delivered'
GROUP BY dp.category_name;