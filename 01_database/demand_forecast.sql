-- ============================================
-- KPI 5 & 6: DEMAND FORECAST
-- 7 Day and 30 Day Simple Moving Average
-- ============================================

SELECT
    w.warehouse_name,
    p.product_name,
    p.category,
    t.transaction_date,
    t.units_sold,
    ROUND(
        AVG(t.units_sold) OVER (
            PARTITION BY t.warehouse_id, t.product_id
            ORDER BY t.transaction_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        )::numeric, 2) AS sma_7_day,
    ROUND(
        AVG(t.units_sold) OVER (
            PARTITION BY t.warehouse_id, t.product_id
            ORDER BY t.transaction_date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        )::numeric, 2) AS sma_30_day
FROM retail.inventory_transactions t
JOIN retail.products p 
    ON t.product_id = p.product_id
JOIN retail.warehouses w 
    ON t.warehouse_id = w.warehouse_id
WHERE t.transaction_date >= (
    SELECT MAX(transaction_date) - INTERVAL '30 days'
    FROM retail.inventory_transactions
)
ORDER BY 
    w.warehouse_name,
    p.product_name,
    t.transaction_date;