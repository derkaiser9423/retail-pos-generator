#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 00:37:12 2024

@author: tin
"""

"""
Generate STAFF records
Creates realistic staff/employee data based on real patterns
"""

import random
from datetime import datetime, timedelta
from config import FIRST_NAMES, LAST_INITIALS, BATCH_SIZES
from utils import (
    setup_logger,
    execute_query,
    record_exists,
    generate_unique_value,
    log_generation_summary,
    count_records,
    random_date,
    format_date_sqlite
)

# Setup logger
logger = setup_logger('StaffGenerator')

# ============================================
# STAFF GENERATION LOGIC
# ============================================

JOB_ROLES = [
    "Pharmacist", "Pharmacy Assistant", "Pharmacy Technician",
    "Store Manager", "Assistant Manager", "Sales Assistant",
    "Customer Service", "Cashier", "Stock Controller",
    "Beauty Consultant", "Health Advisor", "Trainee"
]

def generate_staff_name():
    """Generate staff name in format: FirstName LastInitial ID"""
    first_name = random.choice(FIRST_NAMES)
    last_initial = random.choice(LAST_INITIALS)
    staff_id_number = random.randint(10000, 999999)
    
    # Match real pattern: "Andy R 61499" (name, space, initial, space, ID)
    return f"{first_name} {last_initial} {staff_id_number}"

def generate_hire_date():
    """Generate realistic hire date"""
    # 30% chance of no hire date
    if random.random() < 0.3:
        return None
    
    # Hire date between 5 years ago and 1 month ago
    end_date = datetime.now() - timedelta(days=30)
    start_date = datetime.now() - timedelta(days=365*5)
    
    hire_date = random_date(start_date, end_date)
    return format_date_sqlite(hire_date)

def generate_role():
    """Generate job role"""
    # 20% chance of no role specified
    if random.random() < 0.2:
        return None
    
    return random.choice(JOB_ROLES)

def staff_exists(name):
    """Check if staff with name already exists"""
    return record_exists('STAFF', 'Staff_Name', name)

def insert_staff(name, active_status, hire_date, role):
    """Insert staff into database"""
    query = """
        INSERT INTO STAFF (Staff_Name, Active_Status, Hire_Date, Role)
        VALUES (?, ?, ?, ?)
    """
    try:
        staff_id = execute_query(query, (name, active_status, hire_date, role))
        return staff_id
    except Exception as e:
        logger.error(f"Failed to insert staff '{name}': {e}")
        return None

# ============================================
# MAIN GENERATION FUNCTION
# ============================================

def generate_staff(batch_size=None):
    """Generate batch of staff records"""
    if batch_size is None:
        batch_size = BATCH_SIZES['STAFF']
    
    logger.info(f"Starting staff generation - Batch size: {batch_size}")
    
    success_count = 0
    failed_count = 0
    
    for i in range(batch_size):
        try:
            # Generate unique staff name
            staff_name = generate_unique_value(
                generate_staff_name,
                staff_exists,
                max_retries=50  # Higher retries due to ID randomness
            )
            
            if staff_name is None:
                logger.warning(f"Could not generate unique staff name after max retries")
                failed_count += 1
                continue
            
            # Generate other fields
            active_status = 1 if random.random() < 0.92 else 0  # 92% active
            hire_date = generate_hire_date()
            role = generate_role()
            
            # Insert into database
            staff_id = insert_staff(staff_name, active_status, hire_date, role)
            
            if staff_id:
                logger.info(f"✓ Created staff #{staff_id}: {staff_name} ({role or 'No role'})")
                success_count += 1
            else:
                failed_count += 1
                
        except Exception as e:
            logger.error(f"Error generating staff: {e}")
            failed_count += 1
    
    # Log summary
    log_generation_summary(logger, 'STAFF', success_count, failed_count, batch_size)
    
    # Log current totals
    total_staff = count_records('STAFF')
    logger.info(f"Total staff in database: {total_staff}")
    
    return success_count, failed_count

# ============================================
# SCRIPT EXECUTION
# ============================================

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("STAFF GENERATOR STARTED")
    logger.info(f"Timestamp: {datetime.now()}")
    logger.info("=" * 60)
    
    try:
        success, failed = generate_staff()
        exit_code = 0 if failed == 0 else 1
        
    except Exception as e:
        logger.error(f"Fatal error in staff generation: {e}")
        exit_code = 1
    
    logger.info("STAFF GENERATOR FINISHED")
    logger.info("=" * 60)
    
    exit(exit_code)