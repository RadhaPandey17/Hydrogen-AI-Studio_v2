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
color:#111827;

background:#1E293B;

color:white;

padding:20px;

border-radius:18px;

box-shadow:0 8px 20px rgba(0,0,0,.08);

}

.prediction-card{
    color:#111827;

    background:white;

    padding:22px;

    border-radius:18px;

    border:1px solid #E2E8F0;

    box-shadow:0px 6px 18px rgba(0,0,0,0.08);

}

/* ---------------- Metrics ---------------- */

div[data-testid="stMetric"]{

background:#1E293B;

color:white;

border:1px solid #334155;

border-radius:12px;

padding:15px;

}

div[data-testid="stMetric"] label{

color:white !important;

}

div[data-testid="stMetric"] div{

color:white !important;

}
div[data-testid="stMetricValue"]{
    color:white !important;
}

div[data-testid="stMetricLabel"]{
    color:#CBD5E1 !important;
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
)

if page == "🏠 Dashboard":
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


# ==========================================================
# PREDICTION PAGE
# ==========================================================
# ==========================================================
# PREDICTION PAGE
# ==========================================================

elif page == "🔮 Prediction":

    st.title("⚡ Hydrogen Production Prediction")

    st.caption(
        "Predict hydrogen production using Machine Learning."
    )

    st.markdown("---")

    # ===========================================
    # Prediction Mode
    # ===========================================

    prediction_mode = st.radio(

        "Prediction Mode",

        [

            "📍 Latitude / Longitude",

            "👤 User Based Prediction"

        ],

        horizontal=True

    )

    st.markdown("---")

    custom_inputs = None
    dataset_choice = None
    selected_country = None

    # =====================================================
    # MODE 1
    # Latitude / Longitude
    # =====================================================

    if prediction_mode == "📍 Latitude / Longitude":

        st.subheader("📍 Coordinate Based Prediction")

        c1, c2 = st.columns(2)

        with c1:

            latitude = st.number_input(

                "Latitude",

                min_value=-90.0,

                max_value=90.0,

                value=23.500000,

                step=0.000001,

                format="%.6f"

            )

        with c2:

            longitude = st.number_input(

                "Longitude",

                min_value=-180.0,

                max_value=180.0,

                value=78.900000,

                step=0.000001,

                format="%.6f"

            )

    # =====================================================
    # MODE 2
    # USER BASED
    # =====================================================

    else:

        st.subheader("👤 User Based Prediction")

        dataset_choice = st.radio(

            "Select Dataset",

            [

                "India Dataset",

                "Global Dataset"

            ],

            horizontal=True

        )

        # ===========================================
        # INDIA DATASET
        # ===========================================

        if dataset_choice == "India Dataset":

            row = prediction_agent.india_default_row()

            st.info(
                "Modify the hydrogen production parameters."
            )

            c1, c2 = st.columns(2)

            with c1:

                electrolyzer = st.number_input(

                    "Electrolyzer Capacity (MW)",

                    value=float(row["Electrolyzer_Capacity_MW"])

                )

                capacity_factor = st.number_input(

                    "Capacity Factor (%)",

                    value=float(row["Capacity_Factor_Percent"])

                )

            with c2:

                water = st.number_input(

                    "Water Requirement (L/kg H₂)",

                    value=float(row["Water_Liters_per_kg"])

                )

                production = st.selectbox(

                    "Production Pathway",

                    sorted(
                        prediction_agent.master[
                            "Production_Pathway"
                        ].dropna().unique()
                    ),

                    index=list(

                        sorted(
                            prediction_agent.master[
                                "Production_Pathway"
                            ].dropna().unique()

                        )

                    ).index(

                        row["Production_Pathway"]

                    )

                )

                power = st.selectbox(

                    "Power Source",

                    sorted(
                        prediction_agent.master[
                            "Power_Source"
                        ].dropna().unique()
                    ),

                    index=list(

                        sorted(
                            prediction_agent.master[
                                "Power_Source"
                            ].dropna().unique()

                        )

                    ).index(

                        row["Power_Source"]

                    )

                )

            custom_inputs = {

                "Electrolyzer_Capacity_MW": electrolyzer,

                "Capacity_Factor_Percent": capacity_factor,

                "Water_Liters_per_kg": water,

                "Production_Pathway": production,

                "Power_Source": power

            }

        # ===========================================
        # GLOBAL DATASET
        # ===========================================

        else:

            countries = prediction_agent.get_global_countries()

            selected_country = st.selectbox(

                "Select Country",

                countries

            )

    st.markdown("---")
