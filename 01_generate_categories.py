#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 00:35:31 2024

@author: tin
"""

"""
Generate CATEGORY records
Creates realistic category data for the retail POS system
"""

import random
from datetime import datetime
from config import (
    REAL_CATEGORIES, 
    BATCH_SIZES,
    PRODUCT_PREFIXES,
    PRODUCT_CATEGORIES_WORDS
)
from utils import (
    setup_logger,
    execute_query,
    record_exists,
    generate_unique_value,
    log_generation_summary,
    count_records
)

# Setup logger
logger = setup_logger('CategoryGenerator')

# ============================================
# CATEGORY GENERATION LOGIC
# ============================================

def generate_category_name():
    """Generate realistic category name"""
    
    # 70% chance: Use real category from data
    if random.random() < 0.7 and REAL_CATEGORIES:
        base_category = random.choice(REAL_CATEGORIES)
        
        # 80% chance: Return as-is, 20% chance: Add variation
        if random.random() < 0.8:
            return base_category
        else:
            # Add variation
            variations = [
                f"{base_category} & Accessories",
                f"{base_category} Care",
                f"General {base_category}",
                f"{base_category} Products",
                f"Specialty {base_category}"
            ]
            return random.choice(variations)
    
    # 30% chance: Generate completely new category
    prefix = random.choice(["", ""] + PRODUCT_PREFIXES[:10])  # Weighted to no prefix
    category_word = random.choice([
        "Health", "Wellness", "Beauty", "Personal Care",
        "Medical", "Nutrition", "Supplements", "Skincare",
        "Bodycare", "Healthcare", "Lifestyle", "Essentials"
    ])
    
    if prefix:
        return f"{prefix} {category_word}"
    return category_word

def generate_category_description(name):
    """Generate description for category"""
    templates = [
        f"Products related to {name.lower()}",
        f"Comprehensive range of {name.lower()} products",
        f"Quality {name.lower()} items for daily use",
        f"Professional {name.lower()} solutions",
        f"Essential {name.lower()} products",
        None  # 1 in 6 chance of no description
    ]
    return random.choice(templates)

def category_exists(name):
    """Check if category with name already exists"""
    return record_exists('CATEGORY', 'Category_Name', name)

def insert_category(name, description):
    """Insert category into database"""
    query = """
        INSERT INTO CATEGORY (Category_Name, Description)
        VALUES (?, ?)
    """
    try:
        category_id = execute_query(query, (name, description))
        return category_id
    except Exception as e:
        logger.error(f"Failed to insert category '{name}': {e}")
        return None

# ============================================
# MAIN GENERATION FUNCTION
# ============================================

def generate_categories(batch_size=None):
    """
    Generate batch of category records
    
    Args:
        batch_size: Number of categories to generate (default from config)
    
    Returns:
        tuple: (success_count, failed_count)
    """
    if batch_size is None:
        batch_size = BATCH_SIZES['CATEGORY']
    
    logger.info(f"Starting category generation - Batch size: {batch_size}")
    
    success_count = 0
    failed_count = 0
    
    for i in range(batch_size):
        try:
            # Generate unique category name
            category_name = generate_unique_value(
                generate_category_name,
                category_exists,
                max_retries=20
            )
            
            if category_name is None:
                logger.warning(f"Could not generate unique category name after max retries")
                failed_count += 1
                continue
            
            # Generate description
            description = generate_category_description(category_name)
            
            # Insert into database
            category_id = insert_category(category_name, description)
            
            if category_id:
                logger.info(f"✓ Created category #{category_id}: {category_name}")
                success_count += 1
            else:
                failed_count += 1
                
        except Exception as e:
            logger.error(f"Error generating category: {e}")
            failed_count += 1
    
    # Log summary
    log_generation_summary(logger, 'CATEGORY', success_count, failed_count, batch_size)
    
    # Log current totals
    total_categories = count_records('CATEGORY')
    logger.info(f"Total categories in database: {total_categories}")
    
    return success_count, failed_count

# ============================================
# SCRIPT EXECUTION
# ============================================

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("CATEGORY GENERATOR STARTED")
    logger.info(f"Timestamp: {datetime.now()}")
    logger.info("=" * 60)
    
    try:
        success, failed = generate_categories()
        exit_code = 0 if failed == 0 else 1
        
    except Exception as e:
        logger.error(f"Fatal error in category generation: {e}")
        exit_code = 1
    
    logger.info("CATEGORY GENERATOR FINISHED")
    logger.info("=" * 60)
    
    exit(exit_code)