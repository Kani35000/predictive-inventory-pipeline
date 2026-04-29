# ============================================
# DATA EXTRACTION
# retail-inventory-pipeline/02_pipeline/extract_data.py
# ============================================

import pandas as pd
from db_connection import get_engine

def extract_transactions():
    """Extract all inventory transactions"""
    query = """
        SELECT 
            t.transaction_date,
            t.warehouse_id,
            t.product_id,
            t.units_received,
            t.units_sold,
            t.units_returned,
            t.units_damaged,
            p.unit_cost,
            p.unit_price,
            p.product_name,
            p.category,
            w.warehouse_name
        FROM retail.inventory_transactions t
        JOIN retail.products p ON t.product_id = p.product_id
        JOIN retail.warehouses w ON t.warehouse_id = w.warehouse_id
        ORDER BY t.transaction_date, t.warehouse_id, t.product_id
    """
    engine = get_engine()
    df = pd.read_sql(query, engine)
    print(f"✅ Extracted {len(df):,} transaction rows")
    return df

def extract_cycle_counts():
    """Extract all cycle count data"""
    query = """
        SELECT 
            c.count_date,
            c.warehouse_id,
            c.product_id,
            c.system_inventory,
            c.physical_count,
            p.unit_cost,
            p.product_name,
            w.warehouse_name
        FROM retail.cycle_counts c
        JOIN retail.products p ON c.product_id = p.product_id
        JOIN retail.warehouses w ON c.warehouse_id = w.warehouse_id
        ORDER BY c.count_date, c.warehouse_id, c.product_id
    """
    engine = get_engine()
    df = pd.read_sql(query, engine)
    print(f"✅ Extracted {len(df):,} cycle count rows")
    return df

if __name__ == "__main__":
    transactions = extract_transactions()
    cycle_counts = extract_cycle_counts()
    print(f"\n📊 Transactions shape: {transactions.shape}")
    print(f"📊 Cycle counts shape: {cycle_counts.shape}")
    print(f"\n🔍 Transaction columns:")
    print(transactions.columns.tolist())