"""
Hydrogen AI Studio V2
Gemini Report Agent
"""

from google import genai

from config import *


class ReportAgent:

    def __init__(self):

        self.client = genai.Client(
            api_key=GOOGLE_API_KEY
        )

        with open(
            PROMPT_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            self.prompt = f.read()

    # ===================================================

    def generate_report(
        self,
        prediction,
        feature_importance,
        user_input
    ):

        top = feature_importance.head(5)

        feature_text = ""

        for _, row in top.iterrows():

            feature_text += (
                f"{row['Feature']} : "
                f"{row['Importance']:.4f}\n"
            )

        full_prompt = f"""

{self.prompt}

Country :
{user_input.get('Country')}

State :
{user_input.get('State','N/A')}

Technology :
{user_input.get('Production_Pathway')}

Power Source :
{user_input.get('Power_Source')}

Electrolyzer Capacity :
{user_input.get('Electrolyzer_Capacity_MW')}

Capacity Factor :
{user_input.get('Capacity_Factor_Percent')}

Predicted Hydrogen :

{prediction['Hydrogen_Output']} kg/day

Estimated CO₂ :

{prediction['CO2_Emission']} kg CO₂-eq/kg H₂

Top Important Features

{feature_text}

Generate a concise professional report.
"""

        response = self.client.models.generate_content(

            model=GEMINI_MODEL,

            contents=full_prompt

        )

        return response.text
