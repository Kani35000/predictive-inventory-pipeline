# ============================================
# PROPHET DEMAND FORECAST
# predictive-inventory-pipeline/03_ML_forecast/prophet_forecast.py
# ============================================
# Time series forecasting using Facebook Prophet
# Handles seasonality, trends, and uncertainty
#
# Prophet expects:
# ds → date column
# y  → target column (units_sold)
# ============================================

import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings('ignore')
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '02_forecasting'))
from extract_data import extract_transactions

def train_prophet(df):
    """
    Train Prophet model per SKU per warehouse
    with train/test split and 30 day forecast
    """
    results = []
    groups = df.groupby(
        ['warehouse_name', 'product_name', 'category']
    )

    for (warehouse, product, category), group in groups:

        # Prepare Prophet format
        prophet_df = group[['transaction_date', 'units_sold']].copy()
        prophet_df.columns = ['ds', 'y']
        prophet_df['ds'] = pd.to_datetime(prophet_df['ds'])

        # Train/Test Split
        train = prophet_df.iloc[:-30]
        test  = prophet_df.iloc[-30:]

        # Train Prophet
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            seasonality_mode='multiplicative'
        )
        model.fit(train)

        # Evaluate on test set
        test_forecast = model.predict(
            test[['ds']]
        )
        y_true = test['y'].values
        y_pred = test_forecast['yhat'].values
        rmse   = np.sqrt(mean_squared_error(y_true, y_pred))
        mae    = np.mean(np.abs(y_true - y_pred))

        # Forecast next 30 days
        future = model.make_future_dataframe(
            periods=30, include_history=False
        )
        forecast = model.predict(future)

        avg_predicted  = round(forecast['yhat'].mean(), 2)
        avg_lower      = round(forecast['yhat_lower'].mean(), 2)
        avg_upper      = round(forecast['yhat_upper'].mean(), 2)

        # Trend direction
        trend_change = (
            forecast['yhat'].iloc[-1] - 
            forecast['yhat'].iloc[0]
        )
        if trend_change > 1:
            trend = 'Increasing'
        elif trend_change < -1:
            trend = 'Decreasing'
        else:
            trend = 'Stable'

        results.append({
            'warehouse_name':       warehouse,
            'product_name':         product,
            'category':             category,
            'avg_predicted_demand': avg_predicted,
            'forecast_lower':       avg_lower,
            'forecast_upper':       avg_upper,
            'trend_direction':      trend,
            'rmse':                 round(rmse, 2),
            'mae':                  round(mae, 2)
        })

    results_df = pd.DataFrame(results)

    print(f"✅ Prophet forecast complete")
    print(f"   SKUs modeled:      {len(results_df)}")
    print(f"   Avg RMSE (test):   {results_df['rmse'].mean():.2f}")
    print(f"   Avg MAE (test):    {results_df['mae'].mean():.2f}")
    print(f"   Increasing trends: {len(results_df[results_df['trend_direction']=='Increasing'])}")
    print(f"   Decreasing trends: {len(results_df[results_df['trend_direction']=='Decreasing'])}")
    print(f"   Stable trends:     {len(results_df[results_df['trend_direction']=='Stable'])}")

    return results_df

if __name__ == "__main__":
    df = extract_transactions()
    forecast = train_prophet(df)

    print(f"\n📊 Prophet Forecast Sample:")
    print(forecast[[
        'warehouse_name',
        'product_name',
        'avg_predicted_demand',
        'forecast_lower',
        'forecast_upper',
        'trend_direction',
        'rmse',
        'mae'
    ]].head(10).to_string(index=False))