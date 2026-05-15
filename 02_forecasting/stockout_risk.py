from extract_data import extract_transactions
import pandas as pd
import numpy as np

df = extract_transactions()

def calculate_stockout_risk(df):

    # ============================================
    # Step 1 → Net Units Per Transaction
    # ============================================

    df['net_units'] = (
        df['units_received']
        + df['units_returned']
        - df['units_sold']
        - df['units_damaged']
    )

    # Step 2 → Demand Analysis
    demand_analysis = (
        df.groupby([
            'warehouse_id',
            'warehouse_name',
            'product_id',
            'product_name',
            'category'
        ])
        .agg(
            avg_daily_demand=('units_sold', 'mean'),
            std_daily_demand=('units_sold', 'std')
        )
        .reset_index()
    )

    # Round values
    demand_analysis['avg_daily_demand'] = (
        demand_analysis['avg_daily_demand']
        .round(2)
    )

    demand_analysis['std_daily_demand'] = (
        demand_analysis['std_daily_demand']
        .round(2)
    )

    # Step 3 → Demand Variability %
    demand_analysis['demand_variability_pct'] = (
        (
            demand_analysis['std_daily_demand']
            / demand_analysis['avg_daily_demand']
        ) * 100
    ).round(2)

    # Running Inventory
    current_inventory = (
        df.groupby([
            'warehouse_id',
            'product_id'
        ])['net_units']
        .sum()
        .reset_index()
    )

    current_inventory.rename(
        columns={'net_units': 'current_inventory'},
        inplace=True
    )


    # Step 5 → Merge Demand + Inventory
    risk_df = demand_analysis.merge(
        current_inventory,
        on=['warehouse_id', 'product_id'],
        how='inner'
    )


    # Step 6 → Days Until Stockout
    risk_df['days_until_stockout'] = (
        risk_df['current_inventory']
        / risk_df['avg_daily_demand']
    ).round(2)

    # Replace division-by-zero infinities
    risk_df['days_until_stockout'] = (
        risk_df['days_until_stockout']
        .replace([np.inf, -np.inf], np.nan)
    )

    # Risk Level Classification
    risk_df['risk_level'] = np.where(
        risk_df['days_until_stockout'] < 7,
        '🚨 CRITICAL',

        np.where(
            risk_df['days_until_stockout'] < 14,
            '🔴 HIGH',

            np.where(
                risk_df['days_until_stockout'] < 30,
                '🟡 MEDIUM',
                '🟢 LOW'
            )
        )
    )


    # Step 8 → Final Output
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
    ]]

    risk_df = risk_df.sort_values(
        by='days_until_stockout',
        ascending=True
    )

    return risk_df


if __name__ == "__main__":

    df = extract_transactions()

    stockout_risk = calculate_stockout_risk(df)

    print(stockout_risk)