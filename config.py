"""
Hydrogen AI Studio
Configuration File
"""

from pathlib import Path
import os
import streamlit as st
from dotenv import load_dotenv

# ==========================================================
# PROJECT ROOT
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

# ==========================================================
# LOAD .env (Local Development)
# ==========================================================

load_dotenv(PROJECT_ROOT / ".env")

# ==========================================================
# GOOGLE GEMINI
# ==========================================================

# First try Streamlit Secrets
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Recommended Gemini model
GEMINI_MODEL = "gemini-2.5-flash"
# ==========================================================
# DATASETS
# ==========================================================

INDIA_DATASET = PROJECT_ROOT / "india_dataset.csv"

GLOBAL_DATASET = PROJECT_ROOT / "global_dataset.csv"

# ==========================================================
# MACHINE LEARNING FILES
# ==========================================================

MODEL_PATH = PROJECT_ROOT / "best_final_ensemble_model.pkl"

SCALER_PATH = PROJECT_ROOT / "scaler.pkl"

FEATURE_PATH = PROJECT_ROOT / "feature_names.pkl"

PROMPT_PATH = PROJECT_ROOT / "report_prompt.txt"

# ==========================================================
# OUTPUT FOLDERS
# ==========================================================

REPORT_FOLDER = PROJECT_ROOT / "reports"
REPORT_FOLDER.mkdir(parents=True, exist_ok=True)

PLOT_FOLDER = PROJECT_ROOT / "plots"
PLOT_FOLDER.mkdir(parents=True, exist_ok=True)

# ==========================================================
# APP SETTINGS
# ==========================================================

APP_NAME = "Hydrogen AI Studio"

APP_VERSION = "2.0"

AUTHOR = "Radha Pandey"
