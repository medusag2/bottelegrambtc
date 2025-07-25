FROM python:3.10-slim

# System kutubxonalarni o‘rnatamiz
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Katalog bilan ishlash
WORKDIR /app

# Fayllarni ko‘chirish
COPY . /app

# Virtual muhit va kutubxonalar o‘rnatish
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# PATH sozlash
ENV PATH="/opt/venv/bin:$PATH"

# Ishga tushirish
CMD ["python", "bot.py"]


