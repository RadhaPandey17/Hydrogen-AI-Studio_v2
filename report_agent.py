"""
Gemini AI Report Agent
"""

from google import genai
from config import GOOGLE_API_KEY, GEMINI_MODEL


class ReportAgent:

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(self):

        if GOOGLE_API_KEY is None or GOOGLE_API_KEY == "":

            self.client = None

        else:

            self.client = genai.Client(
                api_key=GOOGLE_API_KEY
            )

    # =====================================================
    # Generate AI Report
    # =====================================================

    def generate_report(
        self,
        prediction,
        feature_importance
    ):

        # --------------------------------------------------
        # API Key Check
        # --------------------------------------------------

        if self.client is None:

            return """
# Gemini API Not Configured

No Gemini API Key was found.

Please configure GOOGLE_API_KEY.
"""

        # --------------------------------------------------
        # Feature Importance
        # --------------------------------------------------

        feature_text = ""

        for _, row in feature_importance.head(8).iterrows():

            feature_text += (
                f"- {row['Feature']} : "
                f"{round(float(row['Contribution']),2)}%\n"
            )

        # --------------------------------------------------
        # Prompt
        # --------------------------------------------------

        prompt = f"""
You are an expert in

• Hydrogen Production

• Life Cycle Assessment (LCA)

• Machine Learning

• Sustainability Assessment

Generate a professional technical report.

--------------------------------------------------

Location

{prediction["Location"]}

Latitude

{prediction["Latitude"]}

Longitude

{prediction["Longitude"]}

--------------------------------------------------

Predicted Hydrogen Production

{prediction["Hydrogen_Output"]:.2f} kg/day

Estimated CO₂ Emission

{prediction["CO2_Emission"]:.2f} kg CO₂-eq/kg H₂

--------------------------------------------------

Important Features

{feature_text}

--------------------------------------------------

Generate the following sections.

1. Executive Summary

2. Prediction Analysis

3. Environmental Impact

4. Explainable AI Interpretation

5. Sustainability Assessment

6. Recommendations

7. Conclusion

Write in professional technical language.
"""

        # --------------------------------------------------
        # Gemini Generation
        # --------------------------------------------------

        try:

            response = self.client.models.generate_content(

                model=GEMINI_MODEL,

                contents=prompt

            )

            if hasattr(response, "text"):

                return response.text

            return str(response)

        except Exception as e:

            return f"""
# Gemini Report Generation Failed

## Reason

{str(e)}

--------------------------------------------

Prediction Summary

Location:
{prediction["Location"]}

Latitude:
{prediction["Latitude"]}

Longitude:
{prediction["Longitude"]}

Hydrogen Production:
{prediction["Hydrogen_Output"]:.2f} kg/day

Estimated CO₂:
{prediction["CO2_Emission"]:.2f} kg CO₂-eq/kg H₂
"""
