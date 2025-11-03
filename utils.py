#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 00:34:31 2024

@author: tin
"""

"""
Utility functions for data generation
Shared helper functions used across all generators
"""

import sqlite3
import logging
import random
import string
from datetime import datetime, timedelta
from config import DATABASE_PATH, LOG_FILE

# ============================================
# LOGGING SETUP
# ============================================

def setup_logger(script_name):
    """Setup logging for each script"""
    logger = logging.getLogger(script_name)
    logger.setLevel(logging.INFO)
    
    # File handler
    fh = logging.FileHandler(LOG_FILE)
    fh.setLevel(logging.INFO)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

# ============================================
# DATABASE FUNCTIONS
# ============================================

def get_db_connection():
    """Get SQLite database connection with foreign keys enabled"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def execute_query(query, params=None, fetch=False):
    """Execute a query and return results if needed"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            results = cursor.fetchall()
            conn.close()
            return results
        else:
            conn.commit()
            lastrowid = cursor.lastrowid
            conn.close()
            return lastrowid
    except sqlite3.Error as e:
        conn.close()
        raise e

def record_exists(table, column, value):
    """Check if a record with given value exists"""
    query = f"SELECT COUNT(*) FROM {table} WHERE {column} = ?"
    result = execute_query(query, (value,), fetch=True)
    return result[0][0] > 0

def get_random_record(table, column='*', where_clause=None):
    """Get a random record from a table"""
    if where_clause:
        query = f"SELECT {column} FROM {table} WHERE {where_clause} ORDER BY RANDOM() LIMIT 1"
    else:
        query = f"SELECT {column} FROM {table} ORDER BY RANDOM() LIMIT 1"
    
    result = execute_query(query, fetch=True)
    return result[0] if result else None

def get_all_records(table, column='*', where_clause=None):
    """Get all records from a table"""
    if where_clause:
        query = f"SELECT {column} FROM {table} WHERE {where_clause}"
    else:
        query = f"SELECT {column} FROM {table}"
    
    return execute_query(query, fetch=True)

def count_records(table, where_clause=None):
    """Count records in a table"""
    if where_clause:
        query = f"SELECT COUNT(*) FROM {table} WHERE {where_clause}"
    else:
        query = f"SELECT COUNT(*) FROM {table}"
    
    result = execute_query(query, fetch=True)
    return result[0][0]

# ============================================
# DATA GENERATION HELPERS
# ============================================

def generate_unique_value(generator_func, checker_func, max_retries=10):
    """
    Generate a unique value using generator function and checker function
    
    Args:
        generator_func: Function that generates a value
        checker_func: Function that checks if value exists (returns True if exists)
        max_retries: Maximum number of attempts
    
    Returns:
        Unique value or None if max retries exceeded
    """
    for _ in range(max_retries):
        value = generator_func()
        if not checker_func(value):
            return value
    return None

def random_string(length=10, chars=string.ascii_uppercase + string.digits):
    """Generate random string"""
    return ''.join(random.choice(chars) for _ in range(length))

def random_phone():
    """Generate random Australian phone number"""
    prefixes = ['04', '02', '03', '07', '08']
    prefix = random.choice(prefixes)
    if prefix == '04':  # Mobile
        return f"{prefix}{random.randint(10000000, 99999999)}"
    else:  # Landline
        return f"{prefix} {random.randint(1000, 9999)} {random.randint(1000, 9999)}"

def random_email(name):
    """Generate random email address"""
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'example.com']
    clean_name = name.lower().replace(' ', '.').replace("'", "")
    return f"{clean_name}@{random.choice(domains)}"

def random_date(start_date, end_date):
    """Generate random date between start and end"""
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randint(0, days_between)
    return start_date + timedelta(days=random_days)

def random_datetime(start_date, end_date, business_hours_only=True):
    """Generate random datetime between start and end"""
    random_date_val = random_date(start_date, end_date)
    
    if business_hours_only:
        hour = random.randint(8, 22)  # 8 AM to 10 PM
    else:
        hour = random.randint(0, 23)
    
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    
    return random_date_val.replace(hour=hour, minute=minute, second=second)

def format_datetime_sqlite(dt):
    """Format datetime for SQLite (YYYY-MM-DD HH:MM:SS)"""
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def format_date_sqlite(dt):
    """Format date for SQLite (YYYY-MM-DD)"""
    return dt.strftime('%Y-%m-%d')

def weighted_random_choice(choices, weights):
    """Make weighted random choice"""
    return random.choices(choices, weights=weights, k=1)[0]

def random_boolean(true_probability=0.5):
    """Generate random boolean with given probability of True"""
    return random.random() < true_probability

def round_price(price):
    """Round price to nearest 0.49 or 0.99 (common retail pricing)"""
    whole = int(price)
    decimal_choices = [0.49, 0.99, 0.95, 0.89, 0.79, 0.69]
    return whole + random.choice(decimal_choices)

# ============================================
# BUSINESS LOGIC HELPERS
# ============================================

def calculate_discount_amount(original_price, quantity, discount_percent):
    """Calculate discount dollar amount"""
    subtotal = original_price * quantity
    discount = subtotal * (discount_percent / 100)
    return round(discount, 2)

def calculate_total_paid(original_price, quantity, discount_percent):
    """Calculate total paid after discount"""
    subtotal = original_price * quantity
    discount = calculate_discount_amount(original_price, quantity, discount_percent)
    return round(subtotal - discount, 2)

def calculate_gross_profit(total_paid, cost, quantity):
    """Calculate gross profit"""
    total_cost = cost * quantity
    profit = total_paid - total_cost
    return round(profit, 2)

def calculate_gross_profit_percent(gross_profit, total_paid):
    """Calculate gross profit percentage"""
    if total_paid == 0:
        return 0.0
    return round((gross_profit / total_paid) * 100, 2)

# ============================================
# VALIDATION HELPERS
# ============================================

def validate_not_null(value, field_name):
    """Validate that value is not null"""
    if value is None or (isinstance(value, str) and value.strip() == ''):
        raise ValueError(f"{field_name} cannot be null or empty")
    return True

def validate_range(value, min_val, max_val, field_name):
    """Validate that value is within range"""
    if not (min_val <= value <= max_val):
        raise ValueError(f"{field_name} must be between {min_val} and {max_val}")
    return True

def validate_length(value, max_length, field_name):
    """Validate string length"""
    if len(value) > max_length:
        raise ValueError(f"{field_name} exceeds maximum length of {max_length}")
    return True

# ============================================
# LOGGING HELPERS
# ============================================

def log_generation_summary(logger, table_name, success_count, failed_count, batch_size):
    """Log summary of generation run"""
    logger.info("=" * 60)
    logger.info(f"Generation Summary for {table_name}")
    logger.info(f"Batch Size: {batch_size}")
    logger.info(f"Successfully Generated: {success_count}")
    logger.info(f"Failed: {failed_count}")
    logger.info(f"Success Rate: {(success_count/batch_size*100):.1f}%")
    logger.info("=" * 60)