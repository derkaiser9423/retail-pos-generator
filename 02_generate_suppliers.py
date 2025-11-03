#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 00:36:22 2025

@author: tin
"""

"""
Generate SUPPLIER records
Creates realistic supplier/vendor data
"""

import random
from datetime import datetime
from config import REAL_SUPPLIERS, BATCH_SIZES
from utils import (
    setup_logger,
    execute_query,
    record_exists,
    generate_unique_value,
    log_generation_summary,
    count_records,
    random_phone,
    random_email
)

# Setup logger
logger = setup_logger('SupplierGenerator')

# ============================================
# SUPPLIER GENERATION LOGIC
# ============================================

# Extended supplier company names
SUPPLIER_COMPANY_TYPES = [
    "Pharmaceuticals", "Labs", "Healthcare", "Medical Supplies",
    "Wellness", "Beauty", "Cosmetics", "Personal Care",
    "Nutrition", "Supplements", "Wholesale", "Distribution",
    "Group", "Industries", "International", "Australia"
]

SUPPLIER_PREFIXES = [
    "Global", "Premier", "United", "National", "Australian",
    "Pacific", "Metro", "Elite", "Quality", "Professional",
    "Advanced", "Supreme", "Direct", "Prime", "Select"
]

def generate_supplier_name():
    """Generate realistic supplier name"""
    
    # 50% chance: Use pattern from real supplier codes
    if random.random() < 0.5 and REAL_SUPPLIERS:
        code = random.choice(REAL_SUPPLIERS).replace('.', '').upper()
        
        # Expand code into full company name
        if len(code) <= 4:
            prefix = random.choice(SUPPLIER_PREFIXES)
            suffix = random.choice(SUPPLIER_COMPANY_TYPES)
            return f"{prefix} {suffix} ({code})"
        else:
            suffix = random.choice(SUPPLIER_COMPANY_TYPES)
            return f"{code} {suffix}"
    
    # 50% chance: Generate new supplier name
    structures = [
        lambda: f"{random.choice(SUPPLIER_PREFIXES)} {random.choice(SUPPLIER_COMPANY_TYPES)} Pty Ltd",
        lambda: f"{random.choice(['ABC', 'XYZ', 'RST', 'MNO', 'DEF'])} {random.choice(SUPPLIER_COMPANY_TYPES)}",
        lambda: f"{random.choice(SUPPLIER_COMPANY_TYPES)} {random.choice(['Direct', 'Plus', 'Pro', 'Express'])}",
    ]
    
    return random.choice(structures)()

def generate_contact_name():
    """Generate contact person name"""
    first_names = [
        "John", "Sarah", "Michael", "Emma", "David", "Lisa",
        "James", "Jennifer", "Robert", "Maria", "William", "Amanda"
    ]
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
        "Miller", "Davis", "Rodriguez", "Martinez", "Wilson", "Anderson"
    ]
    
    # 20% chance of no contact name
    if random.random() < 0.2:
        return None
    
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_address():
    """Generate Australian business address"""
    # 30% chance of no address
    if random.random() < 0.3:
        return None
    
    street_number = random.randint(1, 999)
    street_names = [
        "George", "Pitt", "King", "Elizabeth", "Bourke",
        "Collins", "Swanston", "Queen", "Flinders", "Market"
    ]
    street_types = ["Street", "Road", "Avenue", "Drive", "Way"]
    
    suburbs = [
        "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide",
        "Newcastle", "Gold Coast", "Canberra", "Hobart", "Darwin"
    ]
    
    states = ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "NT", "ACT"]
    
    street = f"{street_number} {random.choice(street_names)} {random.choice(street_types)}"
    suburb = random.choice(suburbs)
    state = random.choice(states)
    postcode = random.randint(2000, 7999)
    
    return f"{street}, {suburb} {state} {postcode}"

def generate_payment_terms():
    """Generate payment terms"""
    # 40% chance of no payment terms
    if random.random() < 0.4:
        return None
    
    terms = [
        "Net 7", "Net 14", "Net 30", "Net 60", "Net 90",
        "EOM", "COD", "Due on Receipt", "2/10 Net 30"
    ]
    return random.choice(terms)

def supplier_exists(name):
    """Check if supplier with name already exists"""
    return record_exists('SUPPLIER', 'Supplier_Name', name)

def insert_supplier(name, contact_name, contact_phone, contact_email, address, payment_terms, active_status):
    """Insert supplier into database"""
    query = """
        INSERT INTO SUPPLIER (
            Supplier_Name, Contact_Name, Contact_Phone, Contact_Email,
            Address, Payment_Terms, Active_Status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    try:
        supplier_id = execute_query(query, (
            name, contact_name, contact_phone, contact_email,
            address, payment_terms, active_status
        ))
        return supplier_id
    except Exception as e:
        logger.error(f"Failed to insert supplier '{name}': {e}")
        return None

# ============================================
# MAIN GENERATION FUNCTION
# ============================================

def generate_suppliers(batch_size=None):
    """Generate batch of supplier records"""
    if batch_size is None:
        batch_size = BATCH_SIZES['SUPPLIER']
    
    logger.info(f"Starting supplier generation - Batch size: {batch_size}")
    
    success_count = 0
    failed_count = 0
    
    for i in range(batch_size):
        try:
            # Generate unique supplier name
            supplier_name = generate_unique_value(
                generate_supplier_name,
                supplier_exists,
                max_retries=20
            )
            
            if supplier_name is None:
                logger.warning(f"Could not generate unique supplier name after max retries")
                failed_count += 1
                continue
            
            # Generate other fields
            contact_name = generate_contact_name()
            contact_phone = random_phone()
            contact_email = random_email(supplier_name.split()[0]) if contact_name else None
            address = generate_address()
            payment_terms = generate_payment_terms()
            active_status = 1 if random.random() < 0.95 else 0  # 95% active
            
            # Insert into database
            supplier_id = insert_supplier(
                supplier_name, contact_name, contact_phone, contact_email,
                address, payment_terms, active_status
            )
            
            if supplier_id:
                logger.info(f"✓ Created supplier #{supplier_id}: {supplier_name}")
                success_count += 1
            else:
                failed_count += 1
                
        except Exception as e:
            logger.error(f"Error generating supplier: {e}")
            failed_count += 1
    
    # Log summary
    log_generation_summary(logger, 'SUPPLIER', success_count, failed_count, batch_size)
    
    # Log current totals
    total_suppliers = count_records('SUPPLIER')
    logger.info(f"Total suppliers in database: {total_suppliers}")
    
    return success_count, failed_count

# ============================================
# SCRIPT EXECUTION
# ============================================

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("SUPPLIER GENERATOR STARTED")
    logger.info(f"Timestamp: {datetime.now()}")
    logger.info("=" * 60)
    
    try:
        success, failed = generate_suppliers()
        exit_code = 0 if failed == 0 else 1
        
    except Exception as e:
        logger.error(f"Fatal error in supplier generation: {e}")
        exit_code = 1
    
    logger.info("SUPPLIER GENERATOR FINISHED")
    logger.info("=" * 60)
    
    exit(exit_code)