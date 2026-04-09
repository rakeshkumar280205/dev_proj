# ---------- Base Image ----------
FROM python:3.11-slim

# ---------- Environment Variables ----------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# ---------- System Dependencies ----------
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---------- Work Directory ----------
WORKDIR /app

# ---------- Copy Requirements First (for caching) ----------
COPY requirements.txt .

# ---------- Install Python Dependencies ----------
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ---------- Download spaCy Model ----------
RUN python -m spacy download en_core_web_sm

# ---------- Copy Project Files ----------
COPY . .

# ---------- Expose Port ----------
EXPOSE 8000

# ---------- Run FastAPI ----------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]