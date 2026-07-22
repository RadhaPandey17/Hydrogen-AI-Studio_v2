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

        self.india = pd.read_csv(INDIA_DATASET)
        self.global_df = pd.read_csv(GLOBAL_DATASET)

        self.master = pd.concat(
            [self.india, self.global_df],
            ignore_index=True
        )

        self.model = joblib.load(MODEL_PATH)
        self.scaler = joblib.load(SCALER_PATH)
        self.required_features = joblib.load(FEATURE_PATH)

    # ==========================================================
    # Find nearest coordinate
    # ==========================================================
    def nearest_location(self, latitude, longitude):

        df = self.master.copy()

        df["distance"] = (
            (df["Latitude"] - latitude) ** 2 +
            (df["Longitude"] - longitude) ** 2
        )

        idx = df["distance"].idxmin()

        return df.loc[idx].copy()

    # ==========================================================
    # Default India Row
    # ==========================================================
    def india_default_row(self):

        return self.india.iloc[0].copy()
        
    
    def get_global_countries(self):
        india_keywords = ["india","gujarat","maharashtra","odisha","jharkhand","karnataka","telangana","tamil nadu","west bengal","uttar pradesh","punjab",
                          "rajasthan","haryana","andhra pradesh","madhya pradesh","bihar","chhattisgarh","adityanagar","surat","bhillai","bhavnagar","jind",
                          "sonipat","northern railway","bokaro","angul","dahej","vijaynagar","babrala","lonavla","leh","bhuj","faridabad","kota","hyderabad",
                          "bengaluru","kolkata","chennai"]
        
        countries = []
        for loc in self.global_df["Location"].dropna():
            location = str(loc)
            if any(keyword in location.lower() for keyword in india_keywords):
                continue
            countries.append(location)
        return sorted(set(countries))

    # ==========================================================
    # Selected Global Country
    # ==========================================================
    def global_location(self, country):

        if country is None:

            return self.global_df.iloc[0].copy()

        for _, row in self.global_df.iterrows():

            location = str(row["Location"])

            if location.endswith(country):

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

        for c in remove_columns:

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

        for f in self.required_features:

            if f not in df.columns:
                df[f] = 0

        df = df[self.required_features]

        return self.scaler.transform(df)

    # ==========================================================
    # Prediction
    # ==========================================================
    def run_prediction(self, row):

        scaled = self.prepare_features(row)

        pred = float(self.model.predict(scaled)[0])

        if pred < 50:
            hydrogen = np.expm1(pred)
        else:
            hydrogen = pred

        return {

            "Location": row["Location"],

            "Country": str(row["Location"]).split(",")[-1].strip(),

            "Latitude": float(row["Latitude"]),

            "Longitude": float(row["Longitude"]),

            "Hydrogen_Output": round(hydrogen,2),

            "CO2_Emission": round(
                float(row["LCA_GWP_kg_CO2_eq_per_kg_H2"]),
                2
            ),

            "Matched_Row": row,

            "Scaled_Data": scaled

        }

    # ==========================================================
    # Latitude Longitude Prediction
    # ==========================================================
    def predict_from_coordinates(self, latitude, longitude):

        row = self.nearest_location(latitude, longitude)

        return self.run_prediction(row)

    # ==========================================================
    # India Custom Prediction
    # ==========================================================
    def predict_india_custom(self, custom_inputs):

        row = self.india_default_row()

        for k, v in custom_inputs.items():

            if k in row.index:
                row[k] = v

        return self.run_prediction(row)

    # ==========================================================
    # Global Prediction
    # ==========================================================
    def predict_from_global(self, country):

        row = self.global_location(country)

        return self.run_prediction(row)

    # ==========================================================
    # Compatibility
    # ==========================================================
    def predict(self, latitude, longitude):

        return self.predict_from_coordinates(latitude, longitude)
