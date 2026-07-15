"""
Hydrogen Production AI Studio

Explainable AI Agent

Version 2.0
"""

import joblib
import numpy as np
import pandas as pd

from config import MODEL_PATH


class XAIAgent:

    def __init__(self):

        self.model = joblib.load(MODEL_PATH)

    # =====================================================

    def explain(

        self,

        scaled_data,

        feature_names

    ):

        values = np.abs(scaled_data[0])

        importance = values / (
            values.sum() + 1e-8
        )

        feature_importance = pd.DataFrame(

            {

                "Feature": feature_names,

                "Importance": importance

            }

        )

        feature_importance = feature_importance.sort_values(

            "Importance",

            ascending=False

        )

        return {

            "feature_importance": feature_importance,

            "top_features": feature_importance.head(10),

            "shap_values": None

        }
