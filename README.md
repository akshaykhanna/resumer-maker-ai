# resumer-maker-ai
Add your experience and skills once and then it will automatically create your customized resume for inputed job description.

## Init
### Source resume data:
> candidates/resume_data.json
### Resume template
> input/resume_template.html
### Output resume
 - output/resume.html
 - output/resume.pdf

## Run 
> `python src/main.py `


## Ollama LLM

https://github.com/jmorganca/ollama#macos
### Run chat & server
`ollama run llama2`

### Run server 
`ollama serve`


## Requirements

> Update requiremnts: `pip freeze > requirements.txt`

> Install requiremnts `pip install -r requirements.txt`


## Git switch to diff account only for current repo
```
# Navigate to the repository directory
cd /path/to/your/repository

# Set the username and email for this specific repository
git config user.email "your.repository.email@example.com"
git config user.name "Your Repository-Specific Username"

```
