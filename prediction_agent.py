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

        self.features = joblib.load(FEATURE_PATH)

    # ==========================================================
    # COUNTRY LIST
    # ==========================================================

    def get_countries(self):

        countries = sorted(self.global_df["Country"].dropna().unique())

        countries.insert(0, "India")

        return countries

    # ==========================================================
    # STATES OF INDIA
    # ==========================================================

    def get_states(self):

        return sorted(

            self.india["State"].dropna().unique()

        )

    # ==========================================================
    # DEFAULT VALUES
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
    # PREPARE FEATURES
    # ==========================================================

    def prepare_input(self, record):

        df = pd.DataFrame([record])

        remove = [

            "Country",
            "State",
            "Location",
            "Paper_Citation",
            "Latitude",
            "Longitude",
            "Hydrogen_Output_kg_day",
            "Hydrogen_Output_log"

        ]

        for col in remove:

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

        for f in self.features:

            if f not in df.columns:

                df[f] = 0

        df = df[self.features]

        scaled = self.scaler.transform(df)

        return scaled

    # ==========================================================
    # PREDICT
    # ==========================================================

    def predict(

            self,
            user_record
    ):

        scaled = self.prepare_input(user_record)

        prediction = float(

            self.model.predict(scaled)[0]

        )

        return {

            "Hydrogen_Output": round(prediction,2),

            "CO2_Emission": round(

                float(

                    user_record["LCA_GWP_kg_CO2_eq_per_kg_H2"]

                ),

                2

            ),

            "Scaled_Data": scaled,

            "Feature_Row": user_record

        }
