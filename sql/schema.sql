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

    zip_code_prefix INTEGER,

    city VARCHAR(100),

    state CHAR(2)

);

-- =====================================================
-- Categories
-- =====================================================

CREATE TABLE categories (

    category_name VARCHAR(100) PRIMARY KEY,

    category_name_english VARCHAR(100)

);

-- =====================================================
-- Products
-- =====================================================

CREATE TABLE products (

    product_id VARCHAR(50) PRIMARY KEY,

    category_name VARCHAR(100),

    name_length INTEGER,

    description_length INTEGER,

    photos_qty INTEGER,

    weight_g NUMERIC,

    length_cm NUMERIC,

    height_cm NUMERIC,

    width_cm NUMERIC,

    CONSTRAINT fk_products_category

        FOREIGN KEY (category_name)

        REFERENCES categories(category_name)

);

-- =====================================================
-- Orders
-- =====================================================

CREATE TABLE orders (

    order_id VARCHAR(50) PRIMARY KEY,

    customer_id VARCHAR(50) NOT NULL,

    status VARCHAR(30),

    purchase_timestamp TIMESTAMP,

    approved_timestamp TIMESTAMP,

    delivered_carrier_date TIMESTAMP,

    delivered_customer_date TIMESTAMP,

    estimated_delivery_date TIMESTAMP,

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
ON orders(purchase_timestamp);

CREATE INDEX idx_items_product
ON order_items(product_id);

CREATE INDEX idx_items_order
ON order_items(order_id);

CREATE INDEX idx_products_category
ON products(category_name);

CREATE INDEX idx_payments_order
ON payments(order_id);