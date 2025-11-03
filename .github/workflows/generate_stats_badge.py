"""
Generate Statistics for README Badges
Creates JSON data for dynamic badges
"""

import json
import os
from datetime import datetime
from utils import count_records, get_db_connection

def generate_stats():
    """Generate database statistics"""
    
    tables = {
        'categories': 'CATEGORY',
        'suppliers': 'SUPPLIER',
        'staff': 'STAFF',
        'machines': 'MACHINE',
        'payment_methods': 'PAYMENT_METHOD',
        'transaction_types': 'TRANSACTION_TYPE',
        'product_groups': 'PRODUCT_GROUP',
        'products': 'PRODUCT',
        'transactions': 'TRANSACTION_HEADER',
        'transaction_lines': 'TRANSACTION_LINE',
    }
    
    stats = {
        'last_updated': datetime.now().isoformat(),
        'tables': {}
    }
    
    total_records = 0
    
    for key, table_name in tables.items():
        try:
            count = count_records(table_name)
            stats['tables'][key] = count
            total_records += count
        except:
            stats['tables'][key] = 0
    
    stats['total_records'] = total_records
    
    # Get database size
    if os.path.exists('retail_pos.db'):
        db_size_mb = os.path.getsize('retail_pos.db') / (1024 * 1024)
        stats['database_size_mb'] = round(db_size_mb, 2)
    else:
        stats['database_size_mb'] = 0
    
    # Save to JSON file
    with open('stats.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    print("Statistics generated:")
    print(json.dumps(stats, indent=2))
    
    return stats

if __name__ == "__main__":
    generate_stats()