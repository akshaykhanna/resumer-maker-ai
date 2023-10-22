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


def _get_work_exp_prompt(work_exp, responsibilities_prompt):
    return f"""
    Update below job work experience as per {responsibilities_prompt} and return only work experience text starting as 'Update:'
    \n {work_exp}
    """


def _update_work_experiences(resume_data, jd, llm, role, isRoleBased=False):
    work_experience = resume_data["work_experience"]
    for i in range(len(work_experience)):
        if not isRoleBased:
            work_exp_prompt = _get_work_exp_prompt(
                work_experience[i]["description"],
                f'this job posting responsibilities: {jd["responsibilities"]}',
            )
        else:
            work_exp_prompt = _get_work_exp_prompt(
                work_experience[i]["description"], f"{role} role"
            )
        print("work_exp_prompt:", work_exp_prompt)
        work_experience[i]["description"] = _prune_response(
            llm.generateResponse(work_exp_prompt)
        )


def _get_skills_prompt(my_skills, skills_prompt):
    return f"""
     Update my below skills based on {skills_prompt} and return list of skills as response starting as 'Update:'
     \n {my_skills}
    """


def _update_skills(resume_data, jd, llm, role=None, isRoleBased=False):
    my_skills = resume_data["skills"]
    if not isRoleBased:
        skills_prompt = _get_skills_prompt(
            my_skills, f'this job posting skills: {jd["skills"]}'
        )
    else:
        skills_prompt = _get_skills_prompt(my_skills, f"{role} role")
    print("skills_prompt:", skills_prompt)
    my_skills = _prune_response(llm.generateResponse(skills_prompt))
    my_skills = my_skills.split("\n")
    resume_data["skills"] = [skill.strip() for skill in my_skills]


def get_resume_data_updated_based_on_jd(resume_data_file, llm):
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

    # llm = LLM(MODELS["resume"]["name"])
    _update_work_experiences(resume_data, jd, llm)
    _update_skills(resume_data, jd, llm)
    # write updated resume data object to JSON file
    with open(resume_data_json_fn, "w") as resume_data_file:
        json.dump(resume_data, resume_data_file)
        return resume_data


def get_resume_data_updated_based_on_role(resume_data_file, role, llm):
    resume_data = get_resume_data(resume_data_file)
    resume_data_json_fn = f"{OUTPUT_FOLDER_PATH}{RESUME_DATA_JSON}"
    # check if resume data file already exists
    if os.path.exists(resume_data_json_fn):
        with open(resume_data_json_fn, "r") as resume_data_file:
            resume_data = json.load(resume_data_file)
            return resume_data

    # llm = LLM(MODELS["resume"]["name"])
    _update_work_experiences(
        resume_data=resume_data, jd=None, llm=llm, role=role, isRoleBased=True
    )
    _update_skills(
        resume_data=resume_data, jd=None, llm=llm, role=role, isRoleBased=True
    )
    # write updated resume data object to JSON file
    with open(resume_data_json_fn, "w") as resume_data_file:
        json.dump(resume_data, resume_data_file)
        return resume_data


if __name__ == "__main__":
    llm = LLM(MODELS["resume"]["name"])
    # get_resume_data_updated_based_on_jd(RESUME_DATA_JSON, llm)
    get_resume_data_updated_based_on_role(
        RESUME_DATA_JSON, "Senior Frontend Developer", llm
    )
