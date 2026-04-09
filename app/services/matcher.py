from app.models.ai_engine import extract_skills_ai

def match_skills(resume_text, jd_text):
    resume_skills = extract_skills_ai(resume_text)
    jd_skills = extract_skills_ai(jd_text)

    matched = sorted(list(set(resume_skills) & set(jd_skills)))
    missing = sorted(list(set(jd_skills) - set(resume_skills)))

    match_score = (len(matched) / len(jd_skills)) * 100 if jd_skills else 0

    return {
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "skills_available_for_job": matched,
        "skill_gap": missing,
        "match_percentage": round(match_score, 2)
    }