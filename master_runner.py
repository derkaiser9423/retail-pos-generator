#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 00:45:22 2024

@author: tin
"""

"""
Master Runner Script
Executes all data generation scripts in correct dependency order
Useful for initial population or bulk regeneration
"""

import subprocess
import sys
from datetime import datetime
from utils import setup_logger

# Setup logger
logger = setup_logger('MasterRunner')

# ============================================
# SCRIPT EXECUTION ORDER
# ============================================

SCRIPT_ORDER = [
    # Phase 1: Reference tables (no dependencies)
    ('01_generate_categories.py', 'Categories'),
    ('02_generate_suppliers.py', 'Suppliers'),
    ('03_generate_staff.py', 'Staff'),
    ('04_generate_machines.py', 'Machines'),
    ('05_generate_payment_methods.py', 'Payment Methods'),
    ('06_generate_transaction_types.py', 'Transaction Types'),
    
    # Phase 2: Dependent master tables
    ('07_generate_product_groups.py', 'Product Groups'),
    ('08_generate_products.py', 'Products'),
    
    # Phase 3: Transaction tables
    ('09_generate_transaction_headers.py', 'Transaction Headers'),
    ('10_generate_transaction_lines.py', 'Transaction Lines'),
]

# ============================================
# EXECUTION FUNCTIONS
# ============================================

def run_script(script_name, description):
    """
    Run a single generation script
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("=" * 60)
    logger.info(f"Running: {description} ({script_name})")
    logger.info("=" * 60)
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        # Log output
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                logger.info(f"  {line}")
        
        # Check for errors
        if result.returncode != 0:
            logger.error(f"Script failed with exit code {result.returncode}")
            if result.stderr:
                logger.error(f"Error output: {result.stderr}")
            return False
        
        logger.info(f"✓ {description} completed successfully")
        return True
        
    except subprocess.TimeoutExpired:
        logger.error(f"Script timed out after 5 minutes")
        return False
    except Exception as e:
        logger.error(f"Error running script: {e}")
        return False

def run_all_scripts():
    """
    Run all generation scripts in order
    
    Returns:
        dict: Summary of results
    """
    logger.info("=" * 60)
    logger.info("MASTER RUNNER STARTED")
    logger.info(f"Timestamp: {datetime.now()}")
    logger.info(f"Total scripts to run: {len(SCRIPT_ORDER)}")
    logger.info("=" * 60)
    
    results = {
        'total': len(SCRIPT_ORDER),
        'successful': 0,
        'failed': 0,
        'failed_scripts': []
    }
    
    for script_name, description in SCRIPT_ORDER:
        success = run_script(script_name, description)
        
        if success:
            results['successful'] += 1
        else:
            results['failed'] += 1
            results['failed_scripts'].append(description)
            
            # Ask if should continue after failure
            logger.warning(f"Script {description} failed. Continuing to next script...")
    
    return results

def print_summary(results):
    """Print execution summary"""
    logger.info("=" * 60)
    logger.info("MASTER RUNNER SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Total Scripts: {results['total']}")
    logger.info(f"Successful: {results['successful']}")
    logger.info(f"Failed: {results['failed']}")
    
    if results['failed'] > 0:
        logger.warning("Failed scripts:")
        for script in results['failed_scripts']:
            logger.warning(f"  - {script}")
    else:
        logger.info("✓ All scripts completed successfully!")
    
    logger.info("=" * 60)

# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    try:
        results = run_all_scripts()
        print_summary(results)
        
        # Exit with error code if any scripts failed
        exit_code = 0 if results['failed'] == 0 else 1
        
    except KeyboardInterrupt:
        logger.warning("Master runner interrupted by user")
        exit_code = 1
    except Exception as e:
        logger.error(f"Fatal error in master runner: {e}")
        exit_code = 1
    
    sys.exit(exit_code)