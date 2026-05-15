from extract_data import extract_transactions
import pandas as pd
import numpy as np

df = extract_transactions()

def calculate_stockout_risk(df):

# KPI 8 → PROJECTED SAVINGS
def calculate_projected_savings(df):

    # Conservative scenario → 70% recovery
    df['savings_conservative'] = (
        df['lost_revenue'] * 0.70
    ).round(2)

    # Moderate scenario → 80% recovery
    df['savings_moderate'] = (
        df['lost_revenue'] * 0.80
    ).round(2)

    # Aggressive scenario → 90% recovery
    df['savings_aggressive'] = (
        df['lost_revenue'] * 0.90
    ).round(2)

    return df


if __name__ == "__main__":

    df = extract_transactions()

    stockout_risk = calculate_stockout_risk(df)

    print(stockout_risk)