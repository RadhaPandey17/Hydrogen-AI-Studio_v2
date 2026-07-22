"""
Gemini AI Report Agent
"""

from google import genai

from config import GOOGLE_API_KEY
from config import GEMINI_MODEL


class ReportAgent:

    def __init__(self):

        if not GOOGLE_API_KEY:

            self.client = None

        else:

            self.client = genai.Client(
                api_key=GOOGLE_API_KEY
            )

    # =====================================================
    # Generate Report
    # =====================================================

    def generate_report(
        self,
        prediction,
        feature_importance
    ):

        if self.client is None:

            return """
# Gemini API Not Configured

No Gemini API Key found.
"""

        feature_text = ""

        for _, row in feature_importance.head(8).iterrows():

            feature_text += (

                f"- {row['Feature']} : "

                f"{round(float(row['Contribution']),2)}%\n"

            )

        prompt = f"""
You are a Hydrogen Sustainability Expert.

Generate a professional technical sustainability report.

---------------------------------------------------

Location

{prediction["Location"]}

Latitude

{prediction["Latitude"]}

Longitude

{prediction["Longitude"]}

---------------------------------------------------

Predicted Hydrogen Production

{prediction["Hydrogen_Output"]:.2f} kg/day

Estimated CO₂ Emission

{prediction["CO2_Emission"]:.2f} kg CO₂-eq/kg H₂

---------------------------------------------------

Most Important Features

{feature_text}

---------------------------------------------------

Generate the following sections.

1. Executive Summary

2. Prediction Analysis

3. Environmental Impact

4. Explainable AI Interpretation

5. Sustainability Assessment

6. Recommendations

7. Conclusion

Use markdown formatting.
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

Model Used

{GEMINI_MODEL}

Prediction Summary

Location

{prediction["Location"]}

Latitude

{prediction["Latitude"]}

Longitude

{prediction["Longitude"]}

Hydrogen Production

{prediction["Hydrogen_Output"]:.2f} kg/day

Estimated CO₂

{prediction["CO2_Emission"]:.2f} kg CO₂-eq/kg H₂
"""
