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

from config import APP_VERSION
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

.big-title{
    font-size:48px;
    font-weight:800;
    color:#4F8BF9;
}

.subtitle{
    font-size:18px;
    color:#B8C1CC;
    margin-bottom:15px;
}

.block-container{
    padding-top:2rem;
}

div[data-testid="stMetric"]{
    background:#1E293B;
    border:1px solid #334155;
    border-radius:12px;
    padding:12px;
}

div[data-testid="stInfo"]{
    border-radius:14px;
}

div[data-testid="stSuccess"]{
    border-radius:14px;
}

</style>
""", unsafe_allow_html=True)





st.markdown("""

<style>

html, body {

background:#F5F7FB;

font-family:Segoe UI;

}

.main {

background:#F5F7FB;

}

.block-container{

padding-top:1.5rem;

padding-bottom:2rem;

}

section[data-testid="stSidebar"]{

background:#0F172A;

}

section[data-testid="stSidebar"] *{

color:white;

}

.metric-card{

background:white;

padding:20px;

border-radius:18px;

box-shadow:0 8px 20px rgba(0,0,0,.08);

text-align:center;

}

.prediction-card{

background:white;

padding:25px;

border-radius:18px;

box-shadow:0 8px 20px rgba(0,0,0,.08);

}

.big-title{

font-size:38px;

font-weight:700;

color:#1E3A8A;

}

