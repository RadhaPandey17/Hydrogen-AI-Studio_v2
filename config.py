"""
Hydrogen AI Studio V2
Configuration
"""

from pathlib import Path
from dotenv import load_dotenv
import os

PROJECT_ROOT = Path(__file__).resolve().parent

load_dotenv(PROJECT_ROOT / ".env")

# =====================================================
# GEMINI
# =====================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY is None:
    raise RuntimeError(
        "GOOGLE_API_KEY not found.\n"
        "Add it inside .env or Streamlit Secrets."
    )

GEMINI_MODEL = "gemini-2.5-flash"

# =====================================================
# DATASETS
# =====================================================

INDIA_DATASET_PATH = PROJECT_ROOT / "india_dataset.csv"

GLOBAL_DATASET_PATH = PROJECT_ROOT / "global_dataset.csv"

# =====================================================
# MODEL
# =====================================================

MODEL_PATH = PROJECT_ROOT / "best_final_ensemble_model.pkl"

SCALER_PATH = PROJECT_ROOT / "scaler.pkl"

FEATURE_PATH = PROJECT_ROOT / "feature_names.pkl"

# =====================================================
# PROMPT
# =====================================================

PROMPT_PATH = PROJECT_ROOT / "report_prompt.txt"

# =====================================================
# OUTPUT
# =====================================================

REPORT_FOLDER = PROJECT_ROOT / "reports"

REPORT_FOLDER.mkdir(exist_ok=True)

PLOT_FOLDER = PROJECT_ROOT / "plots"

PLOT_FOLDER.mkdir(exist_ok=True)

# =====================================================
# APP
# =====================================================

APP_NAME = "Hydrogen AI Studio"

APP_VERSION = "2.0"

AUTHOR = "Radha Pandey"
