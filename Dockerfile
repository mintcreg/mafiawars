# A simplified, robust, single-stage Dockerfile that correctly installs all dependencies.
FROM python:3.9-slim-buster

# Set environment variables for Python to run smoothly
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install system-level libraries required by Python packages BEFORE installing them with pip
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       libjpeg-dev \
       zlib1g-dev \
    # Clean up apt cache to keep the image size down
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker's layer cache
COPY ./requirements.txt /app/

# Install all Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's source code
COPY . /app/
