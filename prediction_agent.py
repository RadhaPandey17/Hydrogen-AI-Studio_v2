"""
Hydrogen AI Studio V2
Prediction Agent
"""

import joblib
import pandas as pd

from config import *


class PredictionAgent:

    def __init__(self):

        self.india = pd.read_csv(INDIA_DATASET_PATH)

        self.global_df = pd.read_csv(GLOBAL_DATASET_PATH)

        self.model = joblib.load(MODEL_PATH)

        self.scaler = joblib.load(SCALER_PATH)

        self.required_features = joblib.load(FEATURE_PATH)

    # ==========================================================
    # Country List
    # ==========================================================

    def get_countries(self):

        countries = sorted(
            self.global_df["Country"].dropna().unique()
        )

        if "India" not in countries:
            countries.insert(0, "India")

        return countries

    # ==========================================================
    # State List
    # ==========================================================

    def get_states(self):

        return sorted(
            self.india["State"].dropna().unique()
        )

    # ==========================================================
    # Default Record
    # ==========================================================

    def get_default_record(

            self,

            country,

            state=None

    ):

        if country == "India":

            row = self.india[

                self.india["State"] == state

            ].iloc[0]

        else:

            row = self.global_df[

                self.global_df["Country"] == country

            ].iloc[0]

        return row.to_dict()

    # ==========================================================
    # Prepare Features
    # ==========================================================

    def prepare_features(self, record):

        df = pd.DataFrame([record])

        remove_columns = [

            "Country",

            "State",

            "Location",

            "Latitude",

            "Longitude",

            "Paper_Citation",

            "Hydrogen_Output_kg_day",

            "Hydrogen_Output_log"

        ]

        for col in remove_columns:

            if col in df.columns:

                df.drop(columns=col, inplace=True)

        df = pd.get_dummies(

            df,

            columns=[

                "Production_Pathway",

                "Power_Source"

            ],

            drop_first=False

        )

        for feature in self.required_features:

            if feature not in df.columns:

                df[feature] = 0

        df = df[self.required_features]

        scaled = self.scaler.transform(df)

        return scaled

    # ==========================================================
    # Prediction
    # ==========================================================

    def predict(self, user_record):

        scaled = self.prepare_features(user_record)

        prediction = float(

            self.model.predict(scaled)[0]

        )

        return {

            "Hydrogen_Output": round(prediction, 2),

            "CO2_Emission": round(

                float(

                    user_record["LCA_GWP_kg_CO2_eq_per_kg_H2"]

                ),

                2

            ),

            "Scaled_Data": scaled,

            "Feature_Row": user_record

        }
