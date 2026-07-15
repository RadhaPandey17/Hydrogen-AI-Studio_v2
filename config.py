"""
Hydrogen Production AI Studio
Configuration File
Version 2.0
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# ==========================================================
# PROJECT ROOT
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv(PROJECT_ROOT / ".env")

# ==========================================================
# GEMINI
# ==========================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

if GOOGLE_API_KEY is None:
    print("Warning : GOOGLE_API_KEY not found.")
    print("Gemini Report will not work until API Key is added.")

# ==========================================================
# DATA FILES
# ==========================================================

DATASET_PATH = PROJECT_ROOT / "Hydrogen_LCA_Final_Preprocessed.csv"

MODEL_PATH = PROJECT_ROOT / "best_final_ensemble_model.pkl"

SCALER_PATH = PROJECT_ROOT / "scaler.pkl"

FEATURE_PATH = PROJECT_ROOT / "feature_names.pkl"

PROMPT_PATH = PROJECT_ROOT / "report_prompt.txt"

# ==========================================================
# OUTPUT
# ==========================================================

OUTPUT_FOLDER = PROJECT_ROOT / "outputs"

OUTPUT_FOLDER.mkdir(exist_ok=True)

REPORT_FOLDER = OUTPUT_FOLDER / "reports"

REPORT_FOLDER.mkdir(exist_ok=True)

# ==========================================================
# APPLICATION
# ==========================================================

APP_NAME = "Hydrogen Production AI Studio"

APP_VERSION = "2.0"

AUTHOR = "Radha Pandey"

# ==========================================================
# SETTINGS
# ==========================================================

DEFAULT_SHAP_SAMPLE = 150

RANDOM_STATE = 42

# ==========================================================
# CHECK FILES
# ==========================================================

FILES = [
    DATASET_PATH,
    MODEL_PATH,
    SCALER_PATH,
    FEATURE_PATH,
    PROMPT_PATH
]

for file in FILES:

    if not file.exists():

        print(f"Missing File : {file}")
