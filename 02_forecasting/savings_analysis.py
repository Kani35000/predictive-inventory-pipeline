# ============================================
# SAVINGS ANALYSIS
# predictive-inventory-pipeline/02_forecasting/savings_analysis.py
# ============================================
# Quantifies potential savings from implementing
# reorder point and safety stock optimization
#
# Scenarios:
# Conservative → 70% stockout prevention
# Moderate     → 80% stockout prevention
# Aggressive   → 90% stockout prevention
#
# Source: Phase 1 KPI 6 stockout losses
# ============================================

import pandas as pd
import numpy as np
from extract_data import extract_transactions

def calculate_stockout_losses(df):
    """
    Calculate stockout lost revenue per warehouse
    using running inventory methodology from Phase 1
    """
    # Sort chronologically
    df = df.sort_values(
        ['warehouse_id', 'product_id', 'transaction_date']
    )

    # Calculate running inventory
    df['net_units'] = (
        df['units_received'] + df['units_returned']
        - df['units_sold'] - df['units_damaged']
    )

    df['running_inventory'] = df.groupby(
        ['warehouse_id', 'product_id']
    )['net_units'].cumsum()

    # Identify stockout events
    stockouts = df[df['running_inventory'] < 0].copy()

    # Calculate lost revenue per stockout event
    stockouts['lost_revenue'] = (
        abs(stockouts['net_units']) * stockouts['unit_price']
    )

    # Aggregate by warehouse
    losses = stockouts.groupby('warehouse_name').agg(
        stockout_days  = ('transaction_date', 'count'),
        lost_revenue   = ('lost_revenue', 'sum')
    ).reset_index()

    losses['lost_revenue'] = losses['lost_revenue'].round(2)

    return losses

def calculate_savings(losses_df):
    """
    Calculate projected savings at three
    optimization scenarios
    """
    df = losses_df.copy()

    # Conservative scenario (70% prevention)
    df['savings_conservative']          = (df['lost_revenue'] * 0.70).round(2)
    df['remaining_loss_conservative']   = (df['lost_revenue'] * 0.30).round(2)

    # Moderate scenario (80% prevention)
    df['savings_moderate']              = (df['lost_revenue'] * 0.80).round(2)
    df['remaining_loss_moderate']       = (df['lost_revenue'] * 0.20).round(2)

    # Aggressive scenario (90% prevention)
    df['savings_aggressive']            = (df['lost_revenue'] * 0.90).round(2)
    df['remaining_loss_aggressive']     = (df['lost_revenue'] * 0.10).round(2)

    df = df.sort_values('lost_revenue', ascending=False).reset_index(drop=True)

    return df

def print_savings_summary(savings_df):
    """Print executive savings summary"""

    total_loss          = savings_df['lost_revenue'].sum()
    total_conservative  = savings_df['savings_conservative'].sum()
    total_moderate      = savings_df['savings_moderate'].sum()
    total_aggressive    = savings_df['savings_aggressive'].sum()

    print(f"\n💰 Network Savings Summary:")
    print(f"   Current Stockout Loss:          ${total_loss:>15,.2f}")
    print(f"   Conservative Savings (70%):     ${total_conservative:>15,.2f}")
    print(f"   Moderate Savings (80%):         ${total_moderate:>15,.2f}")
    print(f"   Aggressive Savings (90%):       ${total_aggressive:>15,.2f}")

if __name__ == "__main__":
    df = extract_transactions()

    print("⚙️  Calculating stockout losses...")
    losses = calculate_stockout_losses(df)

    print("⚙️  Calculating optimization savings...")
    savings = calculate_savings(losses)

    print("\n📊 Savings by Warehouse:")
    print(savings[[
        'warehouse_name',
        'lost_revenue',
        'savings_conservative',
        'savings_moderate',
        'savings_aggressive'
    ]].to_string(index=False))

    print_savings_summary(savings)