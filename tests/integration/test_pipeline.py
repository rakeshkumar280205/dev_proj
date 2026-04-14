import app.services.matcher as matcher

def test_full_pipeline(monkeypatch):
    # Integration-level check: matcher logic with deterministic AI extraction.
    def fake_extract_skills_ai(text):
        text = text.lower()
        if "python and docker" in text:
            return ["python", "docker"]
        if "python and kubernetes" in text:
            return ["python", "kubernetes"]
        return []

    monkeypatch.setattr(matcher, "extract_skills_ai", fake_extract_skills_ai)

    resume = "Python and Docker"
    jd = "Looking for Python and Kubernetes"

    result = matcher.match_skills(resume, jd)

    assert "python" in result["skills_available_for_job"]
    assert "kubernetes" in result["skill_gap"]
    assert result["match_percentage"] == 50.0