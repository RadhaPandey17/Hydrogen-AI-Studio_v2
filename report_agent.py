"""
Gemini AI Report Agent
"""

from google import genai

from config import GOOGLE_API_KEY
from config import GEMINI_MODEL


class ReportAgent:

    def __init__(self):

        self.client = genai.Client(
            api_key=GOOGLE_API_KEY
        )

    # -----------------------------------------------------

    def generate_report(self,prediction,feature_importance):
        feature_text=""
        for _,r in feature_importance.head(8).iterrows():
            feature_text+=f"- {r['Feature']} : {round(float(r['Contribution']),2)}%\n"
            prompt=f"""
            
            You are a Hydrogen Sustainability Expert.
            Generate a professional report.
            Location:
            {prediction['Location']}
            Latitude:
            {prediction['Latitude']}
            Longitude:
            {prediction['Longitude']}
            Predicted Hydrogen:
            {prediction['Hydrogen_Output']} kg/day
            Estimated CO₂:
            {prediction['CO2_Emission']} kg CO₂-eq/kg H₂
            Important Features:
            {feature_text}
            Generate
            1 Executive Summary
            2 Technical Analysis
            3 Environmental Assessment
            4 Explainable AI
            5 Sustainability Score
            6 Recommendations
            7 Conclusion
            """

    try:

        response=self.client.models.generate_content(

            model=GEMINI_MODEL,

            contents=prompt

        )

        return response.text

    except Exception as e:

        return f"""

# Gemini Report Generation Failed

Reason

{e}

Prediction Summary

Location:
{prediction['Location']}

Latitude:
{prediction['Latitude']}

Longitude:
{prediction['Longitude']}

Hydrogen Production:
{prediction['Hydrogen_Output']} kg/day

Estimated CO₂:
{prediction['CO2_Emission']} kg CO₂-eq/kg H₂

"""
