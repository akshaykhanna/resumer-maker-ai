INPUT_FOLDER_PATH = "./input/"
OUTPUT_FOLDER_PATH = "./output/"
RESUME_TEMPLATE_FILE = "resume_template.html"
RESUME_DATA_FILE = "resume_data.json"
RESUME_HTML_FILE = "resume.html"
RESUME_PDF_FILE = "resume.pdf"
PORT_NO = 11434
LOCAL_HOST = "http://localhost"
MODELS = {
    "llama": {
        "name": "llama2",
    },
    "resume": {
        "name": "resume-writer",
    },
}
PDF_OPTIONS = {
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
