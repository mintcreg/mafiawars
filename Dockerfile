# Use python:3.9-slim-buster as the base image
FROM python:3.9-slim-buster

# Set environment variables to prevent .pyc files and ensure output is sent straight to the terminal
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required by Python packages (like Pillow and psycopg2)
# This is the key fix that prevents the build from failing.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       libjpeg-dev \
       zlib1g-dev \
    # Clean up the apt cache to keep the final image size smaller
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from requirements.txt
# First, copy only the requirements file to leverage Docker's build cache
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code into the container
COPY . .
