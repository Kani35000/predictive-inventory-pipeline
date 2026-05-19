# ============================================
# MODEL COMPARISON
# predictive-inventory-pipeline/03_ML_forecast/model_comparison.py
# ============================================
# Compares Linear Regression, Random Forest,
# and Prophet forecasting models using
# RMSE and MAE metrics
# ============================================

import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '02_forecasting'))
from extract_data import extract_transactions
from linear_regression_forecast import prepare_forecast_data, train_linear_regression
from random_forest_forecast import prepare_features, train_random_forest
from prophet_forecast import train_prophet

def compare_models():
    """
    Run all three models and compare results
    """
    print("📥 Extracting data...")
    df = extract_transactions()

    #  Linear Regression 
    print("\n1️⃣  Training Linear Regression...")
    df_lr = prepare_forecast_data(df.copy())
    lr_results = train_linear_regression(df_lr)
    lr_results['model'] = 'Linear Regression'

    #  Random Forest 
    print("\n2️⃣  Training Random Forest...")
    df_rf = prepare_features(df.copy())
    rf_results = train_random_forest(df_rf)
    rf_results['model'] = 'Random Forest'

    #  Prophet 
    print("\n3️⃣  Training Prophet...")
    prophet_results = train_prophet(df.copy())
    prophet_results['model'] = 'Prophet'

    #  Model Comparison 
    comparison = pd.DataFrame({
        'Model': [
            'Linear Regression',
            'Random Forest',
            'Prophet'
        ],
        'Avg RMSE': [
            round(lr_results['rmse'].mean(), 2),
            round(rf_results['rmse'].mean(), 2),
            round(prophet_results['rmse'].mean(), 2)
        ],
        'Avg MAE': [
            round(lr_results['mae'].mean(), 2),
            round(rf_results['mae'].mean(), 2),
            round(prophet_results['mae'].mean(), 2)
        ],
        'RMSE Improvement vs Baseline': [
            '—',
            f"{((22.37 - rf_results['rmse'].mean()) / 22.37 * 100):.1f}%",
            f"{((22.37 - prophet_results['rmse'].mean()) / 22.37 * 100):.1f}%"
        ]
    })

    print("\n" + "="*60)
    print("📊 MODEL COMPARISON RESULTS")
    print("="*60)
    print(comparison.to_string(index=False))

    # Best model
    best_model = comparison.loc[
        comparison['Avg RMSE'].idxmin(), 'Model'
    ]
    best_rmse = comparison['Avg RMSE'].min()

    print(f"\n🏆 Best Model: {best_model}")
    print(f"   RMSE: {best_rmse}")

    # Trend comparison
    print("\n📊 Trend Distribution Comparison:")
    trend_comparison = pd.DataFrame({
        'Trend': ['Increasing', 'Decreasing', 'Stable'],
        'Linear Regression': [
            len(lr_results[lr_results['trend_direction']=='Increasing']),
            len(lr_results[lr_results['trend_direction']=='Decreasing']),
            len(lr_results[lr_results['trend_direction']=='Stable'])
        ],
        'Prophet': [
            len(prophet_results[prophet_results['trend_direction']=='Increasing']),
            len(prophet_results[prophet_results['trend_direction']=='Decreasing']),
            len(prophet_results[prophet_results['trend_direction']=='Stable'])
        ]
    })
    print(trend_comparison.to_string(index=False))


    return comparison, lr_results, rf_results, prophet_results

if __name__ == "__main__":
    comparison, lr, rf, prophet = compare_models()