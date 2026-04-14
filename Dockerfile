# ---------- Base Image ----------
FROM python:3.11-slim

# ---------- Environment Variables ----------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/app/.cache/huggingface \
    TORCH_HOME=/app/.cache/torch

# ---------- Work Directory ----------
WORKDIR /app

# ---------- Copy Requirements First (for caching) ----------
COPY requirements.txt .

# ---------- Install System Dependencies & Python Packages ----------
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    curl \
    && pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apt-get remove -y build-essential gcc && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# ---------- Copy Project Files ----------
COPY . .

# ---------- Note: spaCy model will be downloaded on first app startup ----------
RUN python -m spacy download en_core_web_sm
 
# ---------- Expose Port ----------
EXPOSE 8000

# ---------- Run FastAPI ----------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]