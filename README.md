# Loan Eligibility AI System

## Overview
This project is an end-to-end machine learning application that predicts loan eligibility based on applicant financial and demographic data. The system is designed to support data-driven decision-making in financial services by automating loan approval predictions.

## Key Features
- Machine Learning classification model for loan approval prediction
- Interactive web application built with Streamlit
- Real-time prediction based on user input
- Loan Readiness Score (0–100) for decision support
- Risk categorization (Low / Medium / High)
- Clean and user-friendly interface

## Machine Learning Model
- Algorithms: Logistic Regression / Random Forest
- Accuracy: ~84%
- Evaluation Metrics:
  - Precision
  - Recall
  - F1-score

The model was trained on structured financial data and optimized for classification performance.

## Dataset
The dataset includes key features such as:
- Applicant Income
- Loan Amount
- Credit History
- Education Level

Data preprocessing steps:
- Missing value handling
- Encoding categorical variables
- Feature selection

## Business Impact

This system can support financial institutions by:
- Reducing manual loan approval effort
- Improving decision consistency
- Enabling faster customer response times
- Supporting risk-based decision making

The Loan Readiness Score provides an interpretable metric that helps non-technical stakeholders understand model outputs.

## Tech Stack
- Python
- Pandas, NumPy
- Scikit-learn
- Streamlit
- Pickle

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
