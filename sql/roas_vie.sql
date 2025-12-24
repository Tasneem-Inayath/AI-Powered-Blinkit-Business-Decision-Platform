-- Active: 1766155882698@@127.0.0.1@5432@blinkit_db@public
CREATE OR REPLACE VIEW master_analytical_view AS
WITH
    daily_revenue AS (
        SELECT DATE (order_date) AS date, SUM(order_total) AS total_revenue
        FROM blinkit_orders_clean
        GROUP BY
            DATE (order_date)
    ),
    daily_spend AS (
        SELECT date, SUM(spend) AS total_spend
        FROM blinkit_marketing_performance
        GROUP BY
            date
    )
SELECT r.date, r.total_revenue, s.total_spend, r.total_revenue / NULLIF(s.total_spend, 0) AS roas
FROM
    daily_revenue r
    LEFT JOIN daily_spend s ON r.date = s.date;