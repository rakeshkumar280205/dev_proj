from sentence_transformers import SentenceTransformer, util

# Strong embedding model
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Tech-related anchor words
TECH_CONTEXT = [
    "machine learning", "deep learning", "ai", "ml", "model",
    "api", "backend", "cloud", "data", "pipeline",
    "agent", "database", "deployment", "training",
    "framework", "rag", "llm", "vector database"
]

context_embeddings = model.encode(TECH_CONTEXT, convert_to_tensor=True)


def is_dynamic_skill(phrase):
    phrase_embedding = model.encode(phrase, convert_to_tensor=True)

    similarities = util.cos_sim(phrase_embedding, context_embeddings)[0]

    # If phrase is close to any tech context → accept
    return max(similarities).item() > 0.5


def extract_dynamic_skills(phrases):
    dynamic_skills = set()

    for phrase in phrases:
        if len(phrase.split()) < 2:
            continue

        if is_dynamic_skill(phrase):
            dynamic_skills.add(phrase)

    return dynamic_skills