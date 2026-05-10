-- ============================================
-- KPI 7: STOCKOUT RISK SCORE
-- ============================================
-- Combines demand analysis and running inventory
-- to calculate days until stockout and risk level
--
-- Risk Levels:
-- CRITICAL → < 7 days  → Immediate reorder required
-- HIGH     → < 14 days → Reorder this week
-- MEDIUM   → < 30 days → Monitor closely
-- LOW      → 30+ days  → Sufficient stock
-- ============================================

WITH demand_analysis AS (
    SELECT
        w.warehouse_name,
        w.warehouse_id,
        p.product_id,
        p.product_name,
        p.category,
        ROUND(AVG(t.units_sold)::numeric, 2) 
            AS avg_daily_demand,
        ROUND(STDDEV(t.units_sold)::numeric, 2) 
            AS std_daily_demand,
        ROUND(
            (STDDEV(t.units_sold) /
            NULLIF(AVG(t.units_sold), 0) * 100)::numeric, 2
        ) AS demand_variability_pct
    FROM retail.inventory_transactions t
    JOIN retail.products p
        ON t.product_id = p.product_id
    JOIN retail.warehouses w
        ON t.warehouse_id = w.warehouse_id
    GROUP BY
        w.warehouse_name,
        w.warehouse_id,
        p.product_id,
        p.product_name,
        p.category
),
running_inventory AS (
    SELECT
        warehouse_id,
        product_id,
        SUM(
            units_received + units_returned
            - units_sold - units_damaged
        ) AS current_inventory
    FROM retail.inventory_transactions
    GROUP BY warehouse_id, product_id
),
risk_calc AS (
    SELECT
        da.warehouse_name,
        da.product_name,
        da.category,
        da.avg_daily_demand,
        da.std_daily_demand,
        da.demand_variability_pct,
        ri.current_inventory,
        ROUND(
            (ri.current_inventory / 
             NULLIF(da.avg_daily_demand, 0))::numeric, 2
        ) AS days_until_stockout
    FROM demand_analysis da
    JOIN running_inventory ri
        ON da.warehouse_id = ri.warehouse_id
        AND da.product_id = ri.product_id
)
SELECT
    warehouse_name,
    product_name,
    category,
    avg_daily_demand,
    std_daily_demand,
    demand_variability_pct,
    current_inventory,
    days_until_stockout,
    CASE
        WHEN days_until_stockout < 7  THEN '🚨 CRITICAL'
        WHEN days_until_stockout < 14 THEN '🔴 HIGH'
        WHEN days_until_stockout < 30 THEN '🟡 MEDIUM'
        ELSE                               '🟢 LOW'
    END AS risk_level
FROM risk_calc
ORDER BY days_until_stockout ASC;