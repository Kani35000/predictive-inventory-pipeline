-- ============================================
-- KPI 3 & 4: REORDER POINT AND SAFETY STOCK
-- ============================================
-- Calculates the inventory level at which a 
-- purchase order should be triggered to prevent
-- stockouts during supplier lead time
--
-- Formula:
-- Safety Stock  = Z × σ × √Lead Time
-- Reorder Point = (Avg Daily Demand × Lead Time) + Safety Stock
--
-- Assumptions:
-- Lead Time = 7 days (fixed - see limitations)
-- Z Score   = 1.65  (95% service level)
-- ============================================

WITH demand_analysis AS (
    SELECT
        w.warehouse_name,
        p.product_name,
        p.category,
        ROUND(AVG(t.units_sold)::numeric, 2)
            AS avg_daily_demand,
        ROUND(STDDEV(t.units_sold)::numeric, 2)
            AS std_daily_demand,
        MAX(t.units_sold)
            AS max_daily_demand,
        MIN(t.units_sold)
            AS min_daily_demand,
        COUNT(t.transaction_date)
            AS days_of_data,
        ROUND((STDDEV(t.units_sold) /
            NULLIF(AVG(t.units_sold), 0) * 100)::numeric, 2)
            AS demand_variability_pct
    FROM retail.inventory_transactions t
    JOIN retail.products p
        ON t.product_id = p.product_id
    JOIN retail.warehouses w
        ON t.warehouse_id = w.warehouse_id
    GROUP BY
        w.warehouse_name,
        p.product_name,
        p.category
),
reorder_calc AS (
    SELECT
        warehouse_name,
        product_name,
        category,
        avg_daily_demand,
        std_daily_demand,
        demand_variability_pct,
        7 AS lead_time_days,
        1.65 AS z_score,
        ROUND((1.65 * std_daily_demand * SQRT(7))::numeric, 0) AS safety_stock
    FROM demand_analysis
)
SELECT
    warehouse_name,
    product_name,
    category,
    avg_daily_demand,
    std_daily_demand,
    demand_variability_pct,
    lead_time_days,
    z_score,
    safety_stock,
    ROUND((avg_daily_demand * lead_time_days) 
        + safety_stock, 0) AS reorder_point
FROM reorder_calc
ORDER BY reorder_point DESC;