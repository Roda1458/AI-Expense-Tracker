
# 💰 AI-Powered Expense Tracker & Financial Insights Dashboard

An interactive dashboard that helps users **track, analyze, and forecast their expenses** using AI and Machine Learning. The project automatically categorizes expenses, visualizes spending trends, generates insights, predicts future spending, and allows PDF report downloads.

---

## 🌟 Key Features

### ✅ Core Functionality
- Upload & Track Expenses: Upload your CSV file or use the sample dataset.
- Automatic Category Prediction: AI model predicts missing categories for accurate analysis.
- Interactive Dashboard:
  - Total spending, average transaction, top category metrics
  - Pie chart: spending by category
  - Line chart: monthly spending trends
  - Weekly bar chart: spending per week
  - Category trends over time
- Interactive Filters: Filter by categories, months, or amount ranges.

### 🤖 AI & ML Features
- AI Insights Summary: Shows month-over-month spending changes and top 3 categories.
- Spending Forecast: Predicts next month’s spending using Linear Regression based on historical data.

### 🖥️ Additional Enhancements
- PDF Export: Download professional expense reports.
- Persistent Storage: Stores all data in SQLite database.
- Modern UI Layout: Tabs, colored metrics, and styled charts for a professional look.

---

## 🛠️ Tech Stack
- Python – Core programming language  
- Streamlit – Interactive dashboard UI  
- Pandas – Data analysis and manipulation  
- Plotly / Matplotlib – Data visualization  
- Scikit-learn – ML for category prediction and spending forecast  
- ReportLab – PDF report generation  
- SQLite – Persistent storage  

---

## ⚡ Installation & Setup

**Install dependencies:**
```bash
pip install streamlit pandas matplotlib plotly scikit-learn joblib reportlab sqlalchemy
````

**Run the app:**

```bash
streamlit run app.py
```

---

## 📊 Usage Guide

* **Upload CSV or Use Sample Data:** The app reads your expense data from a CSV file.
* **Explore Dashboard:** Check key metrics, charts, and weekly/monthly trends.
* **AI Insights Tab:** View AI-generated summaries showing spending changes and top categories.
* **Prediction Tab:** See next month’s forecasted spending using ML.
* **Download PDF:** Export your full expense report for record-keeping.

---

## 📝 Sample CSV Format

| Date       | Description      | Category | Amount |
| ---------- | ---------------- | -------- | ------ |
| 2025-01-01 | Grocery Shopping | Food     | 500    |
| 2025-01-02 | Uber Ride        | Travel   | 200    |
| 2025-01-03 | Rent Payment     | Housing  | 15000  |

---

## 📈 Project Highlights

* Real-world application for personal or business expense tracking.
* AI-powered category prediction and monthly insights.
* ML-based spending prediction for budget planning.
* Interactive charts and modern UI layout for portfolio-ready presentation.

---


## 🚀 Future Enhancements

* Google Sheets integration for live data syncing.
* Category-wise budget alerts to monitor overspending.
* Dynamic AI suggestions to optimize spending and save money.

```
