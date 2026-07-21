"""
Prediction Agent

Supports

1. Latitude / Longitude Prediction

2. India Dataset Prediction

3. Global Dataset Prediction
"""

import joblib
import numpy as np
import pandas as pd

from config import *


class PredictionAgent:

    # ==========================================================
    # Initialization
    # ==========================================================

    def __init__(self):

        # -------------------------
        # Load datasets
        # -------------------------

        self.india = pd.read_csv(INDIA_DATASET)

        self.global_df = pd.read_csv(GLOBAL_DATASET)

        # -------------------------
        # Merge datasets
        # -------------------------

        self.master = pd.concat(
            [
                self.india,
                self.global_df
            ],
            ignore_index=True
        )

        # -------------------------
        # Load ML model
        # -------------------------

        self.model = joblib.load(MODEL_PATH)

        self.scaler = joblib.load(SCALER_PATH)

        self.required_features = joblib.load(FEATURE_PATH)

    # ==========================================================
    # Latitude / Longitude Search
    # ==========================================================

    def nearest_location(
        self,
        latitude,
        longitude
    ):

        df = self.master.copy()

        distance = (

            (df["Latitude"] - latitude) ** 2 +

            (df["Longitude"] - longitude) ** 2

        )

        idx = distance.idxmin()

        return df.loc[idx].copy()

    # ==========================================================
    # India Dataset
    # ==========================================================

    def india_default_row(self):

        return self.india.iloc[0].copy()
        
        
    def get_global_countries(self):
        countries = set()
        ignore = {
            "angul","bokaro","bhuj","kota","bengaluru",
            "hyderabad","kolkata","chennai","faridabad",
            "babrala","dahej","vijaynagar","lonavla","leh"
        }
        for loc in self.global_df["Location"].dropna():
            text = str(loc)
            if "," in text:
                country = text.split(",")[-1].strip()
            elif "(" in text:
                country = text.split("(")[0].strip()
            else:
                country = text.strip()
                
                if country.lower() in ignore:
                    continue
                    countries.add(country)
                    
                    return sorted(countries)
    
    # ==========================================================
    # Global Selection
    # ==========================================================



    def global_location(self, country):
        for _, row in self.global_df.iterrows():
            location = str(row["Location"])
            if country.lower() in location.lower():
                return row.copy()
        return self.global_df.iloc[0].copy()

    # ==========================================================
    # Feature Engineering
    # ==========================================================

    def prepare_features(self, row):

        row = row.copy()

        remove_columns = [

            "Paper_Citation",

            "Location",

            "Latitude",

            "Longitude",

            "Hydrogen_Output_kg_day",

            "Hydrogen_Output_log"

        ]

        for column in remove_columns:

            if column in row.index:

                row.drop(column, inplace=True)

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

        scaled = self.scaler.transform(df)

        return scaled
# ==========================================================
# Run Prediction
# ==========================================================
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
                "Latitude": float(row["Latitude"]),
                "Longitude": float(row["Longitude"]),
                "Hydrogen_Output": round(float(hydrogen),2),
                "CO2_Emission": round(float(row["LCA_GWP_kg_CO2_eq_per_kg_H2"]),2
                                     ),
                "Matched_Row": row,
                "Scaled_Data": scaled
            }
    
    # ==========================================================
    # Mode 1
    # Latitude / Longitude
    # ==========================================================

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

    # ==========================================================
    # Mode 2A
    # India Dataset (Editable Inputs)
    # ==========================================================

    def predict_india_custom(

        self,

        custom_inputs

    ):

        row = self.india_default_row()

        for key, value in custom_inputs.items():

            if key in row.index:

                row[key] = value

        return self.run_prediction(row)

    # ==========================================================
    # Mode 2B
    # Global Dataset
    # ==========================================================

    def predict_from_global(

        self,

        country

    ):

        row = self.global_location(

            country

        )

        return self.run_prediction(row)

    # ==========================================================
    # Compatibility Function
    # Old app.py still calls predict()
    # ==========================================================

    def predict(

        self,

        latitude,

        longitude

    ):

        return self.predict_from_coordinates(

            latitude,

            longitude

        )
