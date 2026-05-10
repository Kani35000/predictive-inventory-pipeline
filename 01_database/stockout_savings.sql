-- ============================================
-- KPI 8: PROJECTED SAVINGS FROM OPTIMIZATION
-- ============================================
-- Quantifies potential savings from implementing
-- reorder point and safety stock optimization
-- across the distribution network
--
-- Scenarios:
-- Conservative → 70% stockout prevention
-- Moderate     → 80% stockout prevention  
-- Aggressive   → 90% stockout prevention
--
-- Source: Stockout losses from Phase 1 KPI 6
-- ============================================

WITH running_inventory AS (
    -- Calculate cumulative inventory position
    -- per product per warehouse per day
    SELECT
        transaction_date,
        warehouse_id,
        product_id,
        SUM(units_received + units_returned 
            - units_sold - units_damaged)
        OVER (
            PARTITION BY warehouse_id, product_id
            ORDER BY transaction_date
            ROWS UNBOUNDED PRECEDING
        ) AS running_inventory
    FROM retail.inventory_transactions
),
stockout_days AS (
    -- Identify days where inventory fell below zero
    -- ABS(running_inventory) = unmet demand units
    SELECT
        transaction_date,
        warehouse_id,
        product_id,
        ABS(running_inventory) AS unmet_demand
    FROM running_inventory
    WHERE running_inventory < 0
),
stockout_losses AS (
    -- Calculate total lost revenue per warehouse
    -- Lost Revenue = unmet demand × unit price
    SELECT
        w.warehouse_name,
        COUNT(*)                              AS stockout_days,
        SUM(s.unmet_demand * p.unit_price)    AS lost_revenue
    FROM stockout_days s
    JOIN retail.products p 
        ON s.product_id = p.product_id
    JOIN retail.warehouses w 
        ON s.warehouse_id = w.warehouse_id
    GROUP BY w.warehouse_name
)
-- Final: Calculate projected savings
-- at three optimization scenarios
SELECT
    warehouse_name,
    ROUND(lost_revenue, 2)              AS current_stockout_loss,
    ROUND(lost_revenue * 0.70, 2)       AS savings_conservative,
    ROUND(lost_revenue * 0.30, 2)       AS remaining_loss_conservative,
    ROUND(lost_revenue * 0.80, 2)       AS savings_moderate,
    ROUND(lost_revenue * 0.20, 2)       AS remaining_loss_moderate,
    ROUND(lost_revenue * 0.90, 2)       AS savings_aggressive,
    ROUND(lost_revenue * 0.10, 2)       AS remaining_loss_aggressive
FROM stockout_losses
ORDER BY current_stockout_loss DESC;