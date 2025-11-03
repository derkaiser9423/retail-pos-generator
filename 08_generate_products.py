#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 00:41:38 2024

@author: tin
"""

"""
Generate PRODUCT records
Creates realistic product data with pricing, costs, and inventory
"""

import random
from datetime import datetime
from config import (
    BATCH_SIZES, PRICE_RANGES, COST_MARGIN_RANGE, STOCK_RANGE,
    PRODUCT_PREFIXES, PRODUCT_CATEGORIES_WORDS, PRODUCT_SIZES
)
from utils import (
    setup_logger,
    execute_query,
    record_exists,
    generate_unique_value,
    log_generation_summary,
    count_records,
    get_random_record,
    round_price
)

# Setup logger
logger = setup_logger('ProductGenerator')

# ============================================
# PRODUCT GENERATION LOGIC
# ============================================

# Brand names from real data
BRAND_NAMES = [
    "Blackmores", "Swisse", "Nature's Way", "Healthy Care", "Colgate",
    "Oral B", "Panadol", "Nurofen", "Dettol", "Nivea", "Neutrogena",
    "Lucas Papaw", "Goat", "Bosisto's", "La Roche-Posay", "Cetaphil",
    "QV", "Ego", "Elastoplast", "Bandaid", "Listerine", "Berocca",
    "Ostelin", "Life-Space", "Difflam", "Sudafed", "Panadol",
    "Johnsons", "Curash", "Avent", "Huggies", "Libra", "U by Kotex"
]

def generate_plu():
    """Generate PLU code (3-6 digits)"""
    length = random.choices([3, 4, 5, 6], weights=[10, 30, 40, 20])[0]
    return str(random.randint(10**(length-1), 10**length - 1))

def generate_product_description():
    """Generate realistic product description"""
    
    # Structure: [Brand] [Prefix] [Category] [Size]
    # Example: "Blackmores Super Strength CoQ10 300mg 30 Capsules"
    
    structures = [
        # Brand + Category + Size (most common)
        lambda: f"{random.choice(BRAND_NAMES)} {random.choice(PRODUCT_CATEGORIES_WORDS)} {random.choice(PRODUCT_SIZES)}",
        
        # Brand + Prefix + Category + Size
        lambda: f"{random.choice(BRAND_NAMES)} {random.choice(PRODUCT_PREFIXES)} {random.choice(PRODUCT_CATEGORIES_WORDS)} {random.choice(PRODUCT_SIZES)}",
        
        # Just Category + Size
        lambda: f"{random.choice(PRODUCT_CATEGORIES_WORDS)} {random.choice(PRODUCT_SIZES)}",
        
        # Brand + Two Categories + Size
        lambda: f"{random.choice(BRAND_NAMES)} {random.choice(PRODUCT_CATEGORIES_WORDS)} {random.choice(PRODUCT_CATEGORIES_WORDS[:10])} {random.choice(PRODUCT_SIZES)}",
    ]
    
    description = random.choice(structures)()
    
    # Pad with spaces to match real data format (80-100 chars with trailing spaces)
    # Real data has descriptions padded to ~100 characters
    target_length = random.randint(80, 100)
    if len(description) < target_length:
        description = description + ' ' * (target_length - len(description))
    
    return description

def generate_product_price():
    """Generate realistic product price"""
    # Price distribution based on real data analysis
    # Most products: $2.50 - $50
    # Some expensive: $50 - $100
    
    if random.random() < 0.85:  # 85% common range
        base_price = random.uniform(PRICE_RANGES['common_low'], PRICE_RANGES['common_high'])
    else:  # 15% higher range
        base_price = random.uniform(PRICE_RANGES['common_high'], PRICE_RANGES['max'])
    
    # Round to .49, .99, .95, etc.
    return round_price(base_price)

def generate_cost_from_price(price):
    """Generate cost based on price (Avg Real Cost)"""
    # Cost is typically 30-85% of sale price
    margin = random.uniform(*COST_MARGIN_RANGE)
    cost = price * margin
    return round(cost, 2)

def generate_stock_on_hand():
    """Generate realistic stock on hand"""
    # Most items have 5-50 units
    # Some items out of stock (0)
    # Few items with high stock (50-100)
    
    weights = [5, 70, 20, 5]  # 0, low, medium, high
    ranges = [
        (0, 0),
        (STOCK_RANGE['typical_low'], STOCK_RANGE['typical_high']),
        (STOCK_RANGE['typical_high'], 75),
        (75, STOCK_RANGE['max'])
    ]
    
    selected_range = random.choices(ranges, weights=weights)[0]
    return random.randint(*selected_range)

def generate_expected_stock(soh):
    """Generate expected stock based on SOH"""
    # EXP is typically similar to SOH or slightly higher
    # 30% chance of null
    if random.random() < 0.3:
        return None
    
    # Usually within +/- 30% of SOH
    variation = random.uniform(0.7, 1.3)
    exp = int(soh * variation)
    return max(0, exp)

def generate_history():
    """Generate sales history (space-separated monthly sales)"""
    # Generate 12-13 months of history
    months = random.randint(12, 13)
    history_values = []
    
    # Base monthly sales
    base_sales = random.randint(5, 50)
    
    for _ in range(months):
        # Add variation +/- 50%
        variation = random.uniform(0.5, 1.5)
        monthly_sales = int(base_sales * variation)
        history_values.append(str(max(0, monthly_sales)))
    
    return ' '.join(history_values)

def get_random_product_group_id():
    """Get random product group ID"""
    result = get_random_record('PRODUCT_GROUP', 'Product_Group_ID')
    if result:
        return result[0]
    return None

def get_random_supplier_id():
    """Get random supplier ID"""
    result = get_random_record('SUPPLIER', 'Supplier_ID')
    if result:
        return result[0]
    return None

def plu_exists(plu):
    """Check if PLU already exists"""
    return record_exists('PRODUCT', 'PLU', plu)

def insert_product(plu, description, avg_real_cost, soh, exp, history, 
                  product_group_id, supplier_id):
    """Insert product into database"""
    query = """
        INSERT INTO PRODUCT (
            PLU, Description, Avg_Real_Cost, SOH, EXP, History,
            Product_Group_ID, Supplier_ID
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        execute_query(query, (
            plu, description, avg_real_cost, soh, exp, history,
            product_group_id, supplier_id
        ))
        return plu
    except Exception as e:
        logger.error(f"Failed to insert product PLU '{plu}': {e}")
        return None

# ============================================
# MAIN GENERATION FUNCTION
# ============================================

def generate_products(batch_size=None):
    """Generate batch of product records"""
    if batch_size is None:
        batch_size = BATCH_SIZES['PRODUCT']
    
    logger.info(f"Starting product generation - Batch size: {batch_size}")
    
    # Check dependencies
    group_count = count_records('PRODUCT_GROUP')
    supplier_count = count_records('SUPPLIER')
    
    if group_count == 0:
        logger.error("No product groups found. Run product group generator first.")
        return 0, batch_size
    
    if supplier_count == 0:
        logger.error("No suppliers found. Run supplier generator first.")
        return 0, batch_size
    
    success_count = 0
    failed_count = 0
    
    for i in range(batch_size):
        try:
            # Generate unique PLU
            plu = generate_unique_value(
                generate_plu,
                plu_exists,
                max_retries=50
            )
            
            if plu is None:
                logger.warning(f"Could not generate unique PLU after max retries")
                failed_count += 1
                continue
            
            # Generate product data
            description = generate_product_description()
            price = generate_product_price()  # For reference (not stored in PRODUCT table)
            avg_real_cost = generate_cost_from_price(price)
            soh = generate_stock_on_hand()
            exp = generate_expected_stock(soh)
            history = generate_history()
            
            # Get foreign keys
            product_group_id = get_random_product_group_id()
            supplier_id = get_random_supplier_id()
            
            if product_group_id is None or supplier_id is None:
                logger.error("Failed to get required foreign keys")
                failed_count += 1
                continue
            
            # Insert into database
            result = insert_product(
                plu, description, avg_real_cost, soh, exp, history,
                product_group_id, supplier_id
            )
            
            if result:
                logger.info(f"✓ Created product PLU {plu}: {description.strip()[:50]}... (SOH: {soh}, Cost: ${avg_real_cost:.2f})")
                success_count += 1
            else:
                failed_count += 1
                
        except Exception as e:
            logger.error(f"Error generating product: {e}")
            failed_count += 1
    
    # Log summary
    log_generation_summary(logger, 'PRODUCT', success_count, failed_count, batch_size)
    
    # Log current totals
    total_products = count_records('PRODUCT')
    logger.info(f"Total products in database: {total_products}")
    
    return success_count, failed_count

# ============================================
# SCRIPT EXECUTION
# ============================================

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("PRODUCT GENERATOR STARTED")
    logger.info(f"Timestamp: {datetime.now()}")
    logger.info("=" * 60)
    
    try:
        success, failed = generate_products()
        exit_code = 0 if failed == 0 else 1
        
    except Exception as e:
        logger.error(f"Fatal error in product generation: {e}")
        exit_code = 1
    
    logger.info("PRODUCT GENERATOR FINISHED")
    logger.info("=" * 60)
    
    exit(exit_code)