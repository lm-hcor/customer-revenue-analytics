-- =====================================================
-- Customer Revenue Analytics
-- Database Schema
-- =====================================================

DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS payments CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- =====================================================
-- Customers
-- =====================================================

CREATE TABLE customers (

    customer_id VARCHAR(50) PRIMARY KEY,

    customer_unique_id VARCHAR(50) NOT NULL,

    customer_zip_code_prefix INTEGER,

    customer_city VARCHAR(100),

    customer_state CHAR(2)

);

-- =====================================================
-- Categories
-- =====================================================

CREATE TABLE categories (

    product_category_name VARCHAR(100) PRIMARY KEY,

    product_category_name_english VARCHAR(100)

);

-- =====================================================
-- Products
-- =====================================================

CREATE TABLE products (

    product_id VARCHAR(50) PRIMARY KEY,

    product_category_name VARCHAR(100),

    product_name_length INTEGER,

    product_description_length INTEGER,

    product_photos_qty INTEGER,

    product_weight_g NUMERIC,

    product_length_cm NUMERIC,

    product_height_cm NUMERIC,

    product_width_cm NUMERIC);

-- =====================================================
-- Orders
-- =====================================================

CREATE TABLE orders (

    order_id VARCHAR(50) PRIMARY KEY,

    customer_id VARCHAR(50) NOT NULL,

    order_status VARCHAR(30),

    order_purchase_timestamp TIMESTAMP,

    order_approved_at TIMESTAMP,

    order_delivered_carrier_date TIMESTAMP,

    order_delivered_customer_date TIMESTAMP,

    order_estimated_delivery_date TIMESTAMP,

    CONSTRAINT fk_orders_customer

        FOREIGN KEY (customer_id)

        REFERENCES customers(customer_id)

);

-- =====================================================
-- Payments
-- =====================================================

CREATE TABLE payments (

    payment_id SERIAL PRIMARY KEY,

    order_id VARCHAR(50) NOT NULL,

    payment_sequential INTEGER,

    payment_type VARCHAR(30),

    payment_installments INTEGER,

    payment_value NUMERIC(10,2),

    CONSTRAINT fk_payments_order

        FOREIGN KEY (order_id)

        REFERENCES orders(order_id)

);

-- =====================================================
-- Order Items
-- =====================================================

CREATE TABLE order_items (

    order_item_id INTEGER,

    order_id VARCHAR(50),

    product_id VARCHAR(50),

    seller_id VARCHAR(50),

    shipping_limit_date TIMESTAMP,

    price NUMERIC(10,2),

    freight_value NUMERIC(10,2),

    PRIMARY KEY (order_id, order_item_id),

    CONSTRAINT fk_items_order

        FOREIGN KEY (order_id)

        REFERENCES orders(order_id),

    CONSTRAINT fk_items_product

        FOREIGN KEY (product_id)

        REFERENCES products(product_id)

);

-- =====================================================
-- Indexes
-- =====================================================

CREATE INDEX idx_orders_customer
ON orders(customer_id);

CREATE INDEX idx_orders_purchase
ON orders(order_purchase_timestamp);

CREATE INDEX idx_items_product
ON order_items(product_id);

CREATE INDEX idx_items_order
ON order_items(order_id);

CREATE INDEX idx_products_category
ON products(product_category_name);

CREATE INDEX idx_payments_order
ON payments(order_id);
