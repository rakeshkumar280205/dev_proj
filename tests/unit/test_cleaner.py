from app.services.skill_cleaner import clean_skill

def test_clean_skill():
    raw = "\\nMachine Learning\\"
    cleaned = clean_skill(raw)

    assert cleaned == "machine learning"