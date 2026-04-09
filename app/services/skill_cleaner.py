import re

# ❌ Remove garbage words
NOISE_WORDS = {
    "profile", "phd", "name", "engineer",
    "developer", "researcher", "my", "i"
}

def clean_skill(skill: str):
    # remove escape chars
    skill = skill.replace("\\n", " ").replace("\\", " ")

    # remove extra spaces
    skill = re.sub(r'\s+', ' ', skill).strip()

    # lowercase
    skill = skill.lower()

    return skill


def is_valid_skill(skill: str):
    # remove very short
    if len(skill) < 3:
        return False

    # remove names (simple heuristic)
    if len(skill.split()) > 4:
        return False

    # remove noise words
    if any(word in skill for word in NOISE_WORDS):
        return False

    return True


def normalize_skills(skills):
    cleaned = set()

    for skill in skills:
        skill = clean_skill(skill)

        if not is_valid_skill(skill):
            continue

        cleaned.add(skill)

    return sorted(list(cleaned))