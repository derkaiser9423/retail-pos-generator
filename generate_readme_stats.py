"""
Generate README with Real Database Statistics
Updates README.md with current database stats and generates growth charts
"""

import sqlite3
import json
import os
from datetime import datetime
from config import DATABASE_PATH

def get_database_stats():
    """Get current database statistics"""
    stats = {
        'timestamp': datetime.now().isoformat(),
        'tables': {}
    }
    
    tables = [
        'CATEGORY', 'SUPPLIER', 'STAFF', 'MACHINE', 
        'PAYMENT_METHOD', 'TRANSACTION_TYPE', 'PRODUCT_GROUP',
        'PRODUCT', 'TRANSACTION_HEADER', 'TRANSACTION_LINE'
    ]
    
    if not os.path.exists(DATABASE_PATH):
        print("Database not found, using zeros")
        for table in tables:
            stats['tables'][table] = 0
        stats['total_records'] = 0
        stats['database_size_mb'] = 0.0
        return stats
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        
        # Get record counts
        total = 0
        for table in tables:
            try:
                cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                stats['tables'][table] = count
                total += count
            except:
                stats['tables'][table] = 0
        
        stats['total_records'] = total
        
        # Get database size
        db_size = os.path.getsize(DATABASE_PATH) / (1024 * 1024)
        stats['database_size_mb'] = round(db_size, 2)
        
        conn.close()
        
    except Exception as e:
        print(f"Error getting stats: {e}")
        for table in tables:
            stats['tables'][table] = 0
        stats['total_records'] = 0
        stats['database_size_mb'] = 0.0
    
    return stats

