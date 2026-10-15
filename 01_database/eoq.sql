-- ============================================
-- KPI 10: ECONOMIC ORDER QUANTITY (EOQ)
-- ============================================
-- Calculates the optimal order quantity that
-- minimizes total inventory costs (ordering
-- cost + holding cost) per SKU per warehouse
--
-- Formula:
-- EOQ = SQRT((2 × D × S) / H)
--
-- Where:
-- D = Annual Demand (units per year)
-- S = Order Cost per order ($75 assumed)
-- H = Holding Cost per unit per year
--     (20% of unit cost assumed)
--
-- Assumptions:
-- Order Cost (S) = $75 per order placed
-- Holding Rate   = 20% of unit cost annually
-- Annual Demand  = avg_daily_demand × 365
--
-- Limitations:
-- S and H are assumed constants
-- No vendor agreement data in schema
-- Real values would come from procurement
-- and warehouse cost accounting records
-- ============================================

WITH demand_analysis AS (
    SELECT
        w.warehouse_name,
        w.warehouse_id,
        p.product_id,
        p.product_name,
        p.category,
        p.unit_cost,
        ROUND(AVG(t.units_sold)::numeric, 2)
            AS avg_daily_demand,
        ROUND(STDDEV(t.units_sold)::numeric, 2)
            AS std_daily_demand,
        ROUND(
            (STDDEV(t.units_sold) /
            NULLIF(AVG(t.units_sold), 0) * 100)::numeric, 2)
            AS demand_variability_pct
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
        p.category,
        p.unit_cost
),
eoq_calc AS (
    SELECT
        warehouse_name,
        product_name,
        category,
        unit_cost,
        avg_daily_demand,
        std_daily_demand,
        demand_variability_pct,

        -- Annual demand
        ROUND((avg_daily_demand * 365)::numeric, 0)
            AS annual_demand,

        -- Assumptions
        75.00                                          AS order_cost,
        ROUND((unit_cost * 0.20)::numeric, 2)         AS holding_cost_per_unit,

        -- EOQ formula
        ROUND(
            SQRT(
                (2 * (avg_daily_demand * 365) * 75.00) /
                NULLIF(unit_cost * 0.20, 0)
            )::numeric, 0
        ) AS eoq_units,

        -- Orders per year at EOQ
        ROUND(
            (avg_daily_demand * 365) /
            NULLIF(
                SQRT(
                    (2 * (avg_daily_demand * 365) * 75.00) /
                    NULLIF(unit_cost * 0.20, 0)
                ), 0
            )::numeric, 1
        ) AS orders_per_year,

        -- Days between orders
        ROUND(
            365 /
            NULLIF(
                (avg_daily_demand * 365) /
                NULLIF(
                    SQRT(
                        (2 * (avg_daily_demand * 365) * 75.00) /
                        NULLIF(unit_cost * 0.20, 0)
                    ), 0
                ), 0
            )::numeric, 0
        ) AS days_between_orders,

        -- Total annual inventory cost at EOQ
        ROUND(
            (
                -- Annual ordering cost
                ((avg_daily_demand * 365) /
                NULLIF(
                    SQRT(
                        (2 * (avg_daily_demand * 365) * 75.00) /
                        NULLIF(unit_cost * 0.20, 0)
                    ), 0
                ) * 75.00)
                +
                -- Annual holding cost
                (SQRT(
                    (2 * (avg_daily_demand * 365) * 75.00) /
                    NULLIF(unit_cost * 0.20, 0)
                ) / 2 * (unit_cost * 0.20))
            )::numeric, 2
        ) AS total_annual_cost
    FROM demand_analysis
)
SELECT
    warehouse_name,
    product_name,
    category,
    unit_cost,
    avg_daily_demand,
    annual_demand,
    order_cost,
    holding_cost_per_unit,
    eoq_units,
    orders_per_year,
    days_between_orders,
    total_annual_cost
FROM eoq_calc
ORDER BY total_annual_cost DESC;