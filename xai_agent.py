"""
Hydrogen AI Studio v2

Explainable AI Agent
"""

import joblib
import numpy as np
import pandas as pd

from config import MODEL_PATH


class XAIAgent:

    def __init__(self):

        self.model = joblib.load(MODEL_PATH)

    # ======================================================

    def explain(

        self,

        scaled_data,

        feature_names

    ):

        values = np.abs(

            scaled_data[0]

        )

        importance = pd.DataFrame(

            {

                "Feature": feature_names,

                "Importance": values

            }

        )

        importance = importance.sort_values(

            by="Importance",

            ascending=False

        )

        importance["Contribution"] = (

            importance["Importance"]

            /

            importance["Importance"].sum()

            * 100

        )

        importance["Contribution"] = (

            importance["Contribution"]

            .round(2)

        )

        return {

            "feature_importance": importance,

            "shap_values": None

        }
