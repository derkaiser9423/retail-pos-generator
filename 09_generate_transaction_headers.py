#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 00:42:26 2024

@author: tin
"""

"""
Generate TRANSACTION_HEADER records
Creates realistic transaction header data with proper foreign keys
"""

import random
from datetime import datetime
from config import BATCH_SIZES, DATE_RANGE, BUSINESS_HOURS
from utils import (
    setup_logger,
    execute_query,
    log_generation_summary,
    count_records,
    get_random_record,
    get_all_records,
    random_datetime,
    format_datetime_sqlite,
    random_boolean
)

# Setup logger
logger = setup_logger('TransactionHeaderGenerator')

# ============================================
# TRANSACTION HEADER GENERATION LOGIC
# ============================================

def generate_transaction_timestamp():
    """Generate realistic transaction timestamp"""
    start_date = DATE_RANGE['start_date']
    end_date = DATE_RANGE['end_date']
    
    # Generate during business hours (8 AM - 10 PM)
    transaction_dt = random_datetime(start_date, end_date, business_hours_only=True)
    
    return format_datetime_sqlite(transaction_dt)

def get_random_staff_id():
    """Get random active staff ID"""
    result = get_random_record('STAFF', 'Staff_ID', 'Active_Status = 1')
    if result:
        return result[0]
    
    # If no active staff, get any staff
    result = get_random_record('STAFF', 'Staff_ID')
    if result:
        return result[0]
    
    return None

def get_random_machine_id():
    """Get random active machine ID"""
    result = get_random_record('MACHINE', 'Machine_ID', 'Active_Status = 1')
    if result:
        return result[0]
    
    # If no active machines, get any machine
    result = get_random_record('MACHINE', 'Machine_ID')
    if result:
        return result[0]
    
    return None

def get_random_payment_method_id():
    """Get random active payment method ID"""
    result = get_random_record('PAYMENT_METHOD', 'Payment_Method_ID', 'Active_Status = 1')
    if result:
        return result[0]
    
    # If no active payment methods, get any
    result = get_random_record('PAYMENT_METHOD', 'Payment_Method_ID')
    if result:
        return result[0]
    
    return None

def get_random_transaction_type_id():
    """Get random transaction type ID"""
    # Weight towards "Normal Item Sale" (80% of transactions)
    all_types = get_all_records('TRANSACTION_TYPE', 'Transaction_Type_ID, Transaction_Type_Name')
    
    if not all_types:
        return None
    
    # Find "Normal Item Sale" type
    normal_sale_id = None
    for type_id, type_name in all_types:
        if type_name == "Normal Item Sale":
            normal_sale_id = type_id
            break
    
    # 80% chance of Normal Item Sale, 20% random other type
    if normal_sale_id and random.random() < 0.8:
        return normal_sale_id
    else:
        return random.choice(all_types)[0]

def get_for_staff_id(staff_id):
    """
    Determine if transaction is for a staff member
    10% chance it's a staff purchase
    """
    if random.random() < 0.1:  # 10% staff purchases
        # Could be for the same staff or different staff
        if random.random() < 0.5:
            return staff_id  # Same staff
        else:
            # Different staff
            result = get_random_record('STAFF', 'Staff_ID')
            if result:
                return result[0]
    
    return None  # Regular customer transaction

def insert_transaction_header(timestamp, staff_id, machine_id, payment_method_id,
                              transaction_type_id, for_staff_id):
    """Insert transaction header into database"""
    query = """
        INSERT INTO TRANSACTION_HEADER (
            Time_Stamp, Staff_ID, Machine_ID, Payment_Method_ID,
            Transaction_Type_ID, For_Staff_ID
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """
    try:
        transaction_id = execute_query(query, (
            timestamp, staff_id, machine_id, payment_method_id,
            transaction_type_id, for_staff_id
        ))
        return transaction_id
    except Exception as e:
        logger.error(f"Failed to insert transaction header: {e}")
        return None

# ============================================
# MAIN GENERATION FUNCTION
# ============================================

def generate_transaction_headers(batch_size=None):
    """Generate batch of transaction header records"""
    if batch_size is None:
        batch_size = BATCH_SIZES['TRANSACTION_HEADER']
    
    logger.info(f"Starting transaction header generation - Batch size: {batch_size}")
    
    # Check dependencies
    staff_count = count_records('STAFF')
    machine_count = count_records('MACHINE')
    payment_count = count_records('PAYMENT_METHOD')
    type_count = count_records('TRANSACTION_TYPE')
    
    if staff_count == 0:
        logger.error("No staff found. Run staff generator first.")
        return 0, batch_size
    
    if machine_count == 0:
        logger.error("No machines found. Run machine generator first.")
        return 0, batch_size
    
    if payment_count == 0:
        logger.error("No payment methods found. Run payment method generator first.")
        return 0, batch_size
    
    if type_count == 0:
        logger.error("No transaction types found. Run transaction type generator first.")
        return 0, batch_size
    
    success_count = 0
    failed_count = 0
    
    for i in range(batch_size):
        try:
            # Generate transaction data
            timestamp = generate_transaction_timestamp()
            staff_id = get_random_staff_id()
            machine_id = get_random_machine_id()
            payment_method_id = get_random_payment_method_id()
            transaction_type_id = get_random_transaction_type_id()
            
            if None in [staff_id, machine_id, payment_method_id, transaction_type_id]:
                logger.error("Failed to get required foreign keys")
                failed_count += 1
                continue
            
            # Determine if for staff
            for_staff_id = get_for_staff_id(staff_id)
            
            # Insert into database
            transaction_id = insert_transaction_header(
                timestamp, staff_id, machine_id, payment_method_id,
                transaction_type_id, for_staff_id
            )
            
            if transaction_id:
                staff_flag = f" [Staff Purchase]" if for_staff_id else ""
                logger.info(f"✓ Created transaction #{transaction_id}: {timestamp} on Machine #{machine_id}{staff_flag}")
                success_count += 1
            else:
                failed_count += 1
                
        except Exception as e:
            logger.error(f"Error generating transaction header: {e}")
            failed_count += 1
    
    # Log summary
    log_generation_summary(logger, 'TRANSACTION_HEADER', success_count, failed_count, batch_size)
    
    # Log current totals
    total_transactions = count_records('TRANSACTION_HEADER')
    logger.info(f"Total transaction headers in database: {total_transactions}")
    
    return success_count, failed_count

# ============================================
# SCRIPT EXECUTION
# ============================================

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("TRANSACTION HEADER GENERATOR STARTED")
    logger.info(f"Timestamp: {datetime.now()}")
    logger.info("=" * 60)
    
    try:
        success, failed = generate_transaction_headers()
        exit_code = 0 if failed == 0 else 1
        
    except Exception as e:
        logger.error(f"Fatal error in transaction header generation: {e}")
        exit_code = 1
    
    logger.info("TRANSACTION HEADER GENERATOR FINISHED")
    logger.info("=" * 60)
    
    exit(exit_code)