.footer{

text-align:center;

color:gray;

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
# SESSION
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

st.sidebar.title("🧪 Hydrogen AI Studio")

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

st.sidebar.info(

    f"""

### 📌 Application Info

**Version:** {APP_VERSION}

**Machine Learning**

Voting Regressor Ensemble

**Generative AI**

Gemini 2.5 Flash

**Explainable AI**

Feature Importance Analysis


"""

)
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
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="subtitle">
        Machine Learning Assisted Life Cycle Assessment (LCA) of Hydrogen Production Pathways
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ======================================================
    # RESEARCH OVERVIEW
    # ======================================================

    left, right = st.columns([2, 1])

    with left:

        st.info(
            """
### 🌍 Research Overview

Hydrogen AI Studio integrates Machine Learning, Explainable AI (SHAP),
Life Cycle Assessment (LCA), and Google Gemini AI to support sustainable
hydrogen production analysis.

The platform predicts hydrogen production, estimates environmental
impacts, explains the important influencing factors, and automatically
generates professional sustainability reports.
"""
        )

    with right:

        st.success(
            """
### 🚀 Platform Modules

✔ Hydrogen Prediction

✔ CO₂ Assessment

✔ SHAP Explainability

✔ Gemini AI Report

✔ PDF Report Export
"""
        )

    st.markdown("---")

    # ======================================================
    # DATASET
    # ======================================================

    dataset = prediction_agent.master

    col1, col2 = st.columns([2, 1])

    with col1:

        st.subheader("📊 Hydrogen Production Technologies")

        pathway = (
            dataset["Production_Pathway"]
            .value_counts()
            .reset_index()
        )

        pathway.columns = [
            "Technology",
            "Samples"
        ]

        fig = px.bar(
            pathway,
            x="Technology",
            y="Samples",
            color="Samples",
            text="Samples",
            title="Technology Distribution"
        )

        fig.update_layout(
            template="plotly_dark",
            showlegend=False,
            height=430
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("📈 Dataset Statistics")

        st.metric(
            "Hydrogen Samples",
            len(dataset)
        )

        st.metric(
            "Locations",
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
    # WORKFLOW
    # ======================================================

    st.subheader("⚙ Platform Workflow")

    st.code(
        """
Country / Coordinates
        │
        ▼
 Dataset Retrieval
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
 SHAP Explainability
        │
        ▼
 Gemini Sustainability Report
        │
        ▼
 PDF Report Generation
""",
        language="text"
    )

    st.markdown("---")

    # ======================================================
    # FEATURES
    # ======================================================

    f1, f2 = st.columns(2)

    with f1:

        st.success(
            """
### 🔬 Machine Learning

• Voting Regressor Ensemble

• Coordinate-Based Prediction

• Country & State Prediction

• Automated Feature Engineering

• Environmental Impact Prediction
"""
        )

    with f2:

        st.success(
            """
### 🤖 Artificial Intelligence

• SHAP Explainability

• Google Gemini Report Generation

• Sustainability Assessment

• Professional PDF Export

• Interactive Data Visualisation
"""
        )

    st.markdown("---")

    # ======================================================
    # PROJECT INFORMATION
    # ======================================================

    st.subheader("📚 Project Objective")

    st.write(
        """
This platform is designed to assist researchers and engineers in
evaluating hydrogen production pathways using Machine Learning and
Life Cycle Assessment. It enables rapid prediction of hydrogen output,
estimation of CO₂ emissions, explanation of influential parameters,
and automatic generation of AI-assisted sustainability reports for
decision support.
"""
    )
# ==========================================================
# PREDICTION PAGE
# ==========================================================

elif page == "🔮 Prediction":

    st.title("⚡ Hydrogen Production Prediction")

    st.caption(
        "Predict hydrogen production using either geographical coordinates or dataset locations."
    )

    st.markdown("---")

    # =====================================================
    # Prediction Mode
    # =====================================================
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

   # =====================================================
# MODE 1 : LATITUDE / LONGITUDE
# =====================================================

if prediction_mode == "📍 Latitude / Longitude":

    col1, col2 = st.columns(2)

    with col1:
        latitude = st.number_input(
            "Latitude",
            value=23.500,
            format="%.6f"
        )

    with col2:
        longitude = st.number_input(
            "Longitude",
            value=78.900,
            format="%.6f"
        )

    custom_inputs = None
    dataset_choice = None
    selected_location = None


# =====================================================
# MODE 2 : USER BASED
# =====================================================

else:

    dataset_choice = st.radio(

        "Select Dataset",

        [

            "India Dataset",

            "Global Dataset"

        ],

        horizontal=True

    )

    # ---------------- INDIA ----------------

    if dataset_choice == "India Dataset":

        row = prediction_agent.india_default_row()

        st.info("Modify the plant parameters.")

        c1, c2 = st.columns(2)

        with c1:

            solar = st.number_input(
                "Solar Irradiance",
                value=float(row["Solar_Irradiance"])
            )

            wind = st.number_input(
                "Wind Speed",
                value=float(row["Wind_Speed"])
            )

            water = st.number_input(
                "Water L/kg H₂",
                value=float(row["Water_Liters_per_kg"])
            )

        with c2:

            capacity = st.number_input(
                "Electrolyzer Capacity (MW)",
                value=float(row["Electrolyzer_Capacity_MW"])
            )

            factor = st.number_input(
                "Capacity Factor (%)",
                value=float(row["Capacity_Factor_Percent"])
            )

        custom_inputs = {

            "Solar_Irradiance": solar,

            "Wind_Speed": wind,

            "Water_Liters_per_kg": water,

            "Electrolyzer_Capacity_MW": capacity,

            "Capacity_Factor_Percent": factor

        }

        selected_location = None

    # ---------------- GLOBAL ----------------

    else:

        selected_location = st.selectbox(

            "Select Global Location",

            sorted(

                prediction_agent.global_df["Location"]

                .dropna()

                .unique()

            )

        )

        custom_inputs = None

st.markdown("---")
# =====================================================
# RUN PREDICTION
# =====================================================

if st.button(

    "🚀 Run AI Prediction",

    use_container_width=True

):

    with st.spinner("Running Prediction..."):

        # ----------------------------------------
        # Latitude / Longitude
        # ----------------------------------------

        if prediction_mode == "📍 Latitude / Longitude":

            prediction = prediction_agent.predict_from_coordinates(

                latitude,

                longitude

            )

        # ----------------------------------------
        # User Based Prediction
        # ----------------------------------------

        else:

            if dataset_choice == "India Dataset":

                prediction = prediction_agent.predict_india_custom(

                    custom_inputs

                )

            else:

                prediction = prediction_agent.predict_from_global(

                    selected_location

                )

        # ----------------------------------------
        # Explainability
        # ----------------------------------------

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

    if st.session_state.get("prediction") is not None:

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

                "Estimated CO₂ Emission",

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

        # =================================================
        # LOCATION DETAILS
        # =================================================

        st.subheader("📍 Selected Location")

        info1, info2 = st.columns(2)

        with info1:

            st.write("**Location**")

            st.success(result["Location"])

            st.write("**Country**")

            st.success(result["Country"])

        with info2:

            st.write("**Latitude**")

            st.info(result["Latitude"])

            st.write("**Longitude**")

            st.info(result["Longitude"])

        st.markdown("---")

        # =================================================
        # FEATURE IMPORTANCE
        # =================================================

        st.subheader("🔍 Feature Importance")

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

            template="plotly_dark",

            title="Top Influencing Features"

        )

        fig.update_layout(

            height=450,

            showlegend=False

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

        st.markdown("---")

        # =================================================
        # AI REPORT
        # =================================================

        st.subheader("🤖 AI Sustainability Report")

        if st.button(

            "Generate AI Report",

            use_container_width=True

        ):

            with st.spinner(

                "Generating report using Gemini..."

            ):

                report = report_agent.generate_report(

                    result,

                    st.session_state.feature_importance

                )

                st.session_state.report = report

        if st.session_state.get("report"):

            st.markdown(

                st.session_state.report

            )

            st.markdown("---")

            pdf = pdf_generator.generate(

                result,

                st.session_state.report

            )

            st.download_button(

                "📄 Download PDF Report",

                pdf,

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
        "AI-generated sustainability assessment using Google Gemini."
    )

    st.markdown("---")

    if st.session_state.report is None:

        st.info(
            "No report available.\n\nRun a prediction first, then generate the AI report."
        )

    else:

        tab1, tab2 = st.tabs(

            [

                "📄 AI Report",

                "📥 Download PDF"

            ]

        )

        with tab1:

            st.markdown(

                st.session_state.report

            )

        with tab2:

            pdf_buffer = pdf_generator.generate(

                st.session_state.prediction,

                st.session_state.report

            )

            st.download_button(

                "📄 Download Hydrogen Sustainability Report",

                data=pdf_buffer,

                file_name="Hydrogen_AI_Report.pdf",

                mime="application/pdf",

                use_container_width=True

            )

# ==========================================================
# ABOUT PAGE
# ==========================================================

elif page == "ℹ️ About":

    st.title("ℹ About Hydrogen Production AI Studio")

    st.markdown("---")

    left, right = st.columns([2,1])

    with left:

        st.markdown("""

### Hydrogen Production AI Studio

Hydrogen Production AI Studio is an intelligent decision-support platform developed to assist researchers, industries, and policymakers in evaluating hydrogen production pathways using Machine Learning and Artificial Intelligence.

Unlike traditional hydrogen assessment methods, this platform predicts hydrogen production while simultaneously estimating environmental impact and generating an AI-powered sustainability assessment.

### Major Components

• Hydrogen Production Prediction

• Environmental Impact Assessment

• Explainable AI

• AI Sustainability Report

• Professional PDF Export

### Technologies

- Python

- Streamlit

- Scikit-Learn

- Voting Regressor

- Plotly

- Google Gemini

- ReportLab

### Developed By

**Radha Pandey**

Spark Research Internship

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

            "Gemini 2.5 Flash"

        )

        st.metric(

            "Reports",

            "AI + PDF"

        )

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown(

"""

<div class="footer">

<b>Hydrogen Production AI Studio</b>

<br><br>

Machine Learning • Explainable AI • Google Gemini • Sustainability Analytics

<br><br>

Developed by <b>Radha Pandey</b>

</div>

""",

unsafe_allow_html=True

)
