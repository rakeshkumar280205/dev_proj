import spacy

# Load once
nlp = spacy.load("en_core_web_sm")

TECH_HINTS = [
    "learning", "model", "ai", "ml", "data", "api",
    "cloud", "pipeline", "database", "agent",
    "deployment", "framework", "training", "system"
]

def extract_phrases(text):
    doc = nlp(text)
    phrases = set()

    for chunk in doc.noun_chunks:
        phrase = chunk.text.lower().strip()

        # keep only multi-word meaningful phrases
        if len(phrase.split()) >= 2:
            phrases.add(phrase)

    return phrases


def is_technical_phrase(phrase):
    return any(hint in phrase for hint in TECH_HINTS)