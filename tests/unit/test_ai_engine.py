from app.models.ai_engine import extract_skills_ai

def test_skill_extraction_basic():
    text = "I have experience in Python and Java"

    skills = extract_skills_ai(text)

    assert "python" in skills
    assert "java" in skills