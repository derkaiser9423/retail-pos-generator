#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 00:38:34 2025

@author: tin
"""

"""
Generate MACHINE records
Creates realistic POS terminal/machine data
"""

import random
from datetime import datetime, timedelta
from config import REAL_MACHINES, BATCH_SIZES
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
logger = setup_logger('MachineGenerator')

# ============================================
# MACHINE GENERATION LOGIC
# ============================================

LOCATIONS = [
    "Front Counter", "Pharmacy Counter", "Back Counter",
    "Left Wing", "Right Wing", "Central Station",
    "Express Lane", "Main Entrance", "Dispensary",
    "Beauty Section", "Health Section", "Customer Service",
    "Store Front", "Store Rear", "Mobile Unit"
]

def generate_machine_name():
    """Generate machine name in TILLXX format"""
    # Get existing machines to find next number
    existing = execute_query(
        "SELECT Machine_Name FROM MACHINE WHERE Machine_Name LIKE 'TILL%'",
        fetch=True
    )
    
    existing_numbers = []
    for (name,) in existing:
        try:
            num = int(name.replace('TILL', '').replace('0', ''))
            existing_numbers.append(num)
        except:
            continue
    
    # Find next available number
    if existing_numbers:
        next_num = max(existing_numbers) + 1
    else:
        next_num = 1
    
    # 80% chance: Use TILLXX format, 20% chance: Use custom name
    if random.random() < 0.8:
        return f"TILL{next_num:02d}"
    else:
        prefixes = ["POS", "TERMINAL", "REGISTER", "CHECKOUT"]
        return f"{random.choice(prefixes)}{next_num:02d}"

def generate_location():
    """Generate machine location"""
    # 25% chance of no location
    if random.random() < 0.25:
        return None
    
    return random.choice(LOCATIONS)

def generate_install_date():
    """Generate installation date"""
    # 30% chance of no install date
    if random.random() < 0.3:
        return None
    
    # Install date between 3 years ago and 1 week ago
    end_date = datetime.now() - timedelta(days=7)
    start_date = datetime.now() - timedelta(days=365*3)
    
    install_date = random_date(start_date, end_date)
    return format_date_sqlite(install_date)

def machine_exists(name):
    """Check if machine with name already exists"""
    return record_exists('MACHINE', 'Machine_Name', name)

def insert_machine(name, location, active_status, install_date):
    """Insert machine into database"""
    query = """
        INSERT INTO MACHINE (Machine_Name, Location, Active_Status, Install_Date)
        VALUES (?, ?, ?, ?)
    """
    try:
        machine_id = execute_query(query, (name, location, active_status, install_date))
        return machine_id
    except Exception as e:
        logger.error(f"Failed to insert machine '{name}': {e}")
        return None

# ============================================
# MAIN GENERATION FUNCTION
# ============================================

def generate_machines(batch_size=None):
    """Generate batch of machine records"""
    if batch_size is None:
        batch_size = BATCH_SIZES['MACHINE']
    
    logger.info(f"Starting machine generation - Batch size: {batch_size}")
    
    success_count = 0
    failed_count = 0
    
    for i in range(batch_size):
        try:
            # Generate unique machine name
            machine_name = generate_unique_value(
                generate_machine_name,
                machine_exists,
                max_retries=20
            )
            
            if machine_name is None:
                logger.warning(f"Could not generate unique machine name after max retries")
                failed_count += 1
                continue
            
            # Generate other fields
            location = generate_location()
            active_status = 1 if random.random() < 0.98 else 0  # 98% active
            install_date = generate_install_date()
            
            # Insert into database
            machine_id = insert_machine(machine_name, location, active_status, install_date)
            
            if machine_id:
                logger.info(f"✓ Created machine #{machine_id}: {machine_name} at {location or 'Unknown'}")
                success_count += 1
            else:
                failed_count += 1
                
        except Exception as e:
            logger.error(f"Error generating machine: {e}")
            failed_count += 1
    
    # Log summary
    log_generation_summary(logger, 'MACHINE', success_count, failed_count, batch_size)
    
    # Log current totals
    total_machines = count_records('MACHINE')
    logger.info(f"Total machines in database: {total_machines}")
    
    return success_count, failed_count

# ============================================
# SCRIPT EXECUTION
# ============================================

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("MACHINE GENERATOR STARTED")
    logger.info(f"Timestamp: {datetime.now()}")
    logger.info("=" * 60)
    
    try:
        success, failed = generate_machines()
        exit_code = 0 if failed == 0 else 1
        
    except Exception as e:
        logger.error(f"Fatal error in machine generation: {e}")
        exit_code = 1
    
    logger.info("MACHINE GENERATOR FINISHED")
    logger.info("=" * 60)
    
    exit(exit_code)