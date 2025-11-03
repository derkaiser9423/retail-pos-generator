#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 00:39:27 2024

@author: tin
"""

"""
Generate TRANSACTION_TYPE records
Creates realistic transaction type reference data
"""

import random
from datetime import datetime
from config import REAL_TRANSACTION_TYPES, BATCH_SIZES
from utils import (
    setup_logger,
    execute_query,
    record_exists,
    generate_unique_value,
    log_generation_summary,
    count_records
)

# Setup logger
logger = setup_logger('TransactionTypeGenerator')

# ============================================
# TRANSACTION TYPE GENERATION LOGIC
# ============================================

# Extended transaction types with business rules
TRANSACTION_TYPE_CONFIG = {
    "Normal Item Sale": {
        "description": "Standard item sale transaction",
        "affects_inventory": 1,  # Decreases inventory
        "affects_revenue": 1     # Increases revenue
    },
    "Return Item": {
        "description": "Customer return transaction",
        "affects_inventory": 1,  # Increases inventory
        "affects_revenue": 1     # Decreases revenue (negative)
    },
    "Scriptlink Item": {
        "description": "Prescription medication sale",
        "affects_inventory": 1,
        "affects_revenue": 1
    },
    "Staff Purchase": {
        "description": "Staff member purchase with discount",
        "affects_inventory": 1,
        "affects_revenue": 1
    },
    "Void Item": {
        "description": "Voided transaction (cancelled)",
        "affects_inventory": 0,  # No inventory impact
        "affects_revenue": 0     # No revenue impact
    },
    "Exchange": {
        "description": "Product exchange transaction",
        "affects_inventory": 1,
        "affects_revenue": 0     # Net zero if same value
    },
    "Damaged Goods": {
        "description": "Damaged goods write-off",
        "affects_inventory": 1,
        "affects_revenue": 0
    },
    "Stock Adjustment": {
        "description": "Manual stock level adjustment",
        "affects_inventory": 1,
        "affects_revenue": 0
    },
    "Sample": {
        "description": "Free sample given to customer",
        "affects_inventory": 1,
        "affects_revenue": 0
    },
    "Promotional": {
        "description": "Promotional giveaway",
        "affects_inventory": 1,
        "affects_revenue": 0
    },
    "Refund": {
        "description": "Full refund to customer",
        "affects_inventory": 1,
        "affects_revenue": 1
    },
    "Layby Payment": {
        "description": "Partial payment on layby",
        "affects_inventory": 0,
        "affects_revenue": 0
    }
}

def generate_transaction_type_name():
    """Generate transaction type name"""
    return random.choice(list(TRANSACTION_TYPE_CONFIG.keys()))

def get_transaction_type_config(name):
    """Get configuration for transaction type"""
    return TRANSACTION_TYPE_CONFIG.get(name, {
        "description": f"{name} transaction",
        "affects_inventory": 1,
        "affects_revenue": 1
    })

def transaction_type_exists(name):
    """Check if transaction type with name already exists"""
    return record_exists('TRANSACTION_TYPE', 'Transaction_Type_Name', name)

def insert_transaction_type(name, description, affects_inventory, affects_revenue):
    """Insert transaction type into database"""
    query = """
        INSERT INTO TRANSACTION_TYPE (
            Transaction_Type_Name, Description, Affects_Inventory, Affects_Revenue
        )
        VALUES (?, ?, ?, ?)
    """
    try:
        type_id = execute_query(query, (name, description, affects_inventory, affects_revenue))
        return type_id
    except Exception as e:
        logger.error(f"Failed to insert transaction type '{name}': {e}")
        return None

# ============================================
# MAIN GENERATION FUNCTION
# ============================================

def generate_transaction_types(batch_size=None):
    """Generate batch of transaction type records"""
    if batch_size is None:
        batch_size = BATCH_SIZES['TRANSACTION_TYPE']
    
    logger.info(f"Starting transaction type generation - Batch size: {batch_size}")
    
    success_count = 0
    failed_count = 0
    
    for i in range(batch_size):
        try:
            # Generate unique transaction type name
            type_name = generate_unique_value(
                generate_transaction_type_name,
                transaction_type_exists,
                max_retries=20
            )
            
            if type_name is None:
                logger.warning(f"Could not generate unique transaction type name after max retries")
                failed_count += 1
                continue
            
            # Get configuration
            config = get_transaction_type_config(type_name)
            
            # Insert into database
            type_id = insert_transaction_type(
                type_name,
                config['description'],
                config['affects_inventory'],
                config['affects_revenue']
            )
            
            if type_id:
                inv_flag = "✓" if config['affects_inventory'] else "✗"
                rev_flag = "✓" if config['affects_revenue'] else "✗"
                logger.info(f"✓ Created transaction type #{type_id}: {type_name} [Inv:{inv_flag} Rev:{rev_flag}]")
                success_count += 1
            else:
                failed_count += 1
                
        except Exception as e:
            logger.error(f"Error generating transaction type: {e}")
            failed_count += 1
    
    # Log summary
    log_generation_summary(logger, 'TRANSACTION_TYPE', success_count, failed_count, batch_size)
    
    # Log current totals
    total_types = count_records('TRANSACTION_TYPE')
    logger.info(f"Total transaction types in database: {total_types}")
    
    return success_count, failed_count

# ============================================
# SCRIPT EXECUTION
# ============================================

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("TRANSACTION TYPE GENERATOR STARTED")
    logger.info(f"Timestamp: {datetime.now()}")
    logger.info("=" * 60)
    
    try:
        success, failed = generate_transaction_types()
        exit_code = 0 if failed == 0 else 1
        
    except Exception as e:
        logger.error(f"Fatal error in transaction type generation: {e}")
        exit_code = 1
    
    logger.info("TRANSACTION TYPE GENERATOR FINISHED")
    logger.info("=" * 60)
    
    exit(exit_code)