import jinja2
import json
import pdfkit
from constants import (
    INPUT_FOLDER_PATH,
    OUTPUT_FOLDER_PATH,
    RESUME_TEMPLATE_FILE,
    RESUME_DATA_FILE,
    RESUME_HTML_FILE,
    RESUME_PDF_FILE,
)


class ResumeBuilder:
    def __init__(
        self, resume_template=RESUME_TEMPLATE_FILE, resume_data_file=RESUME_DATA_FILE
    ):
        self._load_template(resume_template)
        self._get_resume_data(resume_data_file)

    def _get_resume_data(self, resume_data_file):
        with open(f"{INPUT_FOLDER_PATH}{resume_data_file}", "r") as data_file:
            self.resume_data = json.load(data_file)

    def _create_resume_html_file_with_data(self):
        html_content = self.template.render(self.resume_data)
        with open(f"{OUTPUT_FOLDER_PATH}{RESUME_HTML_FILE}", "w") as ofile:
            ofile.write(html_content)

    def _load_template(self, resume_template):
        # Load the HTML template
        template_loader = jinja2.FileSystemLoader(searchpath="./")
        template_env = jinja2.Environment(loader=template_loader)
        self.template = template_env.get_template(
            f"{INPUT_FOLDER_PATH}{resume_template}"
        )

    def _generate_pdf_from_html(self):
        options = {
            "dpi": 500,
            "page-size": "A4",
            "margin-top": "0.25in",
            "margin-right": "0.25in",
            "margin-bottom": "0.25in",
            "margin-left": "0.25in",
            "encoding": "UTF-8",
            "custom-header": [("Accept-Encoding", "gzip")],
            "no-outline": None,
        }
        pdfkit.from_file(
            input=f"{OUTPUT_FOLDER_PATH}{RESUME_HTML_FILE}",
            output_path=f"{OUTPUT_FOLDER_PATH}{RESUME_PDF_FILE}",
            options=options,
        )

    def build(self):
        # Render the HTML template with the data
        self._create_resume_html_file_with_data()
        self._generate_pdf_from_html()


if __name__ == "__main__":
    resume_builder = ResumeBuilder()
    resume_builder.build()