def load_history():
    """Load historical statistics"""
    if os.path.exists('stats_history.json'):
        try:
            with open('stats_history.json', 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(current_stats):
    """Save current stats to history"""
    history = load_history()
    
    # Add current stats
    history.append({
        'timestamp': current_stats['timestamp'],
        'total_records': current_stats['total_records'],
        'database_size_mb': current_stats['database_size_mb'],
        'tables': current_stats['tables']
    })
    
    # Keep only last 100 entries
    history = history[-100:]
    
    with open('stats_history.json', 'w') as f:
        json.dump(history, f, indent=2)
    
    return history

def generate_ascii_chart(history, key='total_records'):
    """Generate ASCII chart for data growth"""
    if len(history) < 2:
        return "Not enough data yet (need at least 2 data points)"
    
    # Get last 20 data points
    data = [entry[key] for entry in history[-20:]]
    
    if not data or max(data) == 0:
        return "No data available"
    
    # Normalize to 0-10 range for chart
    max_val = max(data)
    min_val = min(data)
    
    if max_val == min_val:
        normalized = [5] * len(data)
    else:
        normalized = [int((val - min_val) / (max_val - min_val) * 10) for val in data]
    
    # Build chart
    chart = []
    chart.append(f"📈 Growth Trend (Last {len(data)} data points)")
    chart.append("")
    
    # Y-axis and bars
    for i in range(10, -1, -1):
        line = f"{max_val - (max_val - min_val) * (10 - i) / 10:>8.0f} |"
        for val in normalized:
            if val >= i:
                line += "█"
            else:
                line += " "
        chart.append(line)
    
    # X-axis
    chart.append("         +" + "─" * len(data))
    
    return "\n".join(chart)

def generate_table_bar(count, max_count):
    """Generate a visual bar for table records"""
    if max_count == 0:
        return ""
    
    bar_length = int((count / max_count) * 20)
    bar = "█" * bar_length
    return f"{bar} {count:,}"

def generate_readme(stats, history):
    """Generate README.md with current statistics"""
    
    # Calculate growth
    growth_24h = "N/A"
    if len(history) >= 2:
        records_diff = stats['total_records'] - history[-2]['total_records']
        if records_diff > 0:
            growth_24h = f"+{records_diff:,} records"
        elif records_diff < 0:
            growth_24h = f"{records_diff:,} records"
        else:
            growth_24h = "No change"
    
    # Get max count for bar charts
    max_table_count = max(stats['tables'].values()) if stats['tables'].values() else 1
    
    # Generate ASCII chart
    ascii_chart = generate_ascii_chart(history, 'total_records')
    
    readme_content = f"""# 🏪 Retail POS Database - Automated Data Generation

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![SQLite](https://img.shields.io/badge/sqlite-3-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Total Records](https://img.shields.io/badge/records-{stats['total_records']:,}-brightgreen)
![Database Size](https://img.shields.io/badge/size-{stats['database_size_mb']}MB-blue)

![Data Generation](https://github.com/derkaiser9423/retail-pos-generator/actions/workflows/data-generation.yml/badge.svg)
![Tests](https://github.com/derkaiser9423/retail-pos-generator/actions/workflows/test-generators.yml/badge.svg)
![Database Backup](https://github.com/derkaiser9423/retail-pos-generator/actions/workflows/database-backup.yml/badge.svg)

> **Last Updated:** {datetime.fromisoformat(stats['timestamp']).strftime('%Y-%m-%d %H:%M:%S UTC')}  
> **24h Growth:** {growth_24h}

Automated data generation system for a retail pharmacy POS database. Generates realistic transaction data, products, staff, and more using scheduled Python scripts with **GitHub Actions automation**.

---

## 📊 Live Database Statistics

### Overview

| Metric | Value |
|--------|-------|
| 📦 **Total Records** | **{stats['total_records']:,}** |
| 💾 **Database Size** | **{stats['database_size_mb']} MB** |
| 📅 **Last Updated** | {datetime.fromisoformat(stats['timestamp']).strftime('%B %d, %Y at %H:%M UTC')} |
| 📈 **24h Growth** | {growth_24h} |
| 🤖 **Status** | ![Active](https://img.shields.io/badge/status-generating-success) |

### Record Counts by Table
```
┌─────────────────────────┬──────────────────────────────┐
│ Table                   │ Records                      │
├─────────────────────────┼──────────────────────────────┤
│ 📊 Categories           │ {generate_table_bar(stats['tables'].get('CATEGORY', 0), max_table_count):<30} │
│ 🏢 Suppliers            │ {generate_table_bar(stats['tables'].get('SUPPLIER', 0), max_table_count):<30} │
│ 👥 Staff                │ {generate_table_bar(stats['tables'].get('STAFF', 0), max_table_count):<30} │
│ 🖥️ Machines             │ {generate_table_bar(stats['tables'].get('MACHINE', 0), max_table_count):<30} │
│ 💳 Payment Methods      │ {generate_table_bar(stats['tables'].get('PAYMENT_METHOD', 0), max_table_count):<30} │
│ 📋 Transaction Types    │ {generate_table_bar(stats['tables'].get('TRANSACTION_TYPE', 0), max_table_count):<30} │
│ 🏷️ Product Groups       │ {generate_table_bar(stats['tables'].get('PRODUCT_GROUP', 0), max_table_count):<30} │
│ 📦 Products             │ {generate_table_bar(stats['tables'].get('PRODUCT', 0), max_table_count):<30} │
│ 🧾 Transaction Headers  │ {generate_table_bar(stats['tables'].get('TRANSACTION_HEADER', 0), max_table_count):<30} │
│ 📝 Transaction Lines    │ {generate_table_bar(stats['tables'].get('TRANSACTION_LINE', 0), max_table_count):<30} │
└─────────────────────────┴──────────────────────────────┘
```

### Data Growth Visualization
```
{ascii_chart}
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

- ✅ {stats['tables'].get('CATEGORY', 0):,} Categories (+ 2 per run)
- ✅ {stats['tables'].get('SUPPLIER', 0):,} Suppliers (+ 3 per run)
- ✅ {stats['tables'].get('STAFF', 0):,} Staff members (+ 2 per run)
- ✅ {stats['tables'].get('PRODUCT', 0):,} Products (+ 10 per run)
- ✅ {stats['tables'].get('TRANSACTION_HEADER', 0):,} Transactions (+ 20 per run)
- ✅ {stats['tables'].get('TRANSACTION_LINE', 0):,} Transaction lines (+ 50 per run)

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
├── retail_pos.db                # SQLite database ({stats['database_size_mb']} MB)
├── stats_history.json           # Statistics history
├── requirements.txt             # Dependencies
└── README.md                    # This file (auto-updated!)
```

---

## 🔧 Configuration

Edit `config.py` to customize:
```python
BATCH_SIZES = {{
    'CATEGORY': 2,              # Records per run
    'PRODUCT': 10,
    'TRANSACTION_LINE': 50,
}}

PRICE_RANGES = {{
    'min': 0.10,
    'max': 100.00,
}}

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
- **Records:** {stats['total_records']:,}
- **Size:** {stats['database_size_mb']} MB
- **Last Updated:** {datetime.fromisoformat(stats['timestamp']).strftime('%Y-%m-%d %H:%M UTC')}

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

**Current Status:** {stats['total_records']:,} records | {stats['database_size_mb']} MB | Growing every 2 hours

</div>
"""
    
    return readme_content

def main():
    """Main execution"""
    print("Generating README with real statistics...")
    
    # Get current stats
    stats = get_database_stats()
    print(f"Current stats: {stats['total_records']:,} total records, {stats['database_size_mb']} MB")
    
    # Save to history
    history = save_history(stats)
    print(f"History has {len(history)} data points")
    
    # Generate README
    readme = generate_readme(stats, history)
    
    # Write README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme)
    
    print("✓ README.md updated successfully!")
    print(f"  - Total Records: {stats['total_records']:,}")
    print(f"  - Database Size: {stats['database_size_mb']} MB")
    print(f"  - Timestamp: {stats['timestamp']}")

if __name__ == "__main__":
    main()
