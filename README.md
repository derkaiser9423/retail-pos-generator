# 🏪 Retail POS Database - Automated Data Generation

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![SQLite](https://img.shields.io/badge/sqlite-3-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

![Data Generation](https://github.com/yourusername/retail-pos-generator/actions/workflows/data-generation.yml/badge.svg)
![Tests](https://github.com/yourusername/retail-pos-generator/actions/workflows/test-generators.yml/badge.svg)
![Database Backup](https://github.com/yourusername/retail-pos-generator/actions/workflows/database-backup.yml/badge.svg)

[![Total Records](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/yourusername/retail-pos-generator/main/stats.json&label=Total%20Records&query=$.total_records&color=brightgreen&suffix=%20records)](https://github.com/yourusername/retail-pos-generator)
[![Database Size](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/yourusername/retail-pos-generator/main/stats.json&label=Database%20Size&query=$.database_size_mb&color=blue&suffix=%20MB)](https://github.com/yourusername/retail-pos-generator)
[![Last Updated](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/yourusername/retail-pos-generator/main/stats.json&label=Last%20Updated&query=$.last_updated&color=lightgrey)](https://github.com/yourusername/retail-pos-generator)

Automated data generation system for a retail pharmacy POS database. Generates realistic transaction data, products, staff, and more using scheduled Python scripts with **GitHub Actions automation**.

## 📊 Live Database Statistics

<!-- This section is auto-updated by GitHub Actions -->

| Table | Records | Status |
|-------|---------|--------|
| 📊 Categories | ![Categories](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/yourusername/retail-pos-generator/main/stats.json&label=%20&query=$.tables.categories&color=blue) | ✅ |
| 🏢 Suppliers | ![Suppliers](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/yourusername/retail-pos-generator/main/stats.json&label=%20&query=$.tables.suppliers&color=blue) | ✅ |
| 👥 Staff | ![Staff](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/yourusername/retail-pos-generator/main/stats.json&label=%20&query=$.tables.staff&color=blue) | ✅ |
| 🖥️ Machines | ![Machines](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/yourusername/retail-pos-generator/main/stats.json&label=%20&query=$.tables.machines&color=blue) | ✅ |
| 💳 Payment Methods | ![Payment Methods](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/yourusername/retail-pos-generator/main/stats.json&label=%20&query=$.tables.payment_methods&color=blue) | ✅ |
| 📋 Transaction Types | ![Transaction Types](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/yourusername/retail-pos-generator/main/stats.json&label=%20&query=$.tables.transaction_types&color=blue) | ✅ |
| 🏷️ Product Groups | ![Product Groups](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/yourusername/retail-pos-generator/main/stats.json&label=%20&query=$.tables.product_groups&color=blue) | ✅ |
| 📦 Products | ![Products](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/yourusername/retail-pos-generator/main/stats.json&label=%20&query=$.tables.products&color=green) | ✅ |
| 🧾 Transactions | ![Transactions](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/yourusername/retail-pos-generator/main/stats.json&label=%20&query=$.tables.transactions&color=green) | ✅ |
| 📝 Transaction Lines | ![Lines](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/yourusername/retail-pos-generator/main/stats.json&label=%20&query=$.tables.transaction_lines&color=green) | ✅ |

*Statistics updated automatically every 2 hours*

## 🤖 Automation Status

### GitHub Actions Workflows

- **🔄 Data Generation** - Runs every 2 hours, generates new data across all tables
- **🧪 Testing** - Runs on every push, validates schema and data integrity
- **💾 Database Backup** - Daily backups with 90-day retention

### Local Automation

- **Windows Task Scheduler** - For local PC generation
- **Auto-commit** - Automatic Git commits after each generation
- **Smart batching** - Configurable batch sizes per table

## 🚀 Quick Start

### Local Setup
```bash
# Clone repository
git clone https://github.com/yourusername/retail-pos-generator.git
cd retail-pos-generator

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Initial database population
python master_runner.py

# Run with auto-commit
python wrapper_with_git.py 01_generate_categories.py
```

### GitHub Actions (Cloud)

Simply push to main branch - GitHub Actions will automatically:
1. ✅ Run tests
2. 🤖 Generate data every 2 hours
3. 💾 Create daily backups
4. 📊 Update statistics badges

## 📅 Generation Schedules

### Local (Task Scheduler)
- **Every 15 minutes**: Transaction Lines (high volume)
- **Every 30 minutes**: Transaction Headers
- **Every 2 hours**: Products
- **Every 4 hours**: Product Groups
- **Daily**: Reference data

### Cloud (GitHub Actions)
- **Every 2 hours**: Full generation cycle
- **Daily**: Database backup
- **On push**: Automated testing

## 🗄️ Database Schema

Normalized to **3NF** (Third Normal Form):
```
CATEGORY (1) ──→ (M) PRODUCT_GROUP (1) ──→ (M) PRODUCT
                                                   ↓
SUPPLIER (1) ──────────────────────────────────→ (M)

STAFF (1) ──→ (M) TRANSACTION_HEADER (1) ──→ (M) TRANSACTION_LINE
                       ↑
MACHINE (1) ────────────┤
PAYMENT_METHOD (1) ─────┤
TRANSACTION_TYPE (1) ───┘
```

## 📁 Project Structure
```
.
├── .github/
│   └── workflows/
│       ├── data-generation.yml      # Automated data generation
│       ├── test-generators.yml      # CI/CD testing
│       └── database-backup.yml      # Daily backups
├── config.py                         # Configuration
├── utils.py                          # Helper functions
├── git_commit_after_generation.py    # Auto-commit
├── wrapper_with_git.py               # Generator wrapper
├── generate_stats_badge.py           # Statistics generator
├── validate_database.py              # Schema validator
├── master_runner.py                  # Run all generators
├── 01-10_generate_*.py               # Individual generators
├── retail_pos.db                     # SQLite database
├── stats.json                        # Current statistics
├── requirements.txt                  # Python dependencies
└── logs/                             # Generation logs
```

## 🔧 Configuration

Edit `config.py` to customize:
```python
# Batch sizes (records per run)
BATCH_SIZES = {
    'CATEGORY': 2,
    'PRODUCT': 10,
    'TRANSACTION_LINE': 50,
    # ...
}

# Auto-commit settings
AUTO_COMMIT_ENABLED = True
AUTO_PUSH_ENABLED = True

# Business rules
PRICE_RANGES = {'min': 0.10, 'max': 100.00}
DISCOUNT_PROBABILITY = 0.05
```

## 📈 Monitoring

### View Logs
```bash
# Today's log
cat logs/data_generation_$(date +%Y%m%d).log

# Live monitoring
tail -f logs/data_generation_$(date +%Y%m%d).log
```

### GitHub Actions Logs
1. Go to "Actions" tab in GitHub
2. Select workflow run
3. View detailed execution logs

### Database Query
```sql
-- Record counts
SELECT 'TOTAL' as Type, COUNT(*) as Count FROM (
    SELECT Transaction_Line_ID FROM TRANSACTION_LINE
    UNION ALL
    SELECT Transaction_ID FROM TRANSACTION_HEADER
    -- ... etc
);
```

## 🧪 Testing
```bash
# Run all tests
pytest test_generators.py -v

# With coverage
pytest --cov=. --cov-report=html

# Validate schema
python validate_database.py
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

MIT License - See [LICENSE](LICENSE) file

## 🎯 Roadmap

- [x] Core data generators
- [x] GitHub Actions automation
- [x] Auto-commit functionality
- [x] Database backups
- [x] Status badges
- [ ] Web dashboard for statistics
- [ ] REST API for data access
- [ ] Docker containerization
- [ ] Multi-database support (PostgreSQL, MySQL)

## 📞 Support

- 📧 Email: your-email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/retail-pos-generator/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/retail-pos-generator/discussions)

---

**⚡ Powered by Python + SQLite + GitHub Actions**

![Commit Activity](https://img.shields.io/github/commit-activity/w/yourusername/retail-pos-generator)
![Last Commit](https://img.shields.io/github/last-commit/yourusername/retail-pos-generator)
![Repo Size](https://img.shields.io/github/repo-size/yourusername/retail-pos-generator)
```

---

## FILE 27: LICENSE
```
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
{
  "last_updated": "2024-11-02T10:30:00",
  "total_records": 15420,
  "database_size_mb": 2.45,
  "tables": {
    "categories": 45,
    "products": 1250,
    "transactions": 8500,
    ...
  }
}
```

This file is regenerated after each data generation run!

---

## 🚀 Your Repository Will Look Like This
```
yourusername/retail-pos-generator

⭐ 12 stars | 🍴 3 forks | 👀 5 watching

[Python 3.8+] [SQLite 3] [MIT License]
[✓ Data Generation] [✓ Tests Passing] [✓ Backup Active]

📊 Total Records: 15,420 | 💾 Database: 2.45 MB | 🕐 Updated: 2 hours ago

README with live statistics...
GitHub Actions running...
Commits every 2 hours...
Professional documentation...
