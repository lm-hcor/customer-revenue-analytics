-- =====================================================
-- Customer Revenue Analytics
-- Business Analysis Queries
-- =====================================================

-- =====================================================
-- 1. Executive KPIs
-- =====================================================

SELECT

    COUNT(DISTINCT order_id) AS total_orders,

    ROUND(SUM(total_revenue),2) AS total_revenue,

    ROUND(AVG(total_revenue),2) AS average_order_value,

    COUNT(DISTINCT customer_id) AS total_customers

FROM vw_sales_summary;

-- =====================================================
-- 2. Monthly Revenue
-- =====================================================

SELECT

    purchase_month,

    ROUND(SUM(total_revenue),2) AS revenue

FROM vw_sales_summary

GROUP BY purchase_month

ORDER BY purchase_month;

-- =====================================================
-- 3. Top Categories
-- =====================================================

SELECT

    product_category_name_english,

    ROUND(revenue,2) AS revenue,

    total_orders

FROM vw_category_metrics

ORDER BY revenue DESC

LIMIT 10;

-- =====================================================
-- 4. Highest Value Customers
-- =====================================================

SELECT

    customer_unique_id,

    customer_state,

    total_orders,

    ROUND(total_spent,2) AS total_spent

FROM vw_customer_metrics

ORDER BY total_spent DESC

LIMIT 20;

-- =====================================================
-- 5. Payment Methods
-- =====================================================

SELECT

    payment_type,

    total_payments,

    ROUND(total_value,2) AS revenue

FROM vw_payment_metrics

ORDER BY revenue DESC;

-- =====================================================
-- 6. Category Ranking
-- =====================================================

SELECT

    product_category_name_english,

    revenue,

    RANK() OVER(
        ORDER BY revenue DESC
    ) AS revenue_rank

FROM vw_category_metrics;

-- =====================================================
-- 7. Monthly Revenue Growth
-- =====================================================

WITH monthly_revenue AS (

    SELECT

        purchase_month,

        SUM(total_revenue) AS revenue

    FROM vw_sales_summary

    GROUP BY purchase_month

)

SELECT

    purchase_month,

    ROUND(revenue,2) AS revenue,

    ROUND(
        revenue
        - LAG(revenue) OVER (
            ORDER BY purchase_month
        ),
        2
    ) AS revenue_growth

FROM monthly_revenue

ORDER BY purchase_month;

-- =====================================================
-- 8. Cumulative Revenue
-- =====================================================

WITH monthly_revenue AS (

    SELECT

        purchase_month,

        SUM(total_revenue) AS revenue

    FROM vw_sales_summary

    GROUP BY purchase_month

)

SELECT

    purchase_month,

    ROUND(revenue,2),

    ROUND(

        SUM(revenue) OVER (

            ORDER BY purchase_month

        ),

        2

    ) AS cumulative_revenue

FROM monthly_revenue;

-- =====================================================
-- 9. Customer Ranking
-- =====================================================

SELECT

    customer_unique_id,

    total_spent,

    DENSE_RANK() OVER(

        ORDER BY total_spent DESC

    ) AS customer_rank

FROM vw_customer_metrics

LIMIT 20;

-- =====================================================
-- 10. Customer Segmentation
-- =====================================================

SELECT

    customer_unique_id,

    total_spent,

    NTILE(4) OVER(

        ORDER BY total_spent DESC

    ) AS customer_quartile

FROM vw_customer_metrics;

-- =====================================================
-- 11. Average Order Value by State
-- =====================================================

SELECT

    customer_state,

    ROUND(

        AVG(total_spent),

        2

    ) AS average_customer_value,

    COUNT(*) AS customers

FROM vw_customer_metrics

GROUP BY customer_state

ORDER BY average_customer_value DESC;

-- =====================================================
-- 12. Delivery Performance
-- =====================================================

SELECT

    delivered_on_time,

    COUNT(*) AS orders,

    ROUND(

        COUNT(*) * 100.0 /

        SUM(COUNT(*)) OVER(),

        2

    ) AS percentage

FROM vw_delivery_performance

GROUP BY delivered_on_time;

-- =====================================================
-- 14. Best Sales Months
-- =====================================================

SELECT

    month,

    total_revenue

FROM vw_monthly_revenue

ORDER BY total_revenue DESC

LIMIT 10;

-- =====================================================
-- 15. Repeat Customers
-- =====================================================

SELECT

    COUNT(*) AS repeat_customers

FROM vw_customer_metrics

WHERE total_orders > 1;
