# PolyRatings Data Collection

Automated daily collection of professor data and student reviews from PolyRatings API.

## 🚀 Quick Setup

```bash
# Run the setup script
./setup.sh

# Test locally
python get_professor_ids.py
```

## 📁 File Structure

```
data/
├── main/                           # Current data (committed to git)
│   ├── professors_data.csv         # Basic professor info
│   ├── professor_name_to_id.csv    # Name-to-ID mapping
│   ├── department_summary.csv      # Department statistics
│   └── professor_detailed_reviews.csv  # Student reviews & comments
└── tracking/                       # Historical snapshots (ignored by git)
    ├── professors_full_data_YYYYMMDD_HHMMSS.csv
    ├── professor_name_to_id_YYYYMMDD_HHMMSS.csv
    ├── department_summary_YYYYMMDD_HHMMSS.csv
    └── professor_detailed_reviews_YYYYMMDD_HHMMSS.csv
```

## 🔄 How It Works

### Local Development
- Run `python get_professor_ids.py` to collect data
- Main files are updated with fresh data
- Tracking files preserve historical snapshots

### GitHub Actions (Daily Automation)
- **Schedule**: Runs daily at 6 AM UTC
- **Manual**: Can be triggered manually from Actions tab
- **Safety**: Only updates main files if data collection succeeds
- **Artifacts**: Tracking files saved as artifacts (30-day retention)

## 📊 Data Collected

### Basic Professor Data
- Professor information (name, department, ratings)
- Course lists and tags
- Evaluation counts and ratings

### Detailed Reviews
- Student comments for each course
- Individual review ratings
- Grade information and course types
- Post dates and review metadata

## 🛡️ Safety Features

- **Tracking-first approach**: Data saved to tracking before updating main
- **Error resilience**: Main files never corrupted by failed runs
- **Historical preservation**: All runs saved with timestamps
- **Git safety**: Only main files committed, tracking files ignored

## ⚙️ Configuration

### Schedule Adjustment
Edit `.github/workflows/daily-data-collection.yml`:
```yaml
schedule:
  - cron: '0 6 * * *'  # 6 AM UTC daily
```

### Timezone Options
- `'0 6 * * *'` - 6 AM UTC
- `'0 14 * * *'` - 2 PM UTC (8 AM PST)
- `'0 18 * * *'` - 6 PM UTC (10 AM PST)

## 📈 Monitoring

1. **GitHub Actions**: Check the Actions tab for run status
2. **Artifacts**: Download tracking files from successful runs
3. **Commits**: Main data updates are automatically committed
4. **Logs**: Full execution logs available in Actions

## 🔧 Troubleshooting

### Common Issues
- **API rate limits**: Script includes delays between requests
- **Network timeouts**: 30-second timeout per request
- **File permissions**: Ensure write access to data directories

### Manual Runs
```bash
# Test the script
python get_professor_ids.py

# Check what would be committed
git status
git diff --staged
```

## 📝 Notes

- **API Respect**: 0.1-second delay between professor requests
- **Data Freshness**: Main files always contain latest successful run
- **Storage**: Tracking files preserved as GitHub artifacts
- **Reliability**: Failed runs don't affect existing data