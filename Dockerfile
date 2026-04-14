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
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

# ---------- Copy Project Files ----------
COPY . .

# ---------- Expose Port ----------
EXPOSE 8000

# ---------- Run FastAPI ----------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]