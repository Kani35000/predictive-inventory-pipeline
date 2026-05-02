-- ============================================
-- DEMAND ANALYSIS
-- Average Daily Demand per Product per Warehouse
-- ============================================

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
ORDER BY 
    w.warehouse_name,
    avg_daily_demand DESC;s