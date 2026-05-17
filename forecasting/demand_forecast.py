# ============================================
# DEMAND FORECAST
# predictive-inventory-pipeline/02_forecasting/demand_forecast.py
# ============================================
# Calculates 7-day and 30-day simple moving
# averages to identify demand trend signals
# ============================================

from extract_data import extract_transactions
import pandas as pd

def calculate_demand_forecast(df):
    """
    Calculate moving average demand forecast
    and identify high risk divergence signals
    """
    # Sort data chronologically per SKU
    df = df.sort_values(
        by=['warehouse_id', 'product_id', 'transaction_date']
    )

    # Calculate 7 day moving average
    df['sma_7_day'] = (
        df.groupby(['warehouse_id', 'product_id'])['units_sold']
        .transform(lambda x: x.rolling(window=7, min_periods=1).mean())
        .round(2)
    )

    # Calculate 30 day moving average
    df['sma_30_day'] = (
        df.groupby(['warehouse_id', 'product_id'])['units_sold']
        .transform(lambda x: x.rolling(window=30, min_periods=1).mean())
        .round(2)
    )

    # Calculate demand trend signal
    df['demand_trend_signal'] = (
        df['sma_7_day'] - df['sma_30_day']
    ).round(2)

    # Filter last 30 days
    latest_date = df['transaction_date'].max()
    df_filtered = df[
        df['transaction_date'] >= 
        latest_date - pd.Timedelta(days=30)
    ]

    # Filter significant divergence only
    df_filtered = df_filtered[
        abs(df_filtered['demand_trend_signal']) > 10
    ]

    # Select final columns
    df_filtered = df_filtered[[
        'warehouse_name',
        'product_name',
        'category',
        'transaction_date',
        'units_sold',
        'sma_7_day',
        'sma_30_day',
        'demand_trend_signal'
    ]].sort_values(
        by='demand_trend_signal',
        key=abs,
        ascending=False
    ).reset_index(drop=True)

    print(f"✅ Demand forecast complete")
    print(f"   High risk SKUs identified: {len(df_filtered)}")
    print(f"   Max divergence: {df_filtered['demand_trend_signal'].abs().max():.2f} units")

    return df_filtered

if __name__ == "__main__":
    df = extract_transactions()
    forecast = calculate_demand_forecast(df)
    print(f"\n📊 High Risk Demand Signals:")
    print(forecast.head(10).to_string(index=False))