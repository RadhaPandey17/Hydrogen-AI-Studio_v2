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

if page == "Dashboard":

    st.markdown(
        """
        <div class="big-title">
        ⚡ Hydrogen Production AI Studio
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Machine Learning Assisted Life Cycle Assessment of Hydrogen Production Pathways"
    )

    st.markdown("---")

    # ======================================================
    # KPI CARDS
    # ======================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            """
            <div class="metric-card">
            <h4>Dataset</h4>
            <h2>150+</h2>
            <p>Hydrogen Samples</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="metric-card">
            <h4>AI Model</h4>
            <h2>Voting</h2>
            <p>Regressor</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            """
            <div class="metric-card">
            <h4>Prediction</h4>
            <h2>H₂ + CO₂</h2>
            <p>Instant Output</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            """
            <div class="metric-card">
            <h4>AI Report</h4>
            <h2>Gemini</h2>
            <p>Professional Analysis</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ======================================================
    # DATASET OVERVIEW
    # ======================================================

    dataset = prediction_agent.dataset

    left, right = st.columns([2, 1])

    with left:

        st.subheader("🌍 Hydrogen Production Pathways")

        pathway_counts = (
            dataset["Production_Pathway"]
            .value_counts()
            .reset_index()
        )

        pathway_counts.columns = [
            "Pathway",
            "Count"
        ]

        fig = px.bar(
            pathway_counts,
            x="Pathway",
            y="Count",
            color="Count",
            title="Dataset Distribution"
        )

        fig.update_layout(
            template="plotly_white",
            height=420,
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("📊 Dataset Statistics")

        st.metric(
            "Locations",
            dataset["Location"].nunique()
        )

        st.metric(
            "Countries",
            dataset["Country"].nunique()
            if "Country" in dataset.columns
            else 1
        )

        st.metric(
            "Average H₂",
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

    st.subheader("⚙ AI Workflow")

    st.info(
        """
User Inputs

↓

Nearest Dataset Matching

↓

Feature Engineering

↓

Machine Learning Prediction

↓

Hydrogen Production

↓

Environmental Impact

↓

Explainable AI

↓

Gemini Sustainability Report

↓

PDF Download
"""
    )

    st.markdown("---")

    st.subheader("🚀 Key Features")

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            """
✅ Hydrogen Production Prediction

✅ Automatic Feature Engineering

✅ CO₂ Estimation

✅ Explainable AI

"""
        )

    with col2:

        st.success(
            """
✅ AI Sustainability Report

✅ PDF Download

✅ Interactive Visualizations

✅ Modern Dashboard
"""
        )
      # ==========================================================
# PREDICTION PAGE
# ==========================================================

elif page == "Prediction":

    st.title("⚡ Hydrogen Production Prediction")

    st.caption(
        "Choose a prediction mode and provide the required information."
    )

    st.markdown("---")

    # =====================================================
    # Prediction Mode
    # =====================================================

    prediction_mode = st.radio(

        "Prediction Mode",

        [

            "📍 Location Based",

            "🏭 Plant Based (Coming Soon)",

            "⚙ Custom Scenario"

        ],

        horizontal=True

    )

    st.markdown("---")

    # =====================================================
    # LOCATION BASED
    # =====================================================

    if prediction_mode == "📍 Location Based":

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

    # =====================================================
    # CUSTOM SCENARIO
    # =====================================================

    elif prediction_mode == "⚙ Custom Scenario":

        dataset = prediction_agent.dataset

        row = dataset.iloc[0]

        latitude = st.number_input(

            "Latitude",

            value=float(row["Latitude"]),

            format="%.6f"

        )

        longitude = st.number_input(

            "Longitude",

            value=float(row["Longitude"]),

            format="%.6f"

        )

        st.markdown("### Modify Plant Parameters")

        col1, col2 = st.columns(2)

        with col1:

            solar = st.number_input(

                "Solar Irradiance",

                value=float(row["Solar_Irradiance"])

            )

            wind = st.number_input(

                "Wind Speed",

                value=float(row["Wind_Speed"])

            )

            water = st.number_input(

                "Water Availability",

                value=float(row["Water_Availability"])

            )

        with col2:

            land = st.number_input(

                "Land Availability",

                value=float(row["Land_Availability"])

            )

            renewable = st.number_input(

                "Renewable Capacity (MW)",

                value=float(row["Renewable_Capacity_MW"])

            )

            demand = st.number_input(

                "Industrial Demand",

                value=float(row["Industrial_Demand"])

            )

        custom_inputs = {

            "Solar_Irradiance": solar,

            "Wind_Speed": wind,

            "Water_Availability": water,

            "Land_Availability": land,

            "Renewable_Capacity_MW": renewable,

            "Industrial_Demand": demand

        }

    # =====================================================
    # PLANT MODE
    # =====================================================

    else:

        st.info(

            "Plant Based Prediction will be added in Version 3."

        )

        latitude = 0.0

        longitude = 0.0

        custom_inputs = None

    st.markdown("---")

    # =====================================================
    # Predict Button
    # =====================================================

    predict_btn = st.button(

        "🚀 Run AI Prediction",

        use_container_width=True

    )

    # =====================================================
    # Prediction
    # =====================================================

    if predict_btn:

        with st.spinner("Running AI Prediction..."):

            try:

                prediction = prediction_agent.predict(

                    latitude,

                    longitude,

                    custom_inputs

                )

                st.session_state.prediction = prediction

                explanation = xai_agent.explain(

                    prediction["Scaled_Data"],

                    prediction_agent.required_features

                )

                st.session_state.feature_importance = (

                    explanation["feature_importance"]

                )

                st.session_state.report = None

                st.success("Prediction Completed Successfully.")

            except Exception as e:

                st.exception(e)

    # =====================================================
    # Results
    # =====================================================

    if st.session_state.prediction is not None:

        result = st.session_state.prediction

        st.markdown("---")

        st.subheader("Prediction Results")

        a, b, c = st.columns(3)

        with a:

            st.metric(

                "Hydrogen Production",

                f"{result['Hydrogen_Output']:.2f} kg/day"

            )

        with b:

            st.metric(

                "Estimated CO₂",

                f"{result['CO2_Emission']:.2f}"

            )

        with c:

            sustainability = max(

                0,

                round(

                    100 -

                    result["CO2_Emission"] * 5,

                    1

                )

            )

            st.metric(

                "Sustainability Score",

                f"{sustainability}%"

            )

        st.markdown("---")

        st.subheader("Matched Dataset")

        st.dataframe(

            result["Feature_Row"].to_frame(),

            use_container_width=True

        )

        st.markdown("---")

        st.subheader("Top Influencing Features")

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

            template="plotly_white"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

        st.markdown("---")

        if st.button(

            "🤖 Generate AI Sustainability Report",

            use_container_width=True

        ):

            with st.spinner(

                "Generating Report..."

            ):

                st.session_state.report = (

                    report_agent.generate_report(

                        result,

                        st.session_state.feature_importance

                    )

                )

                st.success("Report Generated Successfully.")
              # ==========================================================
# AI REPORT PAGE
# ==========================================================

elif page == "AI Report":

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

elif page == "About":

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
