from sentence_transformers import SentenceTransformer, util
import re
from app.services.skill_cleaner import normalize_skills
from app.services.phrase_extractor import extract_phrases, is_technical_phrase
from app.services.dynamic_skills import extract_dynamic_skills

# -------------------------
# MODEL
# -------------------------
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# -------------------------
# SKILL MAP (KEEP)
# -------------------------
SKILL_MAP = {
    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "html": ["html"],
    "css": ["css"],
    "react": ["react"],
    "nodejs": ["nodejs", "node.js"],
    "fastapi": ["fastapi"],
    "django": ["django"],
    "flask": ["flask"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "sql": ["sql"],
    "mysql": ["mysql"],
    "mongodb": ["mongodb"],
    "aws": ["aws", "amazon web services"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "data analysis": ["data analysis", "data analytics"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "software testing": ["software testing"],
    "test automation": ["test automation"],
    "selenium": ["selenium"],
    "pytest": ["pytest"],
    "agile": ["agile"],
    "scrum": ["scrum"]
}

SKILLS = list(SKILL_MAP.keys())
skill_embeddings = model.encode(SKILLS, convert_to_tensor=True)

# -------------------------
# HELPERS
# -------------------------
def exact_match(keyword, text):
    pattern = r'\b' + re.escape(keyword) + r'\b'
    return re.search(pattern, text) is not None


# -------------------------
# KEYWORD
# -------------------------
def keyword_extract(text):
    text = text.lower()
    found = set()

    for skill, keywords in SKILL_MAP.items():
        for keyword in keywords:
            if exact_match(keyword, text):
                found.add(skill)

    return found


# -------------------------
# EMBEDDING
# -------------------------
def embedding_extract(text):
    sentences = re.split(r'[.\n]', text)
    found = set()

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        sentence_embedding = model.encode(sentence, convert_to_tensor=True)
        similarities = util.cos_sim(sentence_embedding, skill_embeddings)[0]

        for i, score in enumerate(similarities):
            skill = SKILLS[i]

            if score > 0.75:
                if any(exact_match(k, sentence.lower()) for k in SKILL_MAP[skill]):
                    found.add(skill)

    return found


# -------------------------
# PHRASE + DYNAMIC SKILLS
# -------------------------
def dynamic_phrase_extraction(text):
    phrases = extract_phrases(text)

    # Step 1: known phrases
    known_phrases = set()
    for phrase in phrases:
        if is_technical_phrase(phrase):
            known_phrases.add(phrase)

    # Step 2: dynamic discovery
    dynamic_skills = extract_dynamic_skills(known_phrases)

    return dynamic_skills


# -------------------------
# FINAL
# -------------------------
def extract_skills_ai(text):
    text = text.lower()

    keyword_skills = keyword_extract(text)
    embedding_skills = embedding_extract(text)

    # 🔥 NEW
    dynamic_skills = dynamic_phrase_extraction(text)

    final = keyword_skills.union(embedding_skills).union(dynamic_skills)

    return normalize_skills(final)