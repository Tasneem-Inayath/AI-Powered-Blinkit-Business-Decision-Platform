-- Active: 1766155882698@@127.0.0.1@5432@blinkit_db@public

CREATE OR REPLACE VIEW ml_delivery_features AS
SELECT
    o.order_id,
    -- 📅 REQUIRED FOR OPS FILTERING
    DATE (o.order_date) AS order_date,
    -- 🎯 TARGET (ONLY for training, not prediction)
    CASE
        WHEN o.actual_delivery_time > o.promised_delivery_time THEN 1
        ELSE 0
    END AS is_late,
    -- ⏰ TIME FEATURES
    EXTRACT(
        HOUR
        FROM o.order_date
    ) AS hour_of_day,
    EXTRACT(
        DOW
        FROM o.order_date
    ) AS day_of_week,
    CASE
        WHEN EXTRACT(
            DOW
            FROM o.order_date
        ) IN (0, 6) THEN 1
        ELSE 0
    END AS is_weekend,
    -- 📍 LOCATION
    c.area,
    -- 🛒 ORDER FEATURES
    o.order_total,
    -- 🧺 ITEMS COUNT
    COALESCE(SUM(oi.quantity), 1) AS total_items,
    -- ⏳ PROMISE WINDOW (known at order time)
    EXTRACT(
        EPOCH
        FROM (
                o.promised_delivery_time - o.order_date
            )
    ) / 60 AS promised_duration_minutes
FROM
    blinkit_orders_clean o
    JOIN blinkit_customers c ON o.customer_id = c.customer_id
    LEFT JOIN blinkit_order_items oi ON o.order_id = oi.order_id
GROUP BY
    o.order_id,
    DATE (o.order_date),
    o.order_date,
    o.promised_delivery_time,
    o.actual_delivery_time,
    c.area,
    o.order_total;