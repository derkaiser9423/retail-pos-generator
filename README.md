# 🏪 Retail POS Database - Automated Data Generation

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![SQLite](https://img.shields.io/badge/sqlite-3-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Total Records](https://img.shields.io/badge/records-194,633-brightgreen)
![Database Size](https://img.shields.io/badge/size-19.87MB-blue)

![Data Generation](https://github.com/derkaiser9423/retail-pos-generator/actions/workflows/data-generation.yml/badge.svg)
![Tests](https://github.com/derkaiser9423/retail-pos-generator/actions/workflows/test-generators.yml/badge.svg)
![Database Backup](https://github.com/derkaiser9423/retail-pos-generator/actions/workflows/database-backup.yml/badge.svg)

> **Last Updated:** 2025-12-02 20:16:03 UTC  
> **24h Growth:** +726 records

Automated data generation system for a retail pharmacy POS database. Generates realistic transaction data, products, staff, and more using scheduled Python scripts with **GitHub Actions automation**.

---

## 📊 Live Database Statistics

### Overview

| Metric | Value |
|--------|-------|
| 📦 **Total Records** | **194,633** |
| 💾 **Database Size** | **19.87 MB** |
| 📅 **Last Updated** | December 02, 2025 at 20:16 UTC |
| 📈 **24h Growth** | +726 records |
| 🤖 **Status** | ![Active](https://img.shields.io/badge/status-generating-success) |

### Record Counts by Table
```
┌─────────────────────────┬──────────────────────────────┐
│ Table                   │ Records                      │
├─────────────────────────┼──────────────────────────────┤
│ 📊 Categories           │  257                           │
│ 🏢 Suppliers            │  891                           │
│ 👥 Staff                │  594                           │
│ 🖥️ Machines             │  15                            │
│ 💳 Payment Methods      │  18                            │
│ 📋 Transaction Types    │  12                            │
│ 🏷️ Product Groups       │  766                           │
│ 📦 Products             │  5,600                         │
│ 🧾 Transaction Headers  │ ████████ 53,280                │
│ 📝 Transaction Lines    │ ████████████████████ 133,200   │
└─────────────────────────┴──────────────────────────────┘
```

### Data Growth Visualization
```
📈 Growth Trend (Last 20 data points)

  194633 |                   █
  193253 |                  ██
  191874 |                ████
  190494 |              ██████
  189115 |            ████████
  187735 |          ██████████
  186355 |        ████████████
  184976 |      ██████████████
  183596 |    ████████████████
  182217 |  ██████████████████
  180837 |████████████████████
         +────────────────────
```

**Legend:** Each point represents a data collection snapshot. Chart shows total record growth over time.

---

## 🤖 Automation Status

### GitHub Actions Workflows

| Workflow | Status | Frequency | Description |
|----------|--------|-----------|-------------|
| 🔄 **Data Generation** | ![Status](https://github.com/derkaiser9423/retail-pos-generator/actions/workflows/data-generation.yml/badge.svg) | Every 2 hours | Generates new data across all tables |
| 🧪 **Testing** | ![Status](https://github.com/derkaiser9423/retail-pos-generator/actions/workflows/test-generators.yml/badge.svg) | On push | Validates schema and tests generators |
| 💾 **Backup** | ![Status](https://github.com/derkaiser9423/retail-pos-generator/actions/workflows/database-backup.yml/badge.svg) | Daily | Creates compressed database backup |

### What Gets Generated Every 2 Hours:

- ✅ 257 Categories (+ 2 per run)
- ✅ 891 Suppliers (+ 3 per run)
- ✅ 594 Staff members (+ 2 per run)
- ✅ 5,600 Products (+ 10 per run)
- ✅ 53,280 Transactions (+ 20 per run)
- ✅ 133,200 Transaction lines (+ 50 per run)

---

## 🚀 Quick Start

### Option 1: Fully Automated (Recommended)

GitHub Actions handles everything automatically:

1. ✅ **Automatic generation** every 2 hours
2. ✅ **This README updates** with real statistics
3. ✅ **Database grows** continuously
4. ✅ **Nothing to do** - just watch it grow!

📥 **Download latest database:**
- Go to [Actions](https://github.com/derkaiser9423/retail-pos-generator/actions) → Latest run → Artifacts

### Option 2: Run Locally
```bash
# Clone repository
git clone https://github.com/derkaiser9423/retail-pos-generator.git
cd retail-pos-generator

# Generate initial data
python master_runner.py

# Update README with current stats
python generate_readme_stats.py
```

---

## 🗄️ Database Schema (3NF Normalized)
```
┌─────────────┐     ┌──────────────┐     ┌─────────┐
│  CATEGORY   │────▶│PRODUCT_GROUP │────▶│ PRODUCT │
└─────────────┘     └──────────────┘     └─────────┘
                                              ▲
┌─────────────┐                               │
│  SUPPLIER   │───────────────────────────────┘
└─────────────┘

┌─────────────┐     ┌──────────────────┐     ┌──────────────────┐
│    STAFF    │────▶│TRANSACTION_HEADER│────▶│TRANSACTION_LINE  │
└─────────────┘     └──────────────────┘     └──────────────────┘
                              ▲
┌─────────────┐               │
│   MACHINE   │───────────────┤
└─────────────┘               │
┌─────────────┐               │
│   PAYMENT   │───────────────┤
│   METHOD    │               │
└─────────────┘               │
┌─────────────┐               │
│TRANSACTION  │───────────────┘
│    TYPE     │
└─────────────┘
```

**Database Features:**
- ✅ 10 tables with proper foreign key relationships
- ✅ 3NF normalized (no data redundancy)
- ✅ Referential integrity enforced
- ✅ Indexed for query performance
- ✅ Check constraints for data validation

---

## 📅 Generation Schedule

### Automated (GitHub Actions)
```
Every 2 hours:
  ├─ Generate reference data (categories, suppliers, etc.)
  ├─ Generate products
  ├─ Generate transactions
  ├─ Update README statistics
  └─ Upload database artifact

Daily at midnight:
  └─ Create compressed backup (90-day retention)
```

### Local (Optional - Windows Task Scheduler)
```
High Frequency (15 min):  Transaction Lines
Medium Frequency (2 hrs): Products, Transactions
Low Frequency (Daily):    Reference data
```

---

## 📁 Project Structure
```
retail-pos-generator/
├── .github/workflows/           # GitHub Actions (automated)
│   ├── data-generation.yml
│   ├── test-generators.yml
│   └── database-backup.yml
├── 01-10_generate_*.py          # Data generators (10 scripts)
├── master_runner.py             # Run all generators
├── generate_readme_stats.py     # Update this README
├── validate_database.py         # Schema validator
├── config.py                    # Configuration
├── utils.py                     # Helper functions
├── retail_pos.db                # SQLite database (19.87 MB)
├── stats_history.json           # Statistics history
├── requirements.txt             # Dependencies
└── README.md                    # This file (auto-updated!)
```

---

## 🔧 Configuration

Edit `config.py` to customize:
```python
BATCH_SIZES = {
    'CATEGORY': 2,              # Records per run
    'PRODUCT': 10,
    'TRANSACTION_LINE': 50,
}

PRICE_RANGES = {
    'min': 0.10,
    'max': 100.00,
}

DISCOUNT_PROBABILITY = 0.05     # 5% of transactions
```

---

## 📈 Monitoring & Logs

### View Live Statistics
- **This README** - Auto-updated every 2 hours with real data
- **Actions Tab** - Detailed logs of each generation run
- **Artifacts** - Download database and logs

### Query Database Directly
```sql
-- Get all record counts
SELECT 
    'CATEGORY' as Table_Name, 
    COUNT(*) as Records 
FROM CATEGORY
UNION ALL
SELECT 'PRODUCT', COUNT(*) FROM PRODUCT
-- ... (see full query in wiki)
```

---

## 🧪 Testing

**Automated Testing** (runs on every push):
- ✅ Schema validation
- ✅ Generator execution
- ✅ Data integrity checks
- ✅ Foreign key constraints

**Manual Testing:**
```bash
python master_runner.py          # Run all generators
python validate_database.py       # Validate schema
```

---

## 📥 Download Database

### From GitHub Actions:
1. Go to [Actions](https://github.com/derkaiser9423/retail-pos-generator/actions)
2. Click latest "Automated Data Generation"
3. Scroll to **Artifacts**
4. Download `retail-pos-database-run-XXX`

### Current Stats:
- **Records:** 194,633
- **Size:** 19.87 MB
- **Last Updated:** 2025-12-02 20:16 UTC

---

## 🎯 Script Execution Order
```
Phase 1 (No Dependencies):
  01. Categories
  02. Suppliers
  03. Staff
  04. Machines
  05. Payment Methods
  06. Transaction Types

Phase 2 (Requires Phase 1):
  07. Product Groups  → Requires: Categories
  08. Products        → Requires: Product Groups + Suppliers

Phase 3 (Requires Phase 1 & 2):
  09. Transaction Headers → Requires: Staff, Machines, Payment Methods, Transaction Types
  10. Transaction Lines   → Requires: Transaction Headers + Products
```

💡 **Tip:** Use `master_runner.py` to run all in correct order automatically!

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

## 📞 Support

- 🐛 Issues: [GitHub Issues](https://github.com/derkaiser9423/retail-pos-generator/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/derkaiser9423/retail-pos-generator/discussions)

---

## 📊 Statistics

![Repo Size](https://img.shields.io/github/repo-size/derkaiser9423/retail-pos-generator)
![Commit Activity](https://img.shields.io/github/commit-activity/m/derkaiser9423/retail-pos-generator)
![Last Commit](https://img.shields.io/github/last-commit/derkaiser9423/retail-pos-generator)

---

<div align="center">

**⚡ Powered by Python + SQLite + GitHub Actions**

*Generating realistic retail data 24/7 in the cloud*

**Current Status:** 194,633 records | 19.87 MB | Growing every 2 hours

</div>
