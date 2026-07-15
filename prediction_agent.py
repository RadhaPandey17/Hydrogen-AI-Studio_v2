"""
Hydrogen Production AI Studio
Prediction Agent
Version 2.0
"""

import joblib
import numpy as np
import pandas as pd

from config import *


class PredictionAgent:

    def __init__(self):

        self.dataset = pd.read_csv(DATASET_PATH)

        self.model = joblib.load(MODEL_PATH)

        self.scaler = joblib.load(SCALER_PATH)

        self.required_features = joblib.load(FEATURE_PATH)

    # =====================================================

    def nearest_location(self, latitude, longitude):

        df = self.dataset.copy()

        distance = (
            (df["Latitude"] - latitude) ** 2 +
            (df["Longitude"] - longitude) ** 2
        )

        return df.loc[distance.idxmin()].copy()

    # =====================================================

    def prepare_features(self, row):

        feature_row = row.copy()

        remove_columns = [

            "Paper_Citation",
            "Location",
            "Latitude",
            "Longitude",
            "Hydrogen_Output_kg_day",
            "Hydrogen_Output_log"

        ]

        feature_row = feature_row.drop(
            labels=remove_columns,
            errors="ignore"
        )

        df = pd.DataFrame([feature_row])

        df = pd.get_dummies(
            df,
            columns=[
                "Production_Pathway",
                "Power_Source"
            ],
            drop_first=False
        )

        df.columns = df.columns.str.replace(
            r"[\[\]<>]",
            "_",
            regex=True
        )

        for feature in self.required_features:

            if feature not in df.columns:

                df[feature] = 0

        df = df[self.required_features]

        scaled = self.scaler.transform(df)

        return scaled

    # =====================================================

    def predict(
        self,
        latitude,
        longitude,
        custom_inputs=None
    ):

        nearest = self.nearest_location(
            latitude,
            longitude
        )

        if custom_inputs:

            for key, value in custom_inputs.items():

                if key in nearest.index:

                    nearest[key] = value

        scaled = self.prepare_features(nearest)

        prediction = float(
            self.model.predict(scaled)[0]
        )

        if np.isnan(prediction):

            hydrogen = 0.0

        elif prediction < 30:

            hydrogen = np.expm1(prediction)

        else:

            hydrogen = prediction

        hydrogen = max(0, hydrogen)

        co2 = float(
            nearest["LCA_GWP_kg_CO2_eq_per_kg_H2"]
        )

        return {

            "Location": nearest["Location"],

            "Latitude": nearest["Latitude"],

            "Longitude": nearest["Longitude"],

            "Hydrogen_Output": round(hydrogen, 2),

            "CO2_Emission": round(co2, 2),

            "Feature_Row": nearest,

            "Scaled_Data": scaled

        }
