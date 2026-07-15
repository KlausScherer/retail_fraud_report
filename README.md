# 🛒 Retail Fraud Analysis & Sales Intelligence

## 📷 Project Preview

![Dashboard](Images/Dashboard.png)

---

## 📌 Overview

End-to-end data analytics project focused on **fraud detection in retail transactions** and **business performance analysis**.

This project simulates a real-world retail environment, combining:

- Data generation (Python)
- SQL data analysis
- Dashboard visualization
- Automated executive reporting (PDF)

---

## 🎯 Objectives

- Detect and analyze fraudulent transactions  
- Identify high-risk customers  
- Evaluate sales performance across stores and products  
- Deliver an automated executive-level report  

---

## 🧱 Tech Stack

- **Python** (Pandas, ReportLab)
- **MySQL**
- **SQL**
- **Power BI / Data Visualization**
- **Git & GitHub**

---

## 📂 Project Structure
```
Retail-Fraud-Analysis/
│
├── Dashboard/ → Dashboard file
├── Data/ → Generated or source data
├── Images/ image preview
├── Output/ → Generated PDF report
├── Script/ → Python scripts
│ ├── generate_data.py
│ └── retail_fraud_report.py
│
├── SQL/
│ ├── sales.db → Database structure (tables)
│ └── sales_queries.sql → Analysis queries
│
└── README.md
```

---

## 📊 Key Business Metrics

- 💰 **Total Sales**  
- 🧾 **Average Ticket**  
- 👥 **Total Customers**  
- 🚨 **Fraud Rate**  
- 🏬 **Sales by Store**  
- 📦 **Sales by Product**  

---

## 🚨 Fraud Analysis Approach

Fraud detection is based on flagged transactions and analyzed through:

- Fraud frequency per customer  
- Fraud ratio (fraud / total transactions)  
- Identification of high-risk customers  

---

## 📈 Dashboard

The dashboard provides a visual overview of:

- Sales performance  
- Fraud distribution  
- Key KPIs  

📍 Located in:
`Dashboard/DashboardP2.pbix`

---

## 📄 Automated Executive Report

A professional PDF report is automatically generated using Python.

### Includes:

- Executive summary  
- Key business KPIs  
- Fraud insights  
- Top high-risk customers  
- Sales breakdown by store and product  

📍 Output file:
Output/retail_fraud_report.pdf


---

## ⚙️ How to Run the Project

### 1️⃣ Generate data

python Script/generate_data.py
### 2️⃣ Run analysis and generate report
python Script/retail_fraud_report.py

💡 Key Insights
A small group of customers concentrates most fraud cases
Fraud is not evenly distributed across stores and products
Higher transaction frequency may indicate higher fraud exposure
🚀 Project Highlights

✔ End-to-end data pipeline
✔ Business-focused analysis
✔ Fraud detection use case
✔ Automated reporting (PDF)
✔ Clean and structured project

📦 Requirements

Create a requirements.txt file with:
pandas
mysql-connector-python
reportlab

👤 Author

Klaus
Data Analyst | SQL | Python | Business Analytics

📌 Notes

This project is designed for portfolio purposes and simulates a real retail analytics scenario with a focus on fraud detection.
