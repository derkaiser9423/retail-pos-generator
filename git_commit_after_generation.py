#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 01:23:59 2024

@author: tin
"""

"""
Automatic Git Commit Script
Commits database changes and logs after each generation run
Creates clean, meaningful commit messages for GitHub history
"""

import subprocess
import os
from datetime import datetime
from utils import setup_logger, count_records

# Setup logger
logger = setup_logger('GitCommit')

# ============================================
# GIT OPERATIONS
# ============================================

def run_git_command(command):
    """Execute git command and return output"""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        logger.error(f"Git command failed: {e}")
        return False, "", str(e)

def is_git_repo():
    """Check if current directory is a git repository"""
    success, _, _ = run_git_command("git rev-parse --git-dir")
    return success

def has_changes():
    """Check if there are uncommitted changes"""
    success, output, _ = run_git_command("git status --porcelain")
    return success and len(output.strip()) > 0

def get_database_stats():
    """Get current database statistics"""
    tables = [
        'CATEGORY', 'SUPPLIER', 'STAFF', 'MACHINE', 
        'PAYMENT_METHOD', 'TRANSACTION_TYPE', 'PRODUCT_GROUP',
        'PRODUCT', 'TRANSACTION_HEADER', 'TRANSACTION_LINE'
    ]
    
    stats = {}
    for table in tables:
        try:
            count = count_records(table)
            stats[table] = count
        except:
            stats[table] = 0
    
    return stats

def create_commit_message(script_name=None):
    """Create meaningful commit message with database stats"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    stats = get_database_stats()
    
    # Calculate totals
    total_records = sum(stats.values())
    
    if script_name:
        title = f"🤖 Auto-generated data: {script_name}"
    else:
        title = f"🤖 Auto-generated data update"
    
    # Build commit message
    message = f"""{title}

Generated on: {timestamp}

📊 Database Statistics:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reference Tables:
  • Categories: {stats['CATEGORY']}
  • Suppliers: {stats['SUPPLIER']}
  • Staff: {stats['STAFF']}
  • Machines: {stats['MACHINE']}
  • Payment Methods: {stats['PAYMENT_METHOD']}
  • Transaction Types: {stats['TRANSACTION_TYPE']}

Product Data:
  • Product Groups: {stats['PRODUCT_GROUP']}
  • Products: {stats['PRODUCT']}

Transaction Data:
  • Transaction Headers: {stats['TRANSACTION_HEADER']}
  • Transaction Lines: {stats['TRANSACTION_LINE']}

Total Records: {total_records:,}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#automated #data-generation #retail-pos"""
    
    return message

def git_add_all():
    """Stage all changes"""
    logger.info("Staging changes...")
    success, output, error = run_git_command("git add .")
    
    if success:
        logger.info("✓ Changes staged successfully")
        return True
    else:
        logger.error(f"Failed to stage changes: {error}")
        return False

def git_commit(message):
    """Commit staged changes"""
    logger.info("Creating commit...")
    
    # Escape quotes in message
    message = message.replace('"', '\\"')
    
    success, output, error = run_git_command(f'git commit -m "{message}"')
    
    if success:
        logger.info("✓ Commit created successfully")
        return True
    else:
        logger.error(f"Failed to commit: {error}")
        return False

def git_push():
    """Push commits to remote"""
    logger.info("Pushing to GitHub...")
    success, output, error = run_git_command("git push origin main")
    
    if not success:
        # Try 'master' if 'main' fails
        logger.info("Trying 'master' branch...")
        success, output, error = run_git_command("git push origin master")
    
    if success:
        logger.info("✓ Pushed to GitHub successfully")
        return True
    else:
        logger.error(f"Failed to push: {error}")
        return False

# ============================================
# MAIN FUNCTION
# ============================================

def auto_commit_and_push(script_name=None, push_to_github=True):
    """
    Automatically commit and push changes after data generation
    
    Args:
        script_name: Name of the script that generated data
        push_to_github: Whether to push to GitHub (default: True)
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("=" * 60)
    logger.info("GIT AUTO-COMMIT STARTED")
    logger.info("=" * 60)
    
    # Check if git repo
    if not is_git_repo():
        logger.error("Not a git repository. Run 'git init' first.")
        return False
    
    # Check for changes
    if not has_changes():
        logger.info("No changes to commit")
        return True
    
    # Create commit message
    commit_msg = create_commit_message(script_name)
    
    # Stage changes
    if not git_add_all():
        return False
    
    # Commit
    if not git_commit(commit_msg):
        return False
    
    # Push to GitHub (optional)
    if push_to_github:
        if not git_push():
            logger.warning("Failed to push, but commit was created locally")
            return True  # Commit succeeded even if push failed
    
    logger.info("=" * 60)
    logger.info("✓ Git operations completed successfully")
    logger.info("=" * 60)
    
    return True

# ============================================
# SCRIPT EXECUTION
# ============================================

if __name__ == "__main__":
    import sys
    
    script_name = sys.argv[1] if len(sys.argv) > 1 else None
    push_enabled = sys.argv[2].lower() == 'true' if len(sys.argv) > 2 else True
    
    try:
        success = auto_commit_and_push(script_name, push_enabled)
        exit_code = 0 if success else 1
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        exit_code = 1
    
    exit(exit_code)