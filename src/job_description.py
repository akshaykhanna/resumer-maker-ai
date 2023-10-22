import json
import os
from llama_llm import LLM
from constants import (
    OUTPUT_FOLDER_PATH,
    MODELS,
    SUMMARIZED_JD_JSON,
    JD_JSON
)



def _get_summarize_prompt(section, title, company, text, no_of_lines=3):
        return f'''
         Summarize below job {section} text for {title} role in max {no_of_lines} lines. Return only summarize text starting as 'Summary:'
         `{text}`
         
        '''

def _prune_response(response):
    # extract string after 'Summary:' and before '\n'
    responses = response.split("Summary:")
    prune_response = len(responses) > 1 and responses[1] or responses[0]
    # remove new line characters
    prune_response = prune_response.replace("\n", "")
    return prune_response

def get_summarize_jd_or_jd():
    summarize_fn_with_path = f"{OUTPUT_FOLDER_PATH}{SUMMARIZED_JD_JSON}"
    # check if summarize jd file already exists
    if os.path.exists(summarize_fn_with_path):
        with open(summarize_fn_with_path, "r") as jd_file:
            jd = json.load(jd_file)
            return jd
    elif os.path.exists(f"{OUTPUT_FOLDER_PATH}{JD_JSON}"):
        with open(f"{OUTPUT_FOLDER_PATH}{JD_JSON}", "r") as jd_file:
            jd = json.load(jd_file)
            return jd

def write_jd_to_file(jd):
    jd_fn_with_path = f"{OUTPUT_FOLDER_PATH}{JD_JSON}"
    # write jd object to JSON file
    with open(jd_fn_with_path, "w") as jd_file:
        json.dump(jd, jd_file)
        return jd

def summarize_jd(jd, llm):
        summarize_fn_with_path = f"{OUTPUT_FOLDER_PATH}{SUMMARIZED_JD_JSON}"
        # check if summarize jd file already exists
        if os.path.exists(summarize_fn_with_path):
            with open(summarize_fn_with_path, "r") as jd_file:
                jd = json.load(jd_file)
                return jd
      
        # llm = LLM(MODELS["resume"]["name"])
        jd["responsibilities"] = _prune_response(llm.generateResponse(_get_summarize_prompt("responsibilities", jd["title"], jd["company"], jd["responsibilities"])))
        jd["skills"] = _prune_response(llm.generateResponse(_get_summarize_prompt("skills", jd["title"], jd["company"], jd["skills"])))
        # write summarize jd object to JSON file
        with open(summarize_fn_with_path, "w") as jd_file:
            json.dump(jd, jd_file)
            return jd

if __name__ == "__main__":
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
    summarize_jd(jd)