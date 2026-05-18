from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
from extract_data import extract_transactions

def prepare_forecast_data(df):
    df = df.sort_values(
        ['warehouse_id', 'product_id', 'transaction_date']
    )
    df['day_number'] = df.groupby(
        ['warehouse_id', 'product_id']
    ).cumcount() + 1
    return df

def train_linear_regression(df):
    """
    Train Linear Regression per SKU per warehouse
    with proper train/test split evaluation
    """
    results = []
    groups = df.groupby(
        ['warehouse_name', 'product_name', 'category']
    )

    for (warehouse, product, category), group in groups:

        # Train/Test Split
        # Train → first 336 days
        # Test  → last 30 days
        train = group.iloc[:-30]
        test  = group.iloc[-30:]

        X_train = train[['day_number']].values
        y_train = train['units_sold'].values

        X_test  = test[['day_number']].values
        y_test  = test['units_sold'].values

        # Train model on training data only
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Evaluate on TEST data (honest RMSE)
        y_pred_test = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
        mae  = np.mean(np.abs(y_test - y_pred_test))

        # Predict future 30 days
        last_day = group['day_number'].max()
        future_days = np.array(
            range(last_day + 1, last_day + 31)
        ).reshape(-1, 1)
        predictions = model.predict(future_days)
        avg_predicted = round(predictions.mean(), 2)

        # Trend direction from slope
        slope = model.coef_[0]
        if slope > 0.05:
            trend = 'Increasing'
        elif slope < -0.05:
            trend = 'Decreasing'
        else:
            trend = 'Stable'

        results.append({
            'warehouse_name':       warehouse,
            'product_name':         product,
            'category':             category,
            'avg_predicted_demand': avg_predicted,
            'trend_direction':      trend,
            'model_slope':          round(slope, 4),
            'rmse':                 round(rmse, 2),
            'mae':                  round(mae, 2)
        })

    results_df = pd.DataFrame(results)

    print(f"✅ Linear Regression forecast complete")
    print(f"   SKUs modeled:      {len(results_df)}")
    print(f"   Avg RMSE (test):   {results_df['rmse'].mean():.2f}")
    print(f"   Avg MAE (test):    {results_df['mae'].mean():.2f}")
    print(f"   Increasing trends: {len(results_df[results_df['trend_direction']=='Increasing'])}")
    print(f"   Decreasing trends: {len(results_df[results_df['trend_direction']=='Decreasing'])}")
    print(f"   Stable trends:     {len(results_df[results_df['trend_direction']=='Stable'])}")

    return results_df

if __name__ == "__main__":
    df = extract_transactions()
    df = prepare_forecast_data(df)
    forecast = train_linear_regression(df)

    print(f"\n📊 Linear Regression Forecast Sample:")
    print(forecast[[
        'warehouse_name',
        'product_name',
        'avg_predicted_demand',
        'trend_direction',
        'rmse'
    ]].head(10).to_string(index=False))

    print(f"\n📊 Trend Distribution:")
    print(forecast['trend_direction'].value_counts())