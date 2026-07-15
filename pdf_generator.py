"""
Hydrogen AI Studio V2
PDF Generator
"""

from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import (

    SimpleDocTemplate,

    Paragraph,

    Spacer

)


class PDFGenerator:

    def __init__(self):

        self.styles = getSampleStyleSheet()

    # =====================================================

    def generate(

            self,

            prediction,

            report,

            user_input

    ):

        buffer = BytesIO()

        pdf = SimpleDocTemplate(buffer)

        story = []

        story.append(

            Paragraph(

                "Hydrogen AI Studio Report",

                self.styles["Title"]

            )

        )

        story.append(Spacer(1, 20))

        story.append(

            Paragraph(

                "<b>Input Information</b>",

                self.styles["Heading2"]

            )

        )

        fields = [

            ("Country", user_input.get("Country")),

            ("State", user_input.get("State")),

            ("Technology", user_input.get("Production_Pathway")),

            ("Power Source", user_input.get("Power_Source")),

            ("Electrolyzer Capacity",

             user_input.get("Electrolyzer_Capacity_MW")),

            ("Capacity Factor",

             user_input.get("Capacity_Factor_Percent"))

        ]

        for key, value in fields:

            story.append(

                Paragraph(

                    f"<b>{key}</b> : {value}",

                    self.styles["BodyText"]

                )

            )

        story.append(Spacer(1, 20))

        story.append(

            Paragraph(

                "<b>Prediction Results</b>",

                self.styles["Heading2"]

            )

        )

        story.append(

            Paragraph(

                f"Hydrogen Production : "

                f"{prediction['Hydrogen_Output']} kg/day",

                self.styles["BodyText"]

            )

        )

        story.append(

            Paragraph(

                f"Estimated CO₂ : "

                f"{prediction['CO2_Emission']} kg CO₂-eq/kg H₂",

                self.styles["BodyText"]

            )

        )

        story.append(Spacer(1, 20))

        story.append(

            Paragraph(

                "<b>AI Sustainability Report</b>",

                self.styles["Heading2"]

            )

        )

        for line in report.split("\n"):

            if line.strip():

                story.append(

                    Paragraph(

                        line,

                        self.styles["BodyText"]

                    )

                )

        pdf.build(story)

        buffer.seek(0)

        return buffer
