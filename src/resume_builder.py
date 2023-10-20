import jinja2
import json
from weasyprint import HTML

# Load the HTML template
template_loader = jinja2.FileSystemLoader(searchpath="./")
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template("/src/resume_template.html")

# Load data from a JSON file
with open("./src/resume_data.json", "r") as data_file:
    data = json.load(data_file)

# Render the HTML template with the data
html_content = template.render(data)

# Create a PDF from the rendered HTML
HTML(string=html_content).write_pdf("./output/resume.pdf")
