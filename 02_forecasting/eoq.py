# ============================================
# KPI 10: ECONOMIC ORDER QUANTITY (EOQ)
# predictive-inventory-pipeline/02_forecasting/eoq.py
# ============================================
# Calculates optimal order quantity minimizing
# total inventory cost per SKU per warehouse
#
# Formula: EOQ = SQRT((2 × D × S) / H)
#
# Assumptions:
# Order Cost (S) = $75 per order
# Holding Rate   = 20% of unit_cost annually
# Annual Demand  = avg_daily_demand × 365
# ============================================

import pandas as pd
import numpy as np
from extract_data import extract_transactions
from demand_analysis import calculate_demand_analysis

# ── Assumptions ─────────────────────────────
ORDER_COST   = 75.00   # $ per order placed
HOLDING_RATE = 0.20    # 20% of unit cost per year


def calculate_eoq(demand_df, transactions_df):
    """
    Calculate Economic Order Quantity
    per SKU per warehouse

    Parameters:
    -----------
    demand_df      : DataFrame from calculate_demand_analysis
    transactions_df: Raw transactions with unit_cost column

    Returns:
    --------
    DataFrame with EOQ and cost metrics
    """

    # Get unit cost per product per warehouse
    unit_costs = (
        transactions_df
        .groupby(['warehouse_name', 'product_name'])['unit_cost']
        .first()
        .reset_index()
    )

    # Merge demand analysis with unit costs
    df = demand_df.merge(
        unit_costs,
        on=['warehouse_name', 'product_name'],
        how='inner'
    )

    # ── Annual Demand ────────────────────────
    df['annual_demand'] = (
        df['avg_daily_demand'] * 365
    ).round(0)

    # ── Cost Assumptions ─────────────────────
    df['order_cost']          = ORDER_COST
    df['holding_cost_per_unit'] = (
        df['unit_cost'] * HOLDING_RATE
    ).round(2)

    # ── EOQ Formula ──────────────────────────
    # EOQ = SQRT((2 × D × S) / H)
    df['eoq_units'] = np.sqrt(
        (2 * df['annual_demand'] * df['order_cost']) /
        df['holding_cost_per_unit'].replace(0, np.nan)
    ).round(0)

    # ── Orders Per Year ───────────────────────
    df['orders_per_year'] = (
        df['annual_demand'] /
        df['eoq_units'].replace(0, np.nan)
    ).round(1)

    # ── Days Between Orders ───────────────────
    df['days_between_orders'] = (
        365 / df['orders_per_year'].replace(0, np.nan)
    ).round(0)

    # ── Total Annual Inventory Cost ───────────
    # Total Cost = Ordering Cost + Holding Cost
    # = (D/EOQ × S) + (EOQ/2 × H)
    df['annual_ordering_cost'] = (
        (df['annual_demand'] /
         df['eoq_units'].replace(0, np.nan)) *
        df['order_cost']
    ).round(2)

    df['annual_holding_cost'] = (
        (df['eoq_units'] / 2) *
        df['holding_cost_per_unit']
    ).round(2)

    df['total_annual_cost'] = (
        df['annual_ordering_cost'] +
        df['annual_holding_cost']
    ).round(2)

    # ── Final Output ──────────────────────────
    result = df[[
        'warehouse_name',
        'product_name',
        'category',
        'unit_cost',
        'avg_daily_demand',
        'annual_demand',
        'order_cost',
        'holding_cost_per_unit',
        'eoq_units',
        'orders_per_year',
        'days_between_orders',
        'annual_ordering_cost',
        'annual_holding_cost',
        'total_annual_cost'
    ]].sort_values(
        'total_annual_cost', ascending=False
    ).reset_index(drop=True)

    # ── Summary Stats ─────────────────────────
    print(f"✅ EOQ calculation complete")
    print(f"   SKUs analyzed:           {len(result)}")
    print(f"   Avg EOQ:                 {result['eoq_units'].mean():.0f} units")
    print(f"   Avg orders per year:     {result['orders_per_year'].mean():.1f}")
    print(f"   Avg days between orders: {result['days_between_orders'].mean():.0f} days")
    print(f"   Total network annual cost: ${result['total_annual_cost'].sum():,.2f}")

    return result


def print_eoq_summary(eoq_df):
    """Print executive EOQ summary by warehouse"""

    summary = eoq_df.groupby('warehouse_name').agg(
        avg_eoq            = ('eoq_units', 'mean'),
        avg_orders_year    = ('orders_per_year', 'mean'),
        avg_days_between   = ('days_between_orders', 'mean'),
        total_annual_cost  = ('total_annual_cost', 'sum')
    ).round(2).reset_index()

    summary = summary.sort_values(
        'total_annual_cost', ascending=False
    )

    print(f"\n📊 EOQ Summary by Warehouse:")
    print(f"{'Warehouse':<35} {'Avg EOQ':>8} {'Orders/Yr':>10} "
          f"{'Days/Order':>11} {'Annual Cost':>13}")
    print("-" * 80)
    for _, row in summary.iterrows():
        print(f"{row['warehouse_name']:<35} "
              f"{row['avg_eoq']:>8.0f} "
              f"{row['avg_orders_year']:>10.1f} "
              f"{row['avg_days_between']:>11.0f} "
              f"${row['total_annual_cost']:>12,.2f}")

    print("-" * 80)
    print(f"{'NETWORK TOTAL':<35} "
          f"{'':>8} "
          f"{'':>10} "
          f"{'':>11} "
          f"${eoq_df['total_annual_cost'].sum():>12,.2f}")


if __name__ == "__main__":
    print("⚙️  Loading data...")
    df = extract_transactions()

    print("⚙️  Calculating demand analysis...")
    demand = calculate_demand_analysis(df)

    print("⚙️  Calculating EOQ...\n")
    eoq = calculate_eoq(demand, df)

    print(f"\n📊 Top 10 SKUs by Total Annual Cost:")
    print(eoq[[
        'warehouse_name',
        'product_name',
        'eoq_units',
        'orders_per_year',
        'days_between_orders',
        'total_annual_cost'
    ]].head(10).to_string(index=False))

    print_eoq_summary(eoq)