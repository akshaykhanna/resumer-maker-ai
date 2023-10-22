from resume_builder import ResumeBuilder

resume_builder = ResumeBuilder()
builder_obj = {
    "should_tweak_resume_data_based_on_jd": False,
    "should_summarize_jd": False,
    "jd": {
        "title": "Senior Software Engineer",
        "company": "Microsoft",
        "responsibilities": """
        We are looking for a strong product leader to help define a vision and road-map for the next generation autonomous cloud infrastructure which enable M365 Sovereign and Regulated cloud offerings. Become a founding member of the new Special Cloud team, chartered with innovating in this space of internet-scale distributed cloud system. Microsoft is uniquely at the center of this opportunity, and we have the responsibility to advance the frontiers of compliance, regulation and security in the ever expanding digital world.
        This is a Software Engineer role with opportunity for deep technical impact, product innovation and team building with opportunity for advancement. We envision this team to be incubating new technology while executing with clarity and energy to deliver customer success.
        You will be an inspiring, inclusive and collaborative leader to lead a team of 8+ responsible for delivering on customer and business value. You will play a key role in building the team with right culture, partnering with other teams, planning sprints and executing on the plans.
        This is a huge opportunity to make an impact at massive scale, with room for growth in discipline, team-building and learning while working in foundational cloud technologies.
        """,
        "skills": """
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
}
resume_builder.build(builder_obj)