"""
Hydrogen AI Studio V2
Feature Importance Agent
"""

import joblib
import numpy as np
import pandas as pd

from config import MODEL_PATH


class XAIAgent:

    def __init__(self):

        self.model = joblib.load(MODEL_PATH)

    # ===================================================

    def explain(
        self,
        scaled_data,
        feature_names
    ):

        importance = np.abs(
            scaled_data[0]
        )

        df = pd.DataFrame({

            "Feature": feature_names,

            "Importance": importance

        })

        df = df.sort_values(

            by="Importance",

            ascending=False

        )

        return {

            "feature_importance": df,

            "shap_values": None

        }
