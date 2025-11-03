#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 00:32:34 2024

@author: tin
"""

"""
Configuration file for data generation scripts
Centralized settings for all generators
"""

import os
from datetime import datetime, timedelta

# ============================================
# DATABASE CONFIGURATION
# ============================================
DATABASE_PATH = "retail_pos.db"  # Path to your SQLite database

# ============================================
# LOGGING CONFIGURATION
# ============================================
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, f"data_generation_{datetime.now().strftime('%Y%m%d')}.log")

# Create log directory if it doesn't exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# ============================================
# GENERATION BATCH SIZES
# ============================================
# How many records to generate per run (for scheduler)
BATCH_SIZES = {
    'CATEGORY': 2,           # Generate 2 categories per run
    'SUPPLIER': 3,           # Generate 3 suppliers per run
    'STAFF': 2,              # Generate 2 staff per run
    'MACHINE': 1,            # Generate 1 machine per run
    'PAYMENT_METHOD': 1,     # Generate 1 payment method per run
    'TRANSACTION_TYPE': 1,   # Generate 1 transaction type per run
    'PRODUCT_GROUP': 3,      # Generate 3 product groups per run
    'PRODUCT': 10,           # Generate 10 products per run
    'TRANSACTION_HEADER': 20, # Generate 20 transactions per run
    'TRANSACTION_LINE': 50    # Generate 50 line items per run
}

# ============================================
# BUSINESS RULES & CONSTRAINTS
# ============================================

# Price ranges (based on real data analysis)
PRICE_RANGES = {
    'min': 0.10,
    'max': 100.00,
    'common_low': 2.00,
    'common_high': 50.00
}

# Cost margins (Avg_Real_Cost as percentage of sale price)
COST_MARGIN_RANGE = (0.30, 0.85)  # 30% to 85% of sale price

# Stock levels
STOCK_RANGE = {
    'min': 0,
    'max': 100,
    'typical_low': 5,
    'typical_high': 50
}

# Discount settings
DISCOUNT_PROBABILITY = 0.05  # 5% chance of discount
DISCOUNT_PERCENTAGES = [5.0, 10.0, 15.0, 20.0]  # Possible discount %

# Transaction timing
BUSINESS_HOURS = {
    'open': 8,   # 8 AM
    'close': 22  # 10 PM
}

# Date range for historical data generation
DATE_RANGE = {
    'start_date': datetime.now() - timedelta(days=90),  # 90 days ago
    'end_date': datetime.now()
}

# ============================================
# REAL DATA PATTERNS (from your files)
# ============================================

# Categories from your transaction data
REAL_CATEGORIES = [
    "Dental", "Vitamins", "Cold & Flu", "Analgesics", 
    "Therapeutic Skin Care", "Body Care", "Baby & Children",
    "Suncare", "First Aid", "Personal Hygiene", "SkinCare",
    "Hair Care", "Beauty Ancillaries", "Phmcist Only",
    "Personal Care", "Digestive Health", "Ethicals",
    "Cosmetics", "Ear & Eye Care", "Vitamins Slimming",
    "Stationary"
]

# Product Groups from your data (partial list for variety)
REAL_PRODUCT_GROUPS = [
    "Toothpaste & Lotions", "Swisse", "General Vitamins", "Goat",
    "Hand & Nail", "Nature's Way", "Sunscreen", "Lifespace",
    "Topical First Aid", "Bandages & Dressings", "Tapes/Strapping",
    "Pads & Liners", "Baby Skincare", "Baby Wipes", "Baby Accessories",
    "Vaporisers & Oils", "Electric Toothbrushes", "Mouth Washes",
    "Blackmores", "Eaoron", "Sore Throat", "Nasal Preparation",
    "Lip Care", "Healthy Care", "Manuka Honey", "Hair Styling",
    "Shampoos & Conditioners", "Hair Treatment", "Rehydration",
    "General Cold & Flu", "Anti-Itch", "Analgesics", "Acne Treatment",
    "Fungal/Warts", "Deodorants Mens", "Deodorants Womens",
    "Contraception", "Eye Drops & Lotions", "My Beauty Tools",
    "Revlon", "MCo Beauty", "L'Oreal Cosmetics", "La Roche-Posay"
]

# Supplier codes from your product data
REAL_SUPPLIERS = [
    "glo.", "bn..", "jj..", "wqld", "hnz.", "wh..", "kc..",
    "mce.", "PSAP", "be..", "si..", "np..", "etb.", "SWC",
    "bau.", "vinz", "cfc.", "lev.", "pf..", "men.", "sup.",
    "SCK.", "perr", "sanv", "rc..", "col.", "HOM", "mart",
    "blac", "apc.", "amn.", "VE", "arro", "by..", "not.",
    "pheb", "lore", "totn", "eo..", "sn..", "mm..", "iva.",
    "cc..", "seme", "EPCA", "af..", "jc..", "ave.", "coty",
    "rvl.", "apa.", "ky..", "medd", "medt", "clli", "pcl.",
    "llux", "WCB", "fep.", "upi.", "nst.", "fel.", "mg..",
    "pfet", "upj", "cw..", "ans.", "cpa.", "sca.", "PFD",
    "adno", "neve", "srfb", "heri", "halh", "abe.", "ga..",
    "bk..", "cae.", "genh", "hero", "nft.", "bia.", "BIA"
]

# Staff name patterns (FirstName LastInitial ID)
FIRST_NAMES = [
    "Andy", "Tiet", "Huijun", "Joshua", "Yuqing", "Trong Tin",
    "Ngoc Bao Han", "Sarah", "Michael", "Emma", "James", "Olivia",
    "William", "Sophia", "David", "Isabella", "Daniel", "Mia",
    "Matthew", "Charlotte", "Emily", "Benjamin", "Ava", "Lucas",
    "Amelia", "Alexander", "Harper", "Ethan", "Evelyn", "Jackson"
]

LAST_INITIALS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Machine names
REAL_MACHINES = ["TILL01", "TILL02", "TILL03", "TILL04", "TILL05", "TILL06"]

# Payment methods
REAL_PAYMENT_METHODS = ["EFTPOS", "CASH", "CREDIT CARD", "DEBIT CARD", "CONTACTLESS"]

# Transaction types
REAL_TRANSACTION_TYPES = [
    "Normal Item Sale",
    "Return Item",
    "Scriptlink Item",
    "Staff Purchase",
    "Void Item",
    "Exchange"
]

# ============================================
# PRODUCT NAME PATTERNS
# ============================================
PRODUCT_PREFIXES = [
    "Super", "Ultra", "Extra", "Advanced", "Professional", "Premium",
    "Natural", "Organic", "Clinical", "Dermatological", "Therapeutic",
    "Sensitive", "Gentle", "Active", "Daily", "Instant", "Quick",
    "Fast", "Complete", "Total", "Maximum", "Intensive"
]

PRODUCT_CATEGORIES_WORDS = [
    "Cream", "Lotion", "Serum", "Gel", "Oil", "Balm", "Spray",
    "Tablets", "Capsules", "Powder", "Liquid", "Drops", "Wash",
    "Shampoo", "Conditioner", "Moisturizer", "Cleanser", "Treatment",
    "Relief", "Care", "Formula", "Complex", "Support", "Protection"
]

PRODUCT_SIZES = [
    "15g", "25g", "50g", "75g", "100g", "125g", "150g", "200g", "250g",
    "15ml", "25ml", "50ml", "75ml", "100ml", "125ml", "150ml", "200ml",
    "10 Pack", "20 Pack", "30 Pack", "50 Pack", "100 Pack",
    "24 Tablets", "30 Tablets", "60 Tablets", "90 Tablets", "120 Tablets"
]

# ============================================
# VALIDATION SETTINGS
# ============================================
MAX_RETRIES = 10  # Maximum attempts to generate unique values
ENABLE_DUPLICATE_CHECK = True  # Check for duplicates before insert

# ============================================
# SCHEDULER SETTINGS
# ============================================
# For Windows Task Scheduler or cron
RUN_MODE = 'scheduled'  # 'scheduled' or 'manual'
QUIET_MODE = False  # Set True to suppress console output in scheduled mode

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_batch_size(table_name):
    """Get batch size for a specific table"""
    return BATCH_SIZES.get(table_name.upper(), 10)

def get_date_range():
    """Get the configured date range"""
    return DATE_RANGE['start_date'], DATE_RANGE['end_date']

def is_business_hours(hour):
    """Check if given hour is within business hours"""
    return BUSINESS_HOURS['open'] <= hour <= BUSINESS_HOURS['close']

# ============================================
# GIT/GITHUB CONFIGURATION
# ============================================

# Auto-commit settings
AUTO_COMMIT_ENABLED = True  # Set False to disable auto-commits
AUTO_PUSH_ENABLED = True    # Set False to commit locally only

# Commit frequency
# 'always' - commit after every generation
# 'hourly' - commit once per hour (batches multiple runs)
# 'daily' - commit once per day
COMMIT_FREQUENCY = 'always'

# Files to include in commits
GIT_TRACKED_FILES = [
    'retail_pos.db',           # Database file
    'logs/*.log',              # Log files
    'config.py',               # Configuration (if you modify it)
]

# Files to ignore (add to .gitignore)
GIT_IGNORED_FILES = [
    '__pycache__/',
    '*.pyc',
    '.env',
    'venv/',
    '.vscode/',
    '.idea/',
]

# Control auto-commit behavior
AUTO_COMMIT_ENABLED = True     # Enable/disable auto-commits
AUTO_PUSH_ENABLED = True       # Enable/disable auto-push to GitHub

# Commit frequency
COMMIT_FREQUENCY = 'always'  # 'always', 'hourly', or 'daily'
