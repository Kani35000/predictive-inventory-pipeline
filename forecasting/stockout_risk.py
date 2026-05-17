# ============================================
# STOCKOUT RISK ANALYSIS
# predictive-inventory-pipeline/02_forecasting/stockout_risk.py
# ============================================

import pandas as pd
import numpy as np
from extract_data import extract_transactions
from demand_analysis import calculate_demand_analysis

def calculate_stockout_risk(df, demand_df):
    """
    Calculate stockout risk score per SKU per warehouse
    Combines current inventory with demand analysis
    """
    # Calculate net units per transaction
    df['net_units'] = (
        df['units_received'] + df['units_returned']
        - df['units_sold'] - df['units_damaged']
    )

    # Calculate current inventory per SKU per warehouse
    current_inventory = (
        df.groupby(['warehouse_name', 'product_name'])
        ['net_units'].sum().reset_index()
        .rename(columns={'net_units': 'current_inventory'})
    )

    # Merge demand analysis with current inventory
    risk_df = demand_df.merge(
        current_inventory,
        on=['warehouse_name', 'product_name'],
        how='inner'
    )

    # Calculate days until stockout
    risk_df['days_until_stockout'] = (
        risk_df['current_inventory'] /
        risk_df['avg_daily_demand']
    ).round(2)

    # Protect against division by zero
    risk_df['days_until_stockout'] = (
        risk_df['days_until_stockout']
        .replace([np.inf, -np.inf], np.nan)
    )

    # Apply risk classification
    risk_df['risk_level'] = np.where(
        risk_df['days_until_stockout'] < 7,   '🚨 CRITICAL',
        np.where(
        risk_df['days_until_stockout'] < 14,  '🔴 HIGH',
        np.where(
        risk_df['days_until_stockout'] < 30,  '🟡 MEDIUM',
                                               '🟢 LOW'
    )))

    # Select and sort final output
    risk_df = risk_df[[
        'warehouse_name',
        'product_name',
        'category',
        'avg_daily_demand',
        'std_daily_demand',
        'demand_variability_pct',
        'current_inventory',
        'days_until_stockout',
        'risk_level'
    ]].sort_values('days_until_stockout', ascending=True
    ).reset_index(drop=True)

    # Print summary
    critical = len(risk_df[risk_df['risk_level'] == '🚨 CRITICAL'])
    high     = len(risk_df[risk_df['risk_level'] == '🔴 HIGH'])
    medium   = len(risk_df[risk_df['risk_level'] == '🟡 MEDIUM'])
    low      = len(risk_df[risk_df['risk_level'] == '🟢 LOW'])

    print(f"✅ Stockout risk analysis complete")
    print(f"   🚨 CRITICAL: {critical} SKUs")
    print(f"   🔴 HIGH:     {high} SKUs")
    print(f"   🟡 MEDIUM:   {medium} SKUs")
    print(f"   🟢 LOW:      {low} SKUs")

    return risk_df

if __name__ == "__main__":
    df = extract_transactions()
    demand = calculate_demand_analysis(df)
    risk = calculate_stockout_risk(df, demand)

    print(f"\n📊 Most Critical SKUs:")
    print(risk[risk['risk_level'] == '🚨 CRITICAL'][[
        'warehouse_name',
        'product_name',
        'current_inventory',
        'days_until_stockout',
        'risk_level'
    ]].head(10).to_string(index=False))