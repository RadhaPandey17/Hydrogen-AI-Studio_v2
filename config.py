"""
Hydrogen AI Studio v2
Configuration File
"""

from pathlib import Path
import os
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent

load_dotenv(PROJECT_ROOT / ".env")

# ==========================================================
# GEMINI
# ==========================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash-lite"
)

if not GOOGLE_API_KEY:
    raise RuntimeError(
        "GOOGLE_API_KEY not found."
    )

# ==========================================================
# DATASETS
# ==========================================================

INDIA_DATASET = PROJECT_ROOT / "india_dataset.csv"

GLOBAL_DATASET = PROJECT_ROOT / "global_dataset.csv"

# ==========================================================
# MODEL
# ==========================================================

MODEL_PATH = PROJECT_ROOT / "best_final_ensemble_model.pkl"

SCALER_PATH = PROJECT_ROOT / "scaler.pkl"

FEATURE_PATH = PROJECT_ROOT / "feature_names.pkl"

PROMPT_PATH = PROJECT_ROOT / "report_prompt.txt"

# ==========================================================
# OUTPUTS
# ==========================================================

REPORT_FOLDER = PROJECT_ROOT / "reports"
REPORT_FOLDER.mkdir(parents=True, exist_ok=True)

PLOT_FOLDER = PROJECT_ROOT / "plots"
PLOT_FOLDER.mkdir(parents=True, exist_ok=True)

# ==========================================================
# APP
# ==========================================================
APP_NAME = "Hydrogen AI Studio"

APP_VERSION = "2.0"

AUTHOR = "Radha Pandey"
