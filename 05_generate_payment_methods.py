#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 00:38:53 2024

@author: tin
"""

"""
Generate PAYMENT_METHOD records
Creates realistic payment method reference data
"""

import random
from datetime import datetime
from config import REAL_PAYMENT_METHODS, BATCH_SIZES
from utils import (
    setup_logger,
    execute_query,
    record_exists,
    generate_unique_value,
    log_generation_summary,
    count_records
)

# Setup logger
logger = setup_logger('PaymentMethodGenerator')

# ============================================
# PAYMENT METHOD GENERATION LOGIC
# ============================================

# Extended payment methods beyond real data
EXTENDED_PAYMENT_METHODS = REAL_PAYMENT_METHODS + [
    "VISA", "MASTERCARD", "AMEX", "PAYPAL", "AFTERPAY",
    "ZIP PAY", "MOBILE PAYMENT", "APPLE PAY", "GOOGLE PAY",
    "SAMSUNG PAY", "GIFT CARD", "STORE CREDIT", "VOUCHER"
]

PAYMENT_DESCRIPTIONS = {
    "EFTPOS": "Electronic Funds Transfer at Point of Sale",
    "CASH": "Cash payment",
    "CREDIT CARD": "Credit card payment",
    "DEBIT CARD": "Debit card payment",
    "CONTACTLESS": "Contactless tap payment",
    "VISA": "Visa card payment",
    "MASTERCARD": "Mastercard payment",
    "AMEX": "American Express payment",
    "PAYPAL": "PayPal digital payment",
    "AFTERPAY": "Buy now, pay later - Afterpay",
    "ZIP PAY": "Buy now, pay later - Zip Pay",
    "MOBILE PAYMENT": "Mobile wallet payment",
    "APPLE PAY": "Apple Pay contactless",
    "GOOGLE PAY": "Google Pay contactless",
    "SAMSUNG PAY": "Samsung Pay contactless",
    "GIFT CARD": "Store gift card redemption",
    "STORE CREDIT": "Store credit/refund balance",
    "VOUCHER": "Promotional voucher"
}

PROCESSING_FEES = {
    "EFTPOS": 0.5,
    "CASH": 0.0,
    "CREDIT CARD": 1.5,
    "DEBIT CARD": 0.8,
    "CONTACTLESS": 1.0,
    "VISA": 1.6,
    "MASTERCARD": 1.5,
    "AMEX": 2.5,
    "PAYPAL": 2.9,
    "AFTERPAY": 4.0,
    "ZIP PAY": 4.0,
    "MOBILE PAYMENT": 1.0,
    "APPLE PAY": 1.0,
    "GOOGLE PAY": 1.0,
    "SAMSUNG PAY": 1.0,
    "GIFT CARD": 0.0,
    "STORE CREDIT": 0.0,
    "VOUCHER": 0.0
}

def generate_payment_method_name():
    """Generate payment method name"""
    return random.choice(EXTENDED_PAYMENT_METHODS)

def get_payment_description(name):
    """Get description for payment method"""
    return PAYMENT_DESCRIPTIONS.get(name, f"{name} payment method")

def get_processing_fee(name):
    """Get processing fee for payment method"""
    return PROCESSING_FEES.get(name, round(random.uniform(0.5, 2.0), 2))

def payment_method_exists(name):
    """Check if payment method with name already exists"""
    return record_exists('PAYMENT_METHOD', 'Payment_Method_Name', name)

def insert_payment_method(name, description, processing_fee, active_status):
    """Insert payment method into database"""
    query = """
        INSERT INTO PAYMENT_METHOD (
            Payment_Method_Name, Description, Processing_Fee_Percent, Active_Status
        )
        VALUES (?, ?, ?, ?)
    """
    try:
        payment_id = execute_query(query, (name, description, processing_fee, active_status))
        return payment_id
    except Exception as e:
        logger.error(f"Failed to insert payment method '{name}': {e}")
        return None

# ============================================
# MAIN GENERATION FUNCTION
# ============================================

def generate_payment_methods(batch_size=None):
    """Generate batch of payment method records"""
    if batch_size is None:
        batch_size = BATCH_SIZES['PAYMENT_METHOD']
    
    logger.info(f"Starting payment method generation - Batch size: {batch_size}")
    
    success_count = 0
    failed_count = 0
    
    for i in range(batch_size):
        try:
            # Generate unique payment method name
            payment_name = generate_unique_value(
                generate_payment_method_name,
                payment_method_exists,
                max_retries=30
            )
            
            if payment_name is None:
                logger.warning(f"Could not generate unique payment method name after max retries")
                failed_count += 1
                continue
            
            # Generate other fields
            description = get_payment_description(payment_name)
            processing_fee = get_processing_fee(payment_name)
            active_status = 1 if random.random() < 0.96 else 0  # 96% active
            
            # Insert into database
            payment_id = insert_payment_method(payment_name, description, processing_fee, active_status)
            
            if payment_id:
                logger.info(f"✓ Created payment method #{payment_id}: {payment_name} ({processing_fee}% fee)")
                success_count += 1
            else:
                failed_count += 1
                
        except Exception as e:
            logger.error(f"Error generating payment method: {e}")
            failed_count += 1
    
    # Log summary
    log_generation_summary(logger, 'PAYMENT_METHOD', success_count, failed_count, batch_size)
    
    # Log current totals
    total_payment_methods = count_records('PAYMENT_METHOD')
    logger.info(f"Total payment methods in database: {total_payment_methods}")
    
    return success_count, failed_count

# ============================================
# SCRIPT EXECUTION
# ============================================

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("PAYMENT METHOD GENERATOR STARTED")
    logger.info(f"Timestamp: {datetime.now()}")
    logger.info("=" * 60)
    
    try:
        success, failed = generate_payment_methods()
        exit_code = 0 if failed == 0 else 1
        
    except Exception as e:
        logger.error(f"Fatal error in payment method generation: {e}")
        exit_code = 1
    
    logger.info("PAYMENT METHOD GENERATOR FINISHED")
    logger.info("=" * 60)
    
    exit(exit_code)