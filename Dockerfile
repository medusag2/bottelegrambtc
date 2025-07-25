FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc libffi-dev python3-dev build-essential



RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    build-essential \
    python3.10-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

COPY . .

ENV PATH="/opt/venv/bin:$PATH"

CMD ["python", "bot.py"]

