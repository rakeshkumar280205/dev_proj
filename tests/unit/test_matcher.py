import app.services.matcher as matcher

def test_matcher_with_empty_jd(monkeypatch):
    def fake_extract_skills_ai(text):
        text = text.lower()
        if "resume" in text:
            return ["python"]
        return []

    monkeypatch.setattr(matcher, "extract_skills_ai", fake_extract_skills_ai)

    result = matcher.match_skills("Resume: Python", "")

    assert result["jd_skills"] == []
    assert result["match_percentage"] == 0


def test_matcher_skill_gap(monkeypatch):
    def fake_extract_skills_ai(text):
        text = text.lower()
        if "docker" in text:
            return ["docker", "python"]
        return ["python", "kubernetes"]

    monkeypatch.setattr(matcher, "extract_skills_ai", fake_extract_skills_ai)

    resume = "Python and Docker"
    jd = "Looking for Python and Kubernetes"

    result = matcher.match_skills(resume, jd)

    assert "python" in result["skills_available_for_job"]
    assert "kubernetes" in result["skill_gap"]