# =====================================================
# RUN PREDICTION
# =====================================================

    if st.button(
        "🚀 Run AI Prediction",
        use_container_width=True
    ):

        with st.spinner("Running Machine Learning Model..."):

            # -----------------------------------------
            # Latitude / Longitude
            # -----------------------------------------

            if prediction_mode == "📍 Latitude / Longitude":

                prediction = prediction_agent.predict_from_coordinates(
                    latitude,
                    longitude
                )

            # -----------------------------------------
            # User Based
            # -----------------------------------------

            else:

                if dataset_choice == "India Dataset":

                    prediction = prediction_agent.predict_india_custom(
                        custom_inputs
                    )

                else:

                    prediction = prediction_agent.predict_from_global(
                        selected_country
                    )

            # -----------------------------------------
            # Explainability
            # -----------------------------------------

            xai = xai_agent.explain(
                prediction["Scaled_Data"],
                prediction_agent.required_features
            )

            st.session_state.prediction = prediction
            st.session_state.feature_importance = xai["feature_importance"]

            st.success("Prediction Completed Successfully.")

    # =====================================================
    # RESULTS
    # =====================================================

    if st.session_state.prediction is not None:

        result = st.session_state.prediction

        st.markdown("---")

        st.subheader("📈 Prediction Results")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Hydrogen Production",
                f"{result['Hydrogen_Output']:.2f} kg/day"
            )

        with c2:

            st.metric(
                "Estimated CO₂",
                f"{result['CO2_Emission']:.2f} kg CO₂-eq/kg H₂"
            )

        with c3:

            score = max(
                0,
                round(
                    100 - result["CO2_Emission"] * 5,
                    1
                )
            )

            st.metric(
                "Sustainability Score",
                f"{score}%"
            )

        st.markdown("---")

        # =====================================================
        # LOCATION DETAILS
        # =====================================================

        st.subheader("📍 Prediction Location")

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Location**")
            st.success(result["Location"])

        with col2:

            st.write("**Coordinates**")

            st.info(
                f"{result['Latitude']:.6f}, {result['Longitude']:.6f}"
            )

        st.markdown("---")

        # =====================================================
        # MATCHED DATASET
        # =====================================================

        st.subheader("📄 Matched Dataset Record")

        matched = result["Matched_Row"]

        st.dataframe(
            matched.to_frame("Value"),
            use_container_width=True
        )

        st.markdown("---")

        # =====================================================
        # FEATURE IMPORTANCE
        # =====================================================

        st.subheader("🔍 Top Influencing Features")

        importance = (

            st.session_state.feature_importance

            .head(10)

            .sort_values("Importance")

        )

        fig = px.bar(

            importance,

            x="Importance",

            y="Feature",

            orientation="h",

            color="Importance",

            template="plotly_white",

            title="Feature Importance"

        )

        fig.update_layout(

            showlegend=False,

            height=450

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

        st.markdown("---")

        # =====================================================
        # GENERATE AI REPORT
        # =====================================================

        if st.button(

            "🤖 Generate AI Sustainability Report",

            use_container_width=True

        ):

            with st.spinner("Generating Gemini AI Report..."):

                report = report_agent.generate_report(

                    result,

                    st.session_state.feature_importance

                )

                st.session_state.report = report

        # =====================================================
        # SHOW REPORT
        # =====================================================

        if st.session_state.report is not None:

            st.markdown("---")

            st.subheader("🤖 AI Sustainability Report")

            st.markdown(st.session_state.report)

            pdf_buffer = pdf_generator.generate(

                st.session_state.prediction,

                st.session_state.report

            )

            st.download_button(

                "📄 Download PDF Report",

                data=pdf_buffer,

                file_name="Hydrogen_AI_Report.pdf",

                mime="application/pdf",

                use_container_width=True

            )                                          
# ==========================================================
# AI REPORT PAGE
# ==========================================================

elif page == "📄 AI Report":

    st.title("🤖 AI Sustainability Report")

    st.caption(
        "Professional sustainability assessment generated using Google Gemini."
    )

    st.markdown("---")

    if st.session_state.prediction is None:

        st.warning(

            "No prediction available.\n\nPlease run a prediction first."

        )

    elif st.session_state.report is None:

        st.info(

            "Prediction completed.\n\nClick **Generate AI Report** on the Prediction page."

        )

    else:

        report_tab, pdf_tab = st.tabs(

            [

                "📄 AI Report",

                "📥 Download PDF"

            ]

        )

        with report_tab:

            st.markdown(

                st.session_state.report

            )

        with pdf_tab:

            pdf_buffer = pdf_generator.generate(

                st.session_state.prediction,

                st.session_state.report

            )

            st.download_button(

                "📄 Download Sustainability Report",

                data=pdf_buffer,

                file_name="Hydrogen_AI_Report.pdf",

                mime="application/pdf",

                use_container_width=True

            )

# ==========================================================
# ABOUT PAGE
# ==========================================================

elif page == "ℹ️ About":

    st.title("ℹ About Hydrogen AI Studio")
    import google.genai as genai
    st.write("google-genai version")
    
    try:
        import importlib.metadata
        st.write(importlib.metadata.version("google-genai"))
    except Exception as e:
        st.write(e)

        
    st.markdown("---")

    left, right = st.columns([2,1])

    with left:

        st.markdown("""

### Hydrogen AI Studio

Hydrogen AI Studio is an intelligent decision-support platform for
Machine Learning Assisted Life Cycle Assessment (LCA) of hydrogen
production pathways.

The application combines:

- Machine Learning
- Explainable AI
- Google Gemini AI
- Sustainability Assessment
- PDF Report Generation

to support environmentally sustainable hydrogen production decisions.

---

### Major Features

• Hydrogen Production Prediction

• CO₂ Emission Estimation

• Explainable AI

• Gemini AI Sustainability Report

• Professional PDF Export

---

### Technologies

- Python

- Streamlit

- Scikit-Learn

- Voting Regressor

- Plotly

- Google Gemini

- ReportLab

---

### Developed By

**Radha Pandey**

Spark Intern

Department of Hydro & Renewable Energy

Indian Institute of Technology Roorkee

""")

    with right:

        st.metric(

            "Version",

            APP_VERSION

        )

        st.metric(

            "Prediction Model",

            "Voting Regressor"

        )

        st.metric(

            "Explainability",

            "Feature Importance"

        )

        st.metric(

            "LLM",

            GEMINI_MODEL

        )

        st.metric(

            "PDF Reports",

            "Available"

        )

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown(

f"""

<div class="footer">

<b>{APP_NAME}</b>

<br><br>

Machine Learning • Explainable AI • Google Gemini • Sustainability Analytics

<br><br>

Version {APP_VERSION}

<br><br>

Developed by <b>Radha Pandey</b>

</div>

""",

unsafe_allow_html=True

)
