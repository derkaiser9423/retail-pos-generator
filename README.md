# 🏪 Retail POS Database - Automated Data Generation

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![SQLite](https://img.shields.io/badge/sqlite-3-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

![Data Generation](https://github.com/derkaiser9423/retail-pos-generator/actions/workflows/data-generation.yml/badge.svg)
![Tests](https://github.com/derkaiser9423/retail-pos-generator/actions/workflows/test-generators.yml/badge.svg)
![Database Backup](https://github.com/derkaiser9423/retail-pos-generator/actions/workflows/database-backup.yml/badge.svg)

Automated data generation system for a retail pharmacy POS database. Generates realistic transaction data, products, staff, and more using scheduled Python scripts with **GitHub Actions automation**.

## 📊 Live Database Statistics

*Statistics are generated automatically by GitHub Actions every 2 hours*

### Current Status

| Component | Status |
|-----------|--------|
| 🤖 GitHub Actions | ![Active](https://img.shields.io/badge/status-active-brightgreen) |
| 💾 Database | ![Automated](https://img.shields.io/badge/generation-automated-blue) |
| 📈 Data Growth | ![Continuous](https://img.shields.io/badge/growth-continuous-success) |
| ⚡ Last Run | Check Actions tab for latest |

### Database Tables

| Table | Description | Status |
|-------|-------------|--------|
| 📊 Categories | Product categories | ✅ Active |
| 🏢 Suppliers | Supplier information | ✅ Active |
| 👥 Staff | Employee records | ✅ Active |
| 🖥️ Machines | POS terminals | ✅ Active |
| 💳 Payment Methods | Payment types | ✅ Active |
| 📋 Transaction Types | Transaction categories | ✅ Active |
| 🏷️ Product Groups | Product groupings | ✅ Active |
| 📦 Products | Product catalog | ✅ Active |
| 🧾 Transaction Headers | Transaction metadata | ✅ Active |
| 📝 Transaction Lines | Line item details | ✅ Active |

> 💡 **View live statistics:** Check the [Actions tab](https://github.com/derkaiser9423/retail-pos-generator/actions) and look at the latest workflow run logs for current record counts.

## 🤖 Automation Status

### GitHub Actions Workflows

#### 🔄 Automated Data Generation
- **Frequency:** Every 2 hours
- **Status:** ![Data Generation](https://github.com/derkaiser9423/retail-pos-generator/actions/workflows/data-generation.yml/badge.svg)
- **What it does:**
  - Runs all 10 generator scripts
  - Creates new records across all tables
  - Uploads database and logs as artifacts

#### 🧪 Testing
- **Trigger:** On every push
- **Status:** ![Tests](https://github.com/derkaiser9423/retail-pos-generator/actions/workflows/test-generators.yml/badge.svg)
- **What it does:**
  - Validates database schema
  - Tests all generators
  - Reports record counts

#### 💾 Database Backup
- **Frequency:** Daily at midnight UTC
- **Status:** ![Backup](https://github.com/derkaiser9423/retail-pos-generator/actions/workflows/database-backup.yml/badge.svg)
- **What it does:**
  - Creates compressed database backup
  - Retains backups for 90 days
  - Available as downloadable artifacts

### Local Automation (Optional)

You can also run generators on your PC using:
- **Windows Task Scheduler** - Schedule scripts at custom intervals
- **GitHub Desktop** - Commit changes manually with visual interface

## 🚀 Quick Start

### Option 1: Let GitHub Actions Handle Everything (Easiest!)

1. ✅ Repository is already set up
2. ✅ GitHub Actions runs automatically every 2 hours
3. ✅ Data is generated in the cloud
4. ✅ Just watch your database grow!

**To download the latest database:**
1. Go to [Actions tab](https://github.com/derkaiser9423/retail-pos-generator/actions)
2. Click latest "Automated Data Generation" run
3. Scroll to "Artifacts" section
4. Download `retail-pos-database-run-XXX`

### Option 2: Run Locally on Your PC
```bash
# Clone repository
git clone https://github.com/derkaiser9423/retail-pos-generator.git
cd retail-pos-generator

# Initial database population
python master_runner.py

# Run individual generator
python 01_generate_categories.py
```

## 📅 Generation Schedule

### Cloud (GitHub Actions)
- **Every 2 hours:** Full generation cycle (all 10 scripts)
- **Daily:** Automated database backup
- **On push:** Automated testing

### Recommended Local Schedule (Task Scheduler)
- **Every 15 minutes:** Transaction Lines (high volume)
- **Every 30 minutes:** Transaction Headers
- **Every 2 hours:** Products
- **Every 4 hours:** Product Groups
- **Daily:** Reference data (Categories, Suppliers, Staff, etc.)

## 🗄️ Database Schema

Normalized to **3NF** (Third Normal Form):
```
CATEGORY (1:M) ──→ PRODUCT_GROUP (1:M) ──→ PRODUCT
                                               ↓ (M:1)
SUPPLIER (1:M) ────────────────────────────────┘

STAFF (1:M) ──→ TRANSACTION_HEADER (1:M) ──→ TRANSACTION_LINE
                        ↑
MACHINE (1:M) ──────────┤
PAYMENT_METHOD (1:M) ───┤
TRANSACTION_TYPE (1:M) ─┘
```

**Total Tables:** 10  
**Total Relationships:** 10 foreign key constraints  
**Normalization Level:** 3NF (Third Normal Form)

## 📁 Project Structure
```
retail-pos-generator/
├── .github/
│   └── workflows/              # GitHub Actions automation
│       ├── data-generation.yml
│       ├── test-generators.yml
│       └── database-backup.yml
├── logs/                       # Generation logs (auto-created)
├── config.py                   # Configuration settings
├── utils.py                    # Helper functions
├── validate_database.py        # Schema validator
├── master_runner.py            # Run all generators
├── 01_generate_categories.py
├── 02_generate_suppliers.py
├── 03_generate_staff.py
├── 04_generate_machines.py
├── 05_generate_payment_methods.py
├── 06_generate_transaction_types.py
├── 07_generate_product_groups.py
├── 08_generate_products.py
├── 09_generate_transaction_headers.py
├── 10_generate_transaction_lines.py
├── retail_pos.db              # SQLite database
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## 🔧 Configuration

Edit `config.py` to customize generation:
```python
# Batch sizes (records generated per run)
BATCH_SIZES = {
    'CATEGORY': 2,              # 2 categories per run
    'PRODUCT': 10,              # 10 products per run
    'TRANSACTION_LINE': 50,     # 50 line items per run
    # ...
}

# Price ranges
PRICE_RANGES = {
    'min': 0.10,
    'max': 100.00,
    'common_low': 2.00,
    'common_high': 50.00
}

# Discount settings
DISCOUNT_PROBABILITY = 0.05     # 5% chance of discount
DISCOUNT_PERCENTAGES = [5.0, 10.0, 15.0, 20.0]

# Business hours (for transaction timestamps)
BUSINESS_HOURS = {
    'open': 8,   # 8 AM
    'close': 22  # 10 PM
}
```

## 📈 Monitoring

### View Generation Logs

**GitHub Actions:**
1. Go to [Actions tab](https://github.com/derkaiser9423/retail-pos-generator/actions)
2. Click any workflow run
3. Click on job steps to see detailed logs
4. Look for record counts in "Show generation summary"

**Local:**
```bash
# View today's log
notepad logs\data_generation_20241103.log

# Or use PowerShell to view last 50 lines
Get-Content logs\data_generation_20241103.log -Tail 50
```

### Check Database Size
```bash
# Windows
dir retail_pos.db

# Shows file size (e.g., 2.5 MB)
```

### Query Database
```sql
-- Get total records across all tables
SELECT 
    'CATEGORY' as Table_Name, COUNT(*) as Records FROM CATEGORY
UNION ALL
SELECT 'SUPPLIER', COUNT(*) FROM SUPPLIER
UNION ALL
SELECT 'STAFF', COUNT(*) FROM STAFF
UNION ALL
SELECT 'MACHINE', COUNT(*) FROM MACHINE
UNION ALL
SELECT 'PAYMENT_METHOD', COUNT(*) FROM PAYMENT_METHOD
UNION ALL
SELECT 'TRANSACTION_TYPE', COUNT(*) FROM TRANSACTION_TYPE
UNION ALL
SELECT 'PRODUCT_GROUP', COUNT(*) FROM PRODUCT_GROUP
UNION ALL
SELECT 'PRODUCT', COUNT(*) FROM PRODUCT
UNION ALL
SELECT 'TRANSACTION_HEADER', COUNT(*) FROM TRANSACTION_HEADER
UNION ALL
SELECT 'TRANSACTION_LINE', COUNT(*) FROM TRANSACTION_LINE;
```

## 🧪 Testing

### Run Tests via GitHub Actions
- Automatic on every push
- Manual: Go to Actions → Test Data Generators → Run workflow

### Run Tests Locally
```bash
# Run all generators
python master_runner.py

# Validate database schema
python validate_database.py
```

## 📥 Download Database Artifacts

1. Go to [Actions tab](https://github.com/derkaiser9423/retail-pos-generator/actions)
2. Click any completed workflow run
3. Scroll to **Artifacts** section at the bottom
4. Download available artifacts:
   - `retail-pos-database-run-XXX` - Latest generated database
   - `generation-logs-run-XXX` - Execution logs
   - `database-backup-YYYY-MM-DD` - Daily backup (compressed)

## 🎯 Script Execution Order

All scripts must run in this order due to foreign key dependencies:

### Phase 1: Foundation (No Dependencies)
```
1. 01_generate_categories.py
2. 02_generate_suppliers.py
3. 03_generate_staff.py
4. 04_generate_machines.py
5. 05_generate_payment_methods.py
6. 06_generate_transaction_types.py
```
*Can run in any order or simultaneously*

### Phase 2: Product Hierarchy
```
7. 07_generate_product_groups.py    (Needs: Categories)
8. 08_generate_products.py           (Needs: Product Groups + Suppliers)
```

### Phase 3: Transactions
```
9. 09_generate_transaction_headers.py (Needs: Staff + Machines + Payment Methods + Transaction Types)
10. 10_generate_transaction_lines.py  (Needs: Transaction Headers + Products)
```

**💡 Tip:** Use `master_runner.py` to run all scripts in the correct order automatically!

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Roadmap

- [x] Core data generators (10 tables)
- [x] GitHub Actions automation
- [x] Automated testing workflow
- [x] Daily database backups
- [x] Artifact downloads
- [ ] Real-time statistics dashboard
- [ ] REST API for data access
- [ ] Docker containerization
- [ ] Multi-database support (PostgreSQL, MySQL)
- [ ] Data visualization charts

## 📞 Support

- 🐛 **Issues:** [GitHub Issues](https://github.com/derkaiser9423/retail-pos-generator/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/derkaiser9423/retail-pos-generator/discussions)
- 📧 **Email:** Create an issue for support

## 📊 Repository Stats

![GitHub repo size](https://img.shields.io/github/repo-size/derkaiser9423/retail-pos-generator)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/derkaiser9423/retail-pos-generator)
![GitHub last commit](https://img.shields.io/github/last-commit/derkaiser9423/retail-pos-generator)
![GitHub Workflow Status](https://github.com/derkaiser9423/retail-pos-generator/actions/workflows/data-generation.yml/badge.svg)

---

**⚡ Powered by Python + SQLite + GitHub Actions**

*Automated retail POS data generation - running 24/7 in the cloud!*
