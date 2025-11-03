#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 00:42:36 2024

@author: tin
"""

"""
Generate TRANSACTION_LINE records
Creates realistic transaction line items with products, quantities, pricing
"""

import random
from datetime import datetime
from config import BATCH_SIZES, DISCOUNT_PROBABILITY, DISCOUNT_PERCENTAGES
from utils import (
    setup_logger,
    execute_query,
    log_generation_summary,
    count_records,
    get_random_record,
    get_all_records,
    calculate_total_paid,
    round_price
)

# Setup logger
logger = setup_logger('TransactionLineGenerator')

# ============================================
# TRANSACTION LINE GENERATION LOGIC
# ============================================

def get_random_transaction_id():
    """Get random transaction header ID"""
    result = get_random_record('TRANSACTION_HEADER', 'Transaction_ID')
    if result:
        return result[0]
    return None

def get_random_product():
    """Get random product with details"""
    # Get product with positive stock
    result = get_random_record(
        'PRODUCT',
        'PLU, Description, Avg_Real_Cost, SOH',
        'SOH > 0'
    )
    
    if result:
        return result
    
    # If no products with stock, get any product
    result = get_random_record('PRODUCT', 'PLU, Description, Avg_Real_Cost, SOH')
    return result

def generate_quantity():
    """Generate realistic quantity"""
    # Most transactions are 1 item (70%)
    # Some are 2-5 items (25%)
    # Few are 6-10 items (5%)
    
    weights = [70, 25, 5]
    ranges = [(1, 1), (2, 5), (6, 10)]
    
    selected_range = random.choices(ranges, weights=weights)[0]
    return random.randint(*selected_range)

def generate_original_price(avg_cost):
    """
    Generate original price based on product cost
    Typical retail markup: 1.3x to 3x cost
    """
    markup = random.uniform(1.3, 3.0)
    base_price = avg_cost * markup
    
    # Round to realistic price (.49, .99, .95, etc.)
    return round_price(base_price)

def should_apply_discount():
    """Determine if discount should be applied"""
    return random.random() < DISCOUNT_PROBABILITY

def get_discount_percent():
    """Get discount percentage if applicable"""
    return random.choice(DISCOUNT_PERCENTAGES)

def check_transaction_has_lines(transaction_id):
    """Check if transaction already has line items"""
    query = "SELECT COUNT(*) FROM TRANSACTION_LINE WHERE Transaction_ID = ?"
    result = execute_query(query, (transaction_id,), fetch=True)
    return result[0][0] > 0

def insert_transaction_line(transaction_id, plu, qty, original_price, 
                           total_paid, discount_percent):
    """Insert transaction line into database"""
    query = """
        INSERT INTO TRANSACTION_LINE (
            Transaction_ID, PLU, Qty_Supplied, Original_Price,
            Total_Paid, Discount_Percent
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """
    try:
        line_id = execute_query(query, (
            transaction_id, plu, qty, original_price,
            total_paid, discount_percent
        ))
        return line_id
    except Exception as e:
        logger.error(f"Failed to insert transaction line: {e}")
        return None

# ============================================
# MAIN GENERATION FUNCTION
# ============================================

def generate_transaction_lines(batch_size=None):
    """
    Generate batch of transaction line records
    Each line item is linked to a transaction header
    """
    if batch_size is None:
        batch_size = BATCH_SIZES['TRANSACTION_LINE']
    
    logger.info(f"Starting transaction line generation - Batch size: {batch_size}")
    
    # Check dependencies
    transaction_count = count_records('TRANSACTION_HEADER')
    product_count = count_records('PRODUCT')
    
    if transaction_count == 0:
        logger.error("No transaction headers found. Run transaction header generator first.")
        return 0, batch_size
    
    if product_count == 0:
        logger.error("No products found. Run product generator first.")
        return 0, batch_size
    
    success_count = 0
    failed_count = 0
    
    # Strategy: Add 1-5 line items to transactions that don't have lines yet
    # Or add additional lines to existing transactions
    
    for i in range(batch_size):
        try:
            # Get random transaction
            transaction_id = get_random_transaction_id()
            if transaction_id is None:
                logger.error("Failed to get transaction ID")
                failed_count += 1
                continue
            
            # Get random product
            product = get_random_product()
            if product is None:
                logger.error("Failed to get product")
                failed_count += 1
                continue
            
            plu, description, avg_cost, soh = product
            
            # Generate quantity
            qty = generate_quantity()
            
            # Adjust quantity if exceeds stock
            if qty > soh and soh > 0:
                qty = soh
            elif soh == 0:
                qty = 1  # Allow even if out of stock (backorder)
            
            # Generate pricing
            original_price = generate_original_price(avg_cost)
            # Check if discount applies
            discount_percent = 0.0
            if should_apply_discount():
                discount_percent = get_discount_percent()
            
            # Calculate total paid
            total_paid = calculate_total_paid(original_price, qty, discount_percent)
            
            # Insert into database
            line_id = insert_transaction_line(
                transaction_id, plu, qty, original_price,
                total_paid, discount_percent
            )
            
            if line_id:
                discount_str = f" ({discount_percent}% off)" if discount_percent > 0 else ""
                logger.info(f"✓ Created line #{line_id}: Transaction #{transaction_id}, PLU {plu}, Qty {qty}, ${total_paid:.2f}{discount_str}")
                success_count += 1
            else:
                failed_count += 1
                
        except Exception as e:
            logger.error(f"Error generating transaction line: {e}")
            failed_count += 1
    
    # Log summary
    log_generation_summary(logger, 'TRANSACTION_LINE', success_count, failed_count, batch_size)
    
    # Log current totals
    total_lines = count_records('TRANSACTION_LINE')
    logger.info(f"Total transaction lines in database: {total_lines}")
    
    # Log statistics
    transactions_with_lines = execute_query(
        "SELECT COUNT(DISTINCT Transaction_ID) FROM TRANSACTION_LINE",
        fetch=True
    )[0][0]
    logger.info(f"Transactions with line items: {transactions_with_lines}/{transaction_count}")
    
    return success_count, failed_count

# ============================================
# SCRIPT EXECUTION
# ============================================

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("TRANSACTION LINE GENERATOR STARTED")
    logger.info(f"Timestamp: {datetime.now()}")
    logger.info("=" * 60)
    
    try:
        success, failed = generate_transaction_lines()
        exit_code = 0 if failed == 0 else 1
        
    except Exception as e:
        logger.error(f"Fatal error in transaction line generation: {e}")
        exit_code = 1
    
    logger.info("TRANSACTION LINE GENERATOR FINISHED")
    logger.info("=" * 60)
    
    exit(exit_code)