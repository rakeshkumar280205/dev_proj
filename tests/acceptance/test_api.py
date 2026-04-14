from fastapi.testclient import TestClient
import app.main as main
from app.main import app

client = TestClient(app)

def test_api_endpoint(monkeypatch):
    # Keep acceptance test stable by mocking internal service behavior.
    def fake_extract_resume_text(_upload_file):
        return "Python experience with Docker"

    def fake_match_skills(_resume_text, _job_description):
        return {
            "resume_skills": ["docker", "python"],
            "jd_skills": ["kubernetes", "python"],
            "skills_available_for_job": ["python"],
            "skill_gap": ["kubernetes"],
            "match_percentage": 50.0,
        }

    monkeypatch.setattr(main, "extract_resume_text", fake_extract_resume_text)
    monkeypatch.setattr(main, "match_skills", fake_match_skills)

    response = client.post(
        "/analyze",
        data={"job_description": "Python developer"},
        files={"resume": ("resume.txt", b"Python experience", "text/plain")}
    )

    assert response.status_code == 200

    data = response.json()

    assert "resume_skills" in data
    assert "jd_skills" in data
    assert "match_percentage" in data
    assert data["match_percentage"] == 50.0