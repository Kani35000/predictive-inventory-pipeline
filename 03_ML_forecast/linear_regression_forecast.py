from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
from extract_data import extract_transactions


# Create day number per product per warehouse
df = df.sort_values(
    ['warehouse_id', 'product_id', 'transaction_date']
)
df['day_number'] = df.groupby(
    ['warehouse_id', 'product_id']
).cumcount() + 1

print(df)


if __name__ == "__main__":
    df = extract_transactions()