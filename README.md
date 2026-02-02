# 🚀 PySpark Financial Analytics Dashboard

A full-stack big data analytics application that processes multi-departmental financial data using Apache Spark and visualizes insights through an interactive web dashboard.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![PySpark](https://img.shields.io/badge/PySpark-4.1.1-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-green)

## 📊 Features

- ✅ Real-time profit/loss calculation across multiple departments
- 📈 Interactive data visualizations (Bar charts, Pie charts)
- 🔄 Auto-refresh functionality (60-second intervals)
- 📁 Multi-format data ingestion (CSV, JSON)
- 🏢 Department-wise performance tracking (Sales, HR, Finance, Production)
- 📄 PDF export functionality
- ⚡ Fast REST API with sub-second response times

## 🛠️ Tech Stack

**Backend:**
- Apache Spark (PySpark 4.1.1)
- FastAPI 0.128.0
- Python 3.10
- Uvicorn 0.40.0

**Frontend:**
- HTML5, CSS3, JavaScript (ES6+)
- Chart.js

## 📁 Project Structure
```
bigdataproj/
├── api/
│   └── main.py                    # FastAPI REST API
├── data/
│   ├── sales.csv                  # Sales data
│   ├── hr.csv                     # HR data
│   ├── finance.csv                # Finance data
│   └── production.json            # Production data
├── utils/
│   └── spark_analytics.py         # PySpark analytics
├── spark_jobs/
│   ├── phase1_ingestion.py        # Data ingestion
│   ├── phase2_cleaning.py         # Data cleaning
│   └── phase3_file_processing.py  # Data processing
├── combined_dashboard.html         # Web dashboard
├── requirements.txt                # Dependencies
└── README.md                       # Documentation
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+
- pip

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/pyspark-financial-dashboard.git
cd pyspark-financial-dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the API server**
```bash
python api/main.py
```

4. **Open the dashboard**
- Double-click `combined_dashboard.html`
- Or visit: http://localhost:8000/docs for API documentation

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/summary` | GET | Overall profit/loss summary |
| `/api/department-breakdown` | GET | Department-wise breakdown |
| `/api/stats` | GET | Detailed statistics |
| `/api/refresh` | POST | Reload data from files |

## 💡 Usage Example
```python
import requests

response = requests.get('http://localhost:8000/api/summary')
data = response.json()

print(f"Total Income: ${data['total_income']}")
print(f"Profit/Loss: ${data['profit_loss']}")
```

**Sample Output:**
```json
{
  "total_income": 310000.0,
  "total_expenses": 48000.0,
  "profit_loss": 262000.0,
  "status": "Profit"
}
```

## 🎯 System Architecture
```
Data Files (CSV/JSON)
        ↓
Apache Spark (ETL Pipeline)
        ↓
FastAPI (REST API - Port 8000)
        ↓
Web Dashboard (Charts & Visualization)
```

## 📈 Key Results

- Processes 100+ financial transactions
- Real-time profit/loss calculation
- Tracks 4 departments simultaneously
- Auto-refresh every 60 seconds
- Interactive charts with Chart.js

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

---

⭐ If you found this helpful, please star this repository!