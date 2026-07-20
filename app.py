# ==========================================================
# PAGE CONFIG
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from prediction_agent import PredictionAgent
from xai_agent import XAIAgent
from report_agent import ReportAgent
from pdf_generator import PDFGenerator

from config import *

st.set_page_config(
    page_title=APP_NAME,
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# MODERN CSS
# ==========================================================

st.markdown("""
<style>

/* ---------------- Background ---------------- */

.main{
    background-color:#F7F9FC;
}

.block-container{
    padding-top:1.5rem;
    padding-bottom:2rem;
}

/* ---------------- Sidebar ---------------- */

section[data-testid="stSidebar"]{
    background:#0F172A;
}

section[data-testid="stSidebar"] *{
    color:white;
}

/* ---------------- Titles ---------------- */

.big-title{
    font-size:42px;
    font-weight:700;
    color:#1E3A8A;
}

.subtitle{
    font-size:18px;
    color:#475569;
}

/* ---------------- Cards ---------------- */

.metric-card{

    background:white;

    padding:20px;

    border-radius:18px;

    border:1px solid #E2E8F0;

    box-shadow:0px 6px 18px rgba(0,0,0,0.08);

}

.prediction-card{

    background:white;

    padding:22px;

    border-radius:18px;

    border:1px solid #E2E8F0;

    box-shadow:0px 6px 18px rgba(0,0,0,0.08);

}

/* ---------------- Metrics ---------------- */

div[data-testid="stMetric"]{

    background:white;

    border:1px solid #E2E8F0;

    border-radius:14px;

    padding:14px;

}

/* ---------------- Info Boxes ---------------- */

div[data-testid="stInfo"]{

    border-radius:16px;

}

div[data-testid="stSuccess"]{

    border-radius:16px;

}

div[data-testid="stWarning"]{

    border-radius:16px;

}

/* ---------------- Footer ---------------- */

.footer{

    text-align:center;

    color:#64748B;

    padding:30px;

}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD AGENTS
# ==========================================================

@st.cache_resource
def load_prediction():
    return PredictionAgent()

@st.cache_resource
def load_xai():
    return XAIAgent()

@st.cache_resource
def load_report():
    return ReportAgent()

@st.cache_resource
def load_pdf():
    return PDFGenerator()

prediction_agent = load_prediction()
xai_agent = load_xai()
report_agent = load_report()
pdf_generator = load_pdf()

# ==========================================================
# SESSION STATE
# ==========================================================

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "feature_importance" not in st.session_state:
    st.session_state.feature_importance = None

if "report" not in st.session_state:
    st.session_state.report = None

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("⚡ Hydrogen AI Studio")

page = st.sidebar.radio(

    "Navigation",

    [

        "🏠 Dashboard",

        "🔮 Prediction",

        "📄 AI Report",

        "ℹ️ About"

    ]

)

st.sidebar.markdown("---")

st.sidebar.success(

f"""

### 📌 Application Information

**Version**

{APP_VERSION}

---

**Machine Learning**

Voting Regressor Ensemble

---

**Generative AI**

Gemini

---

**Explainable AI**

Feature Importance Analysis

"""
# ==========================================================
# DASHBOARD
# ==========================================================

if page == "🏠 Dashboard":

    # ======================================================
    # TITLE
    # ======================================================

    st.markdown(
        """
        <div class="big-title">
        ⚡ Hydrogen Production AI Studio
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitle">
        Machine Learning Assisted Life Cycle Assessment (LCA)
        for Sustainable Hydrogen Production
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ======================================================
    # OVERVIEW
    # ======================================================

    left, right = st.columns([2,1])

    with left:

        st.info("""
### 🌍 Research Overview

Hydrogen AI Studio integrates

- Machine Learning
- Life Cycle Assessment (LCA)
- Explainable AI
- Google Gemini AI

to estimate hydrogen production, analyse environmental impacts,
and generate professional sustainability reports.
""")

    with right:

        st.success("""
### 🚀 Platform Modules

✔ Hydrogen Prediction

✔ CO₂ Estimation

✔ Explainable AI

✔ AI Sustainability Report

✔ PDF Report Export
""")

    st.markdown("---")

    # ======================================================
    # DATASET
    # ======================================================

    dataset = prediction_agent.master

    col1, col2 = st.columns([2,1])

    with col1:

        st.subheader("📊 Production Pathway Distribution")

        pathway = (
            dataset["Production_Pathway"]
            .value_counts()
            .reset_index()
        )

        pathway.columns = ["Production Pathway","Samples"]

        fig = px.bar(

            pathway,

            x="Production Pathway",

            y="Samples",

            color="Samples",

            text="Samples",

            template="plotly_white"

        )

        fig.update_layout(

            showlegend=False,

            height=420

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with col2:

        st.subheader("📈 Dataset Statistics")

        st.metric(

            "Total Samples",

            len(dataset)

        )

        st.metric(

            "Unique Locations",

            dataset["Location"].nunique()

        )

        st.metric(

            "Average Hydrogen",

            f"{dataset['Hydrogen_Output_kg_day'].mean():.1f} kg/day"

        )

        st.metric(

            "Average CO₂",

            f"{dataset['LCA_GWP_kg_CO2_eq_per_kg_H2'].mean():.2f}"

        )

    st.markdown("---")

    # ======================================================
    # DATA PREVIEW
    # ======================================================

    st.subheader("📄 Dataset Preview")

    st.dataframe(

        dataset.head(10),

        use_container_width=True

    )

    st.markdown("---")

    # ======================================================
    # WORKFLOW
    # ======================================================

    st.subheader("⚙ AI Workflow")

    st.code(

"""
Latitude / Longitude
        OR
User Based Prediction
        │
        ▼
Nearest Dataset Retrieval
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
Professional PDF Export
""",

        language="text"

    )

    st.markdown("---")

    # ======================================================
    # FEATURES
    # ======================================================

    c1, c2 = st.columns(2)

    with c1:

        st.success("""

### 🧠 Machine Learning

• Voting Regressor Ensemble

• Latitude / Longitude Prediction

• User Based Prediction

• Automated Feature Engineering

• Environmental Assessment

""")

    with c2:

        st.success("""

### 🤖 Artificial Intelligence

• Explainable AI

• Gemini AI Report

• Sustainability Analysis

• PDF Report Export

• Interactive Visualisation

""")

    st.markdown("---")

    # ======================================================
    # PROJECT OBJECTIVE
    # ======================================================

    st.subheader("📚 Project Objective")

    st.write("""

Hydrogen AI Studio is designed to assist researchers in analysing
hydrogen production pathways using Machine Learning and Life Cycle
Assessment.

The platform predicts hydrogen production, estimates environmental
impacts, explains important influencing parameters, and generates
professional AI-assisted sustainability reports for decision support.

""")



)
