"""
Hydrogen AI Studio v2
PDF Generator
"""

from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)


class PDFGenerator:

    def __init__(self):

        self.styles = getSampleStyleSheet()

    # ======================================================

    def generate(

        self,

        prediction,

        ai_report,

    ):

        buffer = BytesIO()

        pdf = SimpleDocTemplate(buffer)

        story = []

        # ------------------------------------------------

        story.append(

            Paragraph(

                "<b>Hydrogen AI Studio</b>",

                self.styles["Title"]

            )

        )

        story.append(Spacer(1,20))

        # ------------------------------------------------

        story.append(

            Paragraph(

                "<b>Prediction Summary</b>",

                self.styles["Heading2"]

            )

        )

        story.append(

            Paragraph(

                f"<b>Location :</b> {prediction['Location']}",

                self.styles["BodyText"]

            )

        )

        story.append(

            Paragraph(

                f"<b>Latitude :</b> {prediction['Latitude']}",

                self.styles["BodyText"]

            )

        )

        story.append(

            Paragraph(

                f"<b>Longitude :</b> {prediction['Longitude']}",

                self.styles["BodyText"]

            )

        )

        story.append(

            Paragraph(

                f"<b>Hydrogen Production :</b> {prediction['Hydrogen_Output']} kg/day",

                self.styles["BodyText"]

            )

        )

        story.append(

            Paragraph(

                f"<b>Estimated CO₂ :</b> {prediction['CO2_Emission']} kg CO₂-eq/kg H₂",

                self.styles["BodyText"]

            )

        )

        story.append(Spacer(1,20))

        # ------------------------------------------------

        story.append(

            Paragraph(

                "<b>AI Sustainability Report</b>",

                self.styles["Heading2"]

            )

        )

        story.append(Spacer(1,12))

        # ------------------------------------------------

        for line in ai_report.split("\n"):

            if line.strip():

                story.append(

                    Paragraph(

                        line,

                        self.styles["BodyText"]

                    )

                )

                story.append(

                    Spacer(1,6)

                )

        pdf.build(story)

        buffer.seek(0)

        return buffer
