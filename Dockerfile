# Dockerfile
FROM python:3.9-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       libjpeg-dev \
       zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
