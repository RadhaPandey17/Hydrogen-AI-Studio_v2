"""
Prediction Agent
Supports

1. Latitude / Longitude Prediction

2. Country / State Prediction
"""

import joblib
import numpy as np
import pandas as pd

from config import *

class PredictionAgent:
        
        def __init__(self):
                self.india = pd.read_csv(INDIA_DATASET)
                self.global_df = pd.read_csv(GLOBAL_DATASET)
                self.master = pd.concat(
                        [
                                self.india,self.global_df
                        ],
                        ignore_index=True)
                self.model = joblib.load(MODEL_PATH)
                self.scaler = joblib.load(SCALER_PATH)
                self.required_features = joblib.load(FEATURE_PATH)
                
                
                
                
        def nearest_location(self, latitude, longitude):
                df = self.master.copy()
            distance = (
                    (df["Latitude"] - latitude) ** 2 +
                    (df["Longitude"] - longitude) ** 2
            )
            idx = distance.idxmin()
            return df.loc[idx].copy()
    
    # =======================================================
    # New Workflow
    # =======================================================

    def dataset_location(

        self,

        country,

        state=None

    ):

        if country.lower() == "india":

            df = self.india

            row = df[df["State"] == state]

            return row.iloc[0].copy()

        else:

            df = self.global_df

            row = df[df["Country"] == country]

            return row.iloc[0].copy()

    # =======================================================

    def prepare_features(self, row):

        row = row.copy()

        remove = [

            "Paper_Citation",

            "Location",

            "Latitude",

            "Longitude",

            "Hydrogen_Output_kg_day",

            "Hydrogen_Output_log"

        ]

        for c in remove:

            if c in row.index:

                row.drop(c, inplace=True)

        df = pd.DataFrame([row])

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

        return self.scaler.transform(df)

    # =======================================================

    def run_prediction(self, row):

        scaled = self.prepare_features(row)

        prediction = float(

            self.model.predict(scaled)[0]

        )

        if prediction < 50:

            hydrogen = np.expm1(prediction)

        else:

            hydrogen = prediction

        return {

            "Location": row["Location"],

            "Country": row["Country"],

            "Latitude": row["Latitude"],

            "Longitude": row["Longitude"],

            "Hydrogen_Output": round(float(hydrogen),2),

            "CO2_Emission": round(

                float(

                    row["LCA_GWP_kg_CO2_eq_per_kg_H2"]

                ),

                2

            ),

            "Feature_Row": row,

            "Scaled_Data": scaled

        }

    # =======================================================
    # Mode 1
    # =======================================================

    def predict_from_coordinates(

        self,

        latitude,

        longitude

    ):

        row = self.nearest_location(

            latitude,

            longitude

        )

        return self.run_prediction(row)

    # =======================================================
    # Mode 2
    # =======================================================

    def predict_from_dataset(

        self,

        country,

        state=None

    ):

        row = self.dataset_location(

            country,

            state

        )

        return self.run_prediction(row)
        
        def predict(self, latitude, longitude):
            return self.predict_from_coordinates(
                latitude,
                longitude
            )
