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
    MODELS
)
from llama_llm import LLM


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
    
    def _get_summarize_prompt(self, section, title, company, text, no_of_lines=2):
        return f'''
         Summarize below {section} text for {title} at {company} in max {no_of_lines} lines. Return only summarize text as response.
         `{text}`
        '''
    
    def summarize_jd(self, jd):
        llm = LLM(MODELS["llama"]["name"])
        jd["responsibilities"] = llm.generateResponse(self._get_summarize_prompt("responsibilities", jd["title"], jd["company"], jd["responsibilities"]))
        jd["skills"] = llm.generateResponse(self._get_summarize_prompt("skills", jd["title"], jd["company"], jd["skills"]))
        # write summarize jd object to JSON file
        with open(f"{OUTPUT_FOLDER_PATH}summarize_jd.json", "w") as jd_file:
            json.dump(jd, jd_file)
        
    def update_resume_data_based_on_jd(self, jd):
        self.summarize_jd(jd)
        # #read the jd text file
        # with open(f"{INPUT_FOLDER_PATH}{jd_text_file}", "r") as jd_file:
        #     jd_text = jd_file.read()

    def build(self):
        # Render the HTML template with the data
        self._create_resume_html_file_with_data()
        self._generate_pdf_from_html()


if __name__ == "__main__":
    resume_builder = ResumeBuilder()
    jd = {
        "title" : "Senior Software Engineer",
        "company" : "Microsoft",
        "responsibilities" : 
            """
            We are looking for a strong product leader to help define a vision and road-map for the next generation autonomous cloud infrastructure which enable M365 Sovereign and Regulated cloud offerings. Become a founding member of the new Special Cloud team, chartered with innovating in this space of internet-scale distributed cloud system. Microsoft is uniquely at the center of this opportunity, and we have the responsibility to advance the frontiers of compliance, regulation and security in the ever expanding digital world.
            This is a Software Engineer role with opportunity for deep technical impact, product innovation and team building with opportunity for advancement. We envision this team to be incubating new technology while executing with clarity and energy to deliver customer success.
            You will be an inspiring, inclusive and collaborative leader to lead a team of 8+ responsible for delivering on customer and business value. You will play a key role in building the team with right culture, partnering with other teams, planning sprints and executing on the plans.
            This is a huge opportunity to make an impact at massive scale, with room for growth in discipline, team-building and learning while working in foundational cloud technologies.
            """,
        "skills" : 
            """
            You love this team’s mission
            You love to work in the transformational cloud infrastructure
            Experience in working with distributed teams.
            Plenty of experience in managing highly complex software services at internet scale
            Exceptional management skills to collaborate across teams and to inspire talented engineering talent.
            5+ years of experience in cloud and related technologies.
            10+ years of experience in architecture, performance, scale, backend
            2+ years of engineering management
            Degree in CS or equivalent experience
            """,
    }
    resume_builder.summarize_jd(jd)
    # resume_builder.build()
