#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 01:24:44 2024

@author: tin
"""

"""
Wrapper Script - Run Generator + Auto Commit
Wraps any generator script to automatically commit after execution
"""

import sys
import subprocess
from datetime import datetime
from config import AUTO_COMMIT_ENABLED, AUTO_PUSH_ENABLED
from git_commit_after_generation import auto_commit_and_push
from utils import setup_logger

logger = setup_logger('GeneratorWrapper')

def run_generator_with_git(script_path):
    """
    Run a generator script and auto-commit results
    
    Args:
        script_path: Path to the generator script
    
    Returns:
        int: Exit code
    """
    logger.info(f"Running generator: {script_path}")
    
    # Extract script name
    script_name = script_path.split('/')[-1].replace('.py', '')
    
    # Run the generator script
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # Log output
        if result.stdout:
            print(result.stdout)
        
        if result.returncode != 0:
            logger.error(f"Generator failed with exit code {result.returncode}")
            if result.stderr:
                logger.error(result.stderr)
            return result.returncode
        
        logger.info(f"✓ Generator completed successfully")
        
    except Exception as e:
        logger.error(f"Error running generator: {e}")
        return 1
    
    # Auto-commit if enabled
    if AUTO_COMMIT_ENABLED:
        logger.info("Auto-commit enabled, committing changes...")
        success = auto_commit_and_push(script_name, AUTO_PUSH_ENABLED)
        
        if not success:
            logger.warning("Auto-commit failed, but data was generated")
            return 0  # Don't fail the job if commit fails
    
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python wrapper_with_git.py <generator_script.py>")
        print("Example: python wrapper_with_git.py 01_generate_categories.py")
        sys.exit(1)
    
    script_path = sys.argv[1]
    exit_code = run_generator_with_git(script_path)
    sys.exit(exit_code)


