import json
import os
from constants import (
    CANDIDATES_FOLDER_PATH,
    OUTPUT_FOLDER_PATH,
    RESUME_DATA_JSON,
    MODELS,
)
from job_description import get_summarize_jd_or_jd
from llama_llm import LLM


def get_resume_data(resume_data_file):
    with open(f"{CANDIDATES_FOLDER_PATH}{resume_data_file}", "r") as data_file:
        resume_data = json.load(data_file)
        return resume_data


def _prune_response(response):
    # extract string after 'Summary:' and before '\n'
    responses = response.split("Update:")
    prune_response = len(responses) > 1 and responses[1] or responses[0]
    # remove new line characters
    prune_response = prune_response.replace("\n", "")
    return prune_response


def _get_work_exp_prompt(work_exp, responsibilities):
    return f"""
    Update below job work experience as per this job posting responsibilities: {responsibilities} and return only work experience text starting as 'Update:'
    \n {work_exp}
    """


def _update_work_experiences(resume_data, jd, llm):
    work_experience = resume_data["work_experience"]
    for i in range(len(work_experience)):
        work_experience[i]["description"] = _prune_response(
            llm.generateResponse(
                _get_work_exp_prompt(
                    work_experience[i]["description"], jd["responsibilities"]
                )
            )
        )


def _get_skills_prompt(my_skills, responsibilities):
    return f"""
     Update my below skills based on this job posting skills: {responsibilities} and return comma separate skills as response starting as 'Update:'
     \n {my_skills}
    """


def _update_skills(resume_data, jd, llm):
    my_skills = resume_data["skills"]
    my_skills = _prune_response(
        llm.generateResponse(_get_skills_prompt(my_skills, jd["skills"]))
    )
    my_skills = my_skills.split(",")
    resume_data["skills"] = [skill.strip() for skill in my_skills]


def get_resume_data_updated_based_on_jd(resume_data_file):
    resume_data = get_resume_data(resume_data_file)
    jd = get_summarize_jd_or_jd()
    if not jd or not resume_data:
        return resume_data
    resume_data_json_fn = f"{OUTPUT_FOLDER_PATH}{RESUME_DATA_JSON}"
    # check if resume data file already exists
    if os.path.exists(resume_data_json_fn):
        with open(resume_data_json_fn, "r") as resume_data_file:
            resume_data = json.load(resume_data_file)
            return resume_data

    llm = LLM(MODELS["resume"]["name"])
    _update_work_experiences(resume_data, jd, llm)
    _update_skills(resume_data, jd, llm)
    # write updated resume data object to JSON file
    with open(resume_data_json_fn, "w") as resume_data_file:
        json.dump(resume_data, resume_data_file)
        return resume_data


if __name__ == "__main__":
    get_resume_data_updated_based_on_jd(RESUME_DATA_JSON)
