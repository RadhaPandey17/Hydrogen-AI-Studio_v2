"""
Gemini AI Report Agent
"""

from datetime import datetime
from google import genai

from config import GOOGLE_API_KEY
from config import GEMINI_MODEL


class ReportAgent:

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(self):

        if not GOOGLE_API_KEY:

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

        if self.client is None:

            return """
# Gemini API Not Configured

No Gemini API Key was found.

Please configure GOOGLE_API_KEY.
"""

        # ------------------------------------------------
        # Today's Date
        # ------------------------------------------------

        today = datetime.now().strftime("%d %B %Y")

        # ------------------------------------------------
        # Top Features
        # ------------------------------------------------

        feature_text = ""

        for _, row in feature_importance.head(8).iterrows():

            feature_text += (
                f"- {row['Feature']} : "
                f"{round(float(row['Contribution']),2)}%\n"
            )

        # ------------------------------------------------
        # Prompt
        # ------------------------------------------------

        prompt = f"""
You are a senior Hydrogen Sustainability Expert.

Generate a professional technical report.

IMPORTANT:

• Do NOT invent dates.
• Do NOT write "Prepared By".
• Do NOT write "Prepared For".
• Do NOT create a cover page.
• Start directly from Executive Summary.

------------------------------------------------

Location:
{prediction["Location"]}

Latitude:
{prediction["Latitude"]}

Longitude:
{prediction["Longitude"]}

Predicted Hydrogen Production:
{prediction["Hydrogen_Output"]:.2f} kg/day

Estimated CO₂ Emission:
{prediction["CO2_Emission"]:.2f} kg CO₂-eq/kg H₂

------------------------------------------------

Top Influencing Features

{feature_text}

------------------------------------------------

Generate these sections:

# Executive Summary

# Prediction Analysis

# Environmental Impact

# Explainable AI Interpretation

# Sustainability Assessment

# Recommendations

# Conclusion

Use professional markdown formatting.
"""

        # ------------------------------------------------
        # Generate Report
        # ------------------------------------------------

        try:

            response = self.client.models.generate_content(

                model=GEMINI_MODEL,

                contents=prompt

            )

            report = response.text

            final_report = f"""
# 🤖 AI Sustainability Report

**Date:** {today}

---

{report}
"""

            return final_report

        except Exception as e:

            return f"""
# Gemini Report Generation Failed

## Reason

{str(e)}

---

## Model Used

{GEMINI_MODEL}

---

## Prediction Summary

**Location:** {prediction["Location"]}

**Latitude:** {prediction["Latitude"]}

**Longitude:** {prediction["Longitude"]}

**Hydrogen Production:** {prediction["Hydrogen_Output"]:.2f} kg/day

**Estimated CO₂ Emission:** {prediction["CO2_Emission"]:.2f} kg CO₂-eq/kg H₂
"""
