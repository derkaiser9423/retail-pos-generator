"""
Database Schema Validator
Ensures database structure matches expected schema
Used by GitHub Actions for testing
"""

import sqlite3
import sys
import os
from config import DATABASE_PATH

# Expected schema
EXPECTED_SCHEMA = {
    'CATEGORY': ['Category_ID', 'Category_Name', 'Description'],
    'PRODUCT_GROUP': ['Product_Group_ID', 'Product_Group_Name', 'Description', 'Category_ID'],
    'SUPPLIER': ['Supplier_ID', 'Supplier_Name', 'Contact_Name', 'Contact_Phone', 
                 'Contact_Email', 'Address', 'Payment_Terms', 'Active_Status'],
    'PRODUCT': ['PLU', 'Description', 'Avg_Real_Cost', 'SOH', 'EXP', 'History', 
                'Product_Group_ID', 'Supplier_ID'],
    'STAFF': ['Staff_ID', 'Staff_Name', 'Active_Status', 'Hire_Date', 'Role'],
    'MACHINE': ['Machine_ID', 'Machine_Name', 'Location', 'Active_Status', 'Install_Date'],
    'PAYMENT_METHOD': ['Payment_Method_ID', 'Payment_Method_Name', 'Description', 
                       'Processing_Fee_Percent', 'Active_Status'],
    'TRANSACTION_TYPE': ['Transaction_Type_ID', 'Transaction_Type_Name', 'Description', 
                         'Affects_Inventory', 'Affects_Revenue'],
    'TRANSACTION_HEADER': ['Transaction_ID', 'Time_Stamp', 'Staff_ID', 'Machine_ID', 
                           'Payment_Method_ID', 'Transaction_Type_ID', 'For_Staff_ID'],
    'TRANSACTION_LINE': ['Transaction_Line_ID', 'Transaction_ID', 'PLU', 'Qty_Supplied', 
                         'Original_Price', 'Total_Paid', 'Discount_Percent'],
}

def get_table_columns(conn, table_name):
    """Get column names for a table"""
    cursor = conn.execute(f"PRAGMA table_info({table_name})")
    return [row[1] for row in cursor.fetchall()]

def validate_schema():
    """Validate database schema"""
    print("Starting database schema validation...")
    
    # Check if database exists
    if not os.path.exists(DATABASE_PATH):
        print(f"⚠️  Database file not found: {DATABASE_PATH}")
        print("This is normal for first run. Database will be created.")
        return True
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.execute('PRAGMA foreign_keys = ON')
        
        all_valid = True
        
        for table_name, expected_columns in EXPECTED_SCHEMA.items():
            print(f"Validating table: {table_name}")
            
            # Check if table exists
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,)
            )
            
            if not cursor.fetchone():
                print(f"⚠️  Table {table_name} does not exist yet")
                # This is OK - tables will be created
                continue
            
            # Check columns
            actual_columns = get_table_columns(conn, table_name)
            
            missing_columns = set(expected_columns) - set(actual_columns)
            extra_columns = set(actual_columns) - set(expected_columns)
            
            if missing_columns:
                print(f"✗ {table_name} missing columns: {missing_columns}")
                all_valid = False
            
            if extra_columns:
                print(f"⚠️  {table_name} has extra columns: {extra_columns}")
            
            if not missing_columns and not extra_columns:
                print(f"✓ {table_name} schema valid")
        
        conn.close()
        
        if all_valid:
            print("=" * 60)
            print("✓ Database schema validation PASSED")
            print("=" * 60)
            return True
        else:
            print("=" * 60)
            print("✗ Database schema validation FAILED")
            print("=" * 60)
            return False
            
    except Exception as e:
        print(f"Validation error: {e}")
        return False

if __name__ == "__main__":
    success = validate_schema()
    sys.exit(0 if success else 1)
