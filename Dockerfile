#
# ----- Development Build Stage -----
#
FROM python:3.9-slim-buster AS development

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# --- ADDED THIS SECTION TO INSTALL SYSTEM DEPENDENCIES ---
# Install system dependencies needed for packages like Pillow and psycopg2
RUN apt-get update \
    && apt-get install -y \
       build-essential \
       libpq-dev \
       libjpeg-dev \
       zlib1g-dev \
    # Clean up the apt cache to keep the image size down
    && rm -rf /var/lib/apt/lists/*
# --------------------------------------------------------

# Install Python dependencies
# Using --no-cache-dir reduces the image size
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .
