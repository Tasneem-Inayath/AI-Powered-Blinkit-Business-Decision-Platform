-- Active: 1766155882698@@127.0.0.1@5432@blinkit_db@public
WITH
    daily_orders AS (
        SELECT
            DATE (order_date) AS date,
            COUNT(order_id) AS total_orders,
            SUM(order_total) AS total_revenue,
            AVG(
                GREATEST(
                    EXTRACT(
                        EPOCH
                        FROM (
                                actual_delivery_time - promised_delivery_time
                            )
                    ) / 60,
                    0
                )
            ) AS avg_delay_minutes
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
SELECT
    o.date,
    o.total_orders,
    o.total_revenue,
    COALESCE(s.total_spend, 0) AS total_spend,
    CASE
        WHEN COALESCE(s.total_spend, 0) = 0 THEN NULL
        ELSE o.total_revenue / s.total_spend
    END AS roas,
    o.avg_delay_minutes
FROM daily_orders o
    LEFT JOIN daily_spend s ON o.date = s.date
ORDER BY o.date;