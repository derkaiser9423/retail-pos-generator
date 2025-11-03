{\rtf1\ansi\ansicpg1252\cocoartf2865
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 @echo off\
echo ========================================\
echo GitHub Repository Setup\
echo ========================================\
echo.\
\
REM Check if git is installed\
git --version >nul 2>&1\
if errorlevel 1 (\
    echo ERROR: Git is not installed or not in PATH\
    echo Please install Git from https://git-scm.com/\
    pause\
    exit /b 1\
)\
\
echo Step 1: Initializing Git repository...\
git init\
\
echo.\
echo Step 2: Adding files...\
git add .\
\
echo.\
echo Step 3: Creating initial commit...\
git commit -m "Initial commit: Retail POS Data Generation System\
\
- 10 data generator scripts\
- Automated scheduling support\
- Git integration for clean commit history\
- Comprehensive logging system\
- 3NF normalized database schema"\
\
echo.\
echo Step 4: Setting up remote repository...\
echo.\
echo Please enter your GitHub repository URL:\
echo Example: https://github.com/yourusername/retail-pos-generator.git\
set /p REPO_URL="Repository URL: "\
\
if "%REPO_URL%"=="" (\
    echo ERROR: Repository URL is required\
    pause\
    exit /b 1\
)\
\
git remote add origin %REPO_URL%\
\
echo.\
echo Step 5: Pushing to GitHub...\
git branch -M main\
git push -u origin main\
\
echo.\
echo ========================================\
echo \uc0\u10003  GitHub setup complete!\
echo ========================================\
echo.\
echo Your repository is now set up and ready.\
echo.\
echo Next steps:\
echo 1. Set up Windows Task Scheduler (see scheduler_setup.md)\
echo 2. Enable auto-commit in config.py (already enabled by default)\
echo 3. Watch your GitHub activity graph grow!\
echo.\
pause}