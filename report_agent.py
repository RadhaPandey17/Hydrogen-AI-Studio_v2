"""
Hydrogen AI Studio v2
Gemini Report Agent
"""

from google import genai

from config import (
    GOOGLE_API_KEY,
    GEMINI_MODEL,
    PROMPT_PATH,
)


class ReportAgent:

    def __init__(self):

        self.client = genai.Client(
            api_key=GOOGLE_API_KEY
        )

        if PROMPT_PATH.exists():

            with open(
                PROMPT_PATH,
                "r",
                encoding="utf-8"
            ) as f:

                self.system_prompt = f.read()

        else:

            self.system_prompt = """
You are a Hydrogen Sustainability Expert.

Generate a professional report including:

1. Executive Summary

2. Selected Location

3. Hydrogen Production Prediction

4. Environmental Impact

5. Explainable AI Interpretation

6. Sustainability Assessment

7. Recommendations

8. Conclusion
"""

    # ======================================================

    def generate_report(

        self,

        prediction,

        feature_importance

    ):

        top = feature_importance.head(8)

        feature_text = ""

        for _, row in top.iterrows():

            feature_text += (

                f"- {row['Feature']} "

                f"({round(float(row['Importance']),4)})\n"

            )

        prompt = f"""

{self.system_prompt}

Location Information

Country:
{prediction.get("Country","Unknown")}

Location:
{prediction.get("Location","Unknown")}

Latitude:
{prediction.get("Latitude")}

Longitude:
{prediction.get("Longitude")}

Predicted Hydrogen Production

{prediction["Hydrogen_Output"]} kg/day

Estimated CO₂ Emission

{prediction["CO2_Emission"]} kg CO₂-eq/kg H₂

Important Features

{feature_text}

Generate the report.
"""

        try:

            response = self.client.models.generate_content(

                model=GEMINI_MODEL,

                contents=prompt

            )

            return response.text

        except Exception as e:

            return f"""

Gemini Report Generation Failed

Reason

{e}

Prediction Summary

Location:
{prediction.get("Location")}

Country:
{prediction.get("Country")}

Hydrogen Production

{prediction["Hydrogen_Output"]} kg/day

Estimated CO₂

{prediction["CO2_Emission"]} kg CO₂-eq/kg H₂
"""
