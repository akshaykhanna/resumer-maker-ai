import jinja2
import json
from weasyprint import HTML
from constants import (
    INPUT_FOLDER_PATH,
    OUTPUT_FOLDER_PATH,
    RESUME_TEMPLATE_FILE,
    RESUME_DATA_FILE,
    RESUME_FILE
)

# Load the HTML template
template_loader = jinja2.FileSystemLoader(searchpath="./")
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template(f"{INPUT_FOLDER_PATH}{RESUME_TEMPLATE_FILE}")

# Load data from a JSON file
with open(f"{INPUT_FOLDER_PATH}{RESUME_DATA_FILE}", "r") as data_file:
    data = json.load(data_file)
# with open("./src/resume_data.json", "r") as data_file:
#     data = json.load(data_file)

# Render the HTML template with the data
html_content = template.render(data)

# Create a PDF from the rendered HTML
HTML(string=html_content).write_pdf(f"{OUTPUT_FOLDER_PATH}{RESUME_FILE}")
