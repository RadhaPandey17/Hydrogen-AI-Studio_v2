"""
Gemini AI Report Agent
Compatible with google-genai >= 2.x
"""

from google import genai
from config import GOOGLE_API_KEY, GEMINI_MODEL


class ReportAgent:

    def __init__(self):

        if not GOOGLE_API_KEY:
            self.client = None
        else:
            self.client = genai.Client(
                api_key=GOOGLE_API_KEY
            )

    # ======================================================
    # Generate AI Report
    # ======================================================

    def generate_report(
        self,
        prediction,
        feature_importance
    ):

        if self.client is None:

            return """
# Gemini API Key Missing

Please configure GOOGLE_API_KEY.
"""

        feature_text = ""

        for _, row in feature_importance.head(8).iterrows():

            feature_text += (
                f"- {row['Feature']} : "
                f"{round(float(row['Contribution']),2)}%\n"
            )

        prompt = f"""
You are an expert in Hydrogen Production,
Life Cycle Assessment,
Machine Learning,
and Sustainability.

Generate a professional technical report.

------------------------------------------------

Location:
{prediction['Location']}

Latitude:
{prediction['Latitude']}

Longitude:
{prediction['Longitude']}

Hydrogen Production:
{prediction['Hydrogen_Output']:.2f} kg/day

Estimated CO₂:
{prediction['CO2_Emission']:.2f} kg CO₂-eq/kg H₂

------------------------------------------------

Most Important Features

{feature_text}

------------------------------------------------

Write the report with headings:

# Executive Summary

# Prediction Analysis

# Environmental Impact

# Explainable AI Interpretation

# Sustainability Assessment

# Recommendations

# Conclusion
"""

        try:

            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            return response.text

        except Exception as e:

            return f"""
# Gemini Report Generation Failed

Reason

{str(e)}

Prediction Summary

Location : {prediction['Location']}

Latitude : {prediction['Latitude']}

Longitude : {prediction['Longitude']}

Hydrogen Production :
{prediction['Hydrogen_Output']:.2f} kg/day

Estimated CO₂ :
{prediction['CO2_Emission']:.2f} kg CO₂-eq/kg H₂
"""
