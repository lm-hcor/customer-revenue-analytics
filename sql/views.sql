-- =====================================================
-- Customer Revenue Analytics
-- Analytical Views
-- =====================================================

-- =====================================================
-- Sales Summary
-- =====================================================

DROP VIEW IF EXISTS vw_sales_summary;

CREATE VIEW vw_sales_summary AS

SELECT

    o.order_id,
    o.customer_id,
    o.order_purchase_timestamp,

    DATE_TRUNC('month', o.order_purchase_timestamp) AS purchase_month,

    SUM(oi.price) AS product_revenue,

    SUM(oi.freight_value) AS freight_revenue,

    SUM(oi.price + oi.freight_value) AS total_revenue,

    COUNT(oi.order_item_id) AS total_items,

    AVG(oi.price) AS average_item_price,

    SUM(p.payment_value) AS payment_value

FROM orders o

JOIN order_items oi
    ON o.order_id = oi.order_id

LEFT JOIN payments p
    ON o.order_id = p.order_id

GROUP BY

    o.order_id,
    o.customer_id,
    o.order_purchase_timestamp;


-- =====================================================
-- Customer Metrics
-- =====================================================

DROP VIEW IF EXISTS vw_customer_metrics;

CREATE VIEW vw_customer_metrics AS

SELECT

    c.customer_id,

    c.customer_unique_id,

    c.customer_city,

    c.customer_state,

    COUNT(DISTINCT o.order_id) AS total_orders,

    COALESCE(SUM(p.payment_value),0) AS total_spent,

    COALESCE(AVG(p.payment_value),0) AS average_order_value,

    MIN(o.order_purchase_timestamp) AS first_purchase,

    MAX(o.order_purchase_timestamp) AS last_purchase

FROM customers c

LEFT JOIN orders o
    ON c.customer_id = o.customer_id

LEFT JOIN payments p
    ON o.order_id = p.order_id

GROUP BY

    c.customer_id,
    c.customer_unique_id,
    c.customer_city,
    c.customer_state;

-- =====================================================
-- Category Metrics
-- =====================================================

DROP VIEW IF EXISTS vw_category_metrics;

CREATE VIEW vw_category_metrics AS

SELECT

    p.product_category_name,

    c.product_category_name_english,

    COUNT(DISTINCT oi.order_id) AS total_orders,

    COUNT(oi.product_id) AS products_sold,

    SUM(oi.price) AS revenue,

    SUM(oi.freight_value) AS freight,

    AVG(oi.price) AS average_price

FROM products p

LEFT JOIN categories c
ON p.product_category_name = c.product_category_name

JOIN order_items oi
ON p.product_id = oi.product_id

GROUP BY

    p.product_category_name,
    c.product_category_name_english;

-- =====================================================
-- Monthly Revenue
-- =====================================================

DROP VIEW IF EXISTS vw_monthly_revenue;

CREATE VIEW vw_monthly_revenue AS

SELECT

    DATE_TRUNC('month', o.order_purchase_timestamp) AS month,

    COUNT(DISTINCT o.order_id) AS total_orders,

    SUM(oi.price) AS revenue,

    SUM(oi.freight_value) AS freight,

    SUM(oi.price + oi.freight_value) AS total_revenue

FROM orders o

JOIN order_items oi
ON o.order_id = oi.order_id

GROUP BY

    DATE_TRUNC('month', o.order_purchase_timestamp)

ORDER BY month;

-- =====================================================
-- Delivery Performance
-- =====================================================

DROP VIEW IF EXISTS vw_delivery_performance;

CREATE VIEW vw_delivery_performance AS

SELECT

    order_id,

    customer_id,

    order_purchase_timestamp,

    order_delivered_customer_date,

    order_estimated_delivery_date,

    (order_delivered_customer_date::date
        - order_purchase_timestamp::date) AS delivery_days,

    (order_delivered_customer_date
        <= order_estimated_delivery_date) AS delivered_on_time

FROM orders

WHERE order_delivered_customer_date IS NOT NULL;

-- =====================================================
-- Payment Metrics
-- =====================================================

DROP VIEW IF EXISTS vw_payment_metrics;

CREATE VIEW vw_payment_metrics AS

SELECT

    payment_type,

    COUNT(*) AS total_payments,

    SUM(payment_value) AS total_value,

    AVG(payment_value) AS average_payment,

    AVG(payment_installments) AS average_installments

FROM payments

GROUP BY payment_type;




