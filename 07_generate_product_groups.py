#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 00:41:05 2024

@author: tin
"""

"""
Generate PRODUCT_GROUP records
Creates realistic product groups linked to categories
"""

import random
from datetime import datetime
from config import REAL_PRODUCT_GROUPS, BATCH_SIZES
from utils import (
    setup_logger,
    execute_query,
    record_exists,
    generate_unique_value,
    log_generation_summary,
    count_records,
    get_random_record,
    get_all_records
)

# Setup logger
logger = setup_logger('ProductGroupGenerator')

# ============================================
# PRODUCT GROUP GENERATION LOGIC
# ============================================

# Additional product group variations
PRODUCT_GROUP_MODIFIERS = [
    "Premium", "Standard", "Budget", "Professional", "Clinical",
    "Natural", "Organic", "Advanced", "Essential", "Specialty",
    "Import", "Local", "Generic", "Brand", "Private Label"
]

def generate_product_group_name():
    """Generate realistic product group name"""
    
    # 60% chance: Use real product group from data
    if random.random() < 0.6 and REAL_PRODUCT_GROUPS:
        base_group = random.choice(REAL_PRODUCT_GROUPS)
        
        # 70% chance: Return as-is, 30% chance: Add modifier
        if random.random() < 0.7:
            return base_group
        else:
            modifier = random.choice(PRODUCT_GROUP_MODIFIERS)
            # Remove number suffix if exists
            base_clean = ''.join([c for c in base_group if not c.isdigit()]).strip()
            return f"{modifier} {base_clean}"
    
    # 40% chance: Generate new product group
    categories = [
        "Supplements", "Vitamins", "Skincare", "Haircare", "Dental",
        "Baby Products", "First Aid", "Personal Care", "Beauty",
        "Healthcare", "Nutrition", "Wellness", "Cosmetics"
    ]
    
    subcategories = [
        "Products", "Range", "Solutions", "Essentials", "Collection",
        "Series", "Line", "Items", "Supplies"
    ]
    
    category = random.choice(categories)
    
    # 50% chance: Add subcategory
    if random.random() < 0.5:
        sub = random.choice(subcategories)
        return f"{category} {sub}"
    
    return category

def generate_product_group_description(name):
    """Generate description for product group"""
    templates = [
        f"Complete range of {name.lower()}",
        f"Quality {name.lower()} for everyday needs",
        f"Professional {name.lower()} selection",
        f"Comprehensive {name.lower()} collection",
        f"{name} for all requirements",
        None  # 1 in 6 chance of no description
    ]
    return random.choice(templates)

def get_random_category_id():
    """Get random category ID from database"""
    result = get_random_record('CATEGORY', 'Category_ID')
    if result:
        return result[0]
    
    # If no categories exist, log error
    logger.error("No categories found in database. Run category generator first.")
    return None

def product_group_exists(name):
    """Check if product group with name already exists"""
    return record_exists('PRODUCT_GROUP', 'Product_Group_Name', name)

def insert_product_group(name, description, category_id):
    """Insert product group into database"""
    query = """
        INSERT INTO PRODUCT_GROUP (Product_Group_Name, Description, Category_ID)
        VALUES (?, ?, ?)
    """
    try:
        group_id = execute_query(query, (name, description, category_id))
        return group_id
    except Exception as e:
        logger.error(f"Failed to insert product group '{name}': {e}")
        return None

# ============================================
# MAIN GENERATION FUNCTION
# ============================================

def generate_product_groups(batch_size=None):
    """Generate batch of product group records"""
    if batch_size is None:
        batch_size = BATCH_SIZES['PRODUCT_GROUP']
    
    logger.info(f"Starting product group generation - Batch size: {batch_size}")
    
    # Check if categories exist
    category_count = count_records('CATEGORY')
    if category_count == 0:
        logger.error("No categories found. Please run category generator first.")
        return 0, batch_size
    
    success_count = 0
    failed_count = 0
    
    for i in range(batch_size):
        try:
            # Generate unique product group name
            group_name = generate_unique_value(
                generate_product_group_name,
                product_group_exists,
                max_retries=30
            )
            
            if group_name is None:
                logger.warning(f"Could not generate unique product group name after max retries")
                failed_count += 1
                continue
            
            # Get random category
            category_id = get_random_category_id()
            if category_id is None:
                logger.error("Failed to get category ID")
                failed_count += 1
                continue
            
            # Generate description
            description = generate_product_group_description(group_name)
            
            # Insert into database
            group_id = insert_product_group(group_name, description, category_id)
            
            if group_id:
                logger.info(f"✓ Created product group #{group_id}: {group_name} (Category: {category_id})")
                success_count += 1
            else:
                failed_count += 1
                
        except Exception as e:
            logger.error(f"Error generating product group: {e}")
            failed_count += 1
    
    # Log summary
    log_generation_summary(logger, 'PRODUCT_GROUP', success_count, failed_count, batch_size)
    
    # Log current totals
    total_groups = count_records('PRODUCT_GROUP')
    logger.info(f"Total product groups in database: {total_groups}")
    
    return success_count, failed_count

# ============================================
# SCRIPT EXECUTION
# ============================================

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("PRODUCT GROUP GENERATOR STARTED")
    logger.info(f"Timestamp: {datetime.now()}")
    logger.info("=" * 60)
    
    try:
        success, failed = generate_product_groups()
        exit_code = 0 if failed == 0 else 1
        
    except Exception as e:
        logger.error(f"Fatal error in product group generation: {e}")
        exit_code = 1
    
    logger.info("PRODUCT GROUP GENERATOR FINISHED")
    logger.info("=" * 60)
    
    exit(exit_code)