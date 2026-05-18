# ============================================
# RANDOM FOREST DEMAND FORECAST
# predictive-inventory-pipeline/03_ML_forecast/random_forest_forecast.py
# ============================================
# Feature based ML model capturing non-linear
# demand patterns using ensemble learning
#
# Features:
# → day_number, day_of_week, month, quarter
# → is_q4 (holiday season flag)
# → rolling_7, rolling_30 moving averages
# → category_encoded
# ============================================

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '02_forecasting'))
from extract_data import extract_transactions

def prepare_features(df):
    """Engineer features for Random Forest"""

    df = df.sort_values(
        ['warehouse_id', 'product_id', 'transaction_date']
    )

    # Date features
    df['day_number']  = df.groupby(
        ['warehouse_id', 'product_id']
    ).cumcount() + 1
    df['day_of_week'] = pd.to_datetime(df['transaction_date']).dt.dayofweek
    df['month']       = pd.to_datetime(df['transaction_date']).dt.month
    df['quarter']     = pd.to_datetime(df['transaction_date']).dt.quarter
    df['is_q4']       = (df['quarter'] == 4).astype(int)

    # Rolling averages per SKU per warehouse
    df['rolling_7'] = df.groupby(
        ['warehouse_id', 'product_id']
    )['units_sold'].transform(
        lambda x: x.rolling(7, min_periods=1).mean()
    ).round(2)

    df['rolling_30'] = df.groupby(
        ['warehouse_id', 'product_id']
    )['units_sold'].transform(
        lambda x: x.rolling(30, min_periods=1).mean()
    ).round(2)

    # Encode category
    le = LabelEncoder()
    df['category_encoded'] = le.fit_transform(df['category'])

    print(f"✅ Feature engineering complete")
    return df

def train_random_forest(df):
    """
    Train Random Forest per SKU per warehouse
    with train/test split evaluation
    """
    features = [
        'day_number', 'day_of_week', 'month',
        'quarter', 'is_q4', 'rolling_7',
        'rolling_30', 'category_encoded'
    ]

    results = []
    groups = df.groupby(
        ['warehouse_name', 'product_name', 'category']
    )

    for (warehouse, product, category), group in groups:

        # Train/Test Split
        train = group.iloc[:-30]
        test  = group.iloc[-30:]

        X_train = train[features].values
        y_train = train['units_sold'].values
        X_test  = test[features].values
        y_test  = test['units_sold'].values

        # Train Random Forest
        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)

        # Evaluate on test set
        y_pred = model.predict(X_test)
        rmse   = np.sqrt(mean_squared_error(y_test, y_pred))
        mae    = np.mean(np.abs(y_test - y_pred))

        # Predict next 30 days
        last_row    = group.iloc[-1]
        last_day    = last_row['day_number']
        last_date   = pd.to_datetime(last_row['transaction_date'])
        future_dates = pd.date_range(
            start=last_date + pd.Timedelta(days=1),
            periods=30
        )

        future_features = pd.DataFrame({
            'day_number':       range(last_day + 1, last_day + 31),
            'day_of_week':      future_dates.dayofweek,
            'month':            future_dates.month,
            'quarter':          future_dates.quarter,
            'is_q4':            (future_dates.quarter == 4).astype(int),
            'rolling_7':        [last_row['rolling_7']] * 30,
            'rolling_30':       [last_row['rolling_30']] * 30,
            'category_encoded': [last_row['category_encoded']] * 30
        })

        predictions   = model.predict(future_features.values)
        avg_predicted = round(predictions.mean(), 2)

        # Feature importance
        importance = dict(zip(features, model.feature_importances_))
        top_feature = max(importance, key=importance.get)

        results.append({
            'warehouse_name':       warehouse,
            'product_name':         product,
            'category':             category,
            'avg_predicted_demand': avg_predicted,
            'rmse':                 round(rmse, 2),
            'mae':                  round(mae, 2),
            'top_feature':          top_feature
        })

    results_df = pd.DataFrame(results)

    print(f"✅ Random Forest forecast complete")
    print(f"   SKUs modeled:    {len(results_df)}")
    print(f"   Avg RMSE (test): {results_df['rmse'].mean():.2f}")
    print(f"   Avg MAE (test):  {results_df['mae'].mean():.2f}")
    print(f"\n📊 Top Feature Importance:")
    print(results_df['top_feature'].value_counts())

    return results_df

if __name__ == "__main__":
    df = extract_transactions()
    df = prepare_features(df)
    forecast = train_random_forest(df)

    print(f"\n📊 Random Forest Forecast Sample:")
    print(forecast[[
        'warehouse_name',
        'product_name',
        'avg_predicted_demand',
        'rmse',
        'mae',
        'top_feature'
    ]].head(10).to_string(index=False))