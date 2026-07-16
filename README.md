# ⚡ Hydrogen Production AI Studio V2

### Intelligent Decision Support System for Sustainable Hydrogen Production

HydroIntel AI Studio is an AI-powered decision support platform that predicts hydrogen production, evaluates environmental sustainability, and generates automated AI-based sustainability reports.

Unlike traditional hydrogen assessment tools, HydroIntel allows users to analyze hydrogen production using either geographic locations or custom plant parameters, making it suitable for researchers, industries, and policymakers.

---

## 🚀 Features

- 🌍 Location-based Hydrogen Prediction
- 🏭 Custom Plant Parameter Prediction
- ♻️ Life Cycle Assessment (LCA) Integration
- 🤖 Machine Learning Prediction
- 📊 Interactive Visualizations
- 🔍 Explainable AI (Feature Importance)
- 📝 Google Gemini AI Sustainability Report
- 📄 Automatic PDF Report Generation
- 🎨 Modern Streamlit Dashboard

---

## 🧠 Machine Learning Models

The prediction engine is based on an ensemble learning approach using:

- Voting Regressor
- Random Forest Regressor
- XGBoost Regressor
- Ridge Regression

---

## 🌱 Sustainability Indicators

The platform estimates:

- Hydrogen Production
- CO₂ Emissions
- Sustainability Score
- Environmental Interpretation
- AI-based Recommendations

---

## 🏗 Project Workflow

```text
User Input
(Location / Plant Parameters)

            │
            ▼

Feature Engineering

            │
            ▼

Machine Learning Prediction

            │
            ▼

Hydrogen Production

            │
            ▼

Environmental Impact

            │
            ▼

Explainable AI

            │
            ▼

Gemini AI Report

            │
            ▼

Professional PDF Report
```

---

## 📂 Project Structure

```text
HydroIntel-AI-Studio/

│

├── app.py

├── config.py

├── prediction_agent.py

├── xai_agent.py

├── report_agent.py

├── pdf_generator.py

├── Hydrogen_LCA_Final_Preprocessed.csv

├── best_final_ensemble_model.pkl

├── scaler.pkl

├── feature_names.pkl

├── report_prompt.txt

├── outputs/

│

├── requirements.txt

└── README.md
```

---

## ⚙ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/HydroIntel-AI-Studio.git

cd HydroIntel-AI-Studio
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

Install packages

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file

```text
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

---

## ▶ Run Application

```bash
streamlit run app.py
```

---

## 📚 Technologies Used

- Python
- Streamlit
- Scikit-Learn
- XGBoost
- Plotly
- Pandas
- NumPy
- Google Gemini API
- ReportLab

---

## 🎯 Future Enhancements

- Multi-country hydrogen planning
- Plant optimization engine
- Cost estimation
- Renewable resource integration
- Digital Twin support
- GIS visualization
- Multi-objective optimization
- Carbon footprint comparison dashboard

---

## 👩‍💻 Developer

**Radha Pandey**

Spark Intern

Department of Hydro and Renewable Energy

Indian Institute of Technology Roorkee

---

## 📄 License

This project is intended for academic and research purposes.
