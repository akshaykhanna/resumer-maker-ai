import jinja2

import pdfkit
from constants import (
    INPUT_FOLDER_PATH,
    OUTPUT_FOLDER_PATH,
    RESUME_TEMPLATE_FILE,
    RESUME_DATA_JSON,
    RESUME_HTML_FILE,
    RESUME_PDF_FILE,
    PDF_OPTIONS,
    MODELS,
)
from llama_llm import LLM
from job_description import summarize_jd, write_jd_to_file
from resume_data import get_resume_data, get_resume_data_updated_based_on_jd


class ResumeBuilder:
    def __init__(
        self, resume_template=RESUME_TEMPLATE_FILE, resume_data_file=RESUME_DATA_JSON
    ):
        self._load_template(resume_template)
        self.resume_data_file = resume_data_file

    def _create_resume_html_file_with_data(self):
        html_content = self.template.render(self.resume_data)
        with open(f"{OUTPUT_FOLDER_PATH}{RESUME_HTML_FILE}", "w") as ofile:
            ofile.write(html_content)

    def _load_template(self, resume_template):
        template_loader = jinja2.FileSystemLoader(searchpath="./")
        template_env = jinja2.Environment(loader=template_loader)
        self.template = template_env.get_template(
            f"{INPUT_FOLDER_PATH}{resume_template}"
        )

    def _generate_pdf_from_html(self):
        pdfkit.from_file(
            input=f"{OUTPUT_FOLDER_PATH}{RESUME_HTML_FILE}",
            output_path=f"{OUTPUT_FOLDER_PATH}{RESUME_PDF_FILE}",
            options=PDF_OPTIONS,
        )

    def build(self, builder_obj):
        if builder_obj["should_tweak_resume_data_based_on_jd"] and builder_obj["jd"]:
            llm = LLM(MODELS["resume"]["name"])
            jd = builder_obj["jd"]
            write_jd_to_file(jd)
            if builder_obj["should_summarize_jd"]:
                summarize_jd(jd, llm)
            self.resume_data = get_resume_data_updated_based_on_jd(
                self.resume_data_file, llm
            )
        else:
            self.resume_data = get_resume_data(self.resume_data_file)

        self._create_resume_html_file_with_data()
        self._generate_pdf_from_html()


if __name__ == "__main__":
    resume_builder = ResumeBuilder()
    builder_obj = {
        "should_tweak_resume_data_based_on_jd": False,
        "should_summarize_jd": False,
    }
    resume_builder.build(builder_obj)
