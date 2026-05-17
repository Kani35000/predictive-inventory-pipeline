# ============================================
# DEMAND ANALYSIS
# predictive-inventory-pipeline/02_forecasting/demand_analysis.py
# ============================================

import pandas as pd
from extract_data import extract_transactions

def calculate_demand_analysis(df):
    """Calculate demand statistics per SKU per warehouse"""
    
    demand = df.groupby(['warehouse_name', 'product_name', 'category']).agg(
        avg_daily_demand = ('units_sold', 'mean'),
        std_daily_demand = ('units_sold', 'std'),
        max_daily_demand = ('units_sold', 'max'),
        min_daily_demand = ('units_sold', 'min'),
        days_of_data     = ('units_sold', 'count')
    ).reset_index()

    demand['avg_daily_demand'] = demand['avg_daily_demand'].round(2)
    demand['std_daily_demand'] = demand['std_daily_demand'].round(2)

    demand['demand_variability_pct'] = (
        demand['std_daily_demand'] /
        demand['avg_daily_demand'] * 100
    ).round(2)

    demand = demand.sort_values(
        'avg_daily_demand', ascending=False
    ).reset_index(drop=True)

    print(f"✅ Demand analysis complete")
    print(f"   SKU-Warehouse combinations: {len(demand)}")
    print(f"   Avg demand range: {demand['avg_daily_demand'].min():.1f} - {demand['avg_daily_demand'].max():.1f} units/day")
    print(f"   Avg variability: {demand['demand_variability_pct'].mean():.1f}%")

    return demand

if __name__ == "__main__":
    df = extract_transactions()
    demand = calculate_demand_analysis(df)
    print(f"\n📊 Demand Analysis Sample:")
    print(demand[[
        'warehouse_name',
        'product_name',
        'avg_daily_demand',
        'std_daily_demand',
        'demand_variability_pct'
    ]].head(10).to_string(index=False))