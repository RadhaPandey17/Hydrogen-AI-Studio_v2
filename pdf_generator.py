"""
Hydrogen Production AI Studio

PDF Generator

Version 2.0
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

        report

    ):

        buffer = BytesIO()

        pdf = SimpleDocTemplate(buffer)

        story = []

        styles = self.styles

        story.append(

            Paragraph(

                "<b>Hydrogen Production AI Studio</b>",

                styles["Title"]

            )

        )

        story.append(Spacer(1, 20))

        story.append(

            Paragraph(

                "<b>Prediction Summary</b>",

                styles["Heading2"]

            )

        )

        summary = f"""

Location : {prediction['Location']}<br/>

Latitude : {prediction['Latitude']}<br/>

Longitude : {prediction['Longitude']}<br/><br/>

Hydrogen Production :
<b>{prediction['Hydrogen_Output']} kg/day</b><br/>

Estimated CO₂ :
<b>{prediction['CO2_Emission']} kg CO₂-eq/kg H₂</b>

"""

        story.append(

            Paragraph(

                summary,

                styles["BodyText"]

            )

        )

        story.append(Spacer(1, 25))

        story.append(

            Paragraph(

                "<b>AI Sustainability Report</b>",

                styles["Heading2"]

            )

        )

        for paragraph in report.split("\n"):

            if paragraph.strip():

                story.append(

                    Paragraph(

                        paragraph,

                        styles["BodyText"]

                    )

                )

                story.append(

                    Spacer(1, 6)

                )

        pdf.build(story)

        buffer.seek(0)

        return buffer
