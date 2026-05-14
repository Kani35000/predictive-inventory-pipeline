from extract_data import extract_transactions
from demand_analysis import calculate_demand_analysis
from math import sqrt

# Formula:
# Safety Stock  = Z × σ × √Lead Time
# Reorder Point = (Avg Daily Demand × Lead Time) + Safety Stock
df = extract_transactions()
demand_df = calculate_demand_analysis(df)

def calculate_reorder_point(demand_df):

    df = demand_df.copy()

    # Adding constants
    df['lead_time_days'] = 7
    df['z_score'] = 1.65

    # Calculating safety stock
    df['safety_stock'] = round(df['z_score'] * df['std_daily_demand'] * (df['lead_time_days'] ** 0.5), 0)

    # Calculating reorder point
    df['reorder_point'] = round((df['avg_daily_demand'] * df['lead_time_days']) + df['safety_stock'], 0)
    
    return df


print(calculate_reorder_point(demand_df))