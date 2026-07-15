"""
Hydrogen Production AI Studio
Gemini Report Agent
Version 2.0
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

            self.system_prompt = (
                "You are a Hydrogen Sustainability Expert."
            )

    # =====================================================

    def generate_report(

        self,

        prediction_result,

        feature_importance

    ):

        top = feature_importance.head(5)

        features = "\n".join(

            [

                f"- {r.Feature}: {r.Importance:.3f}"

                for _, r in top.iterrows()

            ]

        )

        prompt = f"""

{self.system_prompt}

Prediction Summary

Location:
{prediction_result['Location']}

Latitude:
{prediction_result['Latitude']}

Longitude:
{prediction_result['Longitude']}

Predicted Hydrogen Production:
{prediction_result['Hydrogen_Output']} kg/day

Estimated CO₂ Emission:
{prediction_result['CO2_Emission']} kg CO₂-eq/kg H₂

Important Features

{features}

Generate a professional sustainability report.

"""

        response = self.client.models.generate_content(

            model=GEMINI_MODEL,

            contents=prompt

        )

        return response.